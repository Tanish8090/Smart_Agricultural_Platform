import urllib.request
import json

locations = [
    ("Kanpur", 26.4499, 80.3319),
    ("Bhopal", 23.2599, 77.4126),
    ("Indore", 22.7196, 75.8577),
    ("GPS (Pune)", 18.5204, 73.8567)
]

print("Testing Open-Meteo live weather data for different locations...")
for name, lat, lon in locations:
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,rain,weather_code,cloud_cover,wind_speed_10m&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max&timezone=auto"
    req = urllib.request.Request(url, headers={'User-Agent': 'SAP-WeatherTest/1.0'})
    try:
        with urllib.request.urlopen(req, timeout=8) as res:
            data = json.loads(res.read().decode('utf-8'))
            cur = data.get('current', {})
            temp = cur.get('temperature_2m')
            humidity = cur.get('relative_humidity_2m')
            wind = cur.get('wind_speed_10m')
            wcode = cur.get('weather_code')
            print(f"[PASS] {name} (Lat: {lat}, Lon: {lon}) -> Temp: {temp}°C, Humidity: {humidity}%, Wind: {wind} km/h, Code: {wcode}")
    except Exception as e:
        print(f"[FAIL] {name}: {e}")
