from flask import Flask, render_template
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

API_KEY = "116a7580f2e9da0fe79698ccd7246265"
BASE_URL = "https://api.openweathermap.org/data/2.5/"

api_manifest = {
    "endpoints": {
        "weather": {
            "path": "weather",
            "params": {
                "q": "Cape Town",
                "units": "metric"
            }
        },
        "forecast": {
            "path": "forecast",
            "params": {
                "q": "Cape Town",
                "units": "metric"
            }
        }
    }
}

def fetch_weather_data(endpoint, params):
    url = f"{BASE_URL}{endpoint}"
    params['appid'] = API_KEY
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def process_daily_forecast_data(forecast_data):
    daily_forecast = {}
    for entry in forecast_data['list']:
        date = datetime.fromtimestamp(entry['dt']).strftime('%Y-%m-%d')
        if date not in daily_forecast:
            daily_forecast[date] = {
                'temp': [],
                'description': entry['weather'][0]['description']
            }
        daily_forecast[date]['temp'].append(entry['main']['temp'])

    daily_summary = []
    for date, data in daily_forecast.items():
        formatted_date = datetime.strptime(date, '%Y-%m-%d').strftime('%a %d %B %Y')
        average_temp = round(sum(data['temp']) / len(data['temp']), 2)
        daily_summary.append({
            'date': formatted_date,
            'average_temp': average_temp,
            'description': data['description']
        })

    return daily_summary

def process_hourly_forecast_data(hourly_forecast_data):
    hourly_forecast = []
    current_time = datetime.now()
    end_time = current_time + timedelta(hours=24)

    for entry in hourly_forecast_data['list']:
        timestamp = entry['dt']
        date_time = datetime.fromtimestamp(timestamp)
        
        if current_time <= date_time <= end_time:
            formatted_time = date_time.strftime('%H:%M')
            temp = entry['main']['temp']
            weather_desc = entry['weather'][0]['description']
            hourly_forecast.append({
                'time': formatted_time,
                'temp': temp,
                'description': weather_desc
            })
    
    return hourly_forecast

@app.route("/")
def home():
    weather_data = fetch_weather_data(api_manifest["endpoints"]["weather"]["path"], api_manifest["endpoints"]["weather"]["params"])
    forecast_data = fetch_weather_data(api_manifest["endpoints"]["forecast"]["path"], api_manifest["endpoints"]["forecast"]["params"])

    if weather_data and forecast_data:
        main_data = weather_data.get('main', {})
        humidity = main_data.get('humidity', None)
        wind_data = weather_data.get('wind', {})
        daily_forecast = process_daily_forecast_data(forecast_data)
        hourly_forecast = process_hourly_forecast_data(forecast_data)
        return render_template("index.html", title="Weather App", weather=weather_data, wind=wind_data, daily_forecast=daily_forecast, hourly_forecast=hourly_forecast, humidity=humidity)
    else:
        return render_template("index.html", title="Weather App", error="Failed to fetch weather data")

if __name__ == "__main__":
    app.run(debug=True)
