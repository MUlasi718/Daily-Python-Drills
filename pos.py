#Day 24: Connected POS (Smart Adjustment Edition)
#Goal: Allow partial quantity removals (e.g., Remove 2 from a stack of 22).

import tkinter as tk
from tkinter import simpledialog, messagebox
import sqlite3

# --- DATABASE SETUP ---
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
    conn.commit()
    conn.close()

ensure_ticket_table()

# --- INVENTORY LOGIC ---
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
    print(f" [LOG] Restocked {qty}x {item_name}")

# --- GLOBAL VARIABLES ---
total_cost = 0.0
current_cart = [] 

# --- GUI FUNCTIONS ---

def add_item(item_name, item_price):
    global total_cost
    
    qty = simpledialog.askinteger("Quantity", f"How many {item_name}s?", minvalue=1, initialvalue=1)
    
    if qty:
        status = check_and_decrement(item_name, qty)
        
        if status == True:
            mod = simpledialog.askstring("Order", f"Notes for these {qty} items?")
            note_text = mod if mod else "None"
            
            #Math
            batch_price = item_price * qty
            order_line = f"{qty}x {item_name} ({note_text})"
            
            #STORE DATA (Added 'unit_price' so we can adjust later)
            current_cart.append({
                "line": order_line, 
                "name": item_name, 
                "qty": qty, 
                "price": batch_price,
                "unit_price": item_price,  # <--- CRITICAL FOR ADJUSTMENTS
                "note": note_text
            })
            
            #Update GUI
            display_text = f"{item_name} (x{qty}) [{note_text}] - ${batch_price:.2f}"
            list_ticket.insert(tk.END, display_text)
            
            total_cost += batch_price
            label_total.config(text=f"TOTAL: ${total_cost:.2f}")
            
        else:
            available = status[1]
            messagebox.showwarning("86'd", f"Chef! We only have {available} {item_name}s left.")

def modify_selected_item():
    global total_cost
    
    #Get Selection
    selected_indices = list_ticket.curselection()
    
    if not selected_indices:
        messagebox.showwarning("Select Item", "Please click an item to modify.")
        return
        
    index = selected_indices[0]
    item = current_cart[index]
    
    # 2. Ask "How many to remove?"
    current_qty = item['qty']
    
    #If there's only 1, just delete it.
    if current_qty == 1:
        qty_to_remove = 1
    else:
        #If there are multiple, ask the user.
        qty_to_remove = simpledialog.askinteger("Adjust Quantity", 
                                              f"You have {current_qty}x {item['name']}.\nHow many do you want to REMOVE?", 
                                              minvalue=1, maxvalue=current_qty)
        if not qty_to_remove:
            return # User hit Cancel

    #Restore Stock
    restore_stock(item['name'], qty_to_remove)
    
    #Calculate Refund
    refund_amount = item['unit_price'] * qty_to_remove
    total_cost -= refund_amount
    
    #Logic Split: Partial Removal vs Full Deletion
    if qty_to_remove == current_qty:
        #Full Deletion
        del current_cart[index]
        list_ticket.delete(index)
        print(f" [LOG] Removed entire line: {item['name']}")
    else:
        #Partial Adjustment
        item['qty'] -= qty_to_remove
        item['price'] -= refund_amount
        
        #Update the visual text
        new_text = f"{item['name']} (x{item['qty']}) [{item['note']}] - ${item['price']:.2f}"
        
        #Update listbox (delete old line, insert new line at same spot)
        list_ticket.delete(index)
        list_ticket.insert(index, new_text)
        
        #Update the hidden cart data
        item['line'] = f"{item['qty']}x {item['name']} ({item['note']})"
        
        print(f" [LOG] Adjusted {item['name']} down to {item['qty']}")

    #Update Total Display
    label_total.config(text=f"TOTAL: ${total_cost:.2f}")

def fire_ticket():
    global total_cost, current_cart
    
    if not current_cart:
        messagebox.showinfo("Empty", "Ticket is empty!")
        return
    
    try:
        conn = sqlite3.connect("kitchen.db")
        cursor = conn.cursor()
        
        full_ticket_text = "\n".join([item["line"] for item in current_cart])
        
        cursor.execute("INSERT INTO active_tickets (items) VALUES (?)", (full_ticket_text,))
        conn.commit()
        conn.close()
        
        print(f" [FIRE] Sent {len(current_cart)} items to Kitchen.")
        messagebox.showinfo("Success", "Ticket Fired to Kitchen!")
        
        list_ticket.delete(0, tk.END)
        current_cart = []
        total_cost = 0.0
        label_total.config(text="TOTAL: $0.00")
        
    except Exception as e:
        print(f" [ERROR] Fire failed: {e}")

def void_all():
    global total_cost, current_cart
    if not current_cart: return

    for item in current_cart:
        restore_stock(item['name'], item['qty'])
        
    list_ticket.delete(0, tk.END)
    current_cart = []
    total_cost = 0.0
    label_total.config(text="TOTAL: $0.00")
    print(" [LOG] Ticket Voided. Stock returned.")

# --- MAIN WINDOW SETUP ---
root = tk.Tk()
root.title("KitchenOS Smart POS")
root.geometry("700x600")

#Left Side: Menu
frame_menu = tk.Frame(root, padx=10, pady=10)
frame_menu.grid(row=0, column=0, sticky="n")

tk.Label(frame_menu, text="MENU", font=("Arial", 16, "bold")).pack(pady=5)

tk.Button(frame_menu, text="Burger ($12.50)", width=15, height=2, bg="#e1f5fe",
          command=lambda: add_item("Burger", 12.50)).pack(pady=5)

tk.Button(frame_menu, text="Fries ($3.50)", width=15, height=2, bg="#e1f5fe",
          command=lambda: add_item("Fries", 3.50)).pack(pady=5)

tk.Button(frame_menu, text="Steak ($25.00)", width=15, height=2, bg="#e1f5fe",
          command=lambda: add_item("Steak", 25.00)).pack(pady=5)

tk.Button(frame_menu, text="Soda ($1.99)", width=15, height=2, bg="#e1f5fe",
          command=lambda: add_item("Soda", 1.99)).pack(pady=5)

#Right Side: Ticket
frame_ticket = tk.Frame(root, padx=20, pady=10)
frame_ticket.grid(row=0, column=1, sticky="n")

tk.Label(frame_ticket, text="PENDING TICKET", font=("Arial", 16, "bold")).pack()

list_ticket = tk.Listbox(frame_ticket, width=40, height=18)
list_ticket.pack(pady=10)

label_total = tk.Label(frame_ticket, text="TOTAL: $0.00", font=("Arial", 18, "bold"), fg="green")
label_total.pack()

#BUTTON ROW
frame_buttons = tk.Frame(frame_ticket)
frame_buttons.pack(pady=10)

#Remove/Modify Item (Orange)
tk.Button(frame_buttons, text="ADJUST QTY", bg="#fff3e0", fg="#e65100", width=12, height=2, command=modify_selected_item).pack(side="left", padx=5)

#Void All (Red)
tk.Button(frame_buttons, text="VOID ALL", bg="#ffcccc", fg="red", width=12, height=2, command=void_all).pack(side="left", padx=5)

#Fire (Green)
tk.Button(frame_buttons, text="FIRE ORDER", bg="#ccffcc", fg="green", font=("Arial", 12, "bold"), width=12, height=2, command=fire_ticket).pack(side="left", padx=5)

root.mainloop()