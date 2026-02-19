# Day 26: The PLATINUM POS (Final + Tendered Amount) 💎
# Fixes: Missing "Tendered" amount on receipt
# Features: Emojis, Data Capture, Smart Inventory, Snapshot Receipts, Single Window

import tkinter as tk
from tkinter import simpledialog, messagebox
import sqlite3
import datetime
import os
import requests 
import csv 
from copy import deepcopy 

# --- 0. CONFIGURATION ---
SETTINGS = {
    "restaurant_name": "MMADU'S KITCHEN",
    "address_line_1": "123 Griffin Blvd",
    "address_line_2": "Griffin, GA 30223",
    "currency_symbol": "$",
    "tax_rate": 0.08
}

# --- 1. GLOBAL STATE ---
subtotal_cost = 0.0
current_cart = [] 
CURRENCY = "$" 
TAX_RATE = 0.08

# --- 2. DATABASE & INVENTORY ---
def ensure_tables():
    conn = sqlite3.connect("kitchen.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS active_tickets (id INTEGER PRIMARY KEY, items TEXT, status TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS inventory (name TEXT UNIQUE, stock_count INTEGER)")
    
    cursor.execute("SELECT count(*) FROM inventory")
    if cursor.fetchone()[0] == 0:
        items = [("Burger", 20), ("Fries", 50), ("Steak", 10), ("Soda", 50)]
        cursor.executemany("INSERT OR IGNORE INTO inventory (name, stock_count) VALUES (?, ?)", items)
        conn.commit()
    conn.close()

def check_stock(name, qty):
    conn = sqlite3.connect("kitchen.db")
    cursor = conn.cursor()
    cursor.execute("SELECT stock_count FROM inventory WHERE name=?", (name,))
    res = cursor.fetchone()
    if res:
        current = res[0]
        if current >= qty:
            cursor.execute("UPDATE inventory SET stock_count = stock_count - ? WHERE name=?", (qty, name))
            conn.commit()
            conn.close()
            return True
        else:
            conn.close()
            return False, current 
    conn.close()
    return False, 0

def restore_stock(name, qty):
    conn = sqlite3.connect("kitchen.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE inventory SET stock_count = stock_count + ? WHERE name=?", (qty, name))
    conn.commit()
    conn.close()

# --- 3. PDF ENGINE (With Tendered Amount) ---
def generate_receipt_pdf(snap_cart, snap_subtotal, tax, tip, grand_total, change_due=0.0, customer_name="Guest", tendered=0.0):
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
    except ImportError:
        return

    now = datetime.datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    filename = f"Receipt_{timestamp}.pdf"
    
    try:
        c = canvas.Canvas(filename, pagesize=letter)
        
        # Header
        c.setFont("Helvetica-Bold", 20)
        c.drawCentredString(300, 750, SETTINGS["restaurant_name"])
        c.setFont("Helvetica", 10)
        c.drawCentredString(300, 735, SETTINGS["address_line_1"])
        c.drawCentredString(300, 720, SETTINGS["address_line_2"])
        c.drawCentredString(300, 710, "-"*50)
        
        # Metadata
        c.drawString(100, 690, f"Date: {now.strftime('%Y-%m-%d %H:%M')}")
        c.drawString(100, 675, f"Ticket #: {timestamp[-6:]}")
        c.setFont("Helvetica-Bold", 11)
        c.drawString(100, 660, f"CUSTOMER: {customer_name.upper()}")
        
        # Items Header
        y = 630 
        c.setFont("Helvetica-Bold", 12)
        c.drawString(100, y, "ITEM")
        c.drawRightString(500, y, "PRICE")
        c.line(100, y-5, 500, y-5)
        
        y -= 25 
        c.setFont("Helvetica", 11)
        
        # Items Loop
        for item in snap_cart:
            name_line = f"{item['qty']}x {item['name']}"
            price_line = f"{CURRENCY}{item['price']:.2f}" 
            
            c.drawString(100, y, name_line)
            c.drawRightString(500, y, price_line)
            
            if item['note'] != "None":
                y -= 15
                c.setFont("Helvetica-Oblique", 9)
                c.drawString(120, y, f"* {item['note']}")
                c.setFont("Helvetica", 11)
            y -= 20 
            
        # --- TOTALS SECTION ---
        y -= 20 
        
        c.setFont("Helvetica", 11)
        c.drawString(320, y, "Subtotal:")
        c.drawRightString(500, y, f"{CURRENCY}{snap_subtotal:.2f}")
        
        y -= 15
        tax_pct = SETTINGS['tax_rate'] * 100
        c.drawString(320, y, f"Tax ({tax_pct:.1f}%):")
        c.drawRightString(500, y, f"{CURRENCY}{tax:.2f}")
        
        if tip > 0:
            y -= 15
            c.drawString(320, y, "Gratuity:")
            c.drawRightString(500, y, f"{CURRENCY}{tip:.2f}")
            
        y -= 25
        c.setFont("Helvetica-Bold", 14)
        c.drawString(320, y, "TOTAL PAID:")
        c.drawRightString(500, y, f"{CURRENCY}{grand_total:.2f}")
        
        # SHOW TENDERED AMOUNT (If Cash)
        if tendered > 0:
            y -= 15
            c.setFont("Helvetica", 11)
            c.drawString(320, y, "Tendered:")
            c.drawRightString(500, y, f"{CURRENCY}{tendered:.2f}")

        if change_due > 0:
            y -= 20
            c.setFont("Helvetica-Bold", 12)
            c.drawString(320, y, "Change Due:")
            c.drawRightString(500, y, f"{CURRENCY}{change_due:.2f}")

        c.setFont("Helvetica-Oblique", 10)
        c.drawCentredString(300, 50, "Thank you for dining with us!")
        
        c.save()
        print(f" [PDF] Receipt saved: {filename}")
        
    except Exception as e:
        print(f" [ERROR] PDF Generation failed: {e}")

# --- 4. THE POS SYSTEM ---
def start_pos_system():
    root = tk.Tk()
    root.title(f"KitchenOS POS - {SETTINGS['restaurant_name']}")
    root.geometry("700x650")

    def update_gui_label():
        tax = subtotal_cost * TAX_RATE
        label_total.config(text=f"SUB: {CURRENCY}{subtotal_cost:.2f}\n(Est. Total: {CURRENCY}{subtotal_cost + tax:.2f})")

    def add_item_handler(name, price):
        global subtotal_cost
        qty = simpledialog.askinteger("Quantity", f"How many {name}?", minvalue=1)
        if qty:
            status = check_stock(name, qty)
            if status == True:
                note = simpledialog.askstring("Order", "Notes?") or "None"
                batch_price = price * qty
                current_cart.append({
                    "line": f"{qty}x {name} ({note})", 
                    "name": name, "qty": qty, "price": batch_price,
                    "unit_price": price, "note": note
                })
                list_ticket.insert(tk.END, f"{name} (x{qty}) [{note}] - {CURRENCY}{batch_price:.2f}")
                subtotal_cost += batch_price
                update_gui_label()
            else:
                available = status[1]
                messagebox.showwarning("86'd", f"Chef! We only have {available} {name}s left.")

    def modify_item_handler():
        global subtotal_cost
        sel = list_ticket.curselection()
        if not sel: return
        idx = sel[0]
        item = current_cart[idx]
        
        qty_rm = simpledialog.askinteger("Adjust", "Remove how many?", minvalue=1, maxvalue=item['qty'])
        if not qty_rm: return
        
        restore_stock(item['name'], qty_rm)
        refund = item['unit_price'] * qty_rm
        subtotal_cost -= refund
        
        if qty_rm == item['qty']:
            del current_cart[idx]
            list_ticket.delete(idx)
        else:
            item['qty'] -= qty_rm
            item['price'] -= refund
            list_ticket.delete(idx)
            list_ticket.insert(idx, f"{item['name']} (x{item['qty']}) [{item['note']}] - {CURRENCY}{item['price']:.2f}")
        
        update_gui_label()

    def void_all_handler():
        global subtotal_cost, current_cart
        if not current_cart: return
        for item in current_cart:
            restore_stock(item['name'], item['qty'])
        list_ticket.delete(0, tk.END)
        current_cart = []
        subtotal_cost = 0.0
        update_gui_label()

    def open_manager_handler():
        mgr = tk.Toplevel(root)
        mgr.title("Inventory")
        mgr.geometry("300x400")
        lb = tk.Listbox(mgr, width=35)
        lb.pack(pady=10)
        
        def refresh():
            lb.delete(0, tk.END)
            conn = sqlite3.connect("kitchen.db")
            for row in conn.execute("SELECT name, stock_count FROM inventory"):
                lb.insert(tk.END, f"{row[0]}: {row[1]}")
            conn.close()
        
        def update():
            sel = lb.curselection()
            if not sel: return
            name = lb.get(sel[0]).split(":")[0]
            qty = simpledialog.askinteger("Restock", f"New count for {name}:")
            if qty is not None:
                conn = sqlite3.connect("kitchen.db")
                conn.execute("UPDATE inventory SET stock_count=? WHERE name=?", (qty, name))
                conn.commit()
                conn.close()
                refresh()
        
        refresh()
        tk.Button(mgr, text="Update Stock", command=update).pack()

    # --- RECEIPT PORTAL ---
    # UPDATED: Now accepts 'tendered'
    def open_receipt_portal(grand, tax, tip, change, cart_snap, sub_snap, method, tendered=0.0):
        win = tk.Toplevel(root)
        win.title("Receipt Options")
        win.geometry("350x350")
        
        tk.Label(win, text="Transaction Approved!", font=("Arial", 14, "bold"), fg="green").pack(pady=10)
        tk.Label(win, text=f"Paid via {method}", font=("Arial", 10)).pack()
        tk.Label(win, text="How would you like your receipt?", font=("Arial", 12)).pack(pady=10)
        
        def do_print():
            generate_receipt_pdf(cart_snap, sub_snap, tax, tip, grand, change, tendered=tendered)
            messagebox.showinfo("Printed", "Receipt Sent to Printer.")
            win.destroy()
            
        def do_email():
            name = simpledialog.askstring("Name", "Customer Name:")
            if not name: return 
            email = simpledialog.askstring("Email", f"Email for {name}:")
            if email:
                with open("marketing_list.csv", "a", newline="") as f:
                    csv.writer(f).writerow([datetime.datetime.now(), name, email, "EMAIL"])
                generate_receipt_pdf(cart_snap, sub_snap, tax, tip, grand, change, name, tendered=tendered)
                messagebox.showinfo("Sent", f"Receipt emailed to {name}")
                win.destroy()
                
        def do_text():
            name = simpledialog.askstring("Name", "Customer Name:")
            if not name: return
            phone = simpledialog.askstring("Text", f"Mobile Number for {name}:")
            if phone:
                with open("marketing_list.csv", "a", newline="") as f:
                    csv.writer(f).writerow([datetime.datetime.now(), name, phone, "SMS"])
                generate_receipt_pdf(cart_snap, sub_snap, tax, tip, grand, change, name, tendered=tendered)
                messagebox.showinfo("Sent", f"Receipt texted to {name}")
                win.destroy()

        tk.Button(win, text="🖨️ PRINT RECEIPT", width=25, height=2, command=do_print).pack(pady=5)
        tk.Button(win, text="📧 EMAIL RECEIPT", width=25, height=2, command=do_email).pack(pady=5)
        tk.Button(win, text="📱 TEXT RECEIPT", width=25, height=2, command=do_text).pack(pady=5)
        tk.Button(win, text="NO RECEIPT", width=25, height=1, bg="#eee", command=win.destroy).pack(pady=10)

    # --- CHECKOUT HANDLER ---
    def open_checkout_handler():
        if not current_cart: return
        win = tk.Toplevel(root)
        win.title("Pay")
        win.geometry("400x500")
        
        tax = subtotal_cost * TAX_RATE
        tip_var = tk.DoubleVar(value=0.0)
        
        lbl = tk.Label(win, text=f"Total: {CURRENCY}{subtotal_cost+tax:.2f}", font=("Arial", 20, "bold"), fg="green")
        lbl.pack(pady=20)
        
        def set_tip(pct=None, val=None):
            t = val if val else subtotal_cost * pct
            tip_var.set(t)
            lbl.config(text=f"Total: {CURRENCY}{subtotal_cost+tax+t:.2f}")
            
        def custom():
            p = simpledialog.askfloat("Tip", "%:")
            if p: set_tip(pct=p/100)
            
        frame = tk.Frame(win)
        frame.pack()
        tk.Button(frame, text="15%", command=lambda: set_tip(0.15)).pack(side="left")
        tk.Button(frame, text="18%", command=lambda: set_tip(0.18)).pack(side="left")
        tk.Button(frame, text="20%", command=lambda: set_tip(0.20)).pack(side="left")
        tk.Button(frame, text="Custom", command=custom).pack(side="left")
        
        def finalize_step(method, tendered=None):
            global subtotal_cost, current_cart
            final_tip = tip_var.get()
            final_total = subtotal_cost + tax + final_tip
            change = tendered - final_total if tendered else 0.0
            
            # SNAPSHOT DATA
            cart_snap = deepcopy(current_cart)
            sub_snap = subtotal_cost       
            
            # SAVE DB
            conn = sqlite3.connect("kitchen.db")
            ticket_text = "\n".join([i["line"] for i in current_cart])
            conn.execute("INSERT INTO active_tickets (items) VALUES (?)", (ticket_text,))
            conn.commit()
            conn.close()
            
            # WIPE SYSTEM
            list_ticket.delete(0, tk.END)
            current_cart.clear()
            subtotal_cost = 0.0
            update_gui_label()
            
            win.destroy()
            
            # OPEN RECEIPT PORTAL (Passing tendered amount)
            open_receipt_portal(final_total, tax, final_tip, change, cart_snap, sub_snap, method, tendered if tendered else 0.0)

        def pay_cash():
            total = subtotal_cost+tax+tip_var.get()
            tender = simpledialog.askfloat("Cash", f"Total: {CURRENCY}{total:.2f}\nTendered:")
            if tender and tender >= total:
                finalize_step("CASH 💵", tender)
            else:
                messagebox.showerror("Error", "Insufficient Funds")
                
        tk.Button(win, text="CREDIT CARD 💳", bg="#bbdefb", width=30, height=2, command=lambda: finalize_step("CARD 💳")).pack(pady=10)
        tk.Button(win, text="CASH 💵", bg="#c8e6c9", width=30, height=2, command=pay_cash).pack(pady=5)

    # --- GUI LAYOUT ---
    frame_menu = tk.Frame(root, padx=10, pady=10)
    frame_menu.grid(row=0, column=0, sticky="n")

    tk.Label(frame_menu, text="MENU", font=("Arial", 16, "bold")).pack(pady=5)
    tk.Button(frame_menu, text=f"Burger ({CURRENCY}12.50)", width=15, height=2, bg="#e1f5fe", command=lambda: add_item_handler("Burger", 12.50)).pack(pady=5)
    tk.Button(frame_menu, text=f"Fries ({CURRENCY}3.50)", width=15, height=2, bg="#e1f5fe", command=lambda: add_item_handler("Fries", 3.50)).pack(pady=5)
    tk.Button(frame_menu, text=f"Steak ({CURRENCY}25.00)", width=15, height=2, bg="#e1f5fe", command=lambda: add_item_handler("Steak", 25.00)).pack(pady=5)
    tk.Button(frame_menu, text=f"Soda ({CURRENCY}1.99)", width=15, height=2, bg="#e1f5fe", command=lambda: add_item_handler("Soda", 1.99)).pack(pady=5)
    tk.Button(frame_menu, text="[MANAGER RESTOCK]", font=("Arial", 8), fg="gray", command=open_manager_handler).pack(pady=20)

    frame_ticket = tk.Frame(root, padx=20, pady=10)
    frame_ticket.grid(row=0, column=1, sticky="n")

    tk.Label(frame_ticket, text="PENDING TICKET", font=("Arial", 16, "bold")).pack()
    list_ticket = tk.Listbox(frame_ticket, width=40, height=18)
    list_ticket.pack(pady=10)
    label_total = tk.Label(frame_ticket, text=f"TOTAL: {CURRENCY}0.00", font=("Arial", 16, "bold"), fg="green", justify="right")
    label_total.pack()

    frame_buttons = tk.Frame(frame_ticket)
    frame_buttons.pack(pady=10)
    tk.Button(frame_buttons, text="ADJUST QTY", bg="#fff3e0", fg="#e65100", width=12, height=2, command=modify_item_handler).pack(side="left", padx=5)
    tk.Button(frame_buttons, text="VOID ALL", bg="#ffcccc", fg="red", width=12, height=2, command=void_all_handler).pack(side="left", padx=5)
    tk.Button(frame_buttons, text="CHECKOUT", bg="#ccffcc", fg="green", font=("Arial", 12, "bold"), width=12, height=2, command=open_checkout_handler).pack(side="left", padx=5)

    root.mainloop()

# --- 5. STARTUP GUARD ---
if __name__ == "__main__":
    ensure_tables()
    try:
        r = requests.get("http://ip-api.com/json/", timeout=1)
        if r.status_code == 200:
            d = r.json()
            SETTINGS["address_line_2"] = f"{d['city']}, {d['region']}"
            if d['region'] == 'GA': TAX_RATE = 0.08
    except: pass
    
    start_pos_system()