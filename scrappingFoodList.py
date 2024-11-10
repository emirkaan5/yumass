import requests
from bs4 import BeautifulSoup
import sqlite3
import time

# SQLite setup with error handling
try:
    conn = sqlite3.connect('umass_dining.db')
    cursor = conn.cursor()

    # Create tables for each dining location if they don't already exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS berkshire (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            meal_type TEXT,
            food_name TEXT,
            diet_info TEXT,
            allergens TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS worcester (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            meal_type TEXT,
            food_name TEXT,
            diet_info TEXT,
            allergens TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS franklin (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            meal_type TEXT,
            food_name TEXT,
            diet_info TEXT,
            allergens TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS hampshire (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            meal_type TEXT,
            food_name TEXT,
            diet_info TEXT,
            allergens TEXT
        )
    ''')
    conn.commit()
    print("Database and tables set up successfully.")

except sqlite3.Error as e:
    print("Error creating or connecting to the database:", e)

# Function to retrieve menu items
def get_menu_items(soup, menu_id):
    menu = soup.find(id=menu_id)
    if not menu:
        return []
    items = menu.find_all('a', {'data-dish-name': True})
    return [
        [
            item['data-dish-name'],
            item.get('data-clean-diet-str', ''),
            item.get('data-allergens', '')
        ]
        for item in items
    ]

# Function to insert data into SQLite
def insert_menu_data(table, meal_type, menu_data):
    for item in menu_data:
        cursor.execute(f'''
            SELECT food_name, diet_info, allergens
            FROM {table}
            WHERE meal_type = ? AND food_name = ?
        ''', (meal_type, item[0]))
        
        existing_entry = cursor.fetchone()
        
        if existing_entry:
            if existing_entry != (item[0], item[1], item[2]):
                cursor.execute(f'''
                    UPDATE {table}
                    SET diet_info = ?, allergens = ?
                    WHERE meal_type = ? AND food_name = ?
                ''', (item[1], item[2], meal_type, item[0]))
        else:
            cursor.execute(f'''
                INSERT INTO {table} (meal_type, food_name, diet_info, allergens)
                VALUES (?, ?, ?, ?)
            ''', (meal_type, item[0], item[1], item[2]))
    conn.commit()

# URL and menu IDs mapping
locations = {
    'berkshire': 'https://umassdining.com/locations-menus/berkshire/menu',
    'worcester': 'https://umassdining.com/locations-menus/worcester/menu',
    'franklin': 'https://umassdining.com/locations-menus/franklin/menu',
    'hampshire': 'https://umassdining.com/locations-menus/hampshire/menu',
}

meal_ids = {
    'Lunch': 'lunch_menu',
    'Dinner': 'dinner_menu',
    'Late Night': 'latenight_menu'
}

# Loop through each location and meal type
for location, url in locations.items():
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error fetching {location} page.")
        continue

    soup = BeautifulSoup(response.content, 'html.parser')
    
    for meal_type, menu_id in meal_ids.items():
        menu_data = get_menu_items(soup, menu_id)
        insert_menu_data(location, meal_type, menu_data)
        print(f"{location.capitalize()} {meal_type}:", menu_data)
        time.sleep(1)  # Pause between requests to avoid rate limiting

# Close the database connection
conn.close()
