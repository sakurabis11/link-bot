import os
import re
import wget
from pyrogram import Client, filters, Message

@Client.on_message(filters.regex(r'^https?://pin.it/([^/?]+))
async def pinterest(client, message: Message):
    try:
        match = re.match(r'^https?://pin.it/([^/?]+)', message.text)
        if match:
            pint_url = f"https://i.pinimg.com/originals/{match.group(1)}"  
        else:
            raise ValueError("Invalid Pinterest URL format")

        download_message = await message.reply_text("Downloading...")


        filename = os.path.basename(pint_url)  
        try:
            wget.download(pint_url, filename)
        except Exception as e:
            raise Exception(f"Download failed: {e}") from e

        upload_message = await download_message.edit("Uploading...")
        try:
            await client.send_document(message.chat.id, filename)
        except Exception as e:
            raise Exception(f"Upload failed: {e}") from e

        try:
            os.remove(filename)
        except Exception as e:
            print(f"Failed to remove downloaded file: {e}")

    except Exception as e:
        error_message = f"An error occurred: {e}"
        await message.reply_text(error_message)

