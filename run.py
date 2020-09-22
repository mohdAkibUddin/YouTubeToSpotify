from youtube import YoutubeClient
from spotify import SpotifyClient


def run():
    youtube_client = YoutubeClient()
    youtube_client.get_playlists()
    youtube_client.select_playlist()
    youtube_client.get_songs()
    tracks_artists = youtube_client.get_tracks_artists()
    print(tracks_artists)

    spotify_client = SpotifyClient()
    spotify_client.get_access_token()
    print("")
    new_question = input("IF YOU WANT TO ADD YOUR SONGS TO AN EXISTING PLAYLIST HIT ENTER. IF NOT TYPE NEW ")
    print("")
    if 'n' in new_question.lower():
        spotify_client.get_user_id()
        spotify_client.create_playlist()
    spotify_client.get_playlists()
    spotify_client.select_playlist()

    for track_artist in tracks_artists:
        spotify_client.search_song(*track_artist)
        spotify_client.add_to_existing_playlist()


if __name__ == "__main__":
    run()
