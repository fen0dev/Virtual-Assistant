from zina import speak
import platform
import subprocess as sb
import requests
import webbrowser
try:
    import spotipy
    from spotipy.oauth2 import SpotifyOAuth
    print("Spotipy imported successfully!")
except ImportError as e:
    print("Error importing spotipy:", e)


# Spotify credentials
SPOTIPY_CLIENT_ID = 'CLIENT_SPOTIFY_ID'
SPOTIPY_CLIENT_SECRET = 'SPOTIFY_CLIENT_SECRET'
SPOTIPY_REDIRECT_URI = 'http://localhost:8888/callback'

# Spotify OAuth init
sp_oauth = SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope="user-read-playback-state,user-modify-playback-state"
)

# Playing music functions
def check_apple_music():
    try:
        if platform.system() == "Darwin":   # For MacOs
            sb.Popen(["open", "-a", "Music"], check=True)
            speak("Apple Music is currently active on your system.")

        # Check status for subscription in order to play music
        if is_subscribed_to_apple_music():
            speak("You are subscribed to Apple Music.")
        else:
            speak("It seems you are not subscribed to Apple Music. Please check your subscription.")

        # Check if music playback is possible (optional)
        if can_play_music():
            speak("You can play music.")
        else:
            speak("It seems music playback is not currently available.")
    except sb.CalledProcessError:
        speak("It seems Apple Music is not active on your system.")
    except Exception as e:
        print(f"[-] Error checking Apple Music: {e}")
        speak("Sorry, there was an error checking Apple Music. Please try again later.")

def is_subscribed_to_apple_music(access_token):
     # Apple Music API endpoint to check subscription status
    url = 'https://api.music.apple.com/v1/me/subscription'

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    try:
        # Make GET request to API endpoint
        response = requests.get(url, headers=headers)
        data = response.json()

        # Check if request was succesfull
        if response.status_code == 200:
            subscription_info = response.json()

            # Check subscription status
            if subscription_info.get('data', {}).get('Attributes', {}).get('hasActiveSubscription', False):
                return True     # if user is subscribed to Apple Music
            else:
                return False
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return False  # Handle error cases

    except requests.exceptions.RequestException as e:
        print(f"Error requesting Apple Music API: {e}")
        return False  # Handle request exception

    except Exception as ex:
        print(f"Unexpected error: {ex}")
        return False  # Handle unexpected errors

def can_play_music():
    try:
        sb.run(['pgrep', '-x', 'Music'], check=True)
        return True
    except sb.CalledProcessError:
        return False

# Check for Spotify
def is_spotify_installed():
    try:
        if platform.system() == "Windows":
            sb.Popen(["Spotify"], stdout=sb.PIPE, stderr=sb.PIPE)
        elif platform.system() == "Darwin":
            sb.Popen(["open", "-a", "Spotify"])
        elif platform.system() == "Linux":
            sb.Popen(["spotify"])
        else:
            return False
        return True
    except Exception:
        return False

# Open Youtube and play song
def open_yt_and_play_song(song_name):
    query = f"https://www.youtube.com/results?search_query={song_name.replace(' ', '+')}"
    webbrowser.open(query)

# check_spotify_subscription
def check_spotify_subscription_and_play(song_name):
    # This requires Spotify OAuth setup and checking subscription via API
    token_info = sp_oauth.get_cached_token()
    if not token_info:
        auth_url = sp_oauth.get_authorize_url()
        print(f"Please navigate here to authorize: {auth_url}")
        response = input("Enter the URL you were redirected to: ")
        code = sp_oauth.parse_response_code(response)
        token_info = sp_oauth.get_access_token(code)

    if token_info:
        sp = spotipy.Spotify(auth=token_info['access_token'])
        results = sp.search(q=song_name, limit=1, type='track')
        if results['track']['items']:
            track = results['track']['items'][0]
            sp.start_playback(uris=[track['uri']])
            speak(f"Playing {track['name']} by {track['artists'][0]['name']} on Spotify")
        else:
            speak(f"Sorry, I couldn't find {song_name} on Spotify.")
    else:
        speak("Spotify authentication failed.")

# Play music
def play_music(song_name):
    if check_apple_music():
        speak(f"Playing {song_name} on Apple Music")
        # Code to play song on Apple Music (depends on AppleScript or MusicKit)
    elif is_spotify_installed():
        if check_spotify_subscription_and_play():
            speak(f"Playing {song_name} on Spotify")
            # Code to play song on Spotify (requires Spotify Web API)
        else:
            speak("Spotify is installed but you do not have a subscription whatsoever. Consider making one to reproduce music!")
    else:
        speak(f"Playing {song_name} on YouTube")
        open_yt_and_play_song(song_name)
