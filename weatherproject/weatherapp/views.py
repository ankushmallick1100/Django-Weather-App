import requests
from django.shortcuts import render
from dotenv import load_dotenv
import os

def configure():
    load_dotenv()

# Create your views here.
def index(request):
    configure()

    api_key = os.getenv('weather_api_key')

    current_weather_url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'

    if request.method == "POST":
        city1 = request.POST['city1']
        city2 = request.POST.get('city2', None)

        weather_data1 = fetch_weather(city1, api_key, current_weather_url)

        if city2:
            weather_data2 = fetch_weather(city2, api_key, current_weather_url)
        else:
            weather_data2 = None

        context = {
            "weather_data1": weather_data1,
            "weather_data2": weather_data2
        }

        return render(request, "weatherapp/index.html", context)
    else:
        return render(request, "weatherapp/index.html")
    
def fetch_weather(city, api_key, current_weather_url):
    response = requests.get(current_weather_url.format(city, api_key)).json()

    weather_data = {
        'city': city,
        'lat': response['coord']['lat'],
        'lon': response['coord']['lon'],
        'temperature': round(response['main']['temp'] - 273.15, 2),
        'min_temperature': round(response['main']['temp_min'] - 273.15, 2),
        'max_temperature': round(response['main']['temp_max'] - 273.15, 2),
        'feel_temperature': round(response['main']['feels_like'] - 273.15, 2),
        'description': response['weather'][0]['description'],
        'icon': response['weather'][0]['icon'],
        'pressure': response['main']['pressure'],
        'humidity': response['main']['humidity'],
        'visibility': response['visibility'],
        'wind_speed': response['wind']['speed'],
        'wind_speed_degree': response['wind']['deg']
    }

    return weather_data
