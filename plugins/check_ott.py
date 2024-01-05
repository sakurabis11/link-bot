from pyrogram import Client, filters
from googlesearch import search
import requests

@Client.on_message(filters.command(["check_ott"]))
async def ott_search(client, message):
    try:
        # Extract movie/series name from the command
        query = ' '.join(message.command[1:])

        search_query = f"https://www.google.com/search?q={query}+ott+release+date+and+platform"
        
