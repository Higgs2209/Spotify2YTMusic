from flask import Flask, request, render_template_string, redirect, render_template
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from Constants import SPOTIPY_CLIENT_ID_CONSTANT, SPOTIPY_CLIENT_SECRET_CONSTANT


class MusicPlatform:
    def __init__(self, client_id, client_secret, redirect_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

    def authenticate(self):
        pass

    def get_liked_songs(self):
        pass

    def get_playlists(self):
        pass

    def add_songs_to_playlist(self, playlist_name, songs):
        pass


class Spotify(MusicPlatform):
    def __init__(self, client_id, client_secret, redirect_uri):
        super().__init__(client_id, client_secret, redirect_uri)
        self.scope = "playlist-read-private,user-library-read"
        self.auth_manager = SpotifyOAuth(client_id=self.client_id,
                                         client_secret=self.client_secret,
                                         redirect_uri=self.redirect_uri,
                                         scope=self.scope,
                                         cache_path="token_info.json")
        self.sp = spotipy.Spotify(auth_manager=self.auth_manager)

    def authenticate(self):
        if not self.auth_manager.get_cached_token():
            auth_url = self.auth_manager.get_authorize_url()
            return redirect(auth_url)
        else:
            return None

    def get_liked_songs(self):
        return self.sp.current_user_saved_tracks()

    def get_playlists(self):
        user = self.sp.current_user()
        return self.sp.user_playlists(user['id'])

    def add_songs_to_playlist(self, playlist_name, songs):
        # TODO: Implement this method
        pass

class YoutubeMusic(MusicPlatform):
    def __init__(self, client_id, client_secret, redirect_uri):
        super().__init__(client_id, client_secret, redirect_uri)

    def authenticate(self):
        pass

    def get_liked_songs(self):
        pass

    def get_playlists(self):
        pass

    def add_songs_to_playlist(self, playlist_name, songs):
        pass

