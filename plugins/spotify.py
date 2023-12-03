import os
import requests
import base64
from pyrogram import Client, filters
from pyrogram.types import *

# Define your client id and client secret
client_id = 'd3a0f15a75014999945b5628dca40d0a'
client_secret = 'e39d1705e35c47e6a0baf50ff3bb587f'

# Encode the client id and client secret
credentials = base64.b64encode(f'{client_id}:{client_secret}'.encode('utf-8')).decode('utf-8')

# Define a function to get the access token
def get_access_token():
    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': f'Basic {credentials}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'client_credentials'
    }
    response = requests.post(url, headers=headers, data=data)
    return response.json()['access_token']

# Define a function to handle the /spotify command
@Client.on_message(filters.command("spotify"))
async def spotify(client, message):
    # Get the access token
    access_token = get_access_token()

    # Get the song name from the command
    song_name = message.command[1:]
    song_name = " ".join(song_name)

    # Search for the song on Spotify
    url = f'https://api.spotify.com/v1/search?q={song_name}&type=album,track'
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    data = response.json()

    # Get the first search result
    item = data["tracks"]["items"][0]

    # Get the song ID
    song_id = item["id"]

    # Get the song thumbnail and details from Spotify
    url = f'https://api.spotify.com/v1/tracks/{song_id}'
    response = requests.get(url, headers=headers)
    data = response.json()

    # Get the song thumbnail
    thumbnail_url = data["album"]["images"][0]["url"]

    # Get the song details
    artist = data["artists"][0]["name"]
    name = data["name"]
    duration_ms = data["duration_ms"]
    duration = str(int(duration_ms / 1000)) + " seconds"

    # Download the song
    url = f'https://api.spotify.com/v1/tracks/{song_id}/download'
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers, stream=True)

    # Save the song to a temporary file
    file_name = f"{name}.mp3"
    with open(file_name, "wb") as f:
        for chunk in response.iter_content(1024):
            f.write(chunk)

    # Upload the downloaded song file
    file_path = os.path.abspath(file_name)
    with open(file_path, 'rb') as file_obj:
        document = await client.upload_document(file_obj)

    # Send the song thumbnail and details to the user
    await message.reply_photo(photo=thumbnail_url)
    await message.reply_text(f"{name} by {artist}({duration})")

    # Send the uploaded song file to the user
    await message.reply_document(document=document)
    await message.reply_text("The requested song has been sent.")

    # Delete the temporary song file
    os.remove(file_name)
