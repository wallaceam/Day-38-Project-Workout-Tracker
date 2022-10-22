import requests
from datetime import datetime as dt
import os

APP_ID = os.environ["APP_ID"]
API_KEY = os.environ["API_KEY"]

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"

query = input("What exercise(s) did you do and for how long? ")

exercise_params = {
    "query": query,
    "gender": "female",
    "weight_kg": 50,
    "height_cm": 167,
    "age": 29
}

exercise_header = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
    "x-remote-user-id": "0",
}

exercise_response = requests.post(url=exercise_endpoint, json=exercise_params, headers=exercise_header)
exercise_data = exercise_response.json()

sheety_endpoint = os.environ["SHEET_ENDPOINT"]

today = dt.today()
date = today.strftime("%d/%m/%Y")
time = today.strftime("%H:%M:%S")

sheety_headers = {
    "Authorization": os.environ["TOKEN"]
}

for item in exercise_data["exercises"]:
    sheety_params = {
        "workout": {
            "date": date,
            "time": time,
            "exercise": item["name"].title(),
            "duration": round(item["duration_min"]),
            "calories": item["nf_calories"],
        }
    }

    sheety_response = requests.post(url=sheety_endpoint, json=sheety_params, headers=sheety_headers)
