from flask import Flask, render_template, request
import requests
import os
from datetime import datetime
from dotenv import load_dotenv

app = Flask(__name__)

# You'll need to sign up for a free API key at OpenWeatherMap
# https://openweathermap.org/api
load_dotenv()
API_KEY = os.getenv('API_KEY')
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    error = None

    if request.method == 'POST':
        city = request.form.get('city')
        
        if city:
            # Make API request
            params = {
                'q': city,
                'appid': API_KEY,
                'units': 'metric'  # Use metric units (Celsius)
            }
            
            try:
                response = requests.get(BASE_URL, params=params)
                data = response.json()

                if response.status_code == 200:
                    weather_data = {
                        'city': data['name'],
                        'country': data['sys']['country'],
                        'temperature': round(data['main']['temp']),
                        'description': data['weather'][0]['description'].capitalize(),
                        'icon': data['weather'][0]['icon'],
                        'humidity': data['main']['humidity'],
                        'wind_speed': data['wind']['speed'],
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                else:
                    error = 'City not found. Please try again.'
            
            except Exception as e:
                error = 'An error occurred. Please try again.'

    return render_template('weather.html', weather_data=weather_data, error=error)

if __name__ == '__main__':
    app.run(debug=True)
