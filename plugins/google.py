import requests  # Imported but not used

# google result finder
from pyrogram import Client, filters

@Client.on_message(filters.command("google"))
async def google(_, message):
    if len(message.command) < 2:
        await message.reply_text("Usage: /google <query>")
        return

    query = message.text.split(None, 1)[1]
    m = await message.reply_text("searching")

    google_search = f"https://www.google.com/search?q={query}+ott+release+date+and+platform"

    try:
        # results = await google_search(query, num_results=5)  # Unclear how this search is intended to be performed
        # for result in results:
        #     await m.edit(result)

        # Example using requests (replace with the intended search method):
        response = requests.get(google_search)
        results = response.text  # Assuming results are in the text content
        for result in results:
            await m.edit(result)

    except Exception as e:
        await m.edit(str(e))  # Consider handling specific exceptions for better error messages
