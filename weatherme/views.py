import json

from django.http import HttpResponse
import requests

import local_key


def get_weather(request,key, lat=None, lon=None, city_name="London", county_name=None, units="metric"):
    if key == local_key.API_KEY:
        weather_pack = "error"
        if city_name is not None:
            geo_coords_req = requests.get(
                url=f"https://maps.googleapis.com/maps/api/geocode/json?address={city_name}&key={local_key.GEOCODDING_API_KEY}")
            if geo_coords_req.status_code == 200:
                geo_coords = geo_coords_req.json()
                if len(geo_coords['results']) > 1:
                    return HttpResponse("please specify a country")
                if len(geo_coords['results']) == 0:
                    return HttpResponse("no such city")
                lat = geo_coords['results'][0]['geometry']['location']['lat']
                lon = geo_coords['results'][0]['geometry']['location']['lng']

        weather_response = requests.get(
            url=f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units={units}&appid={local_key.WEATHER_API_KEY}")
        if weather_response.status_code == 200:
            weather_data = weather_response.json()
            weather_pack = {
                'city_name': weather_data['name'],
                'temp': {
                    'current': weather_data['main']['temp'],
                    'max': weather_data['main']['temp_max'],
                    'min': weather_data['main']['temp_min'],
                },
                'state': {
                    'sky': weather_data['weather'][0]['main'],
                    'sky_info': weather_data['weather'][0]['description'],
                    'sky_icon': weather_data['weather'][0]['icon']
                }
            }
        return HttpResponse(json.dumps(weather_pack))
    else:
        return HttpResponse(status_code=500)


def say_hello(request):
    return HttpResponse("hello!")
