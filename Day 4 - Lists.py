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