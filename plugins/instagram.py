import os
import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

# Define a function to download Instagram posts or Reels
async def download_media(media_url):
    response = requests.get(media_url)
    filename = media_url.split('/')[-1]

    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    with open(f'downloads/{filename}', 'wb') as f:
        f.write(response.content)
    return filename


# Define a command to handle incoming messages
@Client.on_message(filters.command('download'))
async def download_command(client, message):
    # Get the link to the Instagram post or Reel
    link = message.text.split(' ')[1]

    # Check if the link is to an Instagram post or Reel
    if 'instagram.com/p/' in link or 'instagram.com/reel/' in link:
        # Download the media file
        try:
            filename = download_media(link)
            # Send a confirmation message
            message.reply_text(f'Media file downloaded: {filename}')
        except Exception as e:
            # Send an error message if the download fails
            message.reply_text(f'Error downloading media: {e}')
    else:
        # Send an error message if the link is not to an Instagram post or Reel
        message.reply_text('Invalid Instagram link')


# Define a command to handle inline button clicks
@Client.on_callback_query()
async def button_click(client, callback_query):
    # Get the data from the callback query
    data = callback_query.data

    # Check if the button click is for downloading a post or a Reel
    if data == 'post':
        # Get the link to the Instagram post
        link = callback_query.message.reply_to_message.text

        # Download the media file
        try:
            filename = download_media(link)
            # Send a confirmation message
            callback_query.answer('Media file downloaded')
            callback_query.edit_message_text(f'Media file downloaded: {filename}')
        except Exception as e:
            # Send an error message if the download fails
            callback_query.answer('Error downloading media')
            callback_query.edit_message_text(f'Error downloading media: {e}')
    elif data == 'reel':
        # Get the link to the Instagram Reel
        link = callback_query.message.reply_to_message.text

        # Download the Reel
        try:
            # TODO: Implement Reel downloader
            callback_query.answer('Reel downloading is not implemented yet')
            callback_query.edit_message_text('Reel downloading is not implemented yet')
        except Exception as e:
            # Send an error message if the download fails
            callback_query.answer('Error downloading Reel')
            callback_query.edit_message_text(f'Error downloading Reel: {e}')


# Define a function to handle incoming messages
@Client.on_message(filters.group)
async def handle_message(client, message):
    # Check if the message contains a link to an Instagram post or Reel
    if 'instagram.com/p/' in message.text or 'instagram.com/reel/' in message.text:
        # Create a keyboard with two buttons for downloading a post or a Reel
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton('Download Post', callback_data='post') ,
                                          InlineKeyboardButton('Download Reel', callback_data='reel')]])
        # Reply to the message with the keyboard
        message.reply_text('Select an option:', reply_markup=keyboard)
    else:
        # Send an error message if the message does not contain a link to an Instagram post or Reel
        message.reply_text('Please enter a valid Instagram link')
