import os, asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from telegraph import upload_file
from utils import get_file_id

@Client.on_message(filters.command("telegraph"))
async def telegraph_upload(bot, update):
    replied = update.reply_to_message
    if not replied:
        return await update.reply_text("Reply To A Photo Or Video Under 20MB")
    file_info = get_file_id(replied)
    if not file_info:
        return await update.reply_text("Not Supported!")
    text = await update.reply_text(text="<code>Downloading To My Server ...</code>", disable_web_page_preview=True)

    # Check file size before downloading
    file_size = (await replied.download()).size
    if file_size > 20 * 1024 * 1024:  # 20 MB in bytes
        return await update.reply_text("File size exceeds the limit of 20 MB.")

    media = await update.reply_to_message.download()
    await text.edit_text(text="<code>Downloading Completed. Now I am Uploading to telegra.ph Link ...</code>", disable_web_page_preview=True)

    try:
        response = upload_file(media)
    except Exception as error:
        print(error)
        await text.edit_text(text=f"Error :- {error}", disable_web_page_preview=True)
        return

    try:
        os.remove(media)
    except Exception as error:
        print(error)
        return

    await text.edit_text(
        text=f"<b>Link :-</b>\n\n<code>https://graph.org{response[0]}</code>",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton(text="Open Link", url=f"https://graph.org{response[0]}"),
            InlineKeyboardButton(text="Share Link", url=f"https://telegram.me/share/url?url=https://graph.org{response[0]}")
        ], [
            InlineKeyboardButton(text=" Close ", callback_data="close")
        ]])
    )
