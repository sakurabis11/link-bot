import re
from pyrogram import Client, filters
from pyrogram.types import *
import os
import spotipy
import requests
import base64

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

@Client.on_message(filters.command("spotify"))
async def spotify(client, message):
    # Get the access token
    access_token = get_access_token()

    # Get the song name or Spotify URL from the command
    song_name_or_url = message.command[1:]
    song_name_or_url = " ".join(song_name_or_url)

    # Check if the command argument is a Spotify URL
    match = re.match(r'https://open\.spotify\.com/track/([a-zA-Z0-9]+)', song_name_or_url)
    if match:
        # If it is a Spotify URL, extract the song ID from the URL
        song_id = match.group(1)
    else:
        # If it is not a Spotify URL, search for the song on Spotify
        song_name = song_name_or_url
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
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    data = response.json()

    # Get the song thumbnail
    thumbnail_url = data["album"]["images"][0]["url"]

    # Get the song details
    artist = data["artists"][0]["name"]
    name = data["name"]
    album = data["album"]["name"]
    release_date = data["album"]["release_date"]

    # Send the song thumbnail and details to the user
    await message.reply_photo(photo=thumbnail_url, caption=f"ʜᴇʏ {message.from_user.mention}\n\n ᴛɪᴛʟᴇ: <code>{name}</code>\nᴀʀᴛɪsᴛ: <code>{artist}</code>\nᴀʟʙᴜᴍ: <code>{album}</code>\nʀᴇʟᴇᴀsᴇ ᴅᴀᴛᴇ: <code>{release_date}</code>\n")


# Download logic using a function instead of undefined `spotify.download`
def download_song(song_url, output_path):
  response = requests.get(song_url)
  if response.status_code == 200:
    with open(output_path, 'wb') as f:
      for chunk in response.iter_content(1024):
        f.write(chunk)
    return True
  else:
    return False

# Download the song using the defined function
download_successful = download_song(song_url, output_path="temp.mp3")

# Check if download was successful
if download_successful:
  client.send_message(chat_id=user_id, text="Downloading song...")

  # Upload the song to Telegram
  bot.send_message(chat_id=user_id, text="Uploading song...")
  with open("temp.mp3", "rb") as file:
    bot.send_audio(chat_id=user_id, audio=file)

  # Clean up
  os.unlink("temp.mp3")
else:
  client.send_message(chat_id=user_id, text="Error downloading song. Please try again.")
