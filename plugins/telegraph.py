import os, asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from telegraph import upload_file
from utils import get_file_id

@Client.on_message(filters.command("telegraph") & (filters.private | filters.group))
async def telegraph_upload(client, update):
    replied = update.reply_to_message

    if not replied:
        return await update.reply_text("Please reply to a photo or video under 20MB")

    file_info = get_file_id(replied)

    if not file_info:
        return await update.reply_text("Unsupported media type")

    file_size = file_info.file_size
    file_name = file_info.file_name

    if file_size > 20971520:  # 20 MB in bytes
        await update.reply_text("File size exceeds 20 MB. Uploading in chunks...")

        # Initiate chunking and uploading
        chunk_size = 5242880  # 5 MB in bytes
        chunks = []

        with open(file_name, "rb") as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break

                chunks.append(chunk)

        # Upload each chunk to Telegraph
        telegraph_links = []

        for chunk in chunks:
            try:
                response = upload_file(chunk)
            except Exception as error:
                await update.reply_text(f"Error: {error}")
                return

            telegraph_links.append(f"https://graph.org{response[0]}")

        # Combine Telegraph links into a single link
        telegraph_link = "\n".join(telegraph_links)

    else:  # File size is under 20 MB
        # Upload the entire file to Telegraph
        download_message = await update.reply_text("Downloading to my server...")
        media = await replied.download()

        await download_message.edit_text("Download completed. Uploading to telegra.ph...")

        try:
            response = upload_file(media)
        except Exception as error:
            await download_message.edit_text(f"Error: {error}")
            return

        try:
            os.remove(media)
        except Exception:
            pass

        telegraph_link = f"https://graph.org{response[0]}"

    # Generate and send response message
    markup = InlineKeyboardMarkup([[
        InlineKeyboardButton("Open Link", url=telegraph_link),
        InlineKeyboardButton("Share Link", url=f"https://telegram.me/share/url?url={telegraph_link}")
    ], [
        InlineKeyboardButton("Close", callback_data="close")
    ]])

    await download_message.edit_text(
        f"<b>Link:</b>\n\n`{telegraph_link}`",
        disable_web_page_preview=True,
        reply_markup=markup
    )
