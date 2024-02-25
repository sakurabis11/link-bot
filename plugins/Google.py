import requests
from pyrogram import Client, filters

def google_search(query):
    url = f"https://api.safone.dev/google?query={query}&limit=1"
    response = requests.get(url)
    data = response.json()
    return data["results"][0]["title"]

@Client.on_message(filters.command("google"))
async def handle_google_command(client, message):
    query = message.text.split()[1:]
    query = query.replace(" ", "%")
    if not query:
        await message.reply_text("Please provide a search query.")
        return

    try:
        title = google_search(" ".join(query))
        await message.reply_text(title)
    except Exception as e:
        await message.reply_text(f"Error: {e}")
        
