import os
import requests
from pyrogram import Client, filters

shazam_api_key = os.environ.get('6f3350e8e1msh0271352cf1c240dp1736d0jsn3acbbacd481a')
shazam_api_url = 'https://shazam.p.rapidapi.com/recognize'
headers = {
    'X-RapidAPI-Key': '6f3350e8e1msh0271352cf1c240dp1736d0jsn3acbbacd481a',
    'X-RapidAPI-Host': 'shazam.p.rapidapi.com'
}


@Client.on_message(filters.command('recognize'))
async def recognize_audio(client, message):

  if message.audio:
    audio_file_id = message.audio.file_id
    audio_file = client.download_media(audio_file_id)
    message.reply_text('Processing your audio file...')
    with open(audio_file, 'rb') as f:
        response = requests.post(shazam_api_url, headers=headers, data=f.read())
    if response.status_code == 200:
      result = response.json()['track']['title']
      message.reply_text(f'I think the song you sent is "{result}".')
    else:
      message.reply_text('Sorry, I couldn\'t recognize the song in your audio file.')
  else:
    message.reply_text('Please send me an audio file.')
