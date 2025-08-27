import yt_dlp               #Our searching/downloading tool
import time                 
import os
import requests
import re                   #For sanitizing filenames
import unicodedata          #For normalizing strings

HEADERS = {
    "User-Agent": "artist-discography-downloader/1.0 ( rodrigo@example.com )" #Change to a real email
}

def search_artist(artist_name):
    time.sleep(2)
    url = "https://musicbrainz.org/ws/2/artist/"
    params = {
        "query": artist_name,
        "fmt": "json"  #Answer in JSON
    }
    response = requests.get(url, params=params, headers=HEADERS)
    response.raise_for_status()  #Error if response is not 200
    data = response.json()
    return data.get("artists", [])

def search_releases(artist_id, album_name, limit=50):
    time.sleep(1)
    url= "https://musicbrainz.org/ws/2/release/"
    params ={
        "query": f'arid:{artist_id} AND release:"{album_name}"', #Force the search through a query to look for exact coincidences
        "fmt": "json",
        "limit": limit
    }
    response = requests.get(url, params=params, headers=HEADERS)
    response.raise_for_status()  #Error if response is not 200
    data = response.json()
    releases = data.get("releases", [])
    releases = [r for r in releases if r.get("status") == "Official"] #Filter only official releases
    releases = sorted( #We sort the results by track count
        releases,
        key=lambda r: r.get("track-count", float('inf')) #Extract the number of tracks from a release or assign as infinite if there's no track count
    )

    return releases

def search_songs(release_id):
    time.sleep(1)
    url= f"https://musicbrainz.org/ws/2/release/{release_id}" #URL must contain the ID of the album
    params ={
        "inc": "recordings",
        "fmt": "json",
    }
    response = requests.get(url, params=params, headers=HEADERS)
    response.raise_for_status()  #Error if response is not 200
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
    response.raise_for_status()  #Error if response is not 200
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
        return video_url
    
def download_audio(url, output_folder, song):
    #Create a folder if it doesnt exist
    os.makedirs(output_folder, exist_ok=True)
    safe_song = sanitize_filename(song)
    
    #Options for downloading only mp3 format
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
    #Detects the desktop path of the user
    return os.path.join(os.path.expanduser("~"), "Desktop")

def sanitize_filename(name):
    #Replaces special characters for an underscore
    return re.sub(r'[\\/*?:"<>|]', '_', name)

def normalize(string):
    #Helps to homologate strings for better comparison and purgation
    string = unicodedata.normalize("NFD", string) 
    string = "".join(c for c in string if unicodedata.category(c) != "Mn")
    return string.lower().strip()

artist_name = input("Artist's name: ")

results = search_artist(artist_name)

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
    area = artist.get('area', {})
    origin = area.get('name', 'Unknown')
    print(f"Name: {artist['name']} // Life-span: {begin} // Type: {artist['type']} // Origin or Area: {origin}")

    albums = search_albums(artist_id)
    
    global_list = []
    album_name_list = []
    album_song_list = []

    if albums:
        for album in albums: # For each album existing in the response:
            type = album.get('primary-type')
            if (type in ["Album","EP","Single"]) and (album.get('secondary-types') == [] or album.get('secondary-types') == ["Remix"]): #Filter only Albums, EPs and Singles
                print(f"- {type}: {album['title']}")
                global_list.append([album['title'], type]) #Add the name of the release and its type to a global list
    else:
        print("This artist doesn't have any albums")

    for i in global_list: #For each item in global list
        if i[1] in ["Album", "EP"]: # Filter only Albums and EPs
            album_name_list.append(i[0]) #Add the name of the Album/EP to a list

    print(f"Some albums from the artist: {album_name_list}") #Debugging

    release_ids = []
    
    #Here we should have the logic of choosing an artist
    answer = input("Is this your artist? Type YES or NO \n") #The tool user is able to identify the artist before searching and downloading songs

    if answer == normalize("Yes") or normalize("Y"):
        print("Congratulations! You've found your artist. Initializing...")

        for album_name in album_name_list:
            releases = search_releases(artist_id, album_name)

            release_id = None
            if releases:
                for release in releases:
                    primary_type = release.get("release-group", {}).get("primary-type", "")
                    track_count = release.get("track-count", "")

                    #Format Type Logic
                    media_list = release.get("media", []) #Media is a list, so first we need to retrieve the list
                    if media_list: 
                        format_type = media_list[0].get("format", "") #Retrieve the format type from that result
                    else:
                        format_type = ""

                    #Filter by album or ep which is a CD or HDCD and its track count is <30
                    if (primary_type in ["Album","EP"]) and (format_type in ["CD","HDCD", "Digital Media"]) and (track_count <=30):
                        release_id = release.get('id')
                        release_ids.append([album_name, release_id, format_type])
                        print(f"Found ID for {album_name}: {release_id}") #Debugging 
                        break
            else:
                print(f"release_id not found for: {album_name}")
        

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
        
        #Eliminate duplicated values by using comparation in an normalized environment
        seen = set()
        unique_list = []
        for song in download_song_list:
            key = normalize(song)
            if key not in seen:
                seen.add(key)
                unique_list.append(song)
        download_song_list = unique_list

        #   From here we start the part in which we need another kind of tools to download the video/audio from youtube.
        #   We could hardcode it by using an automation tool like Selenium for Chrome but let's use another people's code to simplify
        #   our lives.

        yt_url_list = []
        base_folder = os.path.join(get_desktop_path(), "Music")

        for song in download_song_list:
            search_term = artist_name+" "+song+" Official Audio"
            print(f"Searching {search_term}")
            yt_url_list.append([song, searchURL(search_term)])

        downloaded_songs = []

        #For optimization, before comparation we normalize the list of strings inside the list and we compare only normalized ones instead of calling the function 'normalize' every time the cycle runs and a comparation is made
        normalized_album_song_list = [
            (album_name, {normalize(song) for song in songs})
            for album_name, songs in album_song_list
        ]

        #Iterate through songs and find its respective album + URL
        for song in download_song_list:
            #Search for its album
            found = False
            for album, normalized_track in normalized_album_song_list:
                if normalize(song) in normalized_track: #Cant use normalize(track_list) directly in the comparation because of lack of optimization
                    #Search for its URL
                    song_url = next((url for name, url in yt_url_list if name == song), None)
                    if song_url:
                        print(f"Downloading '{song}' from album '{album}'...")
                        output_folder = os.path.join(base_folder, artist_name, album)
                        download_audio(song_url, output_folder, song)
                        downloaded_songs.append(song) #Debugging
                        found = True
                    else:
                        print(f"URL not found for '{song}'")
                    break  #Album found, we stop searching

            #If the song is not from any album goes to "Singles"
            if not found:
                song_url = next((url for name, url in yt_url_list if name == song), None)
                if song_url:
                    print(f"Downloading '{song}' as Single...")
                    output_folder = os.path.join(base_folder, artist_name, "Singles")
                    download_audio(song_url, output_folder, song)
                    downloaded_songs.append(song) #Debugging

        print("Number of songs to download", len(download_song_list)) # Debugging
        print("Number of downloaded songs", len(downloaded_songs)) # Debugging

        end = time.time() #Marks the end time when the code finished executing. This is just for statistics, not part of the main code.
        
        print(f"Executing time: {end - start:.2f} seconds")
        break