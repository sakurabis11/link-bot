from pyrogram import Client, filters
from pytube import YouTube
from youtube_search import YoutubeSearch
from info import ADMINS


@Client.on_message(filters.command("yt"))
async def download_song(client, message):
    # Get the chat and text
    chat_id = message.chat.id
    text = message.text.replace("yt", "")

    # Check if link provided
    if not text:
        message.reply("Please provide a YouTube video or playlist link!")
        return

    # Try extracting video information
    try:
        if "playlist" in text:
            # Download from playlist
            playlist = YoutubeSearch(text).get_playlist()
            download_playlist(client, chat_id, playlist)
        else:
            # Download single video
            video = YouTube(text)
            download_video(client, chat_id, video)
    except Exception as e:
        message.reply(f"Error: {e}")

def download_video(client, chat_id, video):
    # Send info and ask for format
    message = client.send_message(chat_id, f"Downloading '{video.title}'... Choose format (audio/video):")
    client.register_filters([
        filters.text(matches="(audio|video)")
    ])

    @client.on_message(filters.text & filters.chat(chat_id))
    def choose_format(client, message):
        format = message.text
        download_stream(client, chat_id, video, format)

def download_playlist(client, chat_id, playlist):
    # Send playlist info and ask for confirmation
    message = client.send_message(chat_id, f"Found playlist '{playlist.title}' with {len(playlist.videos)} songs. Download all? (y/n)")
    client.register_filters([
        filters.text(matches="(y|n)")
    ])

@Client.on_message(filters.text & filters.chat(chat_id))
async def confirm_playlist(client, message):
        if message.text == "y":
            for video in playlist.videos:
                download_video(client, chat_id, video)
        else:
            message.reply("Download cancelled.")

def download_stream(client, chat_id, video, format):
    # Download and send file
    if format == "audio":
        stream = video.streams.filter(only_audio=True).order_by('abr').desc().first()
        file_path = stream.download()
    else:
        stream = video.streams.first()
        file_path = stream.download()

    client.send_audio(chat_id, file_path, progress=True)

