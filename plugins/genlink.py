import os
import base64
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Define a message handler to handle file uploads
@Client.on_message(filters.document | filters.video)
async def share_file(client, message):
    # Get the file ID and file name from the message
    file_id = message.document.file_id if message.document else message.video.file_id
    file_name = message.document.file_name if message.document else message.video.file_name

    # Download the file
    file_info = client.get_file(file_id)
    downloaded_file = client.download_file(file_info.file_path)

    # Encode the file as base64
    base64_string = base64.b64encode(downloaded_file).decode('utf-8')

    # Generate a link to the file
    link = f'https://t.me/{client.username}?start={base64_string}'

    # Send a message to the user with a link to the file
    message.reply_text(f'Here is the link to your {file_name} file: {link}')

# Define a callback query handler to handle user clicks on the link
@Client.on_callback_query()
async def handle_callback_query(client, callback_query):
    # Get the data from the callback query
    data = callback_query.data

    # Decode the base64 string from the callback data
    base64_string = data.split(':')[1]
    decoded_string = base64.b64decode(base64_string.encode('utf-8')).decode('utf-8')

    # Download the file
    with open('shared_file.bin', 'wb') as f:
        f.write(decoded_string.encode('utf-8'))

    # Send a message to the user with a link to download the file
    callback_query.answer('Download completed.')
    callback_query.edit_message_text(f'Here is your shared file: https://t.me/{client.username}?download=shared_file.bin')

