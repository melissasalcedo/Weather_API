# Creating a program that will identify the weather in every city

# Import what is needed
import requests
from datetime import datetime
# URL and KEY of API
def get_weather(city):
    api_key = 'e90ba95533437d2b2bf26a7c6085bb75'  
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(url)
# Check if the response is successful
    if response.status_code == 200:
        data = response.json()
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        timestamp = data['dt']

        date_time = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        return weather_description, temperature, humidity, wind_speed, date_time
    else:
        return None, None, None, None

# The city to be inputed
