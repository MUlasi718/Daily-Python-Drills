#Day 20: Data Visualization (Matplotlib)
#Goal: Read financial data from CSV and generate a Bar Chart.

import matplotlib.pyplot as plt
import csv

print("--- GENERATING PROFIT REPORT ---")

items = []
profits = []

#Read data from the csv file
try:
    with open('kitchen_financials.csv', 'r') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            items.append(row['item'])
            #Convert profit string to float for graphing
            profits.append(float(row['profit']))

    print(f" [DATA LOADED] Found {len(items)} items.")

    #Build the chart canvas
    plt.figure(figsize=(10, 6))
    
    #Create a bar chart with green bars
    plt.bar(items, profits, color='green')

    #Add labels and titles
    plt.title('Kitchen Menu Profitability')
    plt.xlabel('Menu Items')
    plt.ylabel('Profit ($)')
    
    #Add grid lines for better readability
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    #Display the final chart window
    print(" [DISPLAY] Opening chart window...")
    plt.show()

except FileNotFoundError:
    print(" [ERROR] kitchen_financials.csv not found. Run Day 16 first!")
except Exception as e:
    print(f" [ERROR] Could not generate chart: {e}")