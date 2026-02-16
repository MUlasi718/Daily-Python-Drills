#Day 19: Database Manager (Update & Delete)
#Day 19 Goal: Modify data inside the kitchen.db using SQL.

import sqlite3

#The database file we are managing
db_file = "kitchen.db"

#--- FUNCTION 1: VIEW (Read) ---
def view_inventory():
    try:
        #Connect specifically for this task
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM inventory")
        items = cursor.fetchall()
        
        print(f"\n--- CURRENT INVENTORY ---")
        print(f"{'ID':<5} | {'ITEM':<15} | {'PRICE':<10} | {'STOCK'}")
        print("-" * 50)
        for item in items:
            #item is (id, name, price, stock)
            print(f"{item[0]:<5} | {item[1]:<15} | ${item[2]:<9.2f} | {item[3]}")
        print("-" * 50)
        
    except sqlite3.Error as e:
        print(f" [ERROR] Database access failed: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

#--- FUNCTION 2: UPDATE (Modify) ---
def update_stock():
    view_inventory() #Show them what they have first
    
    item_name = input("\nEnter Item Name to Update (e.g. Burger): ")
    try:
        new_stock = int(input(f"Enter new stock count for {item_name}: "))
        
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        #SQL UPDATE COMMAND
        #We use '?' placeholders to prevent hacking (SQL Injection)
        command = "UPDATE inventory SET stock_count = ? WHERE name = ?"
        
        cursor.execute(command, (new_stock, item_name))
        conn.commit() #Save the change!
        
        if cursor.rowcount == 0:
            print(f" [ERROR] Item '{item_name}' not found.")
        else:
            print(f" [SUCCESS] Updated {item_name} stock to {new_stock}.")
            
    except ValueError:
        print(" [!] Error: Stock must be a number.")
    except Exception as e:
        print(f" [CRITICAL] Update failed: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

#--- FUNCTION 3: DELETE (Remove) ---
def delete_item():
    view_inventory()
    
    item_name = input("\nEnter Item Name to DELETE (Warning: Permanent): ")
    confirm = input(f"Are you sure you want to delete {item_name}? (y/n): ")
    
    if confirm.lower() == 'y':
        try:
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()
            
            #SQL DELETE COMMAND
            command = "DELETE FROM inventory WHERE name = ?"
            
            cursor.execute(command, (item_name,))
            conn.commit()
            
            if cursor.rowcount == 0:
                print(f" [ERROR] Item '{item_name}' not found.")
            else:
                print(f" [GONE] {item_name} has been removed from the database.")
        
        except sqlite3.Error as e:
            print(f" [ERROR] Delete failed: {e}")
        finally:
            if 'conn' in locals():
                conn.close()

#--- MAIN MENU LOOP ---
while True:
    print("\n=== KITCHEN DB MANAGER ===")
    print("1. View Inventory")
    print("2. Update Stock (Sale/Restock)")
    print("3. Delete Item (86'd)")
    print("4. Exit")
    
    choice = input("\nSelect Option: ")
    
    if choice == '1':
        view_inventory()
    elif choice == '2':
        update_stock()
    elif choice == '3':
        delete_item()
    elif choice == '4':
        print("System Closing.")
        break
    else:
        print("Invalid Selection.")