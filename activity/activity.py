from zina import speak, listen
import json
from MLearning import machine_learning
from weather import weather

# Start process for daily activities -> weather function is above
def ask_follow_up_question(question):
    speak(question)
    response = listen()
    return response

def suggest_activities(preferences, mood, weather_condition, temperature, model):
    # Encoding preferences and mood for prediction
    pref_encoded = 0 if preferences == 'indoor' else 1
    mood_encoded = 0 if mood == 'relaxed' else 1
    weather_encoded = 0 if weather_condition == 'sunny' else 1
    temp_encoded = 0 if temperature <= 15 else 1

    features = [[pref_encoded, mood_encoded, weather_encoded, temp_encoded]]
    acativity_prediction = model.predict(features)[0]

    activities = {
        0: ["Reading a book", "Watching a movie or series", "Cooking or baking something new", "Playing board games or video games"],
        1: ["Going for a walk in the park", "Having a picnic", "Going for a bike ride", "Playing outdoor sports like tennis or soccer", "Going to the beach"],
        2: ["Doing a home workout or yoga session", "Dancing to your favorite music"],
        3: ["Meditating or practicing mindfulness", "Taking a long bath"]
    }

    return activities.get(acativity_prediction, ['Relaxing at home.'])

def track_user_preferences(preferences, mood, activity):
    try:
        with open('user_preferences.json', 'r') as file:
            user_data = json.load(file)
    except FileNotFoundError:
        user_data = {'preferences': [], 'mood': []}

    user_data['preferenecs'].append(preferences)
    user_data['mood'].append(mood)
    user_data['activity'].append(activity)

    with open('user_preferences.json', 'w') as file:
        json.dump(user_data, file)

def daily_activities():
    speak("Let me suggest some activities for you today.")

    # Gather user preferences
    preferences = ask_follow_up_question("Do you prefer outdoor or indoor activities?")
    # Gather user mood
    mood = ask_follow_up_question("How are you feeling today? Energetic or relaxed?")
    
    model = machine_learning.train_model()

    if not model:
        speak("Sorry, I couldn't train the model due to insufficient data. Please try again later.")
        return

    city = weather.get_location()
    weather_description, temperature = weather.get_weather()

    if weather_description:
        speak(f"The current weather in {city} is {weather_description} with a temperature of {temperature} degrees Celsius.")
    else:
        speak("Sorry, I couldn't fetch the current weather details.")

    # Suggest activities based on user preferences
    activities = suggest_activities(preferences, mood, weather_description, temperature, model)
    speak("Here are some activities you can do today:")
    for activity in activities:
        speak(activity)
        track_user_preferences(preferences, mood, activity)