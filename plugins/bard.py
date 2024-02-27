import asyncio
from pyrogram import Client, filters
import requests
from info import REQUESTED_CHANNEL

@Client.on_message(filters.command("bard"))
async def google_text(client, message):
    try:
        user_query = message.text.split()[1:]
        if not user_query:
          await message.reply_text("please provide a query") 
          return
        encoded_query = user_query.replace(" ", "%20")
        response = requests.get(f"https://api.safone.dev/bard?message={encoded_query}")
        if response.status_code == 200:
            data = response.json()
            bard = data['parts'][0]
            bar_d = bard['text']
            await client.send_message(message.chat.id, bar_d)
            await client.send_message(REQUESTED_CHANNEL, text=f"#ᴄᴄ_ɢᴇɴ\nʜᴇʏ {message.from_user.mention}\nʀᴇǫᴜᴇsᴛ ɪs {user_query}")

    except Exception as e:
       await message.reply_text(f"An error occurred: {e}")
