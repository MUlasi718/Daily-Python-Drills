import time
import sys
import random
import requests

# --- STATION 1: IDENTITY & ACCESS (Days 1, 2, 3 & 5) ---
def run_login_system():
    print("\n" + "-"*30)
    print("--- STARTING LOGIN SYSTEM ---")
    
    # Day 1: Input
    Username = input("Enter username: ")
    Password = input("Enter password: ")
    
    # Masking
    mask = '*' * len(Password)
    print(f"User: {Username}")
    print(f"Pass: {mask}")
    
    # Day 2: Role Check
    if Username == 'John Doe':
        user_role = 'Admin'
    elif Username == 'M Ulasi':
        user_role = 'User'
    else:
        user_role = 'Guest'
    print(f"System: Recognized as [{user_role}]")

    # Day 3: Brute Force Loop
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
        
# --- STATION 12: Reservation Search (Day 14) ---
def run_guest_search():
    print("\n" + "-"*40)
    print("--- GUEST RESERVATION SEARCH ---")
    
    #INPUT
    guest_id = input("Enter Guest ID (1-10): ")
    
    #PARAMETER (Query String)
    url = f"https://jsonplaceholder.typicode.com/users?id={guest_id}"
    
    try:
        print(f"Searching for Guest ID #{guest_id}...")
        time.sleep(1)
        response = requests.get(url)
        
        if response.status_code == 200:
            results = response.json()
            
            # Check if the list is not empty
            if len(results) > 0:
                user = results[0] # Grab the first item
                
                print("\n [SUCCESS] Record Found:")
                print("-" * 40)
                print(f" Name:    {user['name']}")
                print(f" Email:   {user['email']}")
                print(f" City:    {user['address']['city']}")
                print(f" Company: {user['company']['name']}")
                print("-" * 40)
            else:
                print(f"\n [!] No record found for ID {user_id}")
        else:
            print(f" [ERROR] Server returned: {response.status_code}")
            
    except Exception as e:
        print(f" [CRITICAL ERROR] Connection failed: {e}")        
        
#      MAIN CONTROL CENTER (The Loop)
# ==========================================
# NOTICE: This loop is at the very END. 
# It runs only after Python has learned all the functions above.

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
    print('Q. Quit Application')

    choice = input("\nSelect an option: ").upper()
    print("Q. Quit Application")
    
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
    elif choice == 'Q':
        print("System Shutting Down. Goodbye Chef.")
        break  
    else:
        print("Invalid Selection. Please try again.")
        

        