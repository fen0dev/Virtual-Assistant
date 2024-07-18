import datetime
import speech_recognition as sr
import pyttsx3
import openai
import time
from weather import weather
from network import browser, news, wifi
from music import play_music
from movies import movies
from meal import meal
from directory import dir_find
from beverages import beverages
from activity import activity, reminder

openai.api_key = 'API_KEI_FROM_OPENAI'
# Initialize speech recognition and text-to-speech engines
recognizer = sr.Recognizer()
engine = pyttsx3.init()

preferences = {
    "default_city": "Copenhagen",
    "voice": "Microsoft David Desktop - English (United States)",
    "rate": 180,
    "volume": 0.9
}

# Function to capture audio input and recognize speech
def listen():
    with sr.Microphone() as source:
        print("[$] Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            print('[%] Recognizing...')
            text = recognizer.recognize_google(audio)
            print(f'[+] You said: {text}')
            return text.lower()
        except sr.UnknownValueError:
            print("[-] Sorry, I couldn't understand what you said!")
            speak("Sorry, I couldn't understand what you said! Please try again.")
            return ""
        except sr.RequestError as e:
            print(f"[-] Speech recognition request failed; {e}")
            speak(f"Sorry, I'm having trouble with speech recognition at the moment.")
            return ""
        except Exception as ex:
            print(f"[-] Unexpected error during speech recognition: {ex}")
            speak("An unexpected error occurred. Please try again.")
            return ""
        
# Function to speak the given text
def speak(text, rate=preferences["rate"], volume=preferences["volume"], voice=preferences["voice"]):
    try:
        engine.setProperty('rate', rate)
        engine.setProperty('volume', volume)
        if voice:
            voices = engine.getProperty('voices')
            for v in voices:
                if v.name == voice:
                    engine.setProperty('voice', v.id)
                    break
        sentences = text.split('.')
        for sentence in sentences:
            engine.say(sentence)
            engine.runAndWait()
        engine.say('.')
        engine.runAndWait()
    except Exception as e:
        print(f"[-] Error while speaking: {e}")
    
# Perform arithmetic calculations
def calculate(expression):
    try:
        # Evaluate the expression carefully
        result = eval(expression, {"__builtins__": None}, {})
        return result
    except Exception as e:
        return str(e)

# Generate response from OpenAI
def generate_response_from_openAI(prompt, model='text-davinci-003', max_tokens=250):
    response = openai.completions.create(
        engine=model,
        prompt=prompt,
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=0.7
    )

    return response.choices[0].text.strip()

# Handle commands
def handleCommands(command):
    if "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak("The current time is:" + current_time)
    elif "weather" in command:
        speak("Which city?")
        city = listen()
        if city:
            weather.get_weather(city)
    elif "What can I do today?" in command:
        activity.daily_activities()
    elif "news" in command:
        news.get_news()
    elif "wifi" in command:
        wifi_name = wifi.get_wifi_name()
        if wifi_name:
            speak(f"You are connected to: {wifi_name}")
        else:
            speak("Sorry, I couldn't retrieve your current WIFI network.")
    elif "find file" in command:
        speak("What is the name of the file you are looking for?")
        file_name = listen()
        if file_name:
            search_path = '/'
            file_path = dir_find.find_file(file_name, search_path)
            if file_path:
                speak(f"I found the file. The path is in: {file_path}")
                print(f"File found at: {file_path}")
            else:
                speak("Sorry, I couldn't find the file you've asked for.")
    elif "calculate" in command:
        speak("What calculation would you like to do?")
        expression = listen()
        if expression:
            result = calculate(expression)
            speak(f"The rsult is: {result}")
    elif "play" in command:
        song_name = command.replace("play", "").strip()
        play_music.play_music(song_name)
    elif "I'm hungry" in command:
        speak("Let me understand what you like.")
        preferences = listen()
        if preferences:
            preferences = preferences.split(",")
            meal.gather_pref(preferences)
        current_hour = datetime.datetime.now().hour
        if 5 <= current_hour < 11:
            meal_type = "breakfast"
        elif 11 <= current_hour < 15:
            meal_type = "lunch"
        elif 15 <= current_hour < 18:
            meal_type = "snack"
        else:
            meal_type = "dinner"
        result = meal.get_recipe(preferences, meal_type)
        speak(f"This meal could be good for you: {result}")
    elif "I'm thirsty" in command:
        beverages.remind_water()
        speak("However let me hear what you're in the mood for")
        preferences = listen()
        if preferences:
            beverages.gather_beverages_pref()
            results = beverages.get_beverages_with_pref(preferences)
            speak(f"The right drink for you is: {results}")
    elif "set reminder" in command:
        reminder.set_reminder()
    elif "recommend" in command:
        genre = command.replace("recommend", "").replace("movies", "").strip()
        movies.recommend_movies(genre)
    elif "open browser" in command:
        speak("Which browser would you like to open?")
        choice = listen()
        if choice:
            browser.open_browser(choice)
    elif "stop" in command:
        speak("Goodbye... Til next time!")
        exit()
    else:
        # Handling unrecognized commands with OpenAI
        response = generate_response_from_openAI(command)
        speak(response)


# Main function
if __name__ == '__main__':
    speak("Hi! I'm your virtual assistant. How can I help you today?")
    time.sleep(0.2)
    while True:
        command = listen()
        if command:
            handleCommands(command)