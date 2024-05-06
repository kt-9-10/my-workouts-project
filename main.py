import requests
from datetime import datetime
import os

APP_ID = os.environ["APP_ID"]
APP_KEY = os.environ["APP_KEY"]
BEARER = os.environ["BEARER"]
SHEET_ENDPOINT = os.environ["SHEET_ENDPOINT"]

nutritionix_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"

headers = {
    "x-app-id": APP_ID,
    "x-app-key": APP_KEY,
}

query = input("Tell me which exercises you did? :")

params = {
    "query": query,
}

response = requests.post(url=nutritionix_endpoint, json=params, headers=headers)
print(response.text)

data_dict = response.json()['exercises']

now = datetime.now()
formatted_date = now.strftime("%Y/%m/%d")
formatted_time = now.strftime("%H:%M:%S")

headers = {
    "Authorization": BEARER,
}

for workout in data_dict:
    exercise = workout["name"].title()
    duration = workout["duration_min"]
    calories = workout["nf_calories"]

    params = {
        "workout": {
            "date": formatted_date,
            "time": formatted_time,
            "exercise": exercise,
            "duration": duration,
            "calories": calories,
        },
    }
    response = requests.post(url=SHEET_ENDPOINT, json=params, headers=headers)
    print(response.text)
