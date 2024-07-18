from zina import speak
import requests

# Get top headlines 
def get_news():
    news_API_key = 'NEWS_API_KEY'
    url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={news_API_key}'
    response = requests.get(url)
    data = response.json()
    if data['status'] == 'ok':
        headlines = [article['title'] for article in data['articles'][:5]]
        speak("Here there are the top news:")
        for headline in headlines:
            speak(headline)
    else:
        speak("Sorry, I could not fetch news at this time.")