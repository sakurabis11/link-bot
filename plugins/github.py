from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import requests



# Define the /github command handler
@Client.on_message(filters.command('github'))
async def search_github(client, message):
    # Get the search query from the user
    query = message.text.split(' ', 1)[1]
    
    # Search for the repository using the GitHub API
    response = requests.get(f'https://api.github.com/search/repositories?q={query}')
    data = response.json()
    
    # Get the first 5 results
    items = data['items'][:5]
    
    # Create a list of buttons for the results
    buttons = [InlineKeyboardButton(item['name'], url=item['html_url']) for item in items]
    
    # Create the keyboard markup with the buttons
    keyboard = InlineKeyboardMarkup([buttons])
    
    # Reply to the message with the search results
    message.reply_text(f'Here are the top 5 results for "{query}":', reply_markup=keyboard)

