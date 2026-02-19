# Day 27: The Manager's Dashboard 📊
# Fixes: CSV Header parsing, Matplotlib Circle object

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import csv
import os
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Circle # <--- NEW: Required for the Donut Chart

# --- 1. DATA FETCHING FUNCTIONS ---

def get_inventory_data():
    try:
        conn = sqlite3.connect("kitchen.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name, stock_count FROM inventory WHERE stock_count > 0")
        data = cursor.fetchall()
        conn.close()
        return data
    except Exception as e:
        print(f"[DB ERROR] {e}")
        return []

def get_financial_data():
    names = []
    profits = []
    try:
        if not os.path.exists("kitchen_financials.csv"):
            return [], []
        
        with open("kitchen_financials.csv", "r") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 4:
                    try:
                        # Try to convert to a number. 
                        # If it fails (because it's the header "Profit"), it skips safely!
                        prof_val = float(row[3])
                        names.append(row[0][:10]) # Truncate long names to 10 chars
                        profits.append(prof_val)
                    except ValueError:
                        pass # It's a header row, just ignore it.
        return names, profits
    except Exception as e:
        print(f"[CSV ERROR] {e}")
        return [], []

def get_marketing_data():
    methods = {"EMAIL": 0, "SMS": 0}
    try:
        if not os.path.exists("marketing_list.csv"):
            return methods
            
        with open("marketing_list.csv", "r") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 4:
                    method = row[3]
                    if "EMAIL" in method:
                        methods["EMAIL"] += 1
                    elif "SMS" in method:
                        methods["SMS"] += 1
        return methods
    except Exception as e:
        print(f"[CSV ERROR] {e}")
        return methods


# --- 2. GUI & CHART DRAWING ---

def launch_dashboard():
    root = tk.Tk()
    root.title("KitchenOS - Manager Dashboard")
    root.geometry("800x600")

    # Create Tabs
    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True, padx=10, pady=10)

    tab1 = ttk.Frame(notebook)
    tab2 = ttk.Frame(notebook)
    tab3 = ttk.Frame(notebook)

    notebook.add(tab1, text="📦 Inventory Health")
    notebook.add(tab2, text="💰 Profit Margins")
    notebook.add(tab3, text="📈 Marketing Capture")

    # --- TAB 1: INVENTORY PIE CHART ---
    inv_data = get_inventory_data()
    if inv_data:
        labels = [item[0] for item in inv_data]
        sizes = [item[1] for item in inv_data]
        
        fig1 = Figure(figsize=(6, 5), dpi=100)
        ax1 = fig1.add_subplot(111)
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=['#ff9999','#66b3ff','#99ff99','#ffcc99'])
        ax1.set_title("Current Stock Distribution")
        
        canvas1 = FigureCanvasTkAgg(fig1, master=tab1)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill="both", expand=True)
    else:
        tk.Label(tab1, text="No Inventory Data Available.", font=("Arial", 14)).pack(pady=50)

    # --- TAB 2: FINANCIAL BAR CHART ---
    dish_names, dish_profits = get_financial_data()
    if dish_names:
        fig2 = Figure(figsize=(6, 5), dpi=100)
        ax2 = fig2.add_subplot(111)
        ax2.bar(dish_names, dish_profits, color='lightgreen')
        ax2.set_title("Profit per Dish ($)")
        ax2.set_ylabel("Profit")
        
        # Rotate x labels so they don't overlap
        ax2.tick_params(axis='x', labelrotation=45)
        fig2.tight_layout() # Fixes cutoff labels
        
        canvas2 = FigureCanvasTkAgg(fig2, master=tab2)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill="both", expand=True)
    else:
        tk.Label(tab2, text="No Financial Data Available. Use Station 13 first.", font=("Arial", 14)).pack(pady=50)

    # --- TAB 3: MARKETING DONUT CHART ---
    mkt_data = get_marketing_data()
    if sum(mkt_data.values()) > 0:
        fig3 = Figure(figsize=(6, 5), dpi=100)
        ax3 = fig3.add_subplot(111)
        
        labels = list(mkt_data.keys())
        sizes = list(mkt_data.values())
        
        # Donut Chart Magic (Fixed Circle import)
        wedges, texts, autotexts = ax3.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['#c2c2f0','#ffb3e6'])
        centre_circle = Circle((0,0), 0.70, fc='white') # <-- Fixed Line
        ax3.add_artist(centre_circle)
        
        ax3.set_title("Receipt Delivery Preferences")
        
        canvas3 = FigureCanvasTkAgg(fig3, master=tab3)
        canvas3.draw()
        canvas3.get_tk_widget().pack(fill="both", expand=True)
    else:
        tk.Label(tab3, text="No Marketing Data Available. Ring up guests first.", font=("Arial", 14)).pack(pady=50)

    # Close Button
    tk.Button(root, text="CLOSE DASHBOARD", bg="red", fg="white", font=("Arial", 12, "bold"), command=root.destroy).pack(pady=10)

    root.mainloop()

# Launch Guard
if __name__ == "__main__":
    launch_dashboard()