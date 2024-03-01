import requests
from pyrogram import Client, filters

PYPI_SEARCH_URL = "https://pypi.org/pypi/{}/json"

@Client.on_message(filter.command("pypi"))
async def pypi_search(client, message):
    try:
        # Extract search query from message text
        search_query = message.text.split()[1]

        # Make request to PyPI search API
        response = requests.get(PYPI_SEARCH_URL.format(search_query))
        data = response.json()

        # Check for successful response and valid package information
        if response.status_code == 200 and "info" in data:
            info = data["info"]

            # Build response message with package details
            response_text = f"**Package:** {info['name']}\n"
            response_text += f"**Version:** {info['version']}"

            await message.reply_text(response_text, parse_mode="markdown")
        else:
            await message.reply_text(f"Package '{search_query}' not found on PyPI.")

    except Exception as e:
        print(f"Error searching PyPI: {e}")
        await message.reply_text(f"An error occurred while searching PyPI:- {e}.")
