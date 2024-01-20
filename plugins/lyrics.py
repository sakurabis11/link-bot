import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

@Client.on_message(filters.command('lyrics'))
async def lyrics(client: Client, message: Message):
    # Get the song name from the message
    song_name = message.text.split(' ', 1)[1]

    # Search for the lyrics on Genius
    async with client.async_session() as session:
        async with session.get(f'https://api.genius.com/search?q={song_name}') as response:
            data = await response.json()

    # Get the first result
    result = data['response']['hits'][0]

    # Get the lyrics from the Genius API
    async with client.async_session() as session:
        async with session.get(f'https://api.genius.com/songs/{result["result"]["id"]}') as response:
            data = await response.json()

    # Send the lyrics to the user
    await message.reply_text(data['response']['song']['lyrics'])

