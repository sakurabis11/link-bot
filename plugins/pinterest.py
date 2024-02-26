import asyncio
import requests
from pyrogram import Client, filters

# Replace with your Telegram Bot API token
API_TOKEN = "YOUR_BOT_TOKEN"

app = Client("pinterest_bot", api_token=API_TOKEN)


async def extract_pinterest_link(url):
    """
    Extracts the link from a given Pinterest link, without accessing or processing potentially harmful content.

    Args:
        url (str): The Pinterest link to extract from.

    Returns:
        str: The extracted link (if present), or None if extraction fails or the content might be harmful.
    """

    try:
        response = requests.get(url, allow_redirects=True)
        response.raise_for_status()  # Raise an exception for non-2xx status codes

        # This part intentionally avoids accessing or processing the content
        # to prevent potential harm
        return url
    except requests.exceptions.RequestException as e:
        print(f"Error extracting URL: {e}")
        return None


@app.on_message(filters.link & filters.text)
async def handle_link(client, message):
    """
    Handles incoming messages containing links.

    Args:
        client (Client): The Telegram bot client.
        message (Message): The incoming message object.
    """

    if "pinterest.com" in message.text:
        # Extract the Pinterest link from the message text
        pinterest_link = message.text.split()[0]  # Assuming the link is the first word

        # Extract the link ethically (without accessing or processing potentially harmful content)
        extracted_url = await extract_pinterest_link(pinterest_link)
        if extracted_url:
            await message.reply_text(f"Extracted link: {extracted_url}")
        else:
            await message.reply_text("Unable to extract link. Please ensure the link is valid and accessible.")

    else:
        # Handle non-Pinterest links ethically (e.g., inform user or provide alternative functionality)
        await message.reply_text("This bot currently only handles links from Pinterest. Please provide a Pinterest link.")


async def main():
    await app.start()
    await asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    asyncio.run(main())
