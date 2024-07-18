from zina import speak, listen
import requests

# Vivino credentials (or replace with another wine API)
VIVINO_API_KEY = 'VIVINO_API_KEY'

def remind_water():
    speak("First of all remember to stay hydrated and drink at least 3 glasses of water an hour!")

# Fetch wine or cocktail recommendations based on user preferences from Vivino or other APIs
def get_beverages_with_pref(preferences):
    url = f"https://api.vivino.com/wines/api/explore/explore?api_key={VIVINO_API_KEY}&country_code=US"

    # Customize the query based on user preferences
    if "alcohol_type" in preferences:
        url += f"&wine_type={preferences['alcohol_type']}"

    response = requests.get(url)
    data = response.json()

    if data.get('explore_vintage', []):
        beverage_name = data['explore_vintage'][0]['vintage']['wine']['name']
        beverage_year = data['explore_vintage'][0]['vintage']['year']
        beverage_style = data['explore_vintage'][0]['vintage']['wine']['style']['title']
        beverage_price = data['explore_vintage'][0]['price']['formatted']
        beverage_rating = data['explore_vintage'][0]['vintage']['statistics']['ratings_average']

        speak(f"I recommend {beverage_name} {beverage_year}, a {beverage_style} style. Price: {beverage_price}. Average rating: {beverage_rating}. Enjoy responsibly!")
    else:
        speak("Sorry, I couldn't find a beverage recommendation that matches your preferences.")

# Function to interactively gather user preferences for beverages
def gather_beverages_pref():
    speak("Let's find the perfect beverage for you. Are you in the mood for alcohol or non-alcoholic drinks?")

    preferences = {
        "alcohol_type": None
    }

    while True:
        response = listen()
        if not response:
            speak("I'm sorry, I didn't catch that. Could you repeat?")
            continue

        # Use NLU or pattern matching to understand user input
        if "alcohol" in response:
            preferences['alcohol_type'] = response.split("alcohol")[1].strip()
            speak(f"You prefer {preferences['alcohol_type']} beverages, noted.")
            break
        elif "non-alcoholic" in response:
            preferences['alcohol_type'] = 'non-alcoholic'
            speak("You prefer non-alcoholic beverages, understood.")
            break
        else:
            speak("I'm sorry, I didn't catch that. Are you in the mood for alcohol or non-alcoholic drinks?")
    
    return preferences