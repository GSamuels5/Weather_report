from flask import Flask, render_template, jsonify
import requests
import os
from datetime import datetime

app = Flask(__name__)

API_KEY = "116a7580f2e9da0fe79698ccd7246265"
BASE_URL = "https://api.openweathermap.org/data/2.5/"

api_manifest = {
    "endpoints": {
        "weather": {
            "q": "Cape Town",
            "units": "metric"
        },
        "wind": {},
        "forcast": {},
        "humidity": {}
    }
}

@app.route("/")
def home():
    return render_template("index.html", title="Weather App")

if __name__ == "__main__":
    app.run()
