import pyrogram
from pyrogram import Client, filters
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
#import shazam

@Client.on_message(filters.video)
async def handle_video(client, message):
    video_file = await client.download_media(message.video)
    video_clip = VideoFileClip(video_file)
    audio = video_clip.audio
    audio.write_audiofile("audio.mp3")

    recognizer = shazam.Shazam()
    audio_segment = AudioSegment.from_mp3("audio.mp3")
    result = recognizer.recognize_song(audio_segment)

    if result:
        await client.send_message(message.chat.id, f"Song: {result['track']['title']}\nArtist: {result['track']['artist']}")
    else:
        await client.send_message(message.chat.id, "Song not recognized.")

@Client.on_message(filters.audio)
async def handle_audio(client, message):
    audio_file = await client.download_media(message.audio)
    recognizer = shazam.Shazam()
    audio_segment = AudioSegment.from_file(audio_file)
    result = recognizer.recognize_song(audio_segment)

    if result:
        await client.send_message(message.chat.id, f"Song: {result['track']['title']}\nArtist: {result['track']['artist']}")
    else:
        await client.send_message(message.chat.id, "Song not recognized.")
