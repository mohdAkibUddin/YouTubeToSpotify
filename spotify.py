import requests
from base64 import b64encode
from urllib import parse


class SpotifyClient:

    def __init__(self):
        f = open('creds/spotify_creds.txt', 'r')
        lines = f.read().splitlines()
        list_lines = []
        for line in lines:
            list_lines.append(line)

        self.client_id = list_lines[0]
        self.client_secret = list_lines[1]
        self.redirect_uri = list_lines[2]
        self.token_url = "https://accounts.spotify.com/api/token"
        self.playlist_ids = []
        self.playlist_id, self.access_token, self.user_id, self.user_id, self.song, self.id = "", "", "", "", "", ""
        self.playlist_json = {}

    def get_client_creds(self):
        client_creds = self.client_id + ":" + self.client_secret
        client_creds_b64encoded = b64encode(client_creds.encode()).decode()
        return client_creds_b64encoded

    def get_code(self):
        url = "https://accounts.spotify.com/authorize"
        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": self.redirect_uri,
            "scope": "playlist-modify-public%20playlist-modify-private"
        }
        r = requests.get(url, params=params)
        print(r.url)
        code = input("Look up at the URL after opening this link. Copy and paste everything after ..code =")
        return code

    def get_token_header(self):
        token_header = {
            "Authorization": f"Basic {self.get_client_creds()}"
        }
        return token_header

    def get_token_data(self):
        token_data = {
            "grant_type": "authorization_code",
            "code": self.get_code(),
            "redirect_uri": self.redirect_uri
        }
        return token_data

    def get_access_token(self):
        r = requests.post(self.token_url, data=self.get_token_data(), headers=self.get_token_header())
        self.access_token = r.json()['access_token']
        return self.access_token

    def get_spotify(self):
        url = "https://api.spotify.com/v1/me"
        header = {
            "Authorization": f"Bearer {self.access_token}"
        }
        r = requests.get(url, headers=header)
        return r.json()

    def get_user_id(self):
        header = {
            "Authorization": f"Bearer {self.access_token}"
        }
        self.id = requests.get("https://api.spotify.com/v1/me", headers=header).json()['id']
        return self.id

    def search_song(self, track, artist):
        url = "https://api.spotify.com/v1/search?q="
        search = parse.quote(f'{track} {artist}')
        url = url + search + "&type=track"
        headers = {
            "content_type": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        }
        r = requests.get(url, headers=headers)
        r_json = r.json()
        self.song = r_json["tracks"]["items"][0]["uri"]
        return self.song

    def get_playlists(self):
        header = {
            "Authorization": f"Bearer {self.access_token}"
        }
        self.playlist_json = requests.get("https://api.spotify.com/v1/me/playlists", headers=header).json()
        total = int(self.playlist_json['total'])
        for i in range(total):
            self.playlist_ids.append(self.playlist_json['items'][i]['id'])
        return self.playlist_ids

    def select_playlist(self):
        playlist_json = self.playlist_json
        playlist_ids = self.playlist_ids
        total = len(playlist_ids)
        for i in range(0, total):
            playlist_ids.append(playlist_json['items'][i]['name'])
            print(i, playlist_json['items'][i]['name'])
        preference = int(input("type the number to the corresponding Spotify playlist"))
        self.playlist_id = playlist_ids[preference]
        return self.playlist_id

    def add_to_existing_playlist(self):
        song = self.song
        song = song.encode()
        playlist_id = self.playlist_id
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        params = {
            "uris": song
        }
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        r = requests.post(url, headers=headers, params=params)
        return r.json()

    def create_playlist(self):
        user_id = self.id
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        playlist_name = input("Type a name for your new spotify playlist. Be careful not to reuse names: ")
        json = {
            "name": playlist_name
        }
        url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
        r = requests.post(url, headers=headers, json=json)
        return r.json()
