import os
from os import environ
import requests
import pyrogram
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

shazam_api_key = os.environ.get('SHAZAM_API_KEY')
shazam_api_url = 'https://shazam.p.rapidapi.com/recognize'
headers = {
    'X-RapidAPI-Key': shazam_api_key,
    'X-RapidAPI-Host': 'hazam.p.rapidapi.com'
}

# Define a command to recognize an audio file
@Client.on_message(filters.command('recognize'))
async def recognize_audio(client, message):
    # Check if the message contains an audio file
    if message.audio:
        # Get the audio file ID
        audio_file_id = message.audio.file_id
        # Download the audio file
        audio_file = bot.download_media(audio_file_id)
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
