import os
import requests

def getWeatherParams(lat, lon):
    api_key = os.environ.get('OPENWEATHERMAP_API_KEY', '')
    data = requests.get('http://api.openweathermap.org/data/2.5/weather?lat=' + str(lat) + '&lon=' + str(lon) + '&appid=' + api_key).json()
    temperature = data['main']['temp'] - 273.15
    totalAirPressure = data['main']['pressure']
    humidity = data['main']['humidity'] / 100
    windVelocity = data['wind']['speed']
    windAngle = data['wind']['deg']
    isRainy = data['weather'][0]['main'] in ('Rain', 'Snow')
    return (temperature, totalAirPressure, humidity, windVelocity, windAngle, isRainy)