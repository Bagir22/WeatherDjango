from itertools import count

import requests
import os
from dotenv import load_dotenv
from django.shortcuts import render
from .models import City
from .forms import CityForm

def index(request):
    load_dotenv()
    owmAPI = os.getenv('owmAPI')
    print(owmAPI)
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid='
    url += str(owmAPI)

    cities = City.objects.all()

    if request.method == 'POST':  # only true if form is submitted
        form = CityForm(request.POST)  # add actual request data to form for processing
        form.save()

    form = CityForm()

    weather_data = []

    for city in cities:
        city_weather = requests.get(
            url.format(city)).json()

        weather = {
            'city': city,
            'temperature': city_weather['main']['temp'],
            'description': city_weather['weather'][0]['description'],
            'icon': city_weather['weather'][0]['icon']
        }

        weather_data.append(weather)  # add the data for the current city into our list

    context = {'weather_data': weather_data, 'form': form}

    return render(request, 'weather/index.html', context)
