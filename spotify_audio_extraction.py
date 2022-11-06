import urllib
import spotipy
import sys
import pandas as pd
import json
import os

path_main = r''
# Bringing to path
sys.path.insert(0, f'{path_main}')
from retriever import token_scope # Created in my Spotify repository 

path_json = path_main + r'\MyData\YourLibrary.json'

# # Loading My liked songs 
def trackID_and_artist(liked_songs_json):
    with open(f'{liked_songs_json}', 'r') as file:
        library = json.load(file)

    library_df = pd.DataFrame(library['tracks'])
    library_uri = library_df['uri'].to_list()
    uri_id = [library_uri[i][14:] for i in range(len(library_uri))]
    library_artist = library_df['artist'].to_list()
    return dict(zip(uri_id, library_artist))


# Search through the artist and replace with their id
# Join id with popularity 
# Pick id with highest popularity and the name equals the name of the search
def artistID_and_trackID(liked_songs_json):
    dictionary = trackID_and_artist(liked_songs_json)
    spotify = spotipy.Spotify(auth=token_scope())
    for track, arts in dictionary.items():
        popularity_id = {}
        error = []
        artist = spotify.search(f'{arts}', type='artist') # returns a dictionary
        for art in artist['artists']['items']:
            if art['name'].lower() == arts.lower():
                popularity_id[f'{art["popularity"]}'] = art['id']
        try:
            dictionary[track] = popularity_id[max(list(popularity_id.keys()))]
        except ValueError as e:
            print(e)
            error.append(arts)

    with open("artistID_and_trackID.json", "w") as outfile:
        json.dump(dictionary, outfile)

    return dictionary

# Retrieving urls
def tracks_urls(artist_id_and_track_id, liked_songs_metadata):
    with open(artist_id_and_track_id) as file:
        artist_and_track = json.load(file)
    spotify = spotipy.Spotify(auth=token_scope())
    for track, art in artist_and_track.items():
        preview = spotify.track(track)
        artist_and_track[track] = preview['preview_url']

    meta = pd.read_csv(liked_songs_metadata)
    meta = meta.set_index('id')
    urls = pd.DataFrame(list(artist_and_track.values()), index=[list(artist_and_track.keys())])
    urls = urls.reset_index()
    urls.columns = ['id', 'preview_url']
    urls = urls.set_index('id')
    meta_urls = pd.concat([meta, urls], axis=1)
    meta_urls = meta_urls[['artist', 'track', 'preview_url']]
    meta_urls = meta_urls.reset_index()
    meta_urls = meta_urls.drop('id', axis=1)
    meta_urls["track_artist"] = meta_urls[["track", "artist"]].apply(lambda x: "_".join(x), axis =1)
    meta_urls = meta_urls[['track_artist', 'preview_url']]
    meta_dict = pd.DataFrame.to_dict(meta_urls)
    meta_tr = list(meta_dict['track_artist'].values())
    meta_url = list(meta_dict['preview_url'].values())
    with open('urls.json', 'w') as out:
        json.dump(urls, out, indent=4)
    return dict(zip(meta_tr, meta_url))

def extract_audio(preview_url):
    with open(preview_url, 'r') as file:
        urls = json.load(file)
    error = []
    for track_art, url in urls.items():
        if os.path.exists('Spotify_previews') is False:
            os.mkdir('Spotify_previews') 
            
            try:
                url_retrieved = urllib.request.urlretrieve(url, f'Spotify_previews\{track_art}.wav')
            except TypeError as e:
                error.append(track_art)
                print(e)
            except OSError:
                track_art = track_art.split('/')
                track_art = ' '.join(track_art).strip(' ')
                url_retrieved = urllib.request.urlretrieve(url, f'Spotify_previews\{track_art}.wav')
        elif os.path.exists('Spotify_previews' + f'\{track_art}') is False:
            try:
                url_retrieved = urllib.request.urlretrieve(url, f'Spotify_previews\{track_art}.wav')
            except TypeError as e:
                error.append(track_art)
                print(e)
            except OSError:
                error.append(track_art)
                # track_art = track_art.split('/')
                # track_art = ' '.join(track_art).strip(' ')
                # url_retrieved = urllib.request.urlretrieve(url, f'Spotify_previews\{track_art}.wav')
        print(error)

if __name__ == '__main__':
    extract_audio('urls.json')
                