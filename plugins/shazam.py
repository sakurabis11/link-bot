import os
import requests
from pyrogram import Client, filters

shazam_api_key = os.environ.get('6f3350e8e1msh0271352cf1c240dp1736d0jsn3acbbacd481a')
shazam_api_url = 'https://shazam.p.rapidapi.com/recognize'
headers = {
    'X-RapidAPI-Key': '6f3350e8e1msh0271352cf1c240dp1736d0jsn3acbbacd481a',
    'X-RapidAPI-Host': 'shazam.p.rapidapi.com'
}

# Define a command to recognize an audio file
@Client.on_message(filters.command('recognize'))
async def recognize_audio(client, message):
    # Check if the message contains an audio file
    if message.audio:
        # Get the audio file ID
        audio_file_id = message.audio.file_id
        # Download the audio file
        audio_file = client.download_media(audio_file_id)
        # Send a message to the user to indicate that the audio file is being processed
        message.reply_text('Processing your audio file...')
        # Send a request to the Shazam API to recognize the audio file
        response = requests.post(shazam_api_url, headers=headers, files={'track': audio_file})
        # Check if the API returned a result
        if response.status_code == 200:
            result = response.json()['track']['title']
            # Send the result to the user
            message.reply_text(f'I think the song you sent is "{result}".')
        else:
            # Send an error message to the user
            message.reply_text('Sorry, I couldn\'t recognize the song in your audio file.')
    else:
        # Send an error message to the user
        message.reply_text('Please send me an audio file.')
