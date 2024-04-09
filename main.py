import requests
from datetime import datetime
import json
import os


GENDER = "Male"
WEIGHT_KG = 55
HEIGHT_CM = 172
AGE = 23

APP_ID = os.environ.get("APP_ID")
API_KEY = os.environ.get("API_KEY")
nutritionix_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheet_endpoint = os.environ.get("SHEET_ENDPOINT")
TOKEN = os.environ.get("TOKEN")

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY
}

user_input = input("Tell me which exercises you did: ")

parameters = {
    "query": user_input,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

response = requests.post(url=nutritionix_endpoint, json=parameters, headers=headers, verify=False)
data_exercises = response.json()['exercises']

today = datetime.now()
today_date = today.strftime("%d/%m/%Y")
today_time = today.strftime("%X")

headers_sheet = {
    "Content-Type": "application/json",
    "Authorization": TOKEN
}

for exercise in data_exercises:
    calories = exercise['nf_calories']
    duration = exercise['duration_min']
    exercise = exercise['name'].title()

    body = {
        "workout": {
            "date": today_date,
            "time": today_time,
            "exercise": exercise,
            "duration": duration,
            "calories": calories
        }
    }

    response = requests.post(url=sheet_endpoint, json=body, headers=headers_sheet, verify=False)
    print(response.json())

