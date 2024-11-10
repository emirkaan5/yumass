import sqlite3
from main import send_goodbye_email

def remove_user(email):
    # Connect to the SQLite database
    conn = sqlite3.connect("umass_dining.db")
    cursor = conn.cursor()

    # Delete the user with the specified email
    cursor.execute("DELETE FROM users WHERE email = ?", (email,))
    conn.commit()

    # Check if any row was deleted
    if cursor.rowcount > 0:
        print(f"User with email {email} has been removed successfully.")
    else:
        print(f"No user found with email {email}.")

    # Close the database connection
    conn.close()

# Example usage
send_goodbye_email("agenc@umass.edu")
remove_user("agenc@umass.edu")
