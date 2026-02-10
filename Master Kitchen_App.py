import random
import datetime

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
    
    # We save this to a variable so we can log it later if we want!
    special_text = f"Today's Special: Pan-seared {p} with {s} and {z} drizzle."
    print(special_text)
    
    # Day 7 Part 2 Integration: Save the Menu automatically
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


# ==========================================
#      MAIN CONTROL CENTER (The Loop)
# ==========================================
while True:
    print("\n" + "="*40)
    print("   MMADU'S KITCHEN OS - MAIN MENU")
    print("="*40)
    print("1. Login System (Days 1-3)")
    print("2. Firewall Check (Day 4)")
    print("3. Password Generator (Day 6)")
    print("4. Daily Special Generator (Day 6/7)")
    print("5. Update Security Logs (Day 7)")
    print("Q. Quit Application")
    
    choice = input("\nSelect an option: ").upper()
    
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
    elif choice == 'Q':
        print("System Shutting Down. Goodbye Chef.")
        break  # This breaks the 'while True' loop and ends the program
    else:
        print("Invalid Selection. Please try again.")
        
