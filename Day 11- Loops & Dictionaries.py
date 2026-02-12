#Mmadu Ulasi Daily Python Drill (Day 1/2)

#Day 1 Drill: Variables & Input (Masked Login)
#Day 1 Goal: Write a script that asks for a 'username' and 'password' and prints them back masked

# 1. The Prompt

Username = input("Enter username: ")
Password = input("Enter password: ")

# 2. The Logic
mask = '*' * len(Password)

# 3. The Output
print(f"User: {Username}")
print(f"Pass: {mask}")

#Day 2 Drill: Logic Gates (Access Control)
#Day 2 Goal: Create a script that checks if a user is 'Admin','User', or 'Guest' and grants diffferent access levels using if/else

if Username == 'John Doe':
    user_role = 'Admin'   # John gets the Admin badge
elif Username == 'M Ulasi':
    user_role = 'User'    # M gets the User badge
else:
    user_role = 'Guest'   # Everyone else gets the Guest badge

print(f"System: User recognized as role [{user_role}]")

# --- STEP 2: Check the Role ---
if user_role == 'Admin':
    print('Access Granted: Full Control')

elif user_role == 'User':
    print('Access Granted: Read Only')

else:
    print('Access Denied: Get On Up Outta Here!')
    
    
#Day 3 Drill: The Loop (Brute Force Stopper)
#Day 3 Goal: Write a loop that asks the user for a password. After 3 failed attempts, the user will be locked out.
    

correct_target = Password
attempts = 0
max_attempts = 3

while attempts < max_attempts:
    
    #Ask for password
    
    user_input = input("Please re-enter password to verify: ")
    
    #Check for match
    
    if user_input == correct_target:
        print("Access Granted. Whattup tho?")
        
        break
    
    else:
        print("Wrong Password. Try again.")
        attempts = attempts + 1 #1 acts as the counter. Once it reaches 3, the user will be locked out.
        
    if attempts == max_attempts:
        print("SYSTEM LOCKED! Dash wey yuhself.")

#Day 4 Drill: IP Whitelist
#Day 4 Drill Goals: Create a list of 'allowed IPs.' Write a script that checks if a new IP input exists in that list.
        
print("FIREWALL SYSTEM STARTING...")

allowed_ips = ["192.168.1.1","10.0.5.1","172.16.0.55","111.111.1.0"]

allowed_ips.append("10.0.0.99")

print(f"Allowed IPs: {allowed_ips}")

user_ip = input("Enter IP Address to Verify: ")

if user_ip in allowed_ips:
    print("Access Granted: IP matches whitelist.")
else:
    print("Access Denied: Your IP is not authorized.")
    
    
# Day 5 Drill: Functions (The Login Station)
# Day 5 Goal: Refactor the Day 2 'Role Check' logic into a reusable function. The function should accept a 'username' and return the corresponding role.

def check_permission(name):
    
    if name == 'John Doe':
        return 'User'
    
    else:
        return 'Guest'
    
    
user_input = input('Enter username to check: ')

status = check_permission(user_input)

print(f'Access Level: {status}')

print("Running automated security acan on 'Hacker'...")
print(check_permission('Hacker'))

#Day 6 Drill: Libraries
#Day 6 Goals: Build a Random Password Generator

import random

print("SECURE PASSWORD GENERATOR")

options = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%"

password_list = random.choices(options, k=12)

final_password = "".join(password_list)

print(f"Generated Secure Password : {final_password}")

#Day 6 Part 2: The Project (KM App)
#Day 6 Part 2 Goals: Generate "Chef Daily Special" using same random function.

print("CHEF: DAILY SPECIAL")

proteins = ["Chicken", "Beef", "Salmon", "Tofu"]
sides = ["Rice", "Broccoli", "Potatoes", "Asparagus"]
sauces = ["Teriyaki", "Garlic Butter", "Spicy Mayo", "Pesto"]

p = random.choice(proteins)
s = random.choice(sides)
z = random.choice(sauces)

print(f"Today's Special: Pan-seared {p} with {s} and {z} drizzle.")

# Day 7 Drill: File I/O (Persistence)
# Day 7 Goal: Write a script that saves a log entry to a text file (Append Mode) and updates a daily menu file (Write Mode).

import datetime

print("--- LOGGING SYSTEM ACTIVATED ---")

current_time = datetime.datetime.now()
log_entry = f"LOGIN EVENT : {current_time} - User: Admin\n"

with open("security_log.txt", "a") as file:
    file.write(log_entry)

print(f" [SUCCESS] Log entry appended to 'security_log.txt'")

#Day 7 Part 2: The Daily Menu (Write Mode)
#Day 7 Part 2 Goal: Write a script that overwrites the previous menu file with a new daily special.

daily_special = "Grilled Salmon with Asparagus"

with open("daily_menu.txt", "w") as file:
    file.write("--- TODAY'S SPECIAL ---\n")
    file.write(daily_special)
    file.write("\n--------------------")
    
print(f" [SUCCESS] Menu overwritten in 'daily_menu.txt'")

#Day 8 & 9 Drill: File Reading & Error Handling
#Day 8 & 9 Goal: safely read a file. If it doesn't exist, handle the error gracefully instead of crashing.

import time

print('--- KITCHEN OPENING PROTOCOL ---')

filename = 'prep_list.txt'

try:
    print(f'Searching for {filename}...')
    time.sleep(1)
    
    with open(filename, 'r') as file:
        content = file.read()
        print('\n[SUCCESS] Prep List Found:')
        print(content)
        
except FileNotFoundError:
    print(f'\n[ERROR] {filename} not found!')
    print('Action: Creating a new emergency prep list...')
    
    with open(filename, "w") as file:
        file.write('- Dice Onions\n- Peep Carrots\n- Stock Check')
        
    print(' [SAVED] New prep list created.')
    
#Day 10 Drill: Dictionaries (Key-Value Pairs)
#Goal: Create a menu pricing system that looks up values based on a key.

print("--- POS SYSTEM: PRICE CHECK ---")

#THE DATA (Dictionary)
#Use Curly Braces {} for dictionaries.
menu_prices = {
    "Burger": 12.99,
    "Fries": 3.50,
    "Soda": 1.99,
    "Steak": 24.99,
    "Salad": 8.50
}

#THE INPUT
order = input("Enter item to check price: ")

#LOGIC (Safe Lookup)
#If we just ask menu_prices[order], it crashes if the item isn't there.
#use .get() which allows a fallback message.

price = menu_prices.get(order, "Not Found")

#OUTPUT
if price == "Not Found":
    print(f" [ERROR] Item '{order}' is not on the menu.")
else:
    print(f" The price of {order} is: ${price}")


#Day 11 Drill: Loops + Dictionaries (The Shopping Cart)
#Goal: Allow a user to add multiple items and calculate the total cost.

print('--- POS SYSTEM: OPEN TAB ---')

menu = {
    "Burger": 12.99,
    "Fries": 3.50,
    "Soda": 1.99,
    "Steak": 24.99,
    "Salad": 8.50
}

#Ledger(Cart, Starts at zero)
total_bill = 0
cart = [] #Item names will be listed here, with the prices.

print('Menu: Burger, Fries, Soda, Steak, Salad')
print("Type 'done' to finish order.\n")

#Loop
while True:
    raw_input = input("Enter Command (e.g. '3 Burger' or 'Del Burger'): ").title()

    #EXIT CHECK
    if raw_input == "Done":
        break

    #PARSE QUANTITY (The Logic Splitter)
    #We assume quantity is 1 unless we find a number
    parts = raw_input.split() 
    qty = 1
    item_name = raw_input # Default: the whole input is the name

    #Check if the first word is a number (like "3")
    if len(parts) > 0 and parts[0].isdigit():
        qty = int(parts[0])             #Extract the number (3)
        item_name = " ".join(parts[1:]) #Extract the rest ("Burger")

    #EXECUTE THE ORDER (Runs 'qty' times)
    for i in range(qty):
        
        #VOID LOGIC
        if item_name.startswith("Del"):
            # Clean up the name (remove "Del " from "Del Burger")
            # We use replace() here to be safe
            clean_item = item_name.replace("Del ", "")
            
            if clean_item in cart:
                price = menu[clean_item]
                total_bill -= price
                cart.remove(clean_item)
                print(f" [VOID] Removed {clean_item} (-${price})")
            else:
                print(f" [ERROR] {clean_item} is not in the cart!")

        #ADD LOGIC
        elif item_name in menu:
            price = menu[item_name]
            total_bill += price
            cart.append(item_name)
            print(f" + Added {item_name} (${price})")
            
        #ERROR LOGIC
        else:
            print(f" [ERROR] We don't serve '{item_name}'.")
            break #Stop the loop so we don't print the error 3 times

    #Show running total after the loop finishes
    print(f" Running Total: ${total_bill:.2f}")