from pyrogram import Client, filters
from instagrapi import Client as InstaClient

insta = InstaClient()

@Client.on_message(filters.command("download"))
async def download(client, message):
    url = message.text.split(" ", 1)[1]
    media = insta.media_download(url)
    message.reply_document(media)

