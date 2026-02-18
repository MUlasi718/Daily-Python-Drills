#Day 25: PDF Receipt Generator (Physical File Creation)
#Goal: Draw a receipt on a blank PDF canvas (ReportLab)

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import datetime

def create_receipt(filename, items, total):
    #Create Canvas (Standard Letter Paper 8.5x11)
    c = canvas.Canvas(filename, pagesize=letter)
    
    #Set Header Font (Bold Title)
    c.setFont("Helvetica-Bold", 24)
    
    #Draw Header Text (Coordinates: 0,0 is Bottom-Left)
    c.drawString(200, 750, "MMADU'S KITCHEN")
    
    #Set Address Font (Regular Text)
    c.setFont("Helvetica", 12)
    c.drawString(230, 730, "123 Python Street")
    c.drawString(230, 715, "Atlanta, GA 30303")
    c.drawString(230, 700, "Tel: (555) 019-CODE")
    
    #Draw Separator Line (Visual Break)
    c.line(100, 690, 500, 690)
    
    #Write Metadata (Date and Order Number)
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.drawString(100, 670, f"Date: {now}")
    c.drawString(400, 670, "Order #: 001")
    
    #Set Column Headers (Item and Price)
    y_position = 640
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, y_position, "ITEM")
    c.drawString(450, y_position, "PRICE")
    
    #Adjust Y Position (Move Down for List)
    y_position -= 20
    c.setFont("Helvetica", 12)
    
    #Loop Through Items (Iterate Cart List)
    for item in items:
        name = item['name']
        price = f"${item['price']:.2f}"
        
        c.drawString(100, y_position, name)
        c.drawString(450, y_position, price)
        
        #Update Position (Next Line Down)
        y_position -= 20 
        
    #Draw Total Line (Bottom Separator)
    c.line(100, y_position-10, 500, y_position-10)
    y_position -= 40
    
    #Write Total Due (Bold Emphasis)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(350, y_position, "TOTAL DUE:")
    c.drawString(450, y_position, f"${total:.2f}")
    
    #Write Footer (Closing Message)
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(180, 100, "Thank you for dining with us!")
    c.drawString(150, 85, "Follow us on GitHub for new menu items.")
    
    #Save File (Generate PDF Output)
    c.save()
    print(f" [SUCCESS] Receipt saved as '{filename}'")

#Define Test Data (Simulation)
mock_cart = [
    {"name": "Burger (x2)", "price": 25.00},
    {"name": "Fries (x1)", "price": 3.50},
    {"name": "Soda (x2)", "price": 3.98},
    {"name": "Steak (x1)", "price": 25.00}
]

#Run Generator (Execute Function)
create_receipt("Test_Receipt.pdf", mock_cart, 57.48)