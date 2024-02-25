from pyrogram import Client, filters
import requests

def google_search(query):
    url = f"https://api.safone.dev/google?query={gurl}&limit=1"
    response = requests.get(url)
    data = response.json()
    return data["results"][2]["description"]

@Client.on_message(filters.command("google"))
async def handle_google_command(client, message):
 try:
    query = message.text.split()[1:]
    if not query:
        await message.reply_text("Please provide a search query.")
        return
        gurl =  " ".join(query).replace(" ", "%")
        title = google_search(" ".join(url))
        await message.reply_text(title)
 except Exception as e:
        await message.reply_text(f"Error: {e}")
