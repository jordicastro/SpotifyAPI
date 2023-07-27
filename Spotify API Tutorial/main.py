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
    token = json_result["access_token"] # parce token (stored in access token field)
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_artist(token, artist_name):
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

def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US" #Endpoint
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result



token = get_token()
# print(token) ## test whether token is generated correctly in get_token()
input_artist = input("Enter a Artist to view their top tracks! ")
result = search_artist(token, artist_name=input_artist)

# print(result) printing solely the artists and items fields as directed with ["artists"]["items"]  in method search_artist ln 42
print(f"{result['name']}'s top tracks:") # print solely the name!
artist_id = result["id"] ## get the artist id! 
# print(artist_id)
songs = get_songs_by_artist(token, artist_id)
# print(songs) #print the entire songs field (jibberish)

for idx, song in enumerate(songs): # enumerate function obtains the index of the value 'song' for each element in the songs list
    print(f"{idx + 1}. {song['name']}") # add one to the index (default is 0), print the id (1, 2, 3...) followed by the song's name at each index in the songs field

