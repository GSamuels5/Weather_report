from flask import Flask, render_template
import requests
import os
from datetime import datetime

app = Flask(__name__)

API_KEY = os.getenv('OPENWEATHER_API_KEY', '116a7580f2e9da0fe79698ccd7246265')
CITY = 'Cape Town,za'

@app.route("/")
def home():
    url = f'http://api.openweathermap.org/data/2.5/weather?q={CITY}&units=metric&APPID={API_KEY}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        temp_min = data['main']['temp_min']
        temp_max = data['main']['temp_max']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        visibility = data.get('visibility', 'N/A')
        visibility = visibility / 1000 if visibility != 'N/A' else 'N/A'
        precipitation = data.get('rain', {}).get('1h', 0) + data.get('snow', {}).get('1h', 0)

        weather_data = {
            'description': weather_description,
            'temperature': temperature,
            'temp_min': temp_min,
            'temp_max': temp_max,
            'humidity': humidity,
            'wind_speed': wind_speed,
            'visibility': visibility,
            'precipitation': precipitation
        }

        return render_template('index.html', weather=weather_data)
    else:
        return f"Error: Unable to fetch data (status code: {response.status_code})"

@app.route("/forecast")
def forecast():
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={CITY}&units=metric&APPID={API_KEY}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        weekly_forecast = []
        for day in data['list']:
            date = datetime.utcfromtimestamp(day['dt'])
            formatted_date = date.strftime('%a %d %B %Y %I:%M%p')

            day_forecast = {
                'date': formatted_date,
                'description': day['weather'][0]['description'],
                'temperature': {
                    'day': day['main']['temp'],
                    'min': day['main']['temp_min'],
                    'max': day['main']['temp_max']
                },
                'humidity': day['main']['humidity'],
                'wind_speed': day['wind']['speed'],
                'precipitation': day.get('rain', {}).get('3h', 0)
            }
            weekly_forecast.append(day_forecast)

        return render_template('forecast.html', forecast=weekly_forecast)
    else:
        return f"Error: Unable to fetch data (status code: {response.status_code})"

if __name__ == "__main__":
    app.run()
