#Day 24: Connected POS (GUI + Database)
#Goal: Decrement inventory in real-time when buttons are clicked.

import tkinter as tk
from tkinter import simpledialog, messagebox
import sqlite3

#--- DATABASE FUNCTION ---
def check_and_decrement(item_name):
    #Connect to the DB
    conn = sqlite3.connect("kitchen.db")
    cursor = conn.cursor()
    
    #1. Check Stock
    cursor.execute("SELECT stock_count FROM inventory WHERE name = ?", (item_name,))
    result = cursor.fetchone()
    
    if result:
        current_stock = result[0]
        
        if current_stock > 0:
            #2. Decrement Stock
            new_stock = current_stock - 1
            cursor.execute("UPDATE inventory SET stock_count = ? WHERE name = ?", (new_stock, item_name))
            conn.commit()
            conn.close()
            return True #Success!
        else:
            conn.close()
            return False #Out of Stock (86'd)
    else:
        conn.close()
        messagebox.showerror("Error", f"Item '{item_name}' not found in DB.")
        return False

#--- GLOBAL VARIABLES ---
total_cost = 0.0

#--- GUI FUNCTIONS ---
def add_item(item_name, item_price):
    global total_cost
    
    #STEP 1: Check the Database FIRST
    if check_and_decrement(item_name):
        
        #STEP 2: Ask for Mods (Only if in stock)
        mod = simpledialog.askstring("Order", f"Notes for {item_name}?")
        
        #STEP 3: Add to Ticket
        if mod:
            line_item = f"{item_name} ({mod}) - ${item_price:.2f}"
        else:
            line_item = f"{item_name} - ${item_price:.2f}"
            
        list_ticket.insert(tk.END, line_item)
        
        #STEP 4: Update Total
        total_cost += item_price
        label_total.config(text=f"TOTAL: ${total_cost:.2f}")
        
        print(f" [LOG] Sold {item_name}. Stock updated.")
        
    else:
        #STEP 5: Handle Out of Stock
        messagebox.showwarning("86'd", f"Sorry, Chef. No more {item_name}s!")

def clear_ticket():
    global total_cost
    list_ticket.delete(0, tk.END)
    total_cost = 0.0
    label_total.config(text="TOTAL: $0.00")

#--- MAIN WINDOW SETUP ---
root = tk.Tk()
root.title("KitchenOS Connected POS")
root.geometry("600x400")

#--- LAYOUT ---
#Left: Menu
frame_menu = tk.Frame(root, padx=10, pady=10)
frame_menu.grid(row=0, column=0, sticky="n")

tk.Label(frame_menu, text="LIVE MENU", font=("Arial", 16, "bold")).pack(pady=5)

#Buttons
tk.Button(frame_menu, text="Burger ($12.50)", width=15, 
          command=lambda: add_item("Burger", 12.50)).pack(pady=5)

tk.Button(frame_menu, text="Steak ($25.00)", width=15, 
          command=lambda: add_item("Steak", 25.00)).pack(pady=5)

#Right: Ticket
frame_ticket = tk.Frame(root, padx=20, pady=10)
frame_ticket.grid(row=0, column=1, sticky="n")

tk.Label(frame_ticket, text="ACTIVE TICKET", font=("Arial", 16, "bold")).pack()

list_ticket = tk.Listbox(frame_ticket, width=30, height=15)
list_ticket.pack(pady=10)

label_total = tk.Label(frame_ticket, text="TOTAL: $0.00", font=("Arial", 18, "bold"), fg="green")
label_total.pack()

tk.Button(frame_ticket, text="VOID TICKET", bg="red", command=clear_ticket).pack(pady=5)

#--- RUN LOOP ---
root.mainloop()