import pyrogram
from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import subprocess

@Client.on_message(filters.command("yt"))
def youtube_link_handler(client, message):
    youtube_url = message.text.split()[1]

    try:
        audio_info = extract_audio_info(youtube_url)
        song_title = audio_info['title']
        audio_url = audio_info['url']

        reply_markup = InlineKeyboardMarkup(
            [[
                InlineKeyboardButton("Song", callback_data=f"song {song_title} {youtube_url}"),
                InlineKeyboardButton("Video", callback_data=f"video {youtube_url}")
            ]]
        )

        message.reply("Choose from the following:", reply_markup=reply_markup)
    except Exception as e:
        message.reply(f"Error processing YouTube link: {e}")

@Client.on_callback_query()
async def callback_handler(client, callback_query):
    data = callback_query.data.split()
    action = data[0]
    media_url = data[1]

    if action == "song":
        try:
            audio_file = download_audio(audio_url)
            client.send_audio(callback_query.message.chat.id, audio_file, caption=audio_info['title'])
            callback_query.edit_message_text("Song sent successfully.")
        except Exception as e:
            callback_query.edit_message_text(f"Error downloading song: {e}")
    elif action == "video":
        try:
            video_file = download_video(media_url)
            client.send_video(callback_query.message.chat.id, video_file)
            callback_query.edit_message_text("Video sent successfully.")
        except Exception as e:
            callback_query.edit_message_text(f"Error downloading video: {e}")

def extract_audio_info(youtube_url):
    ffmpeg_command = f"ffmpeg -i {youtube_url} -f bestaudio -hide_banner -loglevel quiet -show_format 2>&1"
    output = subprocess.check_output(ffmpeg_command, shell=True, universal_newlines=True)

    metadata = {}
    for line in output.splitlines():
        if '=' in line:
            key, value = line.split('=')
            metadata[key] = value

    return metadata

def download_audio(audio_url):
    output_filename = f"audio_{time.time()}.mp3"
    ffmpeg_command = f"ffmpeg -i {audio_url} -f bestaudio {output_filename}"
    subprocess.call(ffmpeg_command, shell=True)
    return output_filename

def download_video(media_url):
    output_filename = f"video_{time.time()}.mp4"
    ffmpeg_command = f"ffmpeg -i {media_url} {output_filename}"
    subprocess.call(ffmpeg_command, shell=True)
    return output_filename
