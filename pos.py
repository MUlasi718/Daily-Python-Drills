#Day 25: The PLATINUM POS System (Name Capture Edition) 💎
#Features: Auto-Location + Custom Tipping + Name/Data Capture + Individual Restock

import tkinter as tk
from tkinter import simpledialog, messagebox
import sqlite3
import datetime
import os
import requests 
import time
import csv 

# --- 0. AUTO-CONFIGURATION ENGINE ---
SETTINGS = {
    "restaurant_name": "MMADU'S KITCHEN",
    "address_line_1": "Unknown Location",
    "address_line_2": "Earth",
    "currency_symbol": "$",
    "tax_rate": 0.08
}

def auto_detect_location():
    global SETTINGS
    print(" [SYSTEM] Detecting Location...")
    try:
        response = requests.get("http://ip-api.com/json/", timeout=2)
        data = response.json()
        if data['status'] == 'success':
            city = data['city']
            region = data['region'] 
            country = data['countryCode']
            
            SETTINGS["address_line_1"] = f"123 {city} Blvd"
            SETTINGS["address_line_2"] = f"{city}, {region} {data['zip']}"
            
            if country == "US":
                SETTINGS["currency_symbol"] = "$"
                if region in ["DE", "OR", "NH", "MT"]: SETTINGS["tax_rate"] = 0.00
                elif region == "GA": SETTINGS["tax_rate"] = 0.08
                else: SETTINGS["tax_rate"] = 0.06
            elif country == "GB":
                SETTINGS["currency_symbol"] = "£"
                SETTINGS["tax_rate"] = 0.20
            
            print(f" [SUCCESS] Detected: {city}, {region} ({country})")
        else:
            print(" [WARN] Detection failed. Using defaults.")
    except:
        print(" [INFO] Offline Mode. Using defaults.")

auto_detect_location()
CURRENCY = SETTINGS["currency_symbol"]
TAX_RATE = SETTINGS["tax_rate"]

# --- PDF SETUP ---
try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    PDF_READY = True
except ImportError:
    PDF_READY = False

# --- 1. DATABASE SETUP ---
def ensure_ticket_table():
    conn = sqlite3.connect("kitchen.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS active_tickets (
            ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
            items TEXT,
            status TEXT DEFAULT 'PENDING'
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE,
            price REAL,
            stock_count INTEGER
        )
    """)
    # Seed Data Check
    cursor.execute("SELECT count(*) FROM inventory")
    if cursor.fetchone()[0] == 0:
        initial_items = [("Burger", 12.50, 20), ("Fries", 3.50, 50), ("Steak", 25.00, 10), ("Soda", 1.99, 50)]
        cursor.executemany("INSERT OR IGNORE INTO inventory (name, price, stock_count) VALUES (?, ?, ?)", initial_items)
        conn.commit()
    conn.commit()
    conn.close()

ensure_ticket_table()

# --- 2. INVENTORY LOGIC ---
def check_and_decrement(item_name, qty_requested):
    conn = sqlite3.connect("kitchen.db")
    cursor = conn.cursor()
    cursor.execute("SELECT stock_count FROM inventory WHERE name = ?", (item_name,))
    result = cursor.fetchone()
    
    if result:
        current_stock = result[0]
        if current_stock >= qty_requested:
            new_stock = current_stock - qty_requested
            cursor.execute("UPDATE inventory SET stock_count = ? WHERE name = ?", (new_stock, item_name))
            conn.commit()
            conn.close()
            return True 
        else:
            conn.close()
            return False, current_stock 
    else:
        conn.close()
        return False, 0

def restore_stock(item_name, qty):
    conn = sqlite3.connect("kitchen.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE inventory SET stock_count = stock_count + ? WHERE name = ?", (qty, item_name))
    conn.commit()
    conn.close()

def open_manager_portal():
    mgr_win = tk.Toplevel(root)
    mgr_win.title("Manager: Inventory Control")
    mgr_win.geometry("400x400")
    
    tk.Label(mgr_win, text="LIVE INVENTORY", font=("Arial", 14, "bold")).pack(pady=10)
    list_inv = tk.Listbox(mgr_win, width=40, height=10, font=("Courier", 12))
    list_inv.pack(pady=5)
    
    def refresh_list():
        list_inv.delete(0, tk.END)
        conn = sqlite3.connect("kitchen.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name, stock_count FROM inventory")
        items = cursor.fetchall()
        conn.close()
        for item in items:
            name, count = item
            list_inv.insert(tk.END, f"{name:<15} : {count}")
            
    def update_stock():
        selection = list_inv.curselection()
        if not selection: return
        line = list_inv.get(selection[0])
        item_name = line.split(":")[0].strip()
        new_qty = simpledialog.askinteger("Restock", f"Enter NEW TOTAL quantity for {item_name}:")
        if new_qty is not None:
            conn = sqlite3.connect("kitchen.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE inventory SET stock_count = ? WHERE name = ?", (new_qty, item_name))
            conn.commit()
            conn.close()
            refresh_list() 
            
    refresh_list()
    tk.Button(mgr_win, text="UPDATE SELECTED STOCK", bg="#b2dfdb", command=update_stock).pack(pady=10)
    tk.Button(mgr_win, text="CLOSE", command=mgr_win.destroy).pack(pady=5)

# --- 3. PDF ENGINE (Updated for Name) ---
def generate_receipt_pdf(cart_items, subtotal, tax, tip, grand_total, change_due=0.0, customer_name="Guest"):
    if not PDF_READY: return
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    filename = f"Receipt_{timestamp}.pdf"
    
    try:
        c = canvas.Canvas(filename, pagesize=letter)
        c.setFont("Helvetica-Bold", 20)
        c.drawCentredString(300, 750, SETTINGS["restaurant_name"])
        c.setFont("Helvetica", 12)
        c.drawCentredString(300, 735, SETTINGS["address_line_1"])
        c.drawCentredString(300, 720, SETTINGS["address_line_2"])
        c.drawCentredString(300, 705, "-"*40)
        
        c.drawString(200, 680, f"Date: {now.strftime('%Y-%m-%d %H:%M')}")
        c.drawString(200, 665, f"Ticket #: {timestamp[-6:]}")
        # NEW: Print Customer Name
        c.drawString(200, 650, f"Customer: {customer_name}")
        
        y = 620
        c.setFont("Helvetica-Bold", 12)
        c.drawString(200, y, "ITEM")
        c.drawRightString(400, y, "PRICE")
        c.line(200, y-5, 400, y-5)
        y -= 20
        
        c.setFont("Helvetica", 12)
        for item in cart_items:
            name_line = f"{item['qty']}x {item['name']}"
            price_line = f"{CURRENCY}{item['price']:.2f}" 
            c.drawString(200, y, name_line)
            c.drawRightString(400, y, price_line)
            if item['note'] != "None":
                y -= 15
                c.setFont("Helvetica-Oblique", 10)
                c.drawString(220, y, f"* {item['note']}")
                c.setFont("Helvetica", 12)
            y -= 20
            
        c.line(200, y+10, 400, y+10)
        y -= 20
        c.drawString(200, y, "Subtotal:")
        c.drawRightString(400, y, f"{CURRENCY}{subtotal:.2f}")
        y -= 15
        tax_pct = TAX_RATE * 100
        c.drawString(200, y, f"Tax ({tax_pct:.1f}%):")
        c.drawRightString(400, y, f"{CURRENCY}{tax:.2f}")
        y -= 15
        if tip > 0:
            c.drawString(200, y, "Gratuity:")
            c.drawRightString(400, y, f"{CURRENCY}{tip:.2f}")
            y -= 20
        
        c.setFont("Helvetica-Bold", 14)
        c.drawString(200, y, "TOTAL PAID:")
        c.drawRightString(400, y, f"{CURRENCY}{grand_total:.2f}")
        
        if change_due > 0:
            y -= 20
            c.setFont("Helvetica", 12)
            c.drawString(200, y, "Change Due:")
            c.drawRightString(400, y, f"{CURRENCY}{change_due:.2f}")

        c.save()
        print(f" [PDF] Receipt saved: {filename}")
    except Exception as e:
        print(f" [ERROR] PDF Generation failed: {e}")

# --- 4. GLOBAL VARIABLES ---
subtotal_cost = 0.0
current_cart = [] 

# --- 5. GUI FUNCTIONS ---
def add_item(item_name, item_price):
    global subtotal_cost
    qty = simpledialog.askinteger("Quantity", f"How many {item_name}s?", minvalue=1, initialvalue=1)
    if qty:
        status = check_and_decrement(item_name, qty)
        if status == True:
            mod = simpledialog.askstring("Order", f"Notes for these {qty} items?")
            note_text = mod if mod else "None"
            batch_price = item_price * qty
            current_cart.append({
                "line": f"{qty}x {item_name} ({note_text})", 
                "name": item_name, "qty": qty, "price": batch_price,
                "unit_price": item_price, "note": note_text
            })
            display_text = f"{item_name} (x{qty}) [{note_text}] - {CURRENCY}{batch_price:.2f}"
            list_ticket.insert(tk.END, display_text)
            subtotal_cost += batch_price
            est_total = subtotal_cost + (subtotal_cost * TAX_RATE)
            label_total.config(text=f"SUB: {CURRENCY}{subtotal_cost:.2f}\n(Est. Total: {CURRENCY}{est_total:.2f})")
        else:
            available = status[1]
            messagebox.showwarning("86'd", f"Chef! We only have {available} {item_name}s left.")

def modify_selected_item():
    global subtotal_cost
    selected_indices = list_ticket.curselection()
    if not selected_indices: return
    index = selected_indices[0]
    item = current_cart[index]
    current_qty = item['qty']
    if current_qty == 1: qty_to_remove = 1
    else:
        qty_to_remove = simpledialog.askinteger("Adjust Quantity", f"Remove how many?", minvalue=1, maxvalue=current_qty)
        if not qty_to_remove: return 

    restore_stock(item['name'], qty_to_remove)
    refund_amount = item['unit_price'] * qty_to_remove
    subtotal_cost -= refund_amount
    
    if qty_to_remove == current_qty:
        del current_cart[index]
        list_ticket.delete(index)
    else:
        item['qty'] -= qty_to_remove
        item['price'] -= refund_amount
        new_text = f"{item['name']} (x{item['qty']}) [{item['note']}] - {CURRENCY}{item['price']:.2f}"
        list_ticket.delete(index)
        list_ticket.insert(index, new_text)
        item['line'] = f"{item['qty']}x {item['name']} ({item['note']})"

    est_total = subtotal_cost + (subtotal_cost * TAX_RATE)
    label_total.config(text=f"SUB: {CURRENCY}{subtotal_cost:.2f}\n(Est. Total: {CURRENCY}{est_total:.2f})")

def void_all():
    global subtotal_cost, current_cart
    if not current_cart: return
    for item in current_cart:
        restore_stock(item['name'], item['qty'])
    list_ticket.delete(0, tk.END)
    current_cart = []
    subtotal_cost = 0.0
    label_total.config(text=f"TOTAL: {CURRENCY}0.00")

# --- 6. CHECKOUT & DATA CAPTURE ---

def save_customer_data(name, contact_info, method):
    # UPDATED: Now saves Name + Contact Info
    with open("marketing_list.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([datetime.datetime.now(), name, contact_info, method])
    print(f" [DATA] Captured {name} | {method}: {contact_info}")

def offer_receipt_options(grand_total, tax_amount, tip_amount, change_due=0.0):
    rcpt_win = tk.Toplevel(root)
    rcpt_win.title("Receipt Options")
    rcpt_win.geometry("350x300")
    
    tk.Label(rcpt_win, text="Transaction Approved!", font=("Arial", 14, "bold"), fg="green").pack(pady=10)
    tk.Label(rcpt_win, text="How would you like your receipt?", font=("Arial", 12)).pack(pady=5)
    
    def process_print():
        generate_receipt_pdf(current_cart, subtotal_cost, tax_amount, tip_amount, grand_total, change_due)
        messagebox.showinfo("Printed", "Receipt Sent to Printer.")
        rcpt_win.destroy()
        
    def process_email():
        # Ask for Name FIRST
        name = simpledialog.askstring("Customer Name", "Enter Customer Name:")
        if not name: return 
        
        email = simpledialog.askstring("Email Receipt", f"Enter Email for {name}:")
        if email:
            save_customer_data(name, email, "EMAIL")
            generate_receipt_pdf(current_cart, subtotal_cost, tax_amount, tip_amount, grand_total, change_due, customer_name=name)
            messagebox.showinfo("Sent", f"Receipt emailed to {name}")
            rcpt_win.destroy()
            
    def process_text():
        # Ask for Name FIRST
        name = simpledialog.askstring("Customer Name", "Enter Customer Name:")
        if not name: return

        phone = simpledialog.askstring("Text Receipt", f"Enter Mobile Number for {name}:")
        if phone:
            save_customer_data(name, phone, "SMS")
            generate_receipt_pdf(current_cart, subtotal_cost, tax_amount, tip_amount, grand_total, change_due, customer_name=name)
            messagebox.showinfo("Sent", f"Receipt texted to {name}")
            rcpt_win.destroy()

    tk.Button(rcpt_win, text="🖨️ PRINT RECEIPT", width=25, height=2, command=process_print).pack(pady=5)
    tk.Button(rcpt_win, text="📧 EMAIL RECEIPT", width=25, height=2, command=process_email).pack(pady=5)
    tk.Button(rcpt_win, text="📱 TEXT RECEIPT", width=25, height=2, command=process_text).pack(pady=5)
    tk.Button(rcpt_win, text="NO RECEIPT", width=25, height=1, bg="#eee", command=rcpt_win.destroy).pack(pady=10)

def finalize_transaction(grand_total, tax_amount, tip_amount, change_due=0.0):
    global subtotal_cost, current_cart
    
    conn = sqlite3.connect("kitchen.db")
    cursor = conn.cursor()
    full_ticket_text = "\n".join([item["line"] for item in current_cart])
    if tip_amount > 0: full_ticket_text += "\n(GRATUITY INCLUDED)"
    cursor.execute("INSERT INTO active_tickets (items) VALUES (?)", (full_ticket_text,))
    conn.commit()
    conn.close()
    
    offer_receipt_options(grand_total, tax_amount, tip_amount, change_due)
    
    list_ticket.delete(0, tk.END)
    current_cart = []
    subtotal_cost = 0.0
    label_total.config(text=f"TOTAL: {CURRENCY}0.00")

def open_checkout_window():
    if not current_cart:
        messagebox.showinfo("Empty", "Cart is empty!")
        return

    pay_win = tk.Toplevel(root)
    pay_win.title("Checkout & Gratuity")
    pay_win.geometry("450x500")
    
    tax_amount = subtotal_cost * TAX_RATE
    selected_tip = tk.DoubleVar(value=0.0)
    
    tk.Label(pay_win, text="CHECKOUT", font=("Arial", 16, "bold")).pack(pady=10)
    
    lbl_sub = tk.Label(pay_win, text=f"Subtotal: {CURRENCY}{subtotal_cost:.2f}")
    lbl_sub.pack()
    lbl_tax = tk.Label(pay_win, text=f"Tax: {CURRENCY}{tax_amount:.2f}")
    lbl_tax.pack()
    
    lbl_total_big = tk.Label(pay_win, text=f"{CURRENCY}{(subtotal_cost + tax_amount):.2f}", font=("Arial", 30, "bold"), fg="green")
    lbl_total_big.pack(pady=10)
    
    def set_tip(percent=None, custom_val=None):
        if custom_val is not None:
            tip_val = custom_val
        else:
            tip_val = subtotal_cost * percent
            
        selected_tip.set(tip_val)
        new_total = subtotal_cost + tax_amount + tip_val
        lbl_total_big.config(text=f"{CURRENCY}{new_total:.2f}")

    def ask_custom_tip():
        pct = simpledialog.askfloat("Custom Gratuity", "Enter Tip Percentage (e.g., 25 for 25%):")
        if pct is not None:
            decimal_pct = pct / 100
            set_tip(percent=decimal_pct)
        
    tk.Label(pay_win, text="Add Gratuity:", font=("Arial", 12)).pack(pady=5)
    frame_tips = tk.Frame(pay_win)
    frame_tips.pack()
    
    t15 = subtotal_cost * 0.15
    t18 = subtotal_cost * 0.18
    t20 = subtotal_cost * 0.20
    
    tk.Button(frame_tips, text=f"15%\n({CURRENCY}{t15:.2f})", height=3, width=8, bg="#e0f7fa", command=lambda: set_tip(0.15)).pack(side="left", padx=5)
    tk.Button(frame_tips, text=f"18%\n({CURRENCY}{t18:.2f})", height=3, width=8, bg="#b2ebf2", command=lambda: set_tip(0.18)).pack(side="left", padx=5)
    tk.Button(frame_tips, text=f"20%\n({CURRENCY}{t20:.2f})", height=3, width=8, bg="#80deea", command=lambda: set_tip(0.20)).pack(side="left", padx=5)
    tk.Button(frame_tips, text="CUSTOM\n%", height=3, width=8, bg="#e1bee7", command=ask_custom_tip).pack(side="left", padx=5)

    tk.Label(pay_win, text="Select Payment Method:", font=("Arial", 12)).pack(pady=10)
    
    def pay_card():
        final_tip = selected_tip.get()
        final_total = subtotal_cost + tax_amount + final_tip
        lbl_status = tk.Label(pay_win, text="Processing...", fg="blue")
        lbl_status.pack()
        pay_win.update()
        time.sleep(1.0)
        pay_win.destroy()
        finalize_transaction(final_total, tax_amount, final_tip)

    def pay_cash():
        final_tip = selected_tip.get()
        final_total = subtotal_cost + tax_amount + final_tip
        tendered = simpledialog.askfloat("Cash", f"Total is {CURRENCY}{final_total:.2f}\nAmount Tendered:")
        if tendered:
            if tendered >= final_total:
                change = tendered - final_total
                messagebox.showinfo("Change", f"Change Due: {CURRENCY}{change:.2f}")
                pay_win.destroy()
                finalize_transaction(final_total, tax_amount, final_tip, change)
            else:
                messagebox.showerror("Error", "Insufficient Funds")

    tk.Button(pay_win, text="CREDIT CARD 💳", bg="#bbdefb", width=30, height=2, command=pay_card).pack(pady=5)
    tk.Button(pay_win, text="CASH 💵", bg="#c8e6c9", width=30, height=2, command=pay_cash).pack(pady=5)

# --- 7. MAIN WINDOW SETUP ---
root = tk.Tk()
title_text = f"KitchenOS POS - {SETTINGS['restaurant_name']}"
root.title(title_text)
root.geometry("700x650")

frame_menu = tk.Frame(root, padx=10, pady=10)
frame_menu.grid(row=0, column=0, sticky="n")

tk.Label(frame_menu, text="MENU", font=("Arial", 16, "bold")).pack(pady=5)
tk.Button(frame_menu, text=f"Burger ({CURRENCY}12.50)", width=15, height=2, bg="#e1f5fe", command=lambda: add_item("Burger", 12.50)).pack(pady=5)
tk.Button(frame_menu, text=f"Fries ({CURRENCY}3.50)", width=15, height=2, bg="#e1f5fe", command=lambda: add_item("Fries", 3.50)).pack(pady=5)
tk.Button(frame_menu, text=f"Steak ({CURRENCY}25.00)", width=15, height=2, bg="#e1f5fe", command=lambda: add_item("Steak", 25.00)).pack(pady=5)
tk.Button(frame_menu, text=f"Soda ({CURRENCY}1.99)", width=15, height=2, bg="#e1f5fe", command=lambda: add_item("Soda", 1.99)).pack(pady=5)
tk.Button(frame_menu, text="[MANAGER RESTOCK]", font=("Arial", 8), fg="gray", command=open_manager_portal).pack(pady=20)

frame_ticket = tk.Frame(root, padx=20, pady=10)
frame_ticket.grid(row=0, column=1, sticky="n")

tk.Label(frame_ticket, text="PENDING TICKET", font=("Arial", 16, "bold")).pack()
list_ticket = tk.Listbox(frame_ticket, width=40, height=18)
list_ticket.pack(pady=10)
label_total = tk.Label(frame_ticket, text=f"TOTAL: {CURRENCY}0.00", font=("Arial", 16, "bold"), fg="green", justify="right")
label_total.pack()

frame_buttons = tk.Frame(frame_ticket)
frame_buttons.pack(pady=10)
tk.Button(frame_buttons, text="ADJUST QTY", bg="#fff3e0", fg="#e65100", width=12, height=2, command=modify_selected_item).pack(side="left", padx=5)
tk.Button(frame_buttons, text="VOID ALL", bg="#ffcccc", fg="red", width=12, height=2, command=void_all).pack(side="left", padx=5)
tk.Button(frame_buttons, text="CHECKOUT", bg="#ccffcc", fg="green", font=("Arial", 12, "bold"), width=12, height=2, command=open_checkout_window).pack(side="left", padx=5)

root.mainloop()