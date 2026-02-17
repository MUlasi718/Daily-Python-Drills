#Day 23: The POS System (Pop-up Edition)
#Goal: Click Item -> Pop-up asks for Mods -> Add to Ticket.

import tkinter as tk
from tkinter import simpledialog #The tool for pop-ups

#--- GLOBAL VARIABLES ---
total_cost = 0.0

#--- FUNCTIONS ---
def add_item(item_name, item_price):
    global total_cost
    
    #1. Open a Pop-up Window immediately
    #parent=root keeps the pop-up on top of the main window
    mod = simpledialog.askstring("Special Request", f"Notes for {item_name}? (Cancel for none):", parent=root)
    
    #2. Format the line item
    if mod:
        line_item = f"{item_name} *{mod}* - ${item_price:.2f}"
    else:
        line_item = f"{item_name} - ${item_price:.2f}"
        
    #3. Add to the Ticket
    list_ticket.insert(tk.END, line_item)
    
    #4. Update the Money
    total_cost += item_price
    label_total.config(text=f"TOTAL: ${total_cost:.2f}")

def clear_ticket():
    global total_cost
    list_ticket.delete(0, tk.END)
    total_cost = 0.0
    label_total.config(text="TOTAL: $0.00")

#--- MAIN WINDOW ---
root = tk.Tk()
root.title("KitchenOS Point of Sale")
root.geometry("600x400")

#--- SECTION 1: THE MENU (Left Side) ---
frame_menu = tk.Frame(root, padx=10, pady=10)
frame_menu.grid(row=0, column=0, sticky="n")

tk.Label(frame_menu, text="MENU", font=("Arial", 16, "bold")).pack(pady=5)

#Menu Buttons
tk.Button(frame_menu, text="Burger ($12.50)", width=15, bg="#f0f0f0",
          command=lambda: add_item("Burger", 12.50)).pack(pady=5)

tk.Button(frame_menu, text="Fries ($3.50)", width=15, 
          command=lambda: add_item("Fries", 3.50)).pack(pady=5)

tk.Button(frame_menu, text="Soda ($1.99)", width=15, 
          command=lambda: add_item("Soda", 1.99)).pack(pady=5)

tk.Button(frame_menu, text="Steak ($25.00)", width=15, 
          command=lambda: add_item("Steak", 25.00)).pack(pady=5)

#--- SECTION 2: THE TICKET (Right Side) ---
#We removed the middle section because the Pop-up replaced it!
frame_ticket = tk.Frame(root, padx=20, pady=10)
frame_ticket.grid(row=0, column=1, sticky="n")

tk.Label(frame_ticket, text="CURRENT TICKET", font=("Arial", 16, "bold")).pack()

list_ticket = tk.Listbox(frame_ticket, width=35, height=15)
list_ticket.pack(pady=10)

label_total = tk.Label(frame_ticket, text="TOTAL: $0.00", font=("Arial", 18, "bold"), fg="green")
label_total.pack()

tk.Button(frame_ticket, text="VOID TICKET", bg="red", fg="black", command=clear_ticket).pack(pady=5)

#--- RUN LOOP ---
root.mainloop()