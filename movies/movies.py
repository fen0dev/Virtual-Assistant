from zina import speak
import requests
import datetime

# TMDB credentials
TMDB_API_KEY = 'TMDB_API_KEY'

# Recommend movies
def recommend_movies(genre):
    genre_mapping = {
        "horror": 27,
        "comedy": 35,
        "drama": 18,
        "sci-fi": 878,
        "animated": 16,
        "romance": 10749,
        "thriller": 53,
        "action": 28,
        "adventure": 12,
        "fantasy": 14,
        "mystery": 9648,
        "documentary": 99
    }
    genre_id = genre_mapping.get(genre.lower())
    if not genre_id:
        speak("Sorry, I don't recognize that genre. Please try again.")
        return
    
    url = f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&with_genres={genre_id}&primary_release_date.gte=2004-01-01&primary_release_date.lte={datetime.datetime.now().strftime('%Y-%m-%d')}"
    response = requests.get(url)
    data = response.json()

    if data['results']:
        movie_titles = [movie['title'] for movie in data['results'][:5]]
        movie_list = ", ".join(movie_titles)
        speak(f"Here are some {genre} movies from the last 20 years: {movie_list}")
    else:
        speak("Sorry, I couldn't find any movies in that genre.")