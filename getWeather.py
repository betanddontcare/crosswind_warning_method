import requests
lat = 55
lon = 55

def getVars(lat, lon):
    response = requests.get('http://api.openweathermap.org/data/2.5/weather?lat=' + str(lat) + '&lon=' + str(lon) + '&appid=4699786fb181c4f7c55e919dbee7b6f0')
    data = response.json()
    temperature = data['main']['temp'] - 273.15
    totalAirPressure = data['main']['pressure']
    humidity = data['main']['humidity'] / 100
    windVelocity = data['wind']['speed']
    windAngle = data['wind']['deg']
    return (temperature, totalAirPressure, humidity, windVelocity, windAngle)