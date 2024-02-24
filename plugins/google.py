from pyrogram import Client,filters
import requests

API_URL = "https://api.safone.dev/google"

@Client.on_message(filters.command("google"))
async def google_search(client, message):
 try:
        query = message.text.split(" ", maxsplit=1)[1]
        response = requests.get(f"{API_URL}?q={query}&limit=1").json()

        search_results = response["results"]

        for result in search_results:
            title = result["title"]
            link = result["link"]
            snippet = result["snippet"]

            await message.reply_text(f"**Title:** {title}\n**Link:** {link}\n**Snippet:** {snippet}")

 except Exception as e:
        await message.reply_text(f"{e}")
