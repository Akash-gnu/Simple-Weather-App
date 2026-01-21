from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv
import random

# Load environment variables
load_dotenv()

app = Flask(__name__,
            static_folder='static',  # Explicitly set static folder
            template_folder='templates')  # Explicitly set template folder

# OpenWeatherMap API Configuration - FIXED: Use the correct environment variable name
API_KEY = os.getenv('OPENWEATHER_API_KEY')
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "http://api.openweathermap.org/data/2.5/forecast"

# Sample inspirational quotes
QUOTES = [
    "The best way to predict the future is to create it. - Peter Drucker",
    "Every day may not be good, but there is something good in every day. - Alice Morse Earle",
    "The sun himself is weak when he first rises, and gathers strength and courage as the day gets on. - Charles Dickens",
    "Wherever you go, no matter what the weather, always bring your own sunshine. - Anthony J. D'Angelo",
    "Nature is not a place to visit. It is home. - Gary Snyder",
    "Sunshine is delicious, rain is refreshing, wind braces us up, snow is exhilarating; there is really no such thing as bad weather, only different kinds of good weather. - John Ruskin",
    "After a day's walk everything has twice its usual value. - George Macauley Trevelyan"
]

# Major cities for nearby display
NEARBY_CITIES = ["London", "Paris", "Berlin", "Tokyo", "Sydney", "New York", "Dubai", "Singapore"]

# Check if API key is loaded
if not API_KEY:
    print("WARNING: OPENWEATHER_API_KEY not found in environment variables!")
    print("Please check your .env file")


@app.route('/')
def index():
    """Render the main page with a random quote"""
    random_quote = random.choice(QUOTES)
    return render_template('index.html', quote=random_quote)


@app.route('/api/weather', methods=['GET'])
def get_weather():
    """API endpoint to fetch weather data for a specific city"""
    city = request.args.get('city', 'London')

    # Check if API key is available
    if not API_KEY:
        return jsonify({'error': 'API key not configured'}), 500

    try:
        # Fetch current weather
        current_params = {
            'q': city,
            'appid': API_KEY,
            'units': 'metric'
        }
        current_response = requests.get(BASE_URL, params=current_params)
        current_data = current_response.json()

        if current_response.status_code != 200:
            error_message = current_data.get('message', 'City not found')
            return jsonify({'error': error_message}), 404

        # Process weather data
        weather_info = {
            'city': current_data['name'],
            'country': current_data['sys']['country'],
            'temperature': round(current_data['main']['temp']),
            'feels_like': round(current_data['main']['feels_like']),
            'humidity': current_data['main']['humidity'],
            'pressure': current_data['main']['pressure'],
            'wind_speed': current_data['wind']['speed'],
            'wind_deg': current_data['wind'].get('deg', 0),
            'description': current_data['weather'][0]['description'].title(),
            'icon': current_data['weather'][0]['icon'],
            'sunrise': current_data['sys']['sunrise'],
            'sunset': current_data['sys']['sunset'],
            'visibility': current_data.get('visibility', 10000) / 1000,  # Convert to km
            'clouds': current_data['clouds']['all']
        }

        return jsonify(weather_info)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/nearby-weather')
def get_nearby_weather():
    """API endpoint to fetch weather for nearby cities"""
    # Check if API key is available
    if not API_KEY:
        return jsonify({'error': 'API key not configured'}), 500

    try:
        nearby_weather = []

        for city in NEARBY_CITIES[:6]:  # Limit to 6 cities for display
            params = {
                'q': city,
                'appid': API_KEY,
                'units': 'metric'
            }
            response = requests.get(BASE_URL, params=params)

            if response.status_code == 200:
                data = response.json()
                city_weather = {
                    'city': data['name'],
                    'temperature': round(data['main']['temp']),
                    'description': data['weather'][0]['description'].title(),
                    'icon': data['weather'][0]['icon'],
                    'humidity': data['main']['humidity']
                }
                nearby_weather.append(city_weather)

        return jsonify({'cities': nearby_weather})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("Starting Weather App...")
    print(f"Static folder: {app.static_folder}")
    print(f"Template folder: {app.template_folder}")
    app.run(debug=True, port=5000)