import pyrogram
from pyrogram import filters, Client, enums
from pyrogram.types import Message
from pydub import AudioSegment

import requests

ALLOWED_GROUP_IDS = [-1001568397419]

@Client.on_message(filters.audio | filters.video)
def handle_audio_or_video(client: pyrogram.Client, message: Message):
    if message.audio or message.video:
        # Check if the message is in an allowed group
        if message.chat.id not in ALLOWED_GROUP_IDS:
            return

        # Download the audio file
        audio_file = client.download_media(message.media)

        # Convert the audio file to MP3 if it's not already MP3
        if not audio_file.endswith(".mp3"):
            audio_file = AudioSegment.from_file(audio_file).export("audio.mp3")

        # Try to recognize the song using Shazam
        try:
            song = shazam.recognize(audio_file)
        except Exception as e:
            print(f"Error recognizing song: {e}")
            client.send_message(message.chat.id, "Sorry, I couldn't recognize the song.")
            return

        # Send the Shazam result to the chat
        if song:
            spotify_link = f"[Spotify]({song.uri})"
            youtube_link = f"[YouTube]({song.youtube_url})"
            apple_music_link = f"[Apple Music]({song.apple_music_url})"
            youtube_music_link = f"[YouTube Music]({song.youtube_music_url})"

            message_text = f"Song: {song.artist} - {song.title}\n\n"
            message_text += f"{spotify_link} | {youtube_link} | {apple_music_link} | {youtube_music_link}"

            client.send_message(message.chat.id, message_text)
        else:
            client.send_message(message.chat.id, "Sorry, I couldn't find any Shazam results for this song.")
