# Creating a program that will identify the weather in every city

# Import what is needed
import requests
# URL and KEY of API
def get_weather(city):
    api_key = 'e90ba95533437d2b2bf26a7c6085bb75'  
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(url)
# Check if the response is successful

# The city to be inputed
