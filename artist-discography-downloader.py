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
    time.sleep(2)
    print(f"INICIANDO BUSQUEDA DE RELEASES PARA EL ALBUM {album_name}")
    url= "https://musicbrainz.org/ws/2/release/"
    params ={
        "artist": artist_id,
        "release": album_name,
        "fmt": "json",
        "limit": limit
    }
    print(f"PARAMS ENVIADOS: {params}")
    response = requests.get(url, params=params, headers=HEADERS)
    response.raise_for_status()  # Lanza error si la respuesta no es 200
    data = response.json()
    return data.get("releases", [])

def search_albums(artist_id, limit=100):
    time.sleep(2)
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
    print(f"- {artist['name']} (MBID: {artist['id']}) Score: {artist['score']} Life-span: {begin} Type: {artist['type']}")

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

    print(album_name_list) #Debugging

    #-----------------------------ARREGLAR----------------------------- 
    release_ids = []
    
    for album_name in album_name_list:
        print(f"Item actual: {album_name}")
        print(f"Llamando función buscar para item: {album_name}")
        releases = search_releases(artist_id, album_name)
        print(releases)
        print("///////////////////////////////")
    
        # releases = search_releases(artist_id, album_name)
        
        # print(releases)
    
    #-----------------------------ARREGLAR----------------------------- 

    if album_song_list:
        print(album_song_list)
    else:
        print("No se encontraron canciones para el álbum")

    answer = input("Is this your artist? Type YES or NO \n")

    if answer == "y":
        print("Congratulations! You've found your artist")
        break

    



    


    
