import asyncio
import requests
from bs4 import BeautifulSoup
from pyrogram import Client, filters

USER_AGENT = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                 'Chrome/61.0.3163.100 Safari/537.36'
}


async def google(text):
    text = text.replace(" ", '+')
    url = f'https://www.google.com/search?q={text}'

    try:
        response = requests.get(url, headers=USER_AGENT)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        titles = soup.find_all('h3')

        results = [title.getText() for title in titles]

        if results:
            return results[0] 
        else:
            return "No relevant results found."

    except requests.exceptions.RequestException as e:
        print(f"Error occurred during search: {e}")
        return "An error occurred while searching. Please try again later."

@Client.on_message(filters.command("google"))
async def handle_search(client, message):
    search_term = message.text.split(" ", 1)[1]
    search_term = text.replace(" ", '+')

    if not search_term:
        await message.reply_text("Please specify a search term to use with the gagala keyword.")
        return

    search_result = await google(f"{search_term}")


    await message.reply_text(search_result)

