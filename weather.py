# Creating a program that will identify the weather in every city

# Import what is needed
import requests
from datetime import datetime
import pytz
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

        ph_timezone = pytz.timezone('Asia/Manila')
        utc_time = datetime.fromtimestamp(timestamp, tz=pytz.UTC)
        local_time = utc_time.astimezone(ph_timezone).strftime('%Y-%m-%d %H:%M:%S')
        return weather_description, temperature, humidity, wind_speed, local_time
    else:
        return None, None, None, None
    
def main():
    city = input("Please input a city name: ")
    weather_description, temperature, humidity, wind_speed, date_time = get_weather(city)

    if weather_description is not None: 
        print(f"Date: {date_time}")
        print(f"Weather in {city}:")
        print(f"Description: {weather_description}")
        print(f"Temperature: {temperature}°C")
        print(f"Humidity: {humidity}%")
        print(f"Wind Speed: {wind_speed} m/s")
    else:
        print(f"Could not found weather data for {city}. Please correct the city name and try again")

if __name__ == "__main__":
    main()

# The city to be inputed
