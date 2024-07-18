import requests
from zina import speak

# Get weather condition for a specified city
def get_weather(city):
    weather_API_key = 'API_KEY'
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_API_key}"
    response = requests.get(url)
    response_ok = 200
    if response.status_code == response_ok:
        data = response.json()
        weather_descr = data['weather'][0]['description']
        temperature = data['main']['temp']
        speak(f"Weather in {city} is: {weather_descr} with {temperature} degrees Celcius.")
        return weather_descr, temperature
    else:
        speak(f"Sorry, couldn't fetch weather condition in {city}.")
        return None, None
    
# Function to dinamically find user location
def get_location():
    try:
        response = requests.get("https://ipinfo.io")
        data = response.json()
        return data['city']
    except Exception as e:
            print(f"[-] Error retrieving location: {e}")
            return 'Copenhagen'