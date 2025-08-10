import time
import os
import requests

HEADERS = {
    "User-Agent": "artist-discography-downloader/1.0 ( rodrigo@example.com )" #Cambiar correo a alguno real
}

def search_artist(artist_name):
    time.sleep(2)
    url = "https://musicbrainz.org/ws/2/artist/"
    params = {
        "query": artist_name,
        "fmt": "json"  # Respuesta en JSON
    }
    response = requests.get(url, params=params, headers=HEADERS)
    response.raise_for_status()  # Lanza error si la respuesta no es 200
    data = response.json()
    return data.get("artists", [])

def search_releases(artist_id, album_name, limit=10):
    time.sleep(1)
    url= "https://musicbrainz.org/ws/2/release/"
    params ={
        "query": f'arid:{artist_id} AND release:"{album_name}"', #Forzamos la búsqueda a través de un query para encontrar coincidencias exactas
        "fmt": "json",
        "limit": limit
    }
    response = requests.get(url, params=params, headers=HEADERS)
    response.raise_for_status()  # Lanza error si la respuesta no es 200
    data = response.json()
    return data.get("releases", [])

def search_songs(release_id):
    time.sleep(1)
    url= f"https://musicbrainz.org/ws/2/release/{release_id}" #URL must contain the ID of the album
    params ={
        "inc": "recordings",
        "fmt": "json",
    }
    response = requests.get(url, params=params, headers=HEADERS)
    response.raise_for_status()  # Lanza error si la respuesta no es 200
    data = response.json()
    tracks = []
    for medium in data.get("media", []):
        for track in medium.get("tracks", []):
            track_title = track.get("title")
            if track_title:
                tracks.append(track_title)
    
    return tracks

def search_albums(artist_id, limit=100):
    time.sleep(1)
    url= "https://musicbrainz.org/ws/2/release-group/"
    params ={
        "artist": artist_id,
        "fmt": "json",
        "limit": limit,
        "type": "album|ep|single"
    }
    response = requests.get(url, params=params, headers=HEADERS)
    response.raise_for_status()  # Lanza error si la respuesta no es 200
    data = response.json()
    return data.get("release-groups", [])

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
    # print(f"- {artist['name']} (MBID: {artist['id']}) Score: {artist['score']} Life-span: {begin} Type: {artist['type']}")
    print(f"-Name: {artist['name']} // Life-span: {begin} // Type: {artist['type']}")

    albums = search_albums(artist_id)

    # print(songs)
    # if songs:
    #     for song in songs:
    #         print(f"- Song: {song['title']} ID: {song['id']}")
    # else:
    #     print("This artist doesn't have any songs")
    
    global_list = []
    album_name_list = []
    album_song_list = []

    if albums:
        for album in albums: # For each album existing in the response:
            type = album.get('primary-type')
            if (type in ["Album","EP","Single"]) and (album.get('secondary-types') == []): #Filter only Albums, EPs and Singles
            # print(f"- Album: {album['title']} ID: {album['id']}")
                print(f"- {type}: {album['title']}")
                global_list.append([album['title'], type]) #Add the name of the release and its type to a global list
    else:
        print("This artist doesn't have any albums")

    for i in global_list: #For each item in global list
        if i[1] in ["Album", "EP"]: # Filter only Albums and EPs
            album_name_list.append(i[0]) #Add the name of the Album/EP to a list

    print(f"Algunos álbumes del artista: {album_name_list}") #Debugging

    release_ids = []
    
    for album_name in album_name_list:
        releases = search_releases(artist_id, album_name)

        release_id = None
        if releases:
            for release in releases:
                primary_type = release.get("release-group", {}).get("primary-type", "")
                # track_count = str_to_int(release.get("track-count", ""))
                track_count = release.get("track-count", "")
                if (primary_type in ["Album","EP"]) and track_count <=30:
                    release_id = release.get('id')
                    release_ids.append([album_name, release_id])
                    # print(f"ID encontrado para {album_name}: {release_id}") #Debugging 
                    break
        else:
            print(f"No se encontró un release_id para: {album_name}")
    
    # print(release_ids) #Debugging

    for id in release_ids:
        songs = search_songs(id[1])
        album_song_list.append([id[0], songs])

    print(album_song_list) #Debugging 
        



    # if album_song_list:
    #     print(album_song_list)
    # else:
    #     print("No se encontraron canciones para el álbum")

    answer = input("Is this your artist? Type YES or NO \n")

    if answer == "y":
        print("Congratulations! You've found your artist")
        break

    



    


    
