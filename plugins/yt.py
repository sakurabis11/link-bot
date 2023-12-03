import pyrogram
from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import youtube_dl

@Client.on_message(filters.command("yt"))
def youtube_link_handler(client, message):
    youtube_url = message.text.split()[1]

    try:
        with youtube_dl.YoutubeDL({'format': 'bestaudio/best'}) as ydl:
            video_info = ydl.extract_info(youtube_url, download=False)
            song_title = video_info['title']
            video_url = video_info['url']

        reply_markup = InlineKeyboardMarkup(
          [[
            InlineKeyboardButton("Song", callback_data=f"song {song_title} {youtube_url}"), 
            InlineKeyboardButton("Video", callback_data=f"video {video_url}")
        ]]
        )

        message.reply("Choose from the following:", reply_markup=reply_markup)
    except youtube_dl.YoutubeDLException as e:
        message.reply(f"Error processing YouTube link: {e}")

@Client.on_callback_query()
async def callback_handler(client, callback_query):
    data = callback_query.data.split()
    action = data[0]
    media_url = data[1]

    if action == "song":
        try:
            with youtube_dl.YoutubeDL({'format': 'bestaudio/best'}) as ydl:
                audio_info = ydl.extract_info(media_url, download=False)
                audio_title = audio_info['title']
                audio_url = audio_info['url']

                client.send_audio(callback_query.message.chat.id, audio_url, caption=audio_title)
                callback_query.edit_message_text("Song sent successfully.")
        except youtube_dl.YoutubeDLException as e:
            callback_query.edit_message_text(f"Error downloading song: {e}")
    elif action == "video":
        client.send_video(callback_query.message.chat.id, media_url)
        callback_query.edit_message_text("Video sent successfully.")

