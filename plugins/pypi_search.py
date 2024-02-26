import asyncio
from pyrogram import Client, filters
import requests

@Client.on_message(filters.command("pypi"))
async def google_text(client, message):
    try:
        user_query = message.text.split()[1:]

        response = requests.get(f"https://api.safone.dev/pypi?query={user_query}")
        if response.status_code == 200:
            data = response.json()
            title = data.get("title")
            version = data.get("version")
            await client.send_message(message.chat.id, text=f"**{title} verison:**\n<code>{version}</code>")
    except Exception as e:
        await message.reply_text(f"An error occurred: {e}")
