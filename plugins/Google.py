from pyrogram import Client, filters
import requests

@Client.on_message(filters.command("google"))
async def google_search(client, message):
    query = message.text.split(" ")[1:]
    url=query.replace(" ", "%")
    search_url = f"https://api.safone.dev/google?query={url}&limit=1"
    response = requests.get(search_url)
    results = response.json()
    message.reply_text(f"Title: {result['title']}\n", parse_mode="HTML")
