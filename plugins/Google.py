from pyrogram import Client, filters
import requests

def google_search(query):
    url = f"https://api.safone.dev/google?query={gurl}&limit=1"
    response = requests.get(url)
    data = response.json()
    try:
        return data["results"][2]["description"]
    except KeyError:
        return "No description found for this query."

@Client.on_message(filters.command("google"))
async def handle_google_command(client, message):
    try:
        query = message.text.split()[1:]
        if not query:
            await message.reply_text("Please provide a search query.")
            return

        gurl = " ".join(query).replace(" ", "%")
        description = google_search(gurl)
        await message.reply_text(description)
    except Exception as e:
        await message.reply_text(f"Error: {e}")

