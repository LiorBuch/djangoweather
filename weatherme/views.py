import json

from django.http import HttpResponse
import requests

import local_key


def get_weather(request, lat=None, lon=None, city_name="London", country_name=None, state_code=None):
    if request.headers["api"] == local_key.API_KEY:
        if lat or lon is None:
            if city_name is not None:
                geo_coords_req = requests.get(
                    url=f"http://api.openweathermap.org/geo/1.0/direct?q={city_name},{state_code},{country_name}&limit=3&appid={local_key.WEATHER_API_KEY}")
                if geo_coords_req.status_code == 200:
                    geo_coords = geo_coords_req.json()
                    if len(geo_coords) > 1:
                        return HttpResponse(status=300, content={
                            'info': 'More than one location was found, need country name as well'})
                    if len(geo_coords['results']) == 0:
                        return HttpResponse("no such city")
                    lat = geo_coords[0]['lat']
                    lon = geo_coords[0]['lon']

                    county_name = geo_coords['results'][0]["formatted_address"]
                    obj = get_weather_gps(request, lat, lon, name=county_name)
                    return obj
    else:
        return HttpResponse(status_code=500)


def say_hello(request):
    return HttpResponse("hello! from v1.2")


def get_weather_gps(request, lat, lon, name, units="metric"):
    weather_pack = None
    if request.headers["api"] == local_key.API_KEY:
        weather_res = requests.get(
            url=f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units={units}&appid={local_key.WEATHER_API_KEY}")
        if weather_res.status_code == 200:
            weather_data = weather_res.json()
            weather_pack = {
                'city_name': str(name),
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
