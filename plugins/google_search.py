import asyncio
from pyrogram import Client, filters
import requests
from info import REQUESTED_CHANNEL

@Client.on_message(filters.command("google"))
async def google_text(client, message):
    try:
        user_query = message.text.split()[1:]
        if not user_query:
          await message.reply_text("provide a query") 
          return
        updated_query = f"What is the release date of {user_query}"
        encoded_query = " ".join(updated_query).replace(" ", "%20")

        response = requests.get(f"https://api.safone.dev/google?query={encoded_query}&limit=1")
        if response.status_code == 200:
            data = response.json()
            google_result = data["results"][0]["description"]
            await client.send_message(message.chat.id, google_result)
            await client.send_message(REQUESTED_CHANNEL, text=f"#google_result\nʜᴇʏ {message.from_user.mention}\nʀᴇǫᴜᴇsᴛ ɪs {user_query}")

    except Exception as e:
       await message.reply_text(f"An error occurred: {e}")
