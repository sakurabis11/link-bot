import os, asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery, ReplyKeyboardMarkup
from telegraph import upload_file
from pyrogram.errors import FloodWait
from utils import get_file_id
from info import API_ID, API_HASH, BOT_TOKEN, PORT
import telegraph

telegraph = telegraph.api.Telegraph()

@Client.on_message(pyrogram.filters.command('telegraph'))
def handle_upload_command(message):
    if message.reply_to_message:
        reply_message = message.reply_to_message

        if reply_message.media:
            if reply_message.media.photo:
                photo_link = upload_photo(reply_message.media.photo)
            elif reply_message.media.video:
                video_link = upload_video(reply_message.media.video)
            elif reply_message.media.document:
                document_link = upload_document(reply_message.media.document)
            else:
                message.reply_text('Unsupported media type')
                return

            keyboard = InlineKeyboardMarkup([
                InlineKeyboardButton('Open in Telegraph', url=photo_link or video_link or document_link)
            ])

            try:
                bot.send_message(message.chat.id, 'Uploaded to Telegraph:', reply_markup=keyboard)
            except TelegramError:
                message.reply_text('Failed to send message')
    else:
        message.reply_text('Please reply to a media message with /telegraph')

def upload_photo(photo):
    result = telegraph.upload_photo(photo)
    return result['url']

def upload_video(video):
    result = telegraph.upload_file(video.file_id)
    return result['url']

def upload_document(document):
    result = telegraph.upload_file(document.file_id)
    return result['url']

