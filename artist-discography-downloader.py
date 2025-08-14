import yt_dlp #Our searching/downloading tool
import time
import os
import requests
import re

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

#   Honestly, ChatGPT gave me this next function, I don't really know how to use yt-dlp
def searchURL(search_term):
    with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
        info = ydl.extract_info(f"ytsearch1:{search_term}", download=False)
        
        # Anti-error validation
        entries = info.get('entries', [])
        if not entries:
            print(f"No se encontraron resultados para: {search_term}")
            return None
        
        video_url = entries[0].get('webpage_url')
        # print("URL encontrada:", video_url)
        return video_url
    
def download_audio(url, output_folder, song):
    # Crear carpeta si no existe
    os.makedirs(output_folder, exist_ok=True)
    safe_song = sanitize_filename(song)
    
    # Opciones para descargar solo el audio en formato mp3
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_folder, f"{safe_song}.%(ext)s"),  # Nombre del archivo = título del video
        'nooverwrites': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',  # Cambia a 'wav', 'flac', etc. si lo prefieres
            'preferredquality': '192',  # Calidad en kbps
        }],
        'quiet': True  # Si quieres que muestre el progreso
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def get_desktop_path():
    # Detecta el escritorio del usuario actual
    return os.path.join(os.path.expanduser("~"), "Desktop")

def sanitize_filename(name):
    # Reemplaza cualquier carácter no permitido por guion bajo
    return re.sub(r'[\\/*?:"<>|]', '_', name)


artist_name = input("Artist's name: ")

results = search_artist(artist_name)
# print(results)

time.sleep(.5)
print("Fetching results...")
time.sleep(.5)
print("Validating...")
time.sleep(1)

start = time.time() #Marks the start time when the code executed. This is just for statistics, not part of the main code.

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

    for id in release_ids: #For each id (album)
        songs = search_songs(id[1]) #Retrieve all the songs of that album
        album_song_list.append([id[0], songs]) #Store the songs into a list which recieves the values: ([Album Name, [List of songs]])
        
    download_song_list = [] #Create the list with the names of the songs we're going to download (must have unique values)

    for i in global_list:
        if i[1] in ["Single"]: # Filter only Singles
            download_song_list.append(i[0]) #Add the name of the song to the download list

    for album_songs in album_song_list: #For each album existing on the list:

        if isinstance(album_songs[1], list): #Ask if the element we want to add is a list
            download_song_list.extend(album_songs[1]) #Flat the list because if not, we would store a list into another list, we want only the values inside the list
        else:
            download_song_list.append(album_songs[1]) #Store the element directly (Unuseful because, if not always, most of the time is going to be a list)




    # print("////////////////DEBUGGING////////////////")
    # print(f"Album Song List: {album_song_list}") #Debugging 
    # print(f"Global List: {global_list}") #Debugging 
    # print(f"Download song list total: {download_song_list}") #Debugging 

    download_song_list = list(dict.fromkeys(download_song_list)) #Eliminate duplicated values

    yt_url_list = []
    base_folder = os.path.join(get_desktop_path(), "Music")

    for song in download_song_list:
        search_term = artist_name+" "+song+" Official Audio"
        print(f"Buscando {search_term}")
        yt_url_list.append([song, searchURL(search_term)])

    # print(yt_url_list) # Debugging

    # Recorrer canciones y encontrar álbum + URL
    for song in download_song_list:
        # Buscar álbum
        for album, track_list in album_song_list:
            if song in track_list:
                # Buscar URL de la canción
                song_url = next((url for name, url in yt_url_list if name == song), None)
                if song_url:
                    print(f"Descargando '{song}' del álbum '{album}'...")
                    output_folder = os.path.join(base_folder, artist_name, album)
                    download_audio(song_url, output_folder, song)
                else:
                    print(f"No se encontró URL para '{song}'")
                break  # Ya encontramos el álbum, no seguir buscando
    

    # print(f"Download song list valores únicos: {download_song_list}") #Debugging 
    # print("////////////////DEBUGGING////////////////")

    #
    #   From here we start the part in which we need another kind of tools to download the video/audio from youtube.
    #   We could hardcode it by using an automation tool like Selenium for Chrome but let's use another people's code to simplify
    #   our lives.
    #

    end = time.time() #Marks the end time when the code finished executing. This is just for statistics, not part of the main code.
    
    print(f"Executing time: {end - start:.2f} segundos")

    answer = input("Is this your artist? Type YES or NO \n")

    if answer == "y":
        print("Congratulations! You've found your artist")
        break

    



    


    
