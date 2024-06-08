from flask import Flask, request, render_template_string, redirect, render_template
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from Constants import SPOTIPY_CLIENT_ID_CONSTANT, SPOTIPY_CLIENT_SECRET_CONSTANT



app = Flask(__name__)

# Set your Spotify app credentials
SPOTIPY_CLIENT_ID = SPOTIPY_CLIENT_ID_CONSTANT
SPOTIPY_CLIENT_SECRET = SPOTIPY_CLIENT_SECRET_CONSTANT
SPOTIPY_REDIRECT_URI = 'http://localhost:8080/callback'

# Set the scope to 'playlist-read-private' and 'user-library-read' to access private playlists and liked songs
scope = "playlist-read-private,user-library-read"

auth_manager = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                            client_secret=SPOTIPY_CLIENT_SECRET,
                            redirect_uri=SPOTIPY_REDIRECT_URI,
                            scope=scope,
                            cache_path="token_info.json")

sp = spotipy.Spotify(auth_manager=auth_manager)

@app.route('/', methods=['GET', 'POST'])
def index():
    if not auth_manager.get_cached_token():
        auth_url = auth_manager.get_authorize_url()
        return redirect(auth_url)
    else:
        # Get the current user
        user = sp.current_user()

        # Get the user's playlists
        playlists = sp.user_playlists(user['id'])

        if request.method == 'POST':
            selected_playlists = request.form.getlist('playlists')
            liked_songs_selected = 'liked_songs' in request.form

            if liked_songs_selected:
                # Get the user's liked songs
                liked_songs = sp.current_user_saved_tracks()
                # Print each song name
                for song in liked_songs['items']:
                    artist_name = song['track']['artists'][0]['name']
                    song_name = song['track']['name']
                    print(f"Artist: {artist_name}, Song: {song_name}")

            # For each selected playlist, use the Spotify API to get all of the songs in the playlist
            for playlist_name in selected_playlists:
                # Find the selected playlist
                for playlist in playlists['items']:
                    if playlist['name'] == playlist_name:
                        # Get all the songs in the playlist
                        songs = sp.playlist_tracks(playlist['id'])
                        # Print each song name
                        for song in songs['items']:
                            artist_name = song['track']['artists'][0]['name']
                            song_name = song['track']['name']
                            print(f"Artist: {artist_name}, Song: {song_name}")

            # TODO: Use the YouTube Music API to create new playlists with the same songs

            return 'Selected playlists: ' + ', '.join(selected_playlists)
        else:
            # Return a form with a checkbox for each playlist and for the liked songs
            return render_template('index.html', playlists=playlists['items'])
@app.route('/callback')
def callback():
    auth_manager.get_access_token(request.args['code'])
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8080)