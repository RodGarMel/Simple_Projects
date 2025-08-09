import time
import os
import requests

HEADERS = {
    "User-Agent": "artist-discography-downloader/1.0 ( rodrigo@example.com )" #Cambiar correo a alguno real
}

def search_artist(artist_name):
    url = "https://musicbrainz.org/ws/2/artist/"
    params = {
        "query": artist_name,
        "fmt": "json"  # Respuesta en JSON
    }
    response = requests.get(url, params=params, headers=HEADERS)
    response.raise_for_status()  # Lanza error si la respuesta no es 200
    data = response.json()
    return data.get("artists", [])

def search_songs(artist_id, limit=100):
    url= "https://musicbrainz.org/ws/2/recording/"
    params ={
        "artist": artist_id,
        "fmt": "json",
        "limit": limit
    }
    response = requests.get(url, params=params, headers=HEADERS)
    response.raise_for_status()  # Lanza error si la respuesta no es 200
    data = response.json()
    return data.get("recordings", [])

def search_albums(artist_id, limit=10):
    url= "https://musicbrainz.org/ws/2/release/"
    params ={
        "artist": artist_id,
        "fmt": "json",
        "limit": limit
    }
    response = requests.get(url, params=params, headers=HEADERS)
    response.raise_for_status()  # Lanza error si la respuesta no es 200
    data = response.json()
    return data.get("releases", [])

artist_name = input("Artist's name:")

results = search_artist(artist_name)
# print(results)

time.sleep(.5)
print("Fetching results...")
time.sleep(.5)
print("Validating...")
time.sleep(1)

for artist in results:
    lifespan = artist.get('life-span', {})
    begin = lifespan.get('begin', '???')
    artist_id = artist.get('id')
    print(f"- {artist['name']} (MBID: {artist['id']}) Score: {artist['score']} Life-span: {begin} Type: {artist['type']}")

    songs = search_songs(artist_id)
    albums = search_albums(artist_id)

    # print(songs)
    if songs:
        for song in songs:
            print(f"- Song: {song['title']} ID: {song['id']}")
    else:
        print("This artist doesn't have any songs")
    
    if albums:
        for album in albums:
            print(f"- Album: {album['title']} ID: {album['id']}")
    else:
        print("This artist doesn't have any albums")


    answer = input("Is this your artist? Type YES or NO \n")

    if answer == "YES":
        print("Congratulations! You've found your artist")
        break

    



    


    
