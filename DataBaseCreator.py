import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("umass_dining.db")
cursor = conn.cursor()

# Create the 'users' table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        diet_info TEXT,
        allergens TEXT,
        favorite_foods TEXT  -- New column for storing user's favorite foods
    )
''')

conn.commit()
print("Database and 'users' table created successfully.")
conn.close()

# Function to add a new user
def add_user(name, email, diet_info, allergens, favorite_foods):
    conn = sqlite3.connect("umass_dining.db")
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO users (name, email, diet_info, allergens, favorite_foods)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, email, diet_info, allergens, favorite_foods))
        conn.commit()
        print(f"User {name} added successfully.")
    except sqlite3.IntegrityError:
        print(f"User with email {email} already exists.")
    finally:
        conn.close()

# Example of adding a user
add_user("Ceren", "coguz@umass.edu", "", "Peanut", "Chicken, Asian Food")
