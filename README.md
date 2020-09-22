Hi! Glad you're looking at my project! 


Project Purpose: 

To take our YouTube playlist and co it over to Spotify



APIs used:

YouTube Data API v3 
Spotify Web API



Instructions:

Generate an OAuth 2.0 Client ID to use the YouTube Data API.
https://console.developers.google.com/apis/library/youtube.googleapis.com (Go here to enable the API)
https://console.developers.google.com/apis/credentials (Generate the Client ID here) 
Download the JSON for the Client ID
Name the JSON "client_secret.json" and save it in the "creds" folder

Generate a Client Credentials for the Spotify Web API
https://developer.spotify.com/dashboard/ (Go here to generate the credentials)
After generating credentials (creating app) select edit settings
For the Redirect URIs you can use any URI. For example: https://www.wikipedia.org/ will work so copy 
and paste that in
Navigate to the creds folder. There is file named "spotify_creds.txt" open it and follow the 3 copy paste instructions

There is a problem with the youtube_DL library right now so you're gonna have to go in and patch it after installing the requirmenents navigate into youtube_dl/extractor/youtube.py go to line 2338 and replace whatever is there with this r'"title":\s*{\s*"simpleText":\s*"%s"\s*},\s*"contents":\s*\[\s*{\s*(?:"runs":\s*\[\s*{\s*"text"|"simpleText"):\s*"([^"]+)"' % field,
