import requests
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
        results = await google_search(query, num_results=5)
        for result in results:
            await m.edit(result)
    except Exception as e:
        await m.edit(str(e))
