import asyncio
import requests
from pyrogram import Client, filters


async def extract_pinterest_link(url):
    try:
        response = requests.get(url, allow_redirects=True)
        response.raise_for_status() 
        return url
    except requests.exceptions.RequestException as e:
        print(f"Error extracting URL: {e}")
        return None


@Client.on_message(filters.regex(r"^https?://pin\.it/([^/?]+)"))
async def handle_link(client, message):
 try:
        pinterest_link = message.text

        extracted_url = await extract_pinterest_link(pinterest_link)
        if extracted_url:
            await message.reply_text(f"Extracted link: {extracted_url}")
        else:
            await message.reply_text("Unable to extract link. Please ensure the link is valid and accessible.")
 except Exception as e:
            await message.rpely_text(f"{e}")
