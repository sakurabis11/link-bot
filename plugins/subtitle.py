from pyrogram import Client, filters
from subscene_api import Subscene
from pyrogram.types import InlineKeyboardButton, ReplyKeyboardMarkup

subscene = Subscene()

@Client.on_message(filters.text & filters.command("sub"))
async def download_subtitles(client, message):
    # Get movie/series title from message
    query = message.text.split(" ", 1)[1]

    # Search for subtitles
    results = subscene.search(query)

    # Prepare keyboard with subtitle options
    keyboard = ReplyKeyboardMarkup(
        [
            [InlineKeyboardButton(f"{title} ({lang})", callback_data=f"{title}|{lang}")]
            for title, lang in results
        ]
    )

    # Send keyboard for user to choose
    await message.reply(
        f"Found subtitles for '{query}':", reply_markup=keyboard
    )


@Client.on_callback_query()
async def download_selected_subtitle(client, query):
    title, lang = query.data.split("|")

    # Download subtitle
    subtitle = subscene.get_subtitle(title, lang)

    # Send downloaded subtitle as document
    await client.send_document(
        chat_id=query.message.chat.id, document=subtitle, filename=f"{title}.srt"
    )

    # Delete keyboard
    await query.answer(cache_time=0)

