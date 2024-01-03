from pyrogram import Client,filters
import requests

api_key = "b0d58dcd0ccbe19340aa143daf4c6ad0"

@Client.on_message(filters.command("ott", prefixes="/"))
async def ott_command(client, message):

    query = message.text.split(" ", 1)[1]  
    
    url = f"https://api.themoviedb.org/3/movie/{query}/release_dates"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    response = requests.get(url, headers=headers)

    await message.reply_text(response.text)


