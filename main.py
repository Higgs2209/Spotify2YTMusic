from flask import Flask, request, render_template_string, redirect, render_template
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from Constants import SPOTIPY_CLIENT_ID_CONSTANT, SPOTIPY_CLIENT_SECRET_CONSTANT
from ytmusicapi import YTMusic

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
                                         redirect_uri='http://localhost:8080/spotify/callback',
                                         scope=self.scope,
                                         cache_path="token_info.json")
        self.sp = spotipy.Spotify(auth_manager=self.auth_manager)

    def authenticate(self):
        if not self.auth_manager.get_cached_token():
            return self.auth_manager.get_authorize_url()
        else:
            return None

    def get_playlists(self):
        return self.sp.current_user_playlists()

    def get_playlist(self, playlist_id):
        return self.sp.playlist(playlist_id)

    def get_playlist_tracks(self, playlist_id):
        results = self.sp.playlist_items(playlist_id)
        tracks = results['items']
        while results['next']:
            results = self.sp.next(results)
            tracks.extend(results['items'])
        return tracks
    def add_songs_to_playlist(self, playlist_name, songs):
        # TODO: Implement this method
        pass



class YoutubeMusic(MusicPlatform):
    def __init__(self, headers_auth_file):
        self.ytmusic = YTMusic(headers_auth_file)

    def create_playlist(self, title, description='', privacy_status='PRIVATE'):
        playlist_id = self.ytmusic.create_playlist(title, description, privacy_status)
        return playlist_id

    def add_songs_to_playlist(self, playlist_id, songs):
        self.ytmusic.add_playlist_items(playlist_id, songs)