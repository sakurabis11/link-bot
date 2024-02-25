
import requests
from pyrogram import Client, filters

def google_search(query):
    url = f"https://api.safone.dev/google?query={query}&limit=1"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to fetch search results. Please try again.")
    if response.headers.get("Content-Type") != "application/json":
        raise Exception("Unexpected response format. Please try again.")
    data = response.json()
    return data["results"][0]["title"]


@Client.on_message(filters.command("google"))
async def handle_google_command(client, message):
    try:
        query = message.text.split()[1:]
        if not query:
            await message.reply_text("Please provide a search query.")
            return
        title = google_search(" ".join(query))
        await message.reply_text(title)
    except Exception as e:
        await message.reply_text(f"Error: {e}")
