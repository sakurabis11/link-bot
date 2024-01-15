import pyrogram
from pyrogram import Client, filters
from pydub import AudioSegment
from shazamio import Shazam
import ffmpeg
import os

# Create a Shazam client
shazam = Shazam()

# Define the main function
@Client.on_message(filters.command(["identify"]))
async def identify_song(client, message):
    # Get the audio file from the user
    audio_file = message.reply_to_message.audio

    # Download the audio file
    audio_file.download()

    # Convert the audio file to a WAV file
    audio_segment = AudioSegment.from_file(audio_file.file_path)
    audio_segment.export("song.wav", format="wav")

    # Identify the song using Shazam
    result = shazam.recognize_song("song.wav")

    # Send the song title and artist to the user
    message.reply_text(f"Title: {result['track']['title']}\nArtist: {result['track']['artist']['name']}")

    # Send the song as an MP3 file to the user
    song_url = result['track']['sections'][0]['result']['mp3']
    client.send_audio(message.chat.id, song_url)

    # Delete the downloaded audio file and the WAV file
    os.remove(audio_file.file_path)
    os.remove("song.wav")



