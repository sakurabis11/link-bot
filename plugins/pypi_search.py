import asyncio
from pyrogram import Client, filters
import requests
from info import REQUESTED_CHANNEL

async def get_package(encoded_query):
   response = requests.get(f"https://pypi.org/pypi/{user_query}/json")
   if response.status_code == 200:
        data = response.json()
        return data.get("info", {}).get("version")
   else:
        return None

@Client.on_message(filters.command("pypi"))
async def google_text(client, message):
    try:
        user_query = message.text.split()[1:]
        if not user_query:
          await message.reply_text("Enter a package name") 
          return  
        encoded_query = " ".join(user_query).replace(" ", "")
        version = await get_package(encoded_query)
        if version:
          await message.reply_text(f"Package: {encoded_query}\nVersion: {version}")
        else:
          await message.reply_text(f"Package '{encoded_query}' not found on PyPI.")
    except Exception as e:
          await message.reply_text(f"{e}")
