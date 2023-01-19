"""djangoweather URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

import weatherme.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hi/',weatherme.views.say_hello),
    path('',weatherme.views.say_hello),
    path('weather/city=<city_name>&key=<key>/', weatherme.views.get_weather),
    path('weather_gps/lat=<lat>&lon=<lon>/', weatherme.views.get_weather_gps),
    path('weather/city=<city_name>&country=<country_name>&key=<key>/', weatherme.views.get_weather)
]
