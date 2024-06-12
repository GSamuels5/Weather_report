from flask import Flask, redirect, render_template, url_for
import requests

app = Flask(__name__)

API_KEY = '116a7580f2e9da0fe79698ccd7246265'
CITY = 'Cape Town,za'
LAT = '-33.9249'
LON = '18.4241'

@app.route("/")
def home():
    url = 'http://api.openweathermap.org/data/2.5/weather?q=Cape%20Town,za&units=metric&APPID=116a7580f2e9da0fe79698ccd7246265'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        # Extract current weather data
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        visibility = data.get('visibility', 'N/A') / 1000

        if 'rain' in data:
            precipitation = data['rain'].get('1h', 0)
        elif 'snow' in data:
            precipitation = data['snow'].get('1h', 0)
        else:
            precipitation = 0

        # Prepare weather data to display
        weather_data = {
            'description': weather_description,
            'temperature': temperature,
            'humidity': humidity,
            'wind_speed': wind_speed,
            'visibility': visibility,
            'precipitation': precipitation
        }

        return render_template('index.html', weather = weather_data)
    else:
        return "Error: Unable to fetch data (status code: {response.status_code})"

# @app.route("/forecast")
# def fore():
#     url = f'http://api.openweathermap.org/data/2.5/forecast?q={CITY}&cnt=7&units=metric&APPID={API_KEY}'
#     response = requests.get(url)

#     if response.status_code == 200:
#         data = response.json()

#         weekly_forecast = []
#         for day in data['list']:
#             day_forecast = {
#                 'date': day['dt'],
#                 'description': day['weather'][0]['description'],
#                 'temperature': {
#                     'day': day['temp']['day'],
#                     'min': day['temp']['min'],
#                     'max': day['temp']['max'],
#                     'night': day['temp']['night'],
#                     'eve': day['temp']['eve'],
#                     'morn': day['temp']['morn']
#                 },
#                 'humidity': day['humidity'],
#                 'wind_speed': day['speed'],
#                 'precipitation': day.get('rain', 0)
#             }
#             weekly_forecast.append(day_forecast)

#         return render_template('index01.html', forecast=weekly_forecast)
#     else:
#         return f"Error: Unable to fetch data (status code: {response.status_code})"



if __name__ == "__main__":
    app.run()


# @app.route("/<name>")
# def user(name):
#     return f"Hello {name}!"

# @app.route("/admin")
# def admin():
#     return redirect(url_for("home"))

# if __name__ == "__main__":
#     app.run()

# API_KEY = '116a7580f2e9da0fe79698ccd7246265'

# lat = '33.9221'
# lon = '18.4231'

# url = 'http://api.openweathermap.org/data/2.5/weather?q=Cape%20Town,za&units=metric&APPID=116a7580f2e9da0fe79698ccd7246265'

# response = requests.get(url)

# if response.status_code == 200:
#     data = response.json()

#     # Extract current weather data
#     weather_description = data['weather'][0]['description']
#     temperature = data['main']['temp']
#     humidity = data['main']['humidity']
#     wind_speed = data['wind']['speed']
#     visibility = data.get('visibility', 'N/A') / 1000

#     if 'rain' in data:
#         precipitation = data['rain'].get('1h', 0)
#     elif 'snow' in data:
#         precipitation = data['snow'].get('1h', 0)
#     else:
#         precipitation = 0
    
#     # Display current weather data
#     print("Current CAPE TOWN Weather: ")
#     print(f"Weather: {weather_description}")
#     print(f"Temperature: {temperature}°C")
#     print(f"Humidity: {humidity}%")
#     print(f"Wind Speed: {wind_speed} m/s")
#     print("Visibility: {visibility} km")
#     print("Precipitation (last hour): {precipitation} mm")

#     # print(data)
# else:
#     print("Error: Unable to fetch data (status code: {response.status_code})")

