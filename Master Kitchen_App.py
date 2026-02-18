import time
import sys
import random
import datetime
import requests
import csv
import sqlite3
import matplotlib.pyplot as plt
import subprocess

#CONFIGURATION
#PASTE YOUR SPOONACULAR API KEY BELOW
SPOON_KEY = "c5bcb06058224f0193c38272d143e1c2" 

# --- STATION 1: IDENTITY & ACCESS (Days 1, 2, 3 & 5) ---
def run_login_system():
    print("\n" + "-"*30)
    print("--- STARTING LOGIN SYSTEM ---")
    
    #Day 1: Input
    Username = input("Enter username: ")
    Password = input("Enter password: ")
    
    #Masking
    mask = '*' * len(Password)
    print(f"User: {Username}")
    print(f"Pass: {mask}")
    
    #Day 2: Role Check
    if Username == 'John Doe':
        user_role = 'Admin'
    elif Username == 'M Ulasi':
        user_role = 'User'
    else:
        user_role = 'Guest'
    print(f"System: Recognized as [{user_role}]")

    #Day 3: Brute Force Loop
    correct_target = Password
    attempts = 0
    max_attempts = 3
    
    while attempts < max_attempts:
        user_input = input("Please re-enter password to verify: ")
        
        if user_input == correct_target:
            print("Access Granted. Whattup tho?")
            break
        else:
            print("Wrong Password. Try again.")
            attempts += 1
            
    if attempts == max_attempts:
        print("SYSTEM LOCKED! Dash wey yuhself.")

# --- STATION 2: FIREWALL (Day 4) ---
def run_firewall():
    print("\n" + "-"*30)
    print("FIREWALL SYSTEM STARTING...")
    
    allowed_ips = ["192.168.1.1","10.0.5.1","172.16.0.55","111.111.1.0"]
    allowed_ips.append("10.0.0.99")
    print(f"Allowed IPs: {allowed_ips}")
    
    user_ip = input("Enter IP Address to Verify: ")
    
    if user_ip in allowed_ips:
        print("Access Granted: IP matches whitelist.")
    else:
        print("Access Denied: Your IP is not authorized.")

# --- STATION 3: PASSWORD GENERATOR (Day 6) ---
def run_password_generator():
    print("\n" + "-"*30)
    print("SECURE PASSWORD GENERATOR")
    
    options = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%"
    password_list = random.choices(options, k=12)
    final_password = "".join(password_list)
    
    print(f"Generated Secure Password : {final_password}")

# --- STATION 4: KITCHEN MANAGER (Day 6 Part 2) ---
def run_daily_special():
    print("\n" + "-"*30)
    print("CHEF: DAILY SPECIAL")
    
    proteins = ["Chicken", "Beef", "Salmon", "Tofu"]
    sides = ["Rice", "Broccoli", "Potatoes", "Asparagus"]
    sauces = ["Teriyaki", "Garlic Butter", "Spicy Mayo", "Pesto"]
    
    p = random.choice(proteins)
    s = random.choice(sides)
    z = random.choice(sauces)
    
    special_text = f"Today's Special: Pan-seared {p} with {s} and {z} drizzle."
    print(special_text)
    
    with open("daily_menu.txt", "w") as file:
        file.write("--- TODAY'S SPECIAL ---\n")
        file.write(special_text)
        file.write("\n--------------------")
    print(" [SAVED] Menu written to daily_menu.txt")

# --- STATION 5: SECURITY LOGS (Day 7) ---
def update_logs():
    print("\n" + "-"*30)
    print("--- UPDATING SECURITY LOGS ---")
    
    current_time = datetime.datetime.now()
    log_entry = f"MANUAL LOG ENTRY: {current_time} - User: Admin\n"
    
    with open("security_log.txt", "a") as file:
        file.write(log_entry)
        
    print(f" [SUCCESS] Log entry appended to 'security_log.txt'")

# --- STATION 6: MENU READER (Day 8 + 9) ---
def view_last_menu():
    print("\n" + "-"*30)
    print("--- RETRIEVING LAST MENU ---")
    try:
        with open("daily_menu.txt", "r") as file:
            saved_menu = file.read()
            print(saved_menu)
    except FileNotFoundError:
        print(" [ERROR] No menu found. Please generate a Daily Special first.")

# --- STATION 7: LOG INSPECTOR (Day 8 + 9) ---
def view_security_logs():
    print("\n" + "-"*30)
    print("--- SECURITY LOG HISTORY ---")
    try:
        with open("security_log.txt", "r") as file:
            logs = file.read()
            print(logs)
    except FileNotFoundError:
        print(" [ERROR] No logs found. System is clean (or logs deleted).")

# --- STATION 8: PRICE CHECKER (Day 10) ---
def run_price_check():
    print("\n" + "-"*30)
    print("--- POS SYSTEM: PRICE CHECK ---")
    
    # The Database (Dictionary)
    menu_prices = {
        "Burger": 12.99,
        "Fries": 3.50,
        "Soda": 1.99,
        "Steak": 24.99,
        "Salad": 8.50,
        "Salmon": 18.99,
        "Tofu": 14.50
    }
    
    # .title() fixes casing (e.g., "burger" -> "Burger")
    item = input("Enter item to check: ").title() 
    
    # Look up the price
    price = menu_prices.get(item, "Not Found")
    
    if price == "Not Found":
        print(f" [ERROR] '{item}' is not in the database.")
    else:
        print(f" The price of {item} is: ${price}")

# --- STATION 9: POS SYSTEM (Day 11) ---
def run_pos_system():
    print("\n" + "-"*30)
    print("--- POS SYSTEM: OPEN TAB ---")
    
    menu = {
        "Burger": 12.99,
        "Fries": 3.50,
        "Soda": 1.99,
        "Steak": 24.99,
        "Salad": 8.50
    }
    
    total_bill = 0
    cart = []
    
    print("Menu: Burger, Fries, Soda, Steak, Salad")
    print("Commands: '3 Burger', '2 Del Soda', 'Done'")
    
    while True:
        raw_input = input("\nEnter Order: ").title()
        
        if raw_input == "Done":
            break
            
        parts = raw_input.split()
        qty = 1
        item_name = raw_input
        
        if len(parts) > 0 and parts[0].isdigit():
            qty = int(parts[0])
            item_name = " ".join(parts[1:])
            
        for i in range(qty):
            if item_name.startswith("Del"):
                clean_item = item_name.replace("Del ", "")
                if clean_item in cart:
                    price = menu[clean_item]
                    total_bill -= price
                    cart.remove(clean_item)
                    print(f" [VOID] Removed {clean_item}")
                else:
                    print(f" [ERROR] {clean_item} not in cart.")
            
            elif item_name in menu:
                price = menu[item_name]
                total_bill += price
                cart.append(item_name)
                print(f" + Added {item_name}")
            
            else:
                print(f" [ERROR] Item {item_name} not found.")
                break
        
        print(f" Running Total: ${total_bill:.2f}")

    # Final Receipt
    print("\n" + "-"*30)
    print("--- FINAL RECEIPT ---")
    unique_items = set(cart)
    for item in unique_items:
        q = cart.count(item)
        print(f"{item} x {q}")
    print(f"TOTAL DUE: ${total_bill:.2f}")
    print("-" * 30)

#STATION 10: API ORDER CHECK (Day 12)
def run_api_check():
    print('--- CONNECTING TO ORDER CLOUD ---')
    
    #Test URL
    url = 'https://jsonplaceholder.typicode.com/todos/1'
    
    print(f'Connecting to: {url}...')
    time.sleep(1)
    
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
           data = response.json()
           
           #Extract Data
           ticket_num = data['id']
           item_name = data['title']
           is_done = data['completed']
           
           print(' [SUCCESS] Connection Established.\n')
           print('--- INCOMING TICKET ---')
           print(f' Ticket #:  {ticket_num}')
           print(f' Item:      {item_name}')
           print(f" Status:    {'READY' if is_done else 'PENDING'}")
           print('----------------------------')
        else:
            print(f' [ERROR] Server returned: {response.status_code}')
            
    except Exception as e:
        print(f' [CRITICAL ERROR] Connection failed: {e}')
        
# --- STATION 11: HOST STAND (Day 13 - Upgraded) ---
def run_host_stand():
    print("\n" + "-"*30)
    print("--- HOST STAND: DOWNLOADING RESERVATIONS ---")
    
    url = "https://jsonplaceholder.typicode.com/users"
    
    #MOCK DATA
    times = ["5:30 PM", "6:00 PM", "6:30 PM", "7:00 PM", "7:30 PM", "8:00 PM"]
    notes = ["Anniversary", "Nut Allergy", "VIP", "Window Seat", "Birthday", "None"]

    try:
        print(f"Contacting: {url}...")
        time.sleep(1)
        response = requests.get(url)
        
        if response.status_code == 200:
            guest_list = response.json()
            
            print(" [SUCCESS] Data Received.\n")
            print(f" Total Guests: {len(guest_list)}")
            
            #HEADER
            print("-" * 75)
            # We use f-strings to set column width (e.g., :<20 means 20 chars wide)
            print(f"{'TIME':<10} | {'NAME':<20} | {'PHONE':<18} | {'NOTE'}")
            print("-" * 75)

            for guest in guest_list:
                #API DATA (From the Internet)
                name = guest['name']
                phone = guest['phone'].split(" ")[0] # Grabbing just the first part of phone
                
                #PYTHON DATA (Randomly Generated)
                res_time = random.choice(times)
                guest_note = random.choice(notes)
                
                #COMBINING DATA
                print(f"{res_time:<10} | {name:<20} | {phone:<18} | {guest_note}")

            print("-" * 75)
        else:
            print(f" [ERROR] Server returned: {response.status_code}")
            
    except Exception as e:
        print(f" [CRITICAL ERROR] Connection failed: {e}")
#--- STATION 12: GUEST SEARCH (Enhanced) ---
def run_guest_search():
    print("\n" + "-"*40)
    print("--- GUEST RESERVATION SEARCH ---")
    
    user_id = input("Enter Guest ID (1-10): ")
    
    #Use f-string to insert the ID into the URL
    url = f"https://jsonplaceholder.typicode.com/users?id={user_id}"
    
    #Mock data to match the host stand
    times = ["5:30 PM", "6:00 PM", "6:30 PM", "7:00 PM", "7:30 PM", "8:00 PM"]
    notes = ["Anniversary", "Nut Allergy", "VIP", "Window Seat", "Birthday", "None"]
    
    try:
        print(f"Searching for Guest ID #{user_id}...")
        response = requests.get(url)
        results = response.json()
        
        if len(results) > 0:
            user = results[0]
            
            #Generate random details on the fly
            res_time = random.choice(times)
            guest_note = random.choice(notes)
            
            print("\n [SUCCESS] Record Found:")
            print("-" * 40)
            print(f" Name:    {user['name']}")
            print(f" Time:    {res_time}")
            print(f" Email:   {user['email']}")
            print(f" City:    {user['address']['city']}")
            print(f" Company: {user['company']['name']}")
            print(f" Note:    {guest_note}")
            print("-" * 40)
        else:
            print(f" [!] No guest found with ID {user_id}")

    except Exception as e:
        print(f" [CRITICAL ERROR] Connection failed: {e}")
# --- STATION 13: RECIPE COST CALCULATOR (Integrated) ---
def run_recipe_cost_calculator():
    print('\n' + '-'*40)
    print('--- RECIPE COST CALCULATOR ---')
    
    query = input('Enter dish to search (e.g. Pasta, Steak): ')
    
    #SEARCH PARAMETERS
    url = "https://api.spoonacular.com/recipes/complexSearch"
    params = {
        'apiKey': "c5bcb06058224f0193c38272d143e1c2",
        'query': query,
        'number': 10,
        'addRecipeInformation': True
    }
    
    try:
        print(f"Searching Spoonacular for '{query}'...")
        response = requests.get(url, params=params)
        data = response.json()
        results = data['results']
        
        if not results:
            print(' [!] No recipes found.')
            return

        #DISPLAY MENU
        print(f"\n [SUCCESS] Found {len(results)} recipes:\n")
        for i, recipe in enumerate(results, 1):
            print(f" {i}. {recipe['title']} (Time: {recipe['readyInMinutes']}m)")
            
        print('-' * 40)
        
        #SELECT & FETCH
        choice = input(f"Select a recipe number (1-{len(results)}): ")
        
        if choice.isdigit() and 1 <= int(choice) <= len(results):
            selected = results[int(choice) - 1]
            
            #FULL DETAILS (For Price)
            id_url = f"https://api.spoonacular.com/recipes/{selected['id']}/information"
            detail_response = requests.get(id_url, params={"apiKey": SPOON_KEY})
            info = detail_response.json()
            
            #CALCULATE REAL NUMBERS
            cost_price = info['pricePerServing'] / 100
            sell_price = cost_price * 3  #Standard 30% Food Cost Rule
            profit = sell_price - cost_price
            
            #PRINT TO SCREEN
            print("\n" + "="*50)
            print(f" RECIPE CARD: {info['title'].upper()}")
            print(f' Cost:   ${cost_price:.2f}')
            print(f' Price:  ${sell_price:.2f} (Recommended)')
            print(f' Profit: ${profit:.2f}')
            print('='*50)
            
            #INTEGRATION (Saving to CSV)
            save = input('Save this to financial log? (y/n): ')
            if save.lower() == 'y':
                with open("kitchen_financials.csv", "a", newline="") as file:
                    writer = csv.writer(file)
                    #We write: Name, Cost, Price, Profit
                    writer.writerow([info['title'], round(cost_price,2), round(sell_price,2), round(profit,2)])
                print(" [SAVED] Log updated.")
            
        else:
            print(" [!] Invalid selection.")

    except Exception as e:
        print(f" [CRITICAL ERROR] {e}")
        
# --- STATION 14: INVENTORY MANAGER (Final v2) ---
def run_inventory_manager():
    db_file = "kitchen.db"
    
    while True:
        print("\n" + "-"*40)
        print("--- INVENTORY MANAGEMENT SYSTEM ---")
        print("1. View Stock")
        print("2. Update Stock Count")
        print("3. Delete Item")
        print("4. Add New Item")  # <--- NEW FEATURE
        print("5. Return to Main Menu")
        
        choice = input("Select Option: ")
        
        if choice == '5':
            break
            
        try:
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()
            
            #VIEW
            if choice == '1':
                cursor.execute("SELECT * FROM inventory")
                items = cursor.fetchall()
                print(f"\n--- CURRENT INVENTORY ---")
                print(f"{'ID':<5} | {'ITEM':<15} | {'PRICE':<10} | {'STOCK'}")
                print("-" * 50)
                for item in items:
                    print(f"{item[0]:<5} | {item[1]:<15} | ${item[2]:<9.2f} | {item[3]}")
                print("-" * 50)

            #UPDATE
            elif choice == '2':
                item_name = input("Item Name: ")
                # Check if it exists first!
                cursor.execute("SELECT * FROM inventory WHERE name = ?", (item_name,))
                if not cursor.fetchone():
                    print(f" [ERROR] '{item_name}' does not exist. Use Option 4 to add it.")
                else:
                    new_stock = int(input("New Stock Count: "))
                    cursor.execute("UPDATE inventory SET stock_count = ? WHERE name = ?", (new_stock, item_name))
                    conn.commit()
                    print(f" [SUCCESS] {item_name} updated.")

            #DELETE
            elif choice == '3':
                item_name = input("Item Name to DELETE: ")
                confirm = input("Confirm Delete? (y/n): ")
                if confirm.lower() == 'y':
                    cursor.execute("DELETE FROM inventory WHERE name = ?", (item_name,))
                    conn.commit()
                    if cursor.rowcount > 0:
                        print(f" [GONE] {item_name} deleted.")
                    else:
                        print(f" [ERROR] Item not found.")

            #ADD (CREATE)
            elif choice == '4':
                print("\n--- NEW ITEM ENTRY ---")
                name = input("Item Name: ")
                try:
                    price = float(input("Price: $"))
                    stock = int(input("Starting Stock: "))
                    
                    #The INSERT Command
                    cursor.execute("INSERT INTO inventory (name, price, stock_count) VALUES (?, ?, ?)", (name, price, stock))
                    conn.commit()
                    print(f" [SUCCESS] {name} added to database.")
                    
                except ValueError:
                    print(" [ERROR] Price/Stock must be numbers.")
                except sqlite3.IntegrityError:
                    print(" [ERROR] Item already exists.")

        except sqlite3.Error as e:
            print(f" [DB ERROR] {e}")
        finally:
            if 'conn' in locals():
                conn.close()

#--- STATION 15: PROFIT CHART (Day 20) ---
def run_profit_chart():
    print("\n" + "-"*40)
    print("--- GENERATING FINANCIAL REPORT ---")
    
    items = []
    profits = []
    
    try:
        #Read the live financial log
        with open('kitchen_financials.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                items.append(row['item'])
                profits.append(float(row['profit']))
        
        if not items:
            print(" [!] No financial data found.")
            return

        print(f" [SUCCESS] Visualizing {len(items)} menu items...")
        
        #Build the chart
        plt.figure(figsize=(10, 6))
        plt.bar(items, profits, color='green')
        plt.title('Kitchen Menu Profitability')
        plt.xlabel('Menu Items')
        plt.ylabel('Profit ($)')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        #Show it
        print(" [DISPLAY] Chart opened in new window. Close it to continue.")
        plt.show()
        
    except FileNotFoundError:
        print(" [ERROR] No financial records found (kitchen_financials.csv).")
    except Exception as e:
        print(f" [CRITICAL ERROR] Visualization failed: {e}")

#--- STATION 16: WEATHER WIDGET (Day 21) ---
def run_weather_widget():
    print("\n" + "-"*40)
    print("--- KITCHEN METEOROLOGY STATION ---")
    
    city = input("Enter City Name to Search: ")
    
    #Open-Meteo Geocoding API (No Key Required)
    search_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=5&language=en&format=json"

    try:
        print(f"Searching for '{city}'...")
        response = requests.get(search_url)
        data = response.json()

        if "results" not in data:
            print(" [!] No locations found.")
            return
            
        results = data["results"]
        print(f"\n [SUCCESS] Found {len(results)} matches:")

        for i, place in enumerate(results):
             name = place.get("name")
             region = place.get("admin1", "N/A") 
             country = place.get("country", "Unknown")
             print(f" {i+1}. {name}, {region} ({country})")

        choice = input("\nSelect Number (1-5): ")
        
        if choice.isdigit() and 1 <= int(choice) <= len(results):
            index = int(choice) - 1
            selected = results[index]

            lat = selected["latitude"]
            lon = selected["longitude"]
            place_name = selected["name"]
            place_region = selected.get("admin1", "")

            print(f"\nLoading forecast for: {place_name}, {place_region}...")

            weather_url = f"https://wttr.in/{lat},{lon}?0"
            weather_response = requests.get(weather_url)

            print("\n" + "="*40)
            print(weather_response.text)
            print("="*40)
        else:
            print(" [!] Invalid selection.")

    except Exception as e:
        print(f" [ERROR] Search failed: {e}")

#--- STATION 17: LAUNCH POS SYSTEM (GUI) ---
def run_pos_launcher():
    print("\n" + "-"*40)
    print("--- LAUNCHING POINT OF SALE ---")
    print(" [INFO] Opening GUI Window...")
    
    # We try both names just in case you renamed it or not
    import os
    if os.path.exists("pos.py"):
        filename = "pos.py"
    elif os.path.exists("Day 24- Connected POS.py"):
        filename = "Day 24- Connected POS.py"
    else:
        print(" [ERROR] Could not find POS file.")
        return

    try:
        subprocess.Popen(["python3", filename])
        print(" [SUCCESS] POS Window Launched.")
    except Exception as e:
        print(f" [CRITICAL] Launcher failed: {e}")

#--- STATION 18: MANAGER ORDER LOG ---
def view_order_history():
    print("\n" + "="*50)
    print("--- PERMANENT ORDER HISTORY (DB) ---")
    print(f"{'ID':<5} | {'TIME':<20} | {'STATUS':<10} | {'ITEMS'}")
    print("-" * 50)
    
    try:
        conn = sqlite3.connect("kitchen.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM active_tickets ORDER BY ticket_id DESC")
        history = cursor.fetchall()
        
        if not history:
            print(" [EMPTY] No orders recorded yet.")
        else:
            for row in history:
                t_id, time, items, status = row
                items = items.replace("\n", ", ") 
                if len(items) > 40: items = items[:37] + "..."
                print(f"{t_id:<5} | {time:<20} | {status:<10} | {items}")
                
        print("-" * 50)
        input("Press Enter to return...")
    except sqlite3.Error as e:
        print(f" [ERROR] Could not read log: {e}")
    finally:
        if 'conn' in locals(): conn.close()

#--- STATION 19: LAUNCH KDS ---
def run_kds_launcher():
    print("\n" + "-"*40)
    print("--- LAUNCHING KITCHEN DISPLAY ---")
    
    import os
    # Try both names
    if os.path.exists("kds.py"):
        filename = "kds.py"
    elif os.path.exists("Kitchen_Display.py"):
        filename = "Kitchen_Display.py"
    else:
        print(" [ERROR] Could not find KDS file.")
        return

    try:
        subprocess.Popen(["python3", filename])
        print(" [SUCCESS] KDS Window Launched.")
    except Exception as e:
        print(f" [CRITICAL] Launcher failed: {e}")

#--- DATABASE SETUP FUNCTION (Must be defined BEFORE it is called) ---
def setup_ticket_table():
    try:
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
    except sqlite3.Error as e:
        print(f" [DATABASE ERROR] Ticket table setup failed: {e}")
    finally:
        if 'conn' in locals(): conn.close()
#      MAIN CONTROL CENTER (The Loop)
# ==========================================

#START THE DATABASE ENGINE
setup_ticket_table() 

while True:
    print('\n' + '='*40)
    print("   MMADU'S KITCHEN OS - MAIN MENU")
    print('='* 40)
    print('1. Login System')
    print('2. Firewall Check')
    print('3. Password Generator')
    print('4. Generate Daily Special')
    print('5. Update Security Logs')
    print('6. View Last Menu')
    print('7. View Security Logs')
    print('8. Check Item Price')
    print('9. Run POS System')
    print('10. Check Online Orders')
    print('11. Check Reservations')
    print('12. Search Guest Database')
    print('13. Calculate Recipe Cost')
    print('14. Inventory Management')
    print('15. View Profit Chart')
    print('16. Check Weather')
    print('17. Launch POS System (GUI)')
    print('18. View Order History Log') 
    print('19. Launch Kitchen Display (KDS)')
    print('Q. Quit Application')

    choice = input('\nSelect an option: ').upper()
    
    if choice == '1':
        run_login_system()
    elif choice == '2':
        run_firewall()
    elif choice == '3':
        run_password_generator()
    elif choice == '4':
        run_daily_special()
    elif choice == '5':
        update_logs()
    elif choice == '6':
        view_last_menu()
    elif choice == '7':
        view_security_logs()
    elif choice == '8':
        run_price_check()
    elif choice == '9':
        run_pos_system()
    elif choice == '10':
        run_api_check()
    elif choice == '11':
        run_host_stand()
    elif choice == '12':
        run_guest_search()  
    elif choice == '13':
        run_recipe_cost_calculator()
    elif choice == '14':
        run_inventory_manager()
    elif choice == '15':
        run_profit_chart()
    elif choice == '16':
        run_weather_widget()
    elif choice == '17':
        run_pos_launcher()
        subprocess.run(["python3", "pos.py"])
    elif choice == '18':
        view_order_history()
    elif choice == '19':    
        run_kds_launcher()
    elif choice == 'Q':
        print('System Shutting Down. Goodbye Chef.')
        break  
    else:
        print('Invalid Selection. Please try again.')