########################################
#SpotifyAPI client credential          #
#Enhanced by Jordi Castro              #
######################################## s

from dotenv import load_dotenv # load local variables in .env file
import os
import base64
from requests import post, get # POST, GET requests
import json

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# print(client_id, client_secret) # check to see if load env is working

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8") # returns a base 64 object converted into a string use to send requests

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data) #POST

    # convert returned json object to python dictionary
    json_result = json.loads(result.content) #load from string
    token = json_result["access_token"] # parse token (stored in access token field)
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_artist(token, artist_name): # returns a json object of the artist which can then be used to get the artist's name and ID and other relevant information
    url = "https://api.spotify.com/v1/search" #Endpoint
    headers = get_auth_header(token)
    query = f"q={artist_name}&type=artist&limit=1" # python formatted string literal to interpolate {artist_name} into query. only grabbing one artist from spotify (top search). type could be artist, track, album, etc.

    query_url = url + "?" + query #formating of endpoint + query request
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"] #JSON FIELDS artists and items
    if len(json_result) == 0: #if length is equal to zero
        print("No artists with this name exists...")
        return None
    
    # print(json_result)
    return json_result[0]

def search_album(token, album_name): # returns a json object of an album which can then be used to get the album name and ID and other relevant information
    url = "https://api.spotify.com/v1/search" #Endpoint
    headers = get_auth_header(token)
    query = f"q={album_name}&type=album&limit=1"
    query_url = url + "?" + query
    result = get(query_url, headers=headers)
    
    json_result = json.loads(result.content)["albums"]["items"] 
    if len(json_result) == 0: 
        print("No album with this name exists...")
        return None

    return json_result[0]

def search_track(token, track_name): # returns a json object of an album which can then be used to get the album name and ID and other relevant information
    url = "https://api.spotify.com/v1/search" #Endpoint
    headers = get_auth_header(token)
    query = f"q={track_name}&type=track&limit=1"
    query_url = url + "?" + query
    result = get(query_url, headers=headers)
    
    json_result = json.loads(result.content)["tracks"]["items"] 
    if len(json_result) == 0: 
        print("No track with this name exists...")
        return None

    return json_result[0]


def artistTopTracksHelper(token, artist_id): # helper function, uses the artist ID and our token to send a GET request of the top tracks endpoint and return a json object.
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US" #Endpoint
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result

def artistTopTracks(): # 1. calls the search_artist to GET a json object. parses json obj to get artist name and artist_id. 2. uses artist_id to call helper function that GET artist's top tracks. returns a json object. Finally, a for loop parses through the json object to neatly print the top tracks.
    input_artist = input("\nEnter an artist to view their top tracks: ")
    result = search_artist(token, artist_name=input_artist)

    # print(result) printing solely the artists and items fields as directed with ["artists"]["items"]  in method search_artist ln 42
    print(f"\n{result['name']}'s top tracks:\n") # print solely the name!
    artist_id = result["id"] ## get the artist id! 
    # print(artist_id)
    songs = artistTopTracksHelper(token, artist_id)
    # print(songs) #print the entire songs field (jibberish)

    for idx, song in enumerate(songs): # enumerate function obtains the index of the value 'song' for each element in the songs list
        print(f"{idx + 1}. {song['name']}") # add one to the index (default is 0), print the id (1, 2, 3...) followed by the song's name at each index in the songs field
    
def artistAlbumsHelper(token, artist_id): # helper function, uses the artist ID and our token to send a GET request of the albums of the artist and returns a json object.
    url = f"https://api.spotify.com/v1/artists/{artist_id}/albums" #Endpoint
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["items"]
    return json_result

def artistAlbums(): # 1. similar to artistTopTracks, calls search_artist to GET artist name and artist_id. 2. calls helper function to GET artist's albums. finally, a for loop parses through the json object (albums) and prints albums, date, and other relevant information
    input_artist = input("\nEnter an artist to view their discography: ")
    result = search_artist(token, artist_name=input_artist)
    print(f"\n{result['name']}'s albums:\n")
    artist_id = result["id"]

    albums = artistAlbumsHelper(token, artist_id)
    for idx, album in enumerate(albums):
        print(f"{idx+1}. {album['name']} - {album['release_date']}")

def albumTracksHelper(token, album_id): # helper function, uses the album ID and our token to send a GET request of the tracks the album and returns a json object of the tracks.
    url = f"https://api.spotify.com/v1/albums/{album_id}/tracks" #Endpoint
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["items"]
    return json_result

def albumTracks(): # 1. slightly different from artistTopTracks and artistAlbums, calls search_album to GET an album json object -> album_id, album_name. 2. uses the album_id and our token to call helper function which returns json object of the album's tracks. finally, json object is parsed to neatly display the album's tracks.
    input_album = input("\nEnter an album to view its tracks: ")
    result = search_album(token, album_name=input_album)
    if result is None:
        return
    
    print(f"\n{result['name']} tracks:\n")
    album_id = result["id"]
    tracks = albumTracksHelper(token, album_id)

    for idx, track in enumerate(tracks):
        print(f"{idx+1}. {track['name']}")

def relatedArtistHelper(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/related-artists" #Endpoint
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["artists"]
    return json_result

def relatedArtist():
    input_artist = input("\nEnter a artist to view related artists: ")
    result = search_artist(token, artist_name=input_artist)
    print(f"\n{result['name']}'s related artists:\n")
    artist_id = result["id"]

    artists = relatedArtistHelper(token, artist_id)
    for artist in artists:
        print(f"{artist['name']}\n\tpopularity: {artist['popularity']}, Spotify URI: {artist['uri']}")

def newReleasesHelper():
    url = "https://api.spotify.com/v1/browse/new-releases" # no parameters in endpoint, therefore retrival of artist/album ID is unnecesary
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["albums"]["items"]
    return json_result

def newReleases():
    print("\nNew Releases:\n")
    releases = newReleasesHelper()

    for idx, release in enumerate(releases):
        print(f"{idx+1}. {release['name']} - {', '.join(artist['name'] for artist in release['artists'])}") # 'release' - '[for loop to extract artists in each release]'

def trackInfoHelper(token, track_id):
    url = f"https://api.spotify.com/v1/tracks/{track_id}" #Endpoint
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content) # no return ['albums'] or any specific field because we want the whole json object to display track name, album release date, and artist name, all in different fields of the json file.
    return json_result

def trackInfo():
    input_track = input("\nEnter a track for more information: ")
    result = search_track(token, track_name=input_track)
    track_id = result["id"]

    track = trackInfoHelper(token, track_id)
    print(f"Track Name: {track['name']}:")
    print(f"Artists: ")
    for artist in track['artists']:
        print(f"\t{artist['name']}")
    print(f"Release Date: {track['album']['release_date']}")
    print(f"Duration: {round(track['duration_ms'] / 1000)} seconds")


token = get_token() # START OF CODE! a new access token is generated at the start of each run
# print(token) ## test whether token is generated correctly in get_token()
choice = -1
while choice !='0':

    print("--------------------------------\nWelcome to the SpotifyAPI client\n--------------------------------\n")
    choice = input("1. View an artist's top tracks\n2. View an artist's albums\n3. View an album's tracks\n4. View related artists\n5. View new releases\n6. View information on a track\n0. Exit\n\n")

    if (choice == '1'):
        artistTopTracks()
    elif (choice == '2'):
        artistAlbums()
    elif (choice == '3'):
        albumTracks()
    elif (choice == '4'):
        relatedArtist()
    elif (choice == '5'):
        newReleases()
    elif (choice == '6'):
        trackInfo()
    print("\n")



