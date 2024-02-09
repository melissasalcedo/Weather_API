from bottle import Bottle, run, request
import requests
from datetime import datetime
import pytz

app = Bottle()

def get_wind_direction(degrees):
    directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
    index = round(degrees / (360 / len(directions))) % len(directions)
    return directions[index]

def get_weather(city):
    if not city:
        return None, None, None, None, None, None

    api_key = 'e90ba95533437d2b2bf26a7c6085bb75'  
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        wind_deg = data['wind']['deg']
        wind_direction = get_wind_direction(wind_deg)
        timestamp = data.get('dt')

        if timestamp:
            ph_timezone = pytz.timezone('Asia/Manila')
            utc_time = datetime.fromtimestamp(timestamp, tz=pytz.UTC)
            local_time = utc_time.astimezone(ph_timezone).strftime('%Y-%m-%d %H:%M:%S')
        else:
            local_time = None

        return weather_description, temperature, humidity, wind_speed, wind_direction, local_time
    else:
        return None, None, None, None, None, None

@app.route('/')
def index():
    city = request.query.get('city', '')
    if not city:
        weather_info = "<p>Please input a city name</p>"
    else:
        weather_description, temperature, humidity, wind_speed, wind_direction, date_time = get_weather(city)

        if weather_description is not None:
            weather_info = f'''
                <p><b>Date:</b> {date_time}</p>
                <p><b>Weather:</b> {weather_description}</p>
                <p><b>Temperature:</b> {temperature}°C</p>
                <p><b>Humidity:</b> {humidity}%</p>
                <p><b>Wind Speed:</b> {wind_speed} m/s {wind_direction}</p>
            '''
        else:
            weather_info = f"<p>Could not find weather data for {city}. Please correct the city name and try again.</p>"

    return f'''
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #BFE6FF; /* Light blue background */
                    background-image: url('bg.jpg');
                    background-repeat: no-repeat;
                    background-attachment: fixed;
                    background-size: cover;
                    background-position: center;
                }}
                .container {{
                    max-width: 600px;
                    margin: 50px auto 20px; /* Changed margin */
                    padding: 20px;
                    background-color: #FFD6E0; /* Light pink background */
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                }}
                h1 {{
                    color: black; /* Changed font color */
                    text-align: center;
                }}
                form {{
                    text-align: center;
                    margin-bottom: 20px;
                }}
                input[type="text"] {{
                    padding: 8px;
                    width: 60%;
                    margin-right: 8px;
                    border-radius: 4px;
                    border: 1px solid #ccc;
                }}
                input[type="submit"] {{
                    padding: 8px 16px;
                    background-color: #B7A9A5; /* Pastel brown */
                    color: #fff;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                }}
                input[type="submit"]:hover {{
                    background-color: #8C7C76; /* Darker pastel brown */
                }}
                .weather-info {{
                    margin-top: 20px;
                    text-align: center;
                }}
                .weather-info p {{
                    font-weight: bold; /* Make text bold */
                    font-family: 'Arial Black', sans-serif; /* Use a different font */
                    font-size: 16px; /* Adjust font size */
                    margin-bottom: 10px; /* Add some bottom margin */
                    color: black; /* Changed font color */
                }}
                .error {{
                    color: red; /* Red color for error messages */
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Weather App</h1>
                <form action="/" method="get">
                    <input type="text" name="city" placeholder="Enter city name" value="{city}" required>
                    <input type="submit" value="Get Weather">
                </form>
                <div class="weather-info">
                    {weather_info}
                </div>
            </div>
        </body>
        </html>
    '''

if __name__ == '__main__':
    run(app, host='localhost', port=8080, debug=True)