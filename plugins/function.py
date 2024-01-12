import pyrogram
import asyncio
import pyrogram.errors.exceptions.bad_request_400 as bad_request
from Script import script
from database.users_db import db
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid
from info import API_ID, API_HASH, BOT_TOKEN, PORT, LOG_CHANNEL, ADMINS, DATABASE_NAME, DATABASE_URI
import logging, re, asyncio, time, shutil, psutil, os, sys
from utils import get_size, temp, extract_user, get_file_id, humanbytes, last_online

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

@Client.on_message(filters.command("restart") & filters.user(ADMINS))
async def restart_bot(client, message):
    # Send a message indicating that the bot is restarting
    message_id = await message.reply("Rᴇꜱᴛᴀᴛɪɴɢ....")
    # Restart the bot
    await asyncio.sleep(2)
    await sts.delete()
    os.execl(sys.executable, sys.executable, *sys.argv)
    # Edit the message to indicate that the restart is complete
    await client.edit_message_text(chat_id=message.chat.id, message_id=message_id, text="ʀᴇsᴛᴀʀᴛᴇᴅ ᴄᴏᴍᴘʟᴇᴛᴇᴅ!")
    # Delete the message after 60 seconds
    await asyncio.sleep(10)
    await client.delete_messages(chat_id=message.chat.id, message_ids=[message_id])

@Client.on_message(filters.command("id"))
async def send_user_id(client, message):
    if message.reply_to_message:
        replied_user = message.reply_to_message.from_user
        chat_id = message.chat.id
        try:
            chat_title = await client.get_chat(chat_id)
            chat_type = chat_title.chat.type
            chat_name = chat_title.chat.title
        except Exception as e:
            chat_type = "Unknown"
            chat_name = "Unknown"

        await message.reply_text(f"**User ID:** {replied_user.id}\n**User Name:** {replied_user.first_name} {replied_user.last_name}\n**User Mention:** @{replied_user.username}\n**Chat ID:** {chat_id}\n**Chat Type:** {chat_type}\n**Chat Name:** {chat_name}")

    else:
        await message.reply_text(f"**Your ID:** {message.from_user.id}\n**Your Name:** {message.from_user.first_name} {message.from_user.last_name}\n**Your Mention:** @{message.from_user.username}")

@Client.on_message(filters.forwarded & filters.command("id") & filters.reply)
async def send_forwarded_user_channel_id(client, message):
    try:
        forwarded_message = message.forward_from_message
        forwarded_user = forwarded_message.from_user
        forwarded_chat_id = forwarded_message.chat.id
        forwarded_chat_title = await client.get_chat(forwarded_chat_id)
        forwarded_chat_type = forwarded_chat_title.chat.type
        forwarded_chat_name = forwarded_chat_title.chat.title

        await message.reply_text(f"**Forwarded User ID:** {forwarded_user.id}\n**Forwarded User Name:** {forwarded_user.first_name} {forwarded_user.last_name}\n**Forwarded Chat ID:** {forwarded_chat_id}\n**Forwarded Chat Type:** {forwarded_chat_type}\n**Forwarded Chat Name:** {forwarded_chat_name}")
    except Exception as e:
        await message.reply_text("Unable to get information from forwarded message.")

@Client.on_message(filters.command("donate"))
async def donate(client, message):
    await message.reply_text(f"ʜᴇʏ {message.from_user.mention}\nᴅᴏɴᴀᴛᴇ ɪғ ʏᴏᴜ ᴄᴀɴ, ᴜᴘɪ ɪᴅ:- <code>zenistu@ibl</code>")
            

@Client.on_message(filters.command(["info"]))
async def user_info(client, message):
    status_message = await message.reply_text("`ᴩʟᴇᴀꜱᴇ ᴡᴀɪᴛ....`")
    from_user = None
    from_user_id, _ = extract_user(message)
    try:
        from_user = await client.get_users(from_user_id)
    except Exception as error:
        return await status_message.edit(str(error))
    if from_user is None:
        return await status_message.edit("ɴᴏ ᴠᴀʟɪᴅ ᴜsᴇʀ_ɪᴅ / ᴍᴇssᴀɢᴇ sᴘᴇᴄɪғɪᴇᴅ")
    message_out_str = ""
    message_out_str += f"<b>➲ꜰɪʀꜱᴛ ɴᴀᴍᴇ:</b> {from_user.first_name}\n"
    last_name = from_user.last_name or "<b>ɴᴏɴᴇ</b>"
    message_out_str += f"<b>➲ʟᴀꜱᴛ ɴᴀᴍᴇ:</b> {last_name}\n"
    message_out_str += f"<b>➲ᴛɢ-ɪᴅ:</b> <code>{from_user.id}</code>\n"
    username = from_user.username or "<b>ɴᴏɴᴇ</b>"
    dc_id = from_user.dc_id or "[ᴜꜱᴇʀ ᴅᴏꜱᴇ'ᴛ ʜᴀᴠᴇ ᴀ ᴠᴀʟɪᴅ ᴅᴩ]"
    message_out_str += f"<b>➲ᴅᴄ-ɪᴅ:</b> <code>{dc_id}</code>\n"
    message_out_str += f"<b>➲ᴜꜱᴇʀɴᴀᴍᴇ:</b> @{username}\n"
    message_out_str += f"<b>➲ᴜꜱᴇʀ ʟɪɴᴋ:</b> <a href='tg://user?id={from_user.id}'><b>ᴄʟɪᴄᴋ ʜᴇʀᴇ</b></a>\n"
    if message.chat.type in ((enums.ChatType.SUPERGROUP, enums.ChatType.CHANNEL)):
        try:
            chat_member_p = await message.chat.get_member(from_user.id)
            joined_date = (chat_member_p.joined_date or datetime.now()).strftime("%Y.%m.%d %H:%M:%S")
            message_out_str += f"<b>➲ᴊᴏɪɴᴇᴅ ᴛʜɪꜱ ᴄʜᴀᴛ ᴏɴ:</b> <code>{joined_date}</code>\n"
        except UserNotParticipant: pass
    chat_photo = from_user.photo
    if chat_photo:
        local_user_photo = await client.download_media(message=chat_photo.big_file_id)
        buttons = [[InlineKeyboardButton('ᴄʟᴏꜱᴇ ', callback_data='close_data')]]
        await message.reply_photo(
            photo=local_user_photo,
            quote=True,
            reply_markup=InlineKeyboardMarkup(buttons),
            caption=message_out_str,
            parse_mode=enums.ParseMode.HTML,
            disable_notification=True
        )
        os.remove(local_user_photo)
    else:
        buttons = [[InlineKeyboardButton('ᴄʟᴏꜱᴇ ', callback_data='close_data')]]
        await message.reply_text(
            text=message_out_str,
            reply_markup=InlineKeyboardMarkup(buttons),
            quote=True,
            parse_mode=enums.ParseMode.HTML,
            disable_notification=True
        )
    await status_message.delete()
