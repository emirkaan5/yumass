import sqlite3
import openai
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

openai.api_key = "lalaylaylay"
# Gmail credentials
gmail_user = "yummymass2024@gmail.com"
gmail_password = "putYourOwn"

def send_goodbye_email(email):
    # Create the goodbye message
    subject = "We're sad to see you go!"
    body = """\
Hi,

We're sorry to see you unsubscribe. Thank you for using our meal recommendation service, and we hope to serve you again in the future.

Best regards,
Yumass Team
"""

    # Set up the email message
    msg = MIMEMultipart()
    msg["From"] = gmail_user
    msg["To"] = email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        # Send the goodbye email
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(gmail_user, gmail_password)
            server.sendmail(gmail_user, email, msg.as_string())
            print(f"Goodbye email sent to {email}")
    except Exception as e:
        print(f"Failed to send goodbye email. Error: {e}")

def get_filtered_foods(email, meal_type, location):
    conn = sqlite3.connect("umass_dining.db")
    cursor = conn.cursor()

    # Retrieve user dietary info, allergens, and favorite foods
    cursor.execute("SELECT diet_info, allergens, favorite_foods FROM users WHERE email = ?", (email,))
    result = cursor.fetchone()

    if not result:
        print(f"No user found with email {email}")
        return ["No user data available"]

    diet_info, allergens_str, favorite_foods = result
    allergens = allergens_str.split(", ")
    favorite_food_list = favorite_foods.split(", ")

    # Query foods for the specified meal_type based on diet_info and allergens
    cursor.execute(f"""
        SELECT food_name FROM {location}
        WHERE meal_type = ? AND diet_info LIKE ?
        AND NOT (
            """ + " OR ".join([f"allergens LIKE ?" for _ in allergens]) + """
        )
    """, [meal_type, f"%{diet_info}%"] + [f"%{allergen}%" for allergen in allergens])

    foods = [row[0] for row in cursor.fetchall()]
    conn.close()

    # Prioritize recommendations that match the user's favorite foods
    prioritized_foods = [food for food in foods if any(fav in food for fav in favorite_food_list)]
    other_foods = [food for food in foods if food not in prioritized_foods]

    return prioritized_foods + other_foods if prioritized_foods or other_foods else ["No suitable options available."]

def generate_chatgpt_prompt(user_name, dietary_info, favorite_foods, dining_halls):
    prompt = f"Hello ChatGPT, I am {user_name} with dietary preferences for {dietary_info}.\n"
    prompt += f"Here are my favorite foods: {favorite_foods}.\n"
    prompt += "Please recommend the best options for each dining hall and meal time based on my dietary preferences and favorite foods, you can also include well liked foods by everyone:\n\n"
    
    for location, meals in dining_halls.items():
        prompt += f"At {location} Dining Hall:\n"
        for meal_type, foods in meals.items():
            prompt += f"  {meal_type.capitalize()}: {', '.join(foods)}\n"
    
    prompt += "\nRecommend the top options for me based on my dietary needs and preferences. Thank you! Only tell me what food to eat, no need for long descriptions! Do Not use **, or anything else provide a clean list!"
    return prompt

def get_chatgpt_recommendations(user_name, dietary_info, favorite_foods, dining_halls):
    prompt = generate_chatgpt_prompt(user_name, dietary_info, favorite_foods, dining_halls)
    
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful meal recommendation assistant, you only provide which foods you reccomend."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000
    )

    recommendations = response['choices'][0]['message']['content'].strip()
    return recommendations

def send_food_recommendation(recipient_email, user_name, dietary_info, favorite_foods):
    dining_halls = {}
    locations = ["worcester", "berkshire", "franklin", "hampshire"]

    # Define meal types based on location
    def get_meal_types(location):
        if location.lower() in ["franklin", "hampshire"]:
            return ["Lunch", "Dinner"]
        return ["Lunch", "Dinner", "Late Night"]

    # Fetch available foods for each dining hall and meal type
    for location in locations:
        dining_halls[location.capitalize()] = {}
        meal_types = get_meal_types(location)
        for meal_type in meal_types:
            dining_halls[location.capitalize()][meal_type.lower()] = get_filtered_foods(recipient_email, meal_type, location)

    # Get ChatGPT recommendations
    chatgpt_recommendations = get_chatgpt_recommendations(user_name, dietary_info, favorite_foods, dining_halls)

    # Construct email content
    subject = "Today's Personalized Food Recommendations"
    body = f"Hi {user_name},\n\nHere are your personalized food recommendations for today based on your dietary preferences and favorite foods:\n\n"
    body += chatgpt_recommendations + "\n\nEnjoy your meals!\n\nBest regards,\nYumass Team"

    # Send the email
    msg = MIMEMultipart()
    msg["From"] = gmail_user
    msg["To"] = recipient_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(gmail_user, gmail_password)
            server.sendmail(gmail_user, recipient_email, msg.as_string())
            print(f"Food recommendation email sent to {recipient_email}")
    except Exception as e:
        print(f"Failed to send email. Error: {e}")

# Main block to iterate through all users in the database and send customized emails
def send_recommendations_to_all_users():
    conn = sqlite3.connect("umass_dining.db")
    cursor = conn.cursor()

    cursor.execute("SELECT name, email, diet_info, favorite_foods FROM users")
    users = cursor.fetchall()

    for user in users:
        name, email, diet_info, favorite_foods = user
        print(f"Sending food recommendation to {name} at {email}...")
        send_food_recommendation(email, name, diet_info, favorite_foods)

    conn.close()
    
def first_send(recipient_email, user_name, dietary_info, favorite_foods):
    dining_halls = {}
    locations = ["worcester", "berkshire", "franklin", "hampshire"]

    # Define meal types based on location
    def get_meal_types(location):
        if location.lower() in ["franklin", "hampshire"]:
            return ["Lunch", "Dinner"]
        return ["Lunch", "Dinner", "Late Night"]

    # Fetch available foods for each dining hall and meal type
    for location in locations:
        dining_halls[location.capitalize()] = {}
        meal_types = get_meal_types(location)
        for meal_type in meal_types:
            dining_halls[location.capitalize()][meal_type.lower()] = get_filtered_foods(recipient_email, meal_type, location)

    # Get ChatGPT recommendations
    chatgpt_recommendations = get_chatgpt_recommendations(user_name, dietary_info, favorite_foods, dining_halls)

    # Construct email content
    subject = "Welcome to your Personalized Food Recommendation"
    body = f"Hi {user_name},\n\nWelcome to our newsletter. Here are your personalized food recommendations for today based on your dietary preferences and favorite foods:\n\n"
    body += chatgpt_recommendations + "\n\nEnjoy your meals!\n\nBest regards,\Yumass Team"

    # Send the email
    msg = MIMEMultipart()
    msg["From"] = gmail_user
    msg["To"] = recipient_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(gmail_user, gmail_password)
            server.sendmail(gmail_user, recipient_email, msg.as_string())
            print(f"Food recommendation email sent to {recipient_email}")
    except Exception as e:
        print(f"Failed to send email. Error: {e}")