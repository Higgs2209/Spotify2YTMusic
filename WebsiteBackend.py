from flask import Flask, request, render_template, redirect, session
from main import Spotify
from Constants import SPOTIPY_CLIENT_ID_CONSTANT, SPOTIPY_CLIENT_SECRET_CONSTANT
from ytmusicapi import YTMusic
from main import Spotify

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # replace with your own secret key

spotify = Spotify(SPOTIPY_CLIENT_ID_CONSTANT, SPOTIPY_CLIENT_SECRET_CONSTANT, 'http://localhost:8080/callback')


@app.route('/')
def home():
    return render_template('home.html')  # create a home.html template with links to /spotify and /youtube


@app.route('/spotify')
def spotify_auth():
    auth_url = spotify.authenticate()
    if auth_url:
        return redirect(auth_url)
    else:
        return redirect('/spotify/playlists')


@app.route('/spotify/callback')
def spotify_callback():
    spotify.auth_manager.get_access_token(request.args['code'])
    return redirect('/spotify/playlists')


@app.route('/spotify/playlists', methods=['GET', 'POST'])
def spotify_playlists():
    if request.method == 'POST':
        selected_playlists = request.form.getlist('playlists')
        session['selected_playlists'] = selected_playlists
        return redirect('/select-platform')  # redirect to the new route
    else:
        playlists = spotify.get_playlists()
        return render_template('index.html', playlists=playlists['items'])


@app.route('/select-platform')
def select_platform():
    return render_template('select_platform.html')  # create a new HTML template for this route


@app.route('/transfer/youtube')
def transfer_youtube():
    ytmusic = YTMusic('oauth.json')  # replace with your headers auth file
    selected_playlists = session.get('selected_playlists', [])

    for playlist_id in selected_playlists:
        print(f"Playlist ID: {playlist_id}")  # print out the playlist ID
        # Get the playlist details and tracks from Spotify
        playlist = spotify.get_playlist(playlist_id)  # use get_playlist method here
        tracks = spotify.get_playlist_tracks(playlist_id)

        # Search for each track on YouTube Music and get its ID
        youtube_track_ids = []
        for track in tracks:
            search_results = ytmusic.search(f"{track['track']['artists'][0]['name']} {track['track']['name']}",
                                            filter='songs', limit=1)
            if search_results:
                print(
                    f"Search results for {track['track']['artists'][0]['name']} {track['track']['name']}: {search_results[0]}")  # print out the first search result
                youtube_track_ids.append(search_results[0]['videoId'])

        print(f"YouTube track IDs: {youtube_track_ids}")  # print out the YouTube track IDs

        # Create a new playlist on YouTube Music and add the tracks
        youtube_playlist_id = ytmusic.create_playlist(playlist['name'], playlist['description'])
        result = ytmusic.add_playlist_items(youtube_playlist_id, youtube_track_ids)
        print(f"Result of add_playlist_items: {result}")  # print out the result of add_playlist_items

    return 'Playlists have been transferred to YouTube Music!'


if __name__ == '__main__':
    app.run(port=8080)
