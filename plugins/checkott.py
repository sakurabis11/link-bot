import asyncio
import os
from pyrogram import Client, filters
from pyrogram.types import *

@Client.on_message(filters.command("checkott"))
async def check_ott(client, message):
    # Extract the movie or TV show name from the message
    query = message.text.split(" ", 1)[1]

    # Construct the Google search query
    google_search_query = f"when {query} coming to ott"

    # Perform a Google search using the aiohttp library
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://www.google.com/search?q={google_search_query}") as response:
            html = await response.text()

    # Parse the HTML response to extract the relevant information
    soup = BeautifulSoup(html, "html.parser")
    results = soup.find_all("div", class_="ZINbbc xpd O9g5cc uUPGi")

    # Prepare the inline keyboard markup with the OTT platforms and dates
    keyboard = []
    for result in results:
        platform = result.find("div", class_="BNeawe iBp4i AP7Wnd").text
        date = result.find("div", class_="BNeawe tAd8D AP7Wnd").text
        keyboard.append([InlineKeyboardButton(f"{platform}: {date}", callback_data=f"{platform}-{date}")])

    # Send the inline keyboard markup to the user
    await message.reply_text("Select the OTT platform and date:", reply_markup=InlineKeyboardMarkup(keyboard))

# Define the callback handler for the inline keyboard buttons
@Client.on_callback_query()
async def callback_handler(client, callback_query):
    # Extract the OTT platform and date from the callback data
    platform, date = callback_query.data.split("-")

    # Send a message to the user with the selected OTT platform and date
    await callback_query.message.edit_text(f"OTT Platform: {platform}\nRelease Date: {date}")


