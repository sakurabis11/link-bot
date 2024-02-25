from pyrogram import Client, filters
import requests

def convert_text(query):
    return " ".join(query).replace(" ", "%")

def google_search(query):
    encoded_query = convert_text(query)
    url = f"https://api.safone.dev/google?query={encoded_query}&limit=1"

    try:
        if response == 200:
          response = requests.get(url)
          response.raise_for_status() 

          data = response.json()
          return data["results"][0]["description"]
        pass

    except requests.exceptions.RequestException as e:
          print(f"Error fetching search results: {e}")
          return f"An error occurred while fetching data. Please try again later.{e}"

    except Exception as e:
          return f"No description found for this query.{e}"

@Client.on_message(filters.command("google"))
async def handle_google_command(client, message):
    try:
        query = message.text.split()[1:]
        if not query:
            await message.reply_text("Please provide a search query.")
            return

        description = google_search(query)
        await message.reply_text(description)

    except Exception as e:
        await message.reply_text(f"An error occurred: {e}")

