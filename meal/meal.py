from zina import speak, listen
import requests

# Spoonacular credentials
SPOONACULAR_API_KEY = 'SPOONACULAR_API_KEY'

# Fetch recipe based on meal type
def get_recipe(preferences, meal_type):
    query_params = {
        "apiKey": SPOONACULAR_API_KEY,
        "number": 1,
        "instructionsRequired": True
    }

    #Construct query based on user preferences
    if 'cuisine' in preferences:
        query_params['cuisine'] = preferences['cuisine']
    if 'diet' in preferences:
        query_params['diet'] = preferences['diet']
    if 'intolerances' in preferences:
        query_params['intolerances'] = preferences['intolerances']

    url = f"https://api.spoonacular.com/recipes/complexSearch"
    response = requests.get(url, params=query_params)
    data = response.json()

    if data['results']:
        recipe_id = data['results'][0]['id']
        recipe_title = data['results'][0]['title']
        recipe_url = f"https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={SPOONACULAR_API_KEY}"
        recipe_response = requests.get(recipe_url)
        recipe_data = recipe_response.json()

        ingredients = ", ".join([ingredient['name'] for ingredient in recipe_data['extendedIngredients']])
        instructions = ", ".join([step['step'] for step in recipe_data['analyzedInstructions'][0]['steps']])
        speak(f"I recommend you to have {recipe_title} for {meal_type}. Here is the recipe: Ingredients: {ingredients}. Instructions: {instructions}")
    else:
        speak(f"Sorry, I couldn't find a {meal_type} recipe at the moment.")

# Function to interactively gather user preferences
def gather_pref():
    speak("Let's find the perfect meal for you. Please tell me about your preferences for cuisine, diet, and any intolerances or allergies.")

    preferences = {
        'cuisine': None,
        'diet': None,
        'intolerances': None
    }

    while True:
        response = listen()
        if not response:
            speak("I'm sorry, I didn't catch that. Could you repeat?")
            continue

        # Use NLU or pattern matching to understand user input
        if 'cuisine' in response:
            preferences['cuisine'] = response.split('cuisine')[1].strip()
            speak(f"You prefer {preferences['cuisine']} cuisine, noted.")
        elif 'diet' in response:
            preferences['diet'] = response.split('diet')[1].strip()
            speak(f"You follow a {preferences['diet']} diet, understood.")
        elif 'intolerances' in response:
            preferences['intolerances'] = response.split('intolerances')[1].strip()
            speak(f"You have intolerance to {preferences['intolerances']}, duly noted.")
        
        speak("Do you have any other preferences? You can tell me about cuisine, diet, or intolerances.")

        # Break the loop if user confirms no more preferences
        if "no" in response:
            break
    
    return preferences