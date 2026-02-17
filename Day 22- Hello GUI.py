#Day 22: Hello GUI (Tkinter)
#Goal: Build a real window with buttons and labels.

import tkinter as tk

#--- THE LOGIC ---
#Global variable to track orders
order_count = 0

def add_order():
    global order_count
    order_count += 1
    
    #Update the label text dynamically
    label_status.config(text=f"Total Orders: {order_count}")
    print(f" [LOG] Order received. Total: {order_count}")

def reset_counter():
    global order_count
    order_count = 0
    label_status.config(text="Total Orders: 0")
    print(" [LOG] Counter reset.")

#--- THE WINDOW ---
#Create the main application window
root = tk.Tk()
root.title("Kitchen Kiosk v1.0")
root.geometry("400x300") #Width x Height in pixels

#--- THE WIDGETS ---
#The Title (Label)
label_title = tk.Label(root, text="Mmadu's Kitchen", font=("Arial", 24, "bold"))
label_title.pack(pady=20) #pady adds vertical spacing

#The Status (Label)
label_status = tk.Label(root, text="Total Orders: 0", font=("Arial", 18))
label_status.pack(pady=20)

#The Button (Action)
btn_order = tk.Button(root, text="NEW ORDER (+1)", command=add_order, font=("Arial", 14), bg="green", fg="black")
btn_order.pack(ipadx=10, ipady=5) #internal padding makes the button bigger

#The Reset Button
btn_reset = tk.Button(root, text="Reset Counter", command=reset_counter, fg="red")
btn_reset.pack(pady=20)

#--- THE LOOP ---
#This keeps the window open until you hit the X button
print("System Online. Window is open.")
root.mainloop()