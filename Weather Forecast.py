import requests
import json
import sys
from datetime import datetime, timedelta
import tkinter

# All APIs came from open meteo

country = input("country: ")
geocoding_api_url = "https://geocoding-api.open-meteo.com/v1/search?" + "name=" + country.replace(" ", "+") + "&count=1" + "&language=en&format=json"
location_response = requests.get(geocoding_api_url)

if location_response.status_code == requests.codes.ok:
    raw_location_data = json.loads(location_response.text)
    try: 
        location_data = raw_location_data["results"][0]
    except:
        print(f"\033[91m Error: you have probably not entered a valid country or typed incorrectly\033[0m")
        sys.exit()
    latitude = location_data["latitude"]
    longitude = location_data["longitude"]

else:
    print("Error: " + location_response.status_code, location_response.text)

weather_api_url = "https://api.open-meteo.com/v1/forecast?" + "latitude=" + str(latitude) + "&longitude=" + str(longitude) + "&hourly=temperature_2m&forecast_days=1"
weather_response = requests.get(weather_api_url)
now = datetime.now()
current_time = (now + timedelta(minutes=30)).replace(minute=0, second=0, microsecond=0)
formatted_now = current_time.isoformat()

if weather_response.status_code == requests.codes.ok:
    raw_weather_data = json.loads(weather_response.text)
    weather_data = raw_weather_data["hourly"]["temperature_2m"]
    # does not take into account the current time, only shows the average of the temperatures that the API gave
    index = 0
    for time in raw_weather_data["hourly"]["time"]:
        if time != formatted_now[:-3]:
            index += 1
        else:
            break
    temp = weather_data[index]
    avg_temp = round(sum(weather_data) / len(weather_data), 2)

else:
    print("Error: ", weather_response.status_code, weather_response.text)

print("==============================================================")
print("Country/City: " + country)
print("Date & Time: " + str(current_time)[:-3])
print("Current Temp: " + str(temp))
print("Avg Temp(Today): " + str(avg_temp) + raw_weather_data["hourly_units"]["temperature_2m"])
