import numpy as np
import pandas as pd
import streamlit as st
import time
import spotipy
from getpass import getpass
from spotipy.oauth2 import SpotifyClientCredentials
from os import getcwd

client_id = "a944f2f3b9644e9888ce87e6a1b13e56"
client_secret = "644b210bd7dd4e348be8e7bed0e0babd"

client_credentials = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)

sp = spotipy.Spotify(client_credentials_manager = client_credentials)

st.title("Spotify Artist Data Collection App")

name = st.text_input("What is the name of the artist: ")

result = sp.search(name)

# Extracting Spotify Albums

artist_uri = result['tracks']['items'][0]['artists'][0]['uri']

sp_albums = sp.artist_albums(artist_uri, album_type='album')

album_names = []
album_uris = []

for i in range(len(sp_albums['items'])):
    album_names.append(sp_albums['items'][i]['name'])
    album_uris.append(sp_albums['items'][i]['uri'])

# Grabbing the Songs from Each Album

def albumSongs(uri):
    album = uri

    spotify_albums[album] = {}

    spotify_albums[album]['album'] = []
    spotify_albums[album]['track_number'] = []
    spotify_albums[album]['id'] = []
    spotify_albums[album]['name'] = []
    spotify_albums[album]['uri'] = []

    tracks = sp.album_tracks(album)

    for n in range(len(tracks['items'])):
        spotify_albums[album]['album'].append(album_names[album_count])
        spotify_albums[album]['track_number'].append(tracks['items'][n]['track_number'])
        spotify_albums[album]['id'].append(tracks['items'][n]['id'])
        spotify_albums[album]['name'].append(tracks['items'][n]['name'])
        spotify_albums[album]['uri'].append(tracks['items'][n]['uri'])


spotify_albums = {}

album_count = 0

for i in album_uris:
    albumSongs(i)
    st.write(f"Album {album_names[album_count]} songs have been added to the Spotify Albums Dictionary")
    album_count += 1


st.write(spotify_albums)

# Extracting Audio Features for Each Song

def audio_features(album):
    spotify_albums[album]['acousticness'] = []
    spotify_albums[album]['danceability'] = []
    spotify_albums[album]['energy'] = []
    spotify_albums[album]['instrumentalness'] = []
    spotify_albums[album]['liveness'] = []
    spotify_albums[album]['loudness'] = []
    spotify_albums[album]['speechiness'] = []
    spotify_albums[album]['tempo'] = []
    spotify_albums[album]['valence'] = []
    spotify_albums[album]['popularity'] = []

    track_count = 0

    for track in spotify_albums[album]['uri']:
        # Get the Features
        features = sp.audio_features(track)
        spotify_albums[album]['acousticness'].append(features[0]['acousticness'])
        spotify_albums[album]['danceability'].append(features[0]['danceability'])
        spotify_albums[album]['energy'].append(features[0]['energy'])
        spotify_albums[album]['instrumentalness'].append(features[0]['instrumentalness'])
        spotify_albums[album]['liveness'].append(features[0]['liveness'])
        spotify_albums[album]['loudness'].append(features[0]['loudness'])
        spotify_albums[album]['speechiness'].append(features[0]['speechiness'])
        spotify_albums[album]['tempo'].append(features[0]['tempo'])
        spotify_albums[album]['valence'].append(features[0]['valence'])

        # Getting the Popularity Feature
        pop = sp.track(track)
        spotify_albums[album]['popularity'].append(pop['popularity'])
        track_count += 1

sleep_min = 2
sleep_max = 5
start_time = time.time()
request_count = 0

for i in spotify_albums:
    audio_features(i)
    request_count += 1
    if request_count % 5 == 0:
        # st.write(f"{request_count} playlists completed")
        time.sleep(np.random.uniform(sleep_min, sleep_max))
        # st.write(f"Loop #: {request_count}")
        # st.write(f"Elapsed Time: {time.time() - start_time} seconds")

# Saving Results to a CSV File

song_df = {}

song_df['album'] = []
song_df['track_number'] = []
song_df['id'] = []
song_df['name'] = []
song_df['uri'] = []
song_df['acousticness'] = []
song_df['danceability'] = []
song_df['energy'] = []
song_df['instrumentalness'] = []
song_df['liveness'] = []
song_df['loudness'] = []
song_df['speechiness'] = []
song_df['tempo'] = []
song_df['valence'] = []
song_df['popularity'] = []

for album in spotify_albums:
    for feature in spotify_albums[album]:
        song_df[feature].extend(spotify_albums[album][feature])

df = pd.DataFrame.from_dict(song_df)

final_df = df.sort_values('popularity', ascending=False).drop_duplicates('name').sort_index()

st.write(final_df.head())

data_path = getcwd() + "/data"

final_df.to_csv(f"{data_path}/{name}.csv", index=False)

st.write("Data generated!")
