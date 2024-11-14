import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import threading

# Define your Spotify Developer credentials
CLIENT_ID = '27bea52ca5e74e5aaa292559b07375bf'
CLIENT_SECRET = 'd086997ad2ae42d1befe57ed9b188951'
REDIRECT_URI = 'http://localhost:8888/callback'

# Define scope for controlling playback
SCOPE = 'user-modify-playback-state user-read-playback-state'

# Authenticate with Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope=SCOPE))

# Flag to control skipping function
skip_active = False

def skip_song_every_35_seconds():
    global skip_active
    while True:
        if skip_active:
            # Check if Spotify is currently playing
            playback = sp.current_playback()
            if playback and playback['is_playing']:
                print("Currently playing:", playback['item']['name'], "by", playback['item']['artists'][0]['name'])
                # Wait 35 seconds
                time.sleep(35)
                # Skip to the next track
                sp.next_track()
                print("Skipped to the next track.")
            else:
                print("No track currently playing. Retrying in 5 seconds.")
                time.sleep(5)
        else:
            # Wait before checking the flag again
            time.sleep(1)

def toggle_skip():
    global skip_active
    while True:
        user_input = input("Enter 'start' to enable skipping or 'stop' to disable: ").strip().lower()
        if user_input == "start":
            skip_active = True
            print("Skipping enabled.")
        elif user_input == "stop":
            skip_active = False
            print("Skipping disabled.")

# Run the song-skipping function in a separate thread
skipping_thread = threading.Thread(target=skip_song_every_35_seconds)
skipping_thread.daemon = True
skipping_thread.start()

# Run the toggle function in the main thread
toggle_skip()