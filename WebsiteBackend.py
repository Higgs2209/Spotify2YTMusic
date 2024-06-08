from flask import Flask, request, render_template, redirect, session
from main import Spotify
from Constants import SPOTIPY_CLIENT_ID_CONSTANT, SPOTIPY_CLIENT_SECRET_CONSTANT

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
        return 'Selected playlists: ' + ', '.join(selected_playlists)
    else:
        playlists = spotify.get_playlists()
        return render_template('index.html', playlists=playlists['items'])

if __name__ == '__main__':
    app.run(port=8080)