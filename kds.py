import tkinter as tk
import sqlite3

#--- DATABASE LOGIC ---
def mark_done(ticket_id):
    """Marks a ticket as DONE so it disappears from the screen."""
    try:
        conn = sqlite3.connect("kitchen.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE active_tickets SET status = 'DONE' WHERE ticket_id = ?", (ticket_id,))
        conn.commit()
        conn.close()
        refresh_tickets() #Refresh immediately to remove it
    except Exception as e:
        print(f"Error completing ticket: {e}")

def refresh_tickets():
    """Checks the database every 3 seconds for new PENDING tickets."""
    
    #Clear the screen (Delete old widgets)
    for widget in scroll_frame.winfo_children():
        widget.destroy()

    try:
        conn = sqlite3.connect("kitchen.db")
        cursor = conn.cursor()
        
        #Get only PENDING tickets
        cursor.execute("SELECT ticket_id, timestamp, items FROM active_tickets WHERE status = 'PENDING'")
        tickets = cursor.fetchall()
        conn.close()
        
        #Draw the Tickets
        if not tickets:
            lbl_empty = tk.Label(scroll_frame, text="NO PENDING ORDERS", font=("Arial", 14), fg="gray", bg="#333333")
            lbl_empty.pack(pady=20)
        
        for t in tickets:
            t_id, time, content = t
            
            #The Ticket Paper (Yellow Box)
            ticket_box = tk.Frame(scroll_frame, bg="#fff9c4", bd=2, relief="raised", padx=10, pady=10)
            ticket_box.pack(fill="x", pady=5, padx=5)
            
            #Header: Ticket # and Time
            header = f"TICKET #{t_id}  |  {time[11:16]}" # Slices time to show just HH:MM
            tk.Label(ticket_box, text=header, font=("Courier", 12, "bold"), bg="#fff9c4", fg="black").pack(anchor="w")
            
            #The Items
            tk.Label(ticket_box, text=content, font=("Arial", 14), bg="#fff9c4", fg="#d32f2f", justify="left").pack(anchor="w", pady=5)
            
            #The "Done" Button
            btn_done = tk.Button(ticket_box, text="ORDER UP! (Complete)", bg="#a5d6a7", fg="green", font=("Arial", 10, "bold"),
                               command=lambda id=t_id: mark_done(id))
            btn_done.pack(fill="x", pady=2)
            
    except Exception as e:
        print(f"Database Error: {e}")

    #Schedule the next check in 3000 milliseconds (3 seconds)
    root.after(3000, refresh_tickets)

#--- MAIN WINDOW SETUP ---
root = tk.Tk()
root.title("KITCHEN DISPLAY SYSTEM (BOH)")
root.geometry("400x600")
root.configure(bg="#333333") # Dark Mode Background

#Title Bar
tk.Label(root, text="👨‍🍳 LINE COOK STATION", font=("Arial", 18, "bold"), bg="black", fg="white", pady=10).pack(fill="x")

#Scrollable Area (Placeholder Frame for now)
#In a real app we'd use a Canvas for scrolling, but this Frame works for lists that fit on screen
scroll_frame = tk.Frame(root, bg="#333333")
scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

#Start the Loop
refresh_tickets()
root.mainloop()