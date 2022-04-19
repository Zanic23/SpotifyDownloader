import spotipy
from spotipy.oauth2 import SpotifyOAuth
from difflib import SequenceMatcher
from pytube import Search, YouTube
import os, sys

spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="YOUR CLIENT ID HERE",
                                               client_secret="YOUR CLIENT SECRET HERE",
                                               redirect_uri="ADD REDIRECT URI IN SPOTIFY DASHBOARD AND PASTE LINK HERE",
                                               scope="user-library-read"))

def guess_playlist(playlists, query):
    correlation = 0
    guess = None
    for playlist in playlists["items"]:
        curr_correlation = SequenceMatcher(None, playlist["name"], query).ratio()
        if curr_correlation > 0.6 and curr_correlation > correlation:
            guess = playlist
            correlation = curr_correlation
    return guess

def prompt_playlist():
    playlists = spotify.current_user_playlists()
    while True:
        print("\nPlease input playlist you would like to download:")
        user_input = input()
        playlist = guess_playlist(playlists, user_input)
        if playlist is None:
            print("Unable to find playlist. Make sure the playlist is public on your profile.")
        else:
            print(f"Did you mean to download playlist (y/n): {playlist['name']}?")
            res = input()
            if res == "y":
                return playlist
            elif res == "n":
                continue

def get_playlist_songs(playlist):
    songs = []
    for track in spotify.playlist_items(playlist["id"])["items"]:
        songs.append(f"{track['track']['name']} by {track['track']['album']['artists'][0]['name']}")
    return songs

def download_song(dir, name):
    try:
        search_results = Search(f"{name} song").results
        video = YouTube(search_results[0].watch_url)
        stream = video.streams.filter(only_audio=True, file_extension="mp4").first()
        stream.download(dir, filename = f"{name}.mp4")
    except e:
        print(f"Unable to download {name}. Sorry.")

def main():
    playlist = prompt_playlist()
    dir_path = os.path.dirname(sys.argv[0]) + f"/{playlist['name']}/"

    print(f"Chosen playlist to download: {playlist['name']}")
    print(f'Downloading to: {dir_path}')
    songs = get_playlist_songs(playlist)
    for song in songs:
        download_song(dir_path, song)
    print('Finished Downloading')

if __name__ == "__main__":
    main()
