from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sqlite3
import time

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

# Function to retrieve meal items
def get_menu_items(menu_id):
    menu = wait.until(EC.presence_of_element_located((By.ID, menu_id)))
    items = menu.find_elements(By.XPATH, './/a[@data-dish-name]')
    return [
        [
            item.get_attribute("data-dish-name"),
            item.get_attribute("data-clean-diet-str"),
            item.get_attribute("data-allergens")
        ]
        for item in items
    ]

# SQLite setup with error handling
try:
    conn = sqlite3.connect('umass_dining.db')  # Connect to the database (or create it if it doesn't exist)
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

# Function to insert data into SQLite
def insert_menu_data(table, meal_type, menu_data):
    # Clear old data for the meal_type in the table
    for item in menu_data:
        # Check if the entry already exists in the database
        cursor.execute(f'''
            SELECT food_name, diet_info, allergens
            FROM {table}
            WHERE meal_type = ? AND food_name = ?
        ''', (meal_type, item[0]))
        
        existing_entry = cursor.fetchone()
        
        # If entry exists and is different, update it
        if existing_entry:
            if existing_entry != (item[0], item[1], item[2]):
                cursor.execute(f'''
                    UPDATE {table}
                    SET diet_info = ?, allergens = ?
                    WHERE meal_type = ? AND food_name = ?
                ''', (item[1], item[2], meal_type, item[0]))
        else:
            # Insert new entry if it doesn't exist
            cursor.execute(f'''
                INSERT INTO {table} (meal_type, food_name, diet_info, allergens)
                VALUES (?, ?, ?, ?)
            ''', (meal_type, item[0], item[1], item[2]))
    conn.commit()

# Berkshire arrays and database insertion
driver.get('https://umassdining.com/locations-menus/berkshire/menu')
BerkLunch = get_menu_items("lunch_menu")
insert_menu_data("berkshire", "Lunch", BerkLunch)
print("BerkLunch:", BerkLunch)

dinner_tab = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@href="#dinner_menu"]')))
dinner_tab.click()
time.sleep(1)
BerkDinner = get_menu_items("dinner_menu")
insert_menu_data("berkshire", "Dinner", BerkDinner)
print("BerkDinner:", BerkDinner)

latenight_tab = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@href="#latenight_menu"]')))
latenight_tab.click()
time.sleep(1)
BerkLatenight = get_menu_items("latenight_menu")
insert_menu_data("berkshire", "Late Night", BerkLatenight)
print("BerkLatenight:", BerkLatenight)

# Worcester arrays and database insertion
driver.get('https://umassdining.com/locations-menus/worcester/menu')
WoLunch = get_menu_items("lunch_menu")
insert_menu_data("worcester", "Lunch", WoLunch)
print("WoLunch:", WoLunch)

dinner_tab = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@href="#dinner_menu"]')))
dinner_tab.click()
time.sleep(1)
WoDinner = get_menu_items("dinner_menu")
insert_menu_data("worcester", "Dinner", WoDinner)
print("WoDinner:", WoDinner)

latenight_tab = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@href="#latenight_menu"]')))
latenight_tab.click()
time.sleep(1)
WoLateNight = get_menu_items("latenight_menu")
insert_menu_data("worcester", "Late Night", WoLateNight)
print("WoLateNight:", WoLateNight)

# Franklin arrays and database insertion
driver.get('https://umassdining.com/locations-menus/franklin/menu')
FrankLunch = get_menu_items("lunch_menu")
insert_menu_data("franklin", "Lunch", FrankLunch)
print("FrankLunch:", FrankLunch)

dinner_tab = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@href="#dinner_menu"]')))
dinner_tab.click()
time.sleep(1)
FrankDinner = get_menu_items("dinner_menu")
insert_menu_data("franklin", "Dinner", FrankDinner)
print("FrankDinner:", FrankDinner)

# Hampshire arrays and database insertion
driver.get('https://umassdining.com/locations-menus/hampshire/menu')
HampLunch = get_menu_items("lunch_menu")
insert_menu_data("hampshire", "Lunch", HampLunch)
print("HampLunch:", HampLunch)

dinner_tab = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@href="#dinner_menu"]')))
dinner_tab.click()
time.sleep(1)
HampDinner = get_menu_items("dinner_menu")
insert_menu_data("hampshire", "Dinner", HampDinner)
print("HampDinner:", HampDinner)

# Close the WebDriver and database connection
driver.quit()
conn.close()
