#Day 21: Weather Widget (Search & Select)
#Goal: Search for a city, pick the right one from a list, and show the weather.

import requests

print("--- KITCHEN METEOROLOGY STATION ---")
city = input("Enter City Name to Search: ")

#--- STEP 1: SEARCH LOCATIONS ---
#We use Open-Meteo Geocoding API (No Key Required) to get a list
search_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=5&language=en&format=json"

try:
    print(f"Searching for '{city}'...")
    response = requests.get(search_url)
    data = response.json()

    #Check if we found anything
    if "results" not in data:
        print(" [!] No locations found.")
    else:
        results = data["results"]
        print(f"\n [SUCCESS] Found {len(results)} matches:")

        #--- STEP 2: DISPLAY OPTIONS ---
        for i, place in enumerate(results):
             name = place.get("name")
             #Get State/Region (admin1) and Country
             region = place.get("admin1", "N/A") 
             country = place.get("country", "Unknown")
             
             print(f" {i+1}. {name}, {region} ({country})")

        #--- STEP 3: USER SELECTION ---
        choice = input("\nSelect Number (1-5): ")
        
        if choice.isdigit() and 1 <= int(choice) <= len(results):
            index = int(choice) - 1
            selected = results[index]

            #Get Coordinates (Latitude/Longitude)
            #This is the most precise way to find a place
            lat = selected["latitude"]
            lon = selected["longitude"]
            place_name = selected["name"]
            place_region = selected.get("admin1", "")

            print(f"\nLoading forecast for: {place_name}, {place_region}...")

            #--- STEP 4: GET WEATHER ART ---
            #wttr.in accepts coordinates (lat,lon) to give exact weather
            weather_url = f"https://wttr.in/{lat},{lon}?0"
            weather_response = requests.get(weather_url)

            print("\n" + "="*40)
            print(weather_response.text)
            print("="*40)
            
        else:
            print(" [!] Invalid selection.")

except Exception as e:
    print(f" [ERROR] Search failed: {e}")