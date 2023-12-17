from pyrogram import Client, filters
from pytube import YouTube
from youtube_search import YoutubeSearch

@Client.on_message(filters.command("yt"))
async def download_handler(client, message):
    # Extract URL and split by space for playlist handling
    url = message.text.split()[1]

    try:
        if "playlist" in url:
            # Download from playlist
            download_playlist(url, message.chat.id)
        else:
            # Download single video
            download_video(url, message.chat.id)
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {e}")

def download_video(url, chat_id):
    try:
        # Get audio stream as an mp3 file
        youtube = YouTube(url)
        audio_stream = youtube.streams.filter(only_audio=True).desc("mp3").first()
        filename = f"{youtube.title}.mp3"

        # Send download progress message
        bot.send_message(chat_id, f"Downloading: {filename}")

        # Download and send file
        audio_stream.download(filename=filename)
        bot.send_document(chat_id, open(filename, "rb"))
        os.remove(filename)
        bot.send_message(chat_id, f"Downloaded: {filename}")
    except Exception as e:
        bot.send_message(chat_id, f"Error: {e}")

def download_playlist(url, chat_id):
    try:
        # Get videos from playlist
        playlist = YoutubeSearch(url, max_results=10).results[0]
        videos = playlist.get("playlist")

        # Download each video
        for video in videos:
            download_video(video["link"], chat_id)
    except Exception as e:
        bot.send_message(chat_id, f"Error: {e}")

