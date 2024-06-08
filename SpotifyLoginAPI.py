import spotipy
from spotipy.oauth2 import SpotifyOAuth
SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET

def spotify_login():
    # Set your Spotify app credentials
    SPOTIPY_CLIENT_ID = SPOTIPY_CLIENT_ID
    SPOTIPY_CLIENT_SECRET = '189f08634fa74b3f89e9dad50aaaee88'
    SPOTIPY_REDIRECT_URI = 'http://localhost:8080/callback'

    # Set the scope to 'playlist-read-private' and 'user-library-read' to access private playlists and liked songs
    scope = "playlist-read-private,user-library-read"

    auth_manager = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                client_secret=SPOTIPY_CLIENT_SECRET,
                                redirect_uri=SPOTIPY_REDIRECT_URI,
                                scope=scope,
                                cache_path="token_info.json")

    sp = spotipy.Spotify(auth_manager=auth_manager)
    return auth_manager, sp
