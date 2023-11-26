import pyrogram
from pyrogram import Client, filters, enums
import requests
from info import API_ID, API_HASH, BOT_TOKEN, OPENAI_API_KEY, PORT

@Client.on_message(filters.command("generate"))
async def on_message(client, message):
        response = requests.get("https://api.openai.com/v1/images/generate", params={
            "model": "dall-e-3",
            "prompt": "a white siamese cat",
            "size": "1024x1024",
            "quality": "standard",
            "n": 1,
        }, headers={
            "Authorization": "Bearer {OPENAI_API_KEY}",
        })

        image_url = response.json()["data"][0]["url"]

        client.send_photo(message.chat.id, image_url)
