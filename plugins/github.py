import os
import re
import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Define the search function
def github_repositories(query):
    url = f'https://api.github.com/search/repositories?q={query}&per_page=5'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        items = data['items']
        results = []
        for item in items:
            name = item['name']
            description = item['description']
            url = item['html_url']
            results.append(f'<a href="{url}">{name}</a> - {description}')
        return '\n'.join(results)
    else:
        return 'No results found.'

# Define the /search command handler
@Client.on_message(filters.command('search'))
async def github_command(client, message):
    # Get the search query from the message text
    query = message.text.split(' ', 1)[1]
    # Search for repositories on GitHub
    results = search_repositories(query)
    # Send the search results as a message
    message.reply_text(results, parse_mode='HTML')
