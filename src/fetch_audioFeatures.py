import pandas as pd
from bs4 import BeautifulSoup
import requests
import argparse
import pprint
import sys
import os
import subprocess
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


cid ='c685ccf5f0aa4e4ab0ec16b51e52b223'
secret ='d4c8ad439f5045eb8ed870b0371aa360'

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

def get_playlist_audio_features(username, playlist_id, sp):
    offset = 0
    songs = []
    items = []
    ids = []
    while True:
        content = sp.user_playlist_tracks(username, playlist_id, fields=None, limit=100, offset=offset, market=None)
        songs += content['items']
        if content['next'] is not None:
            offset += 100
        else:
            break

    for i in songs:
        ids.append(i['track']['id'])

    index = 0
    audio_features = []
    while index < len(ids):
        audio_features += sp.audio_features(ids[index:index + 50])
        index += 50

    features_list = []
    for features in audio_features:
        features_list.append([features['energy'], features['liveness'],
                              features['tempo'], features['speechiness'],
                              features['acousticness'], features['instrumentalness'],
                              features['time_signature'], features['danceability'],
                              features['key'], features['duration_ms'],
                              features['loudness'], features['valence'],
                              features['mode'], features['type'],
                              features['uri']])

    df = pd.DataFrame(features_list, columns=['energy', 'liveness',
                                              'tempo', 'speechiness',
                                              'acousticness', 'instrumentalness',
                                              'time_signature', 'danceability',
                                              'key', 'duration_ms', 'loudness',
                                              'valence', 'mode', 'type', 'uri'])
    df.to_csv('{}-{}.csv'.format(username, playlist_id), index=False)

username = "unlikeanna"
playlist_uri = 'spotify:playlist:0NX7P6iRdI7nUABn1gh2Zl'
get_playlist_audio_features(username, playlist_uri, sp)
