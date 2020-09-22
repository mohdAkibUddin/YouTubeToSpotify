from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from youtube_dl import YoutubeDL


class YoutubeClient:
    def __init__(self):
        self.video_ids = []
        self.playlists = []
        self.playlist_id = ""
        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

        flow = InstalledAppFlow.from_client_secrets_file(
            "creds/client_secret.json",
            scopes
        )
        credentials = flow.run_console()

        self.youtube_client = build(
            "youtube",
            "v3",
            credentials=credentials
        )

    def get_playlists(self):
        request = self.youtube_client.playlists().list(
            part="id, snippet",
            mine=True,
            maxResults=50
        )
        response = request.execute()

        for playlist in response['items']:
            self.playlists.append(playlist)
        return self.playlists

    def select_playlist(self):
        playlists = self.playlists
        playlist_name_and_id = {}
        k = 0
        for playlist in playlists:
            v = [playlist['id'], playlist['snippet']['title']]
            playlist_name_and_id.update({k: v})
            print(k, v[1])
            k += 1
        preference = int(input("type the number corresponding to the playlist you want to copy: "))
        self.playlist_id = playlist_name_and_id[preference][0]
        return self.playlist_id

    def get_songs(self):
        request = self.youtube_client.playlistItems().list(
            part="id, snippet",
            playlistId=self.playlist_id,
            maxResults=50
        )
        response = request.execute()
        # pprint.pprint(response)
        total_songs = response["pageInfo"]["totalResults"]
        for i in range(total_songs):
            video_id = response["items"][i]["snippet"]["resourceId"]["videoId"]
            self.video_ids.append(video_id)
        return self.video_ids

    def get_tracks_artists(self):
        video_ids = self.video_ids
        tracks_artists = []
        counter = 0
        for video_id in video_ids:
            url = "https://www.youtube.com/watch?v=" + video_id
            video = YoutubeDL({'quiet': True}).extract_info(
                url,
                download=False,
            )
            if video['track'].__eq__("None"):
                print(
                    "https://www.youtube.com/watch?v=" + video_id + " IS NOT A SONG OR THE SONG INFORMATION IS NOT "
                                                                    "AVAILABLE")
                continue
            tracks_artists.append((video['track'], video['artist']))
            print(video['track'] + " by " + video['artist'] + " will be added!")
            counter += 1
        return tracks_artists
