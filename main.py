import requests
from datetime import datetime
import os

# Time
today = datetime.now()
date = today.strftime("%d/%m/%Y")
current_time = datetime.now().strftime("%H:%M:%S")

# Nutritionix
API_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"
MY_GENDER = "Male"
MY_WEIGHT = "55"
MY_HEIGHT = "167"
AGE = "27"


APP_ID = os.environ['APP_ID']
API_KEY = os.environ['API_KEY']
query = input("Tell me which exercise you did: ")
user_params = {
    "query": query,
    "gender": MY_GENDER,
    "weight_kg": MY_WEIGHT,
    "height_cm": MY_HEIGHT,
    "age": AGE
}

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
    "Content-Type": "application/json"
    # This ensures the server knows you're sending JSON data
}

response = requests.post(url=API_ENDPOINT, json=user_params, headers=headers)
result = response.json()
exercise = result["exercises"][0]["user_input"]
duration = result["exercises"][0]["duration_min"]
calories = result["exercises"][0]["nf_calories"]


projectName = "copyOfMyWorkouts"
sheetName = "workouts"

USERNAME = os.environ['USERNAME']
PASSWORD = os.environ['PASSWORD']
SHEETY_TOKEN = f"Bearer {PASSWORD}"
SHEETY_API = f"https://api.sheety.co/{USERNAME}/{projectName}/{sheetName}"

sheety_headers = {
    "Authorization": SHEETY_TOKEN
}
# Data to send to Sheety
sheet_data = {
    "workout": {
        "date": date,
        "time": current_time,
        "exercise": exercise,
        "duration": duration,
        "calories": calories
    }
}

# Making the POST request to Sheety API
response = requests.post(url=SHEETY_API, json=sheet_data, headers=sheety_headers)

# Check the response status
if response.status_code == 200:
    print("Data successfully added to the spreadsheet!")
else:
    print(f"Failed to add data. Status code: {response.status_code}")
    print(response.text)

try:
    APP_ID = os.environ['APP_ID']
except KeyError:
    print("APP_ID is not set in the environment.")
    exit(1)  # Exit the script if the variable is not found
