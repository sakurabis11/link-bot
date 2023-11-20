from pyrogram import Client, filters, enums
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
import logging, re, asyncio, time, shutil, psutil, os, sys
from datetime import datetime
from Script import script
from info import ADMINS, SUPPORT_CHAT
from utils import get_size, temp

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

@Client.on_message(filters.command('id'))
async def show_id(client, message):
    chat_type = message.chat.type
    if chat_type == enums.ChatType.PRIVATE:
        user_id = message.chat.id
        first = message.from_user.first_name
        last = message.from_user.last_name or ""
        username = message.from_user.username
        dc_id = message.from_user.dc_id or ""
        await message.reply_text(f"<b>➲ ꜰɪʀꜱᴛ ɴᴀᴍᴇ:</b> {first}\n<b>➲ ʟᴀꜱᴛ ɴᴀᴍᴇ:</b> {last}\n<b>➲ ᴜꜱᴇʀɴᴀᴍᴇ:</b> {username}\n<b>➲ ᴛᴇʟᴇɢʀᴀᴍ ɪᴅ:</b> <code>{user_id}</code>\n<b>➲ ᴅᴄ ɪᴅ:</b> <code>{dc_id}</code>", quote=True)

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        _id = ""
        _id += f"<b>➲ ᴄʜᴀᴛ ɪᴅ</b>: <code>{message.chat.id}</code>\n"
        
        if message.reply_to_message:
            _id += (
                "<b>➲ ᴜꜱᴇʀ ɪᴅ</b>: "
                f"<code>{message.from_user.id if message.from_user else 'Anonymous'}</code>\n"
                "<b>➲ ʀᴇᴩʟɪᴇᴅ ᴜꜱᴇʀ ɪᴅ</b>: "
                f"<code>{message.reply_to_message.from_user.id if message.reply_to_message.from_user else 'Anonymous'}</code>\n"
            )
            file_info = get_file_id(message.reply_to_message)
        else:
            _id += (
                "<b>➲ ᴜꜱᴇʀ ɪᴅ</b>: "
                f"<code>{message.from_user.id if message.from_user else 'Anonymous'}</code>\n"
            )
            file_info = get_file_id(message)
        if file_info:
            _id += (
                f"<b>{file_info.message_type}</b>: "
                f"<code>{file_info.file_id}</code>\n"
            )
        await message.reply_text(_id, quote=True)
            

@Client.on_message(filters.command("info"))
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
        buttons = [[InlineKeyboardButton('ᴄʟᴏꜱᴇ ✘', callback_data='close_data')]]
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

@Client.on_message(filters.command('leave') & filters.user(ADMINS))
async def leave_a_chat(bot, message):
    if len(message.command) == 1: return await message.reply('Gɪᴠᴇ Mᴇ A Cʜᴀᴛ Iᴅ')
    chat = message.command[1]
    try: chat = int(chat)
    except: chat = chat
    try:
        buttons = [[InlineKeyboardButton('Sᴜᴩᴩᴏʀᴛ', url=f'https://t.me/{SUPPORT_CHAT}')]]
        await bot.send_message(chat_id=chat, text='<b>Hᴇʟʟᴏ Fʀɪᴇɴᴅs, \nMʏ Aᴅᴍɪɴ Hᴀs Tᴏʟᴅ Mᴇ Tᴏ Lᴇᴀᴠᴇ Fʀᴏᴍ Gʀᴏᴜᴘ Sᴏ I Gᴏ! Iғ Yᴏᴜ Wᴀɴɴᴀ Aᴅᴅ Mᴇ Aɢᴀɪɴ Cᴏɴᴛᴀᴄᴛ Mʏ Sᴜᴘᴘᴏʀᴛ Gʀᴏᴜᴘ</b>', reply_markup=InlineKeyboardMarkup(buttons))
        await bot.leave_chat(chat)
    except Exception as e:
        await message.reply(f'Eʀʀᴏʀ: {e}')

@Client.on_message(filters.command('disable') & filters.user(ADMINS))
async def disable_chat(bot, message):
    if len(message.command) == 1: return await message.reply('Gɪᴠᴇ Mᴇ A Cʜᴀᴛ Iᴅ')
    r = message.text.split(None)
    if len(r) > 2:
        reason = message.text.split(None, 2)[2]
        chat = message.text.split(None, 2)[1]
    else:
        chat = message.command[1]
        reason = "No Reason Provided"
    try:
        chat_ = int(chat)
    except:
        return await message.reply('Gɪᴠᴇ Mᴇ A Vᴀʟɪᴅ Cʜᴀᴛ ID')
    cha_t = await db.get_chat(int(chat_))
    if not cha_t:
        return await message.reply("Cʜᴀᴛ Nᴏᴛ Fᴏᴜɴᴅ Iɴ DB")
    if cha_t['is_disabled']:
        return await message.reply(f"Tʜɪꜱ Cʜᴀᴛ Is Aʟʀᴇᴅʏ  Dɪꜱᴀʙʟᴇᴅ:\nRᴇᴀꜱᴏɴ: <code> {cha_t['reason']} </code>")
    await db.disable_chat(int(chat_), reason)
    temp.BANNED_CHATS.append(int(chat_))
    await message.reply('Cʜᴀᴛ Sᴜᴄᴄᴇꜱꜰᴜʟʟʏ Dɪꜱᴀʙʟᴇᴅ')
    try:
        buttons = [[InlineKeyboardButton('Sᴜᴩᴩᴏʀᴛ', url=f'https://t.me/{SUPPORT_CHAT}')]]
        await bot.send_message(chat_id=chat_,  text=f'<b>Hᴇʟʟᴏ Fʀɪᴇɴᴅs, \nᴍʏ Aᴅᴍɪɴ Hᴀs Tᴏʟᴅ Mᴇ Tᴏ Lᴇᴀᴠᴇ Fʀᴏᴍ Gʀᴏᴜᴘ Sᴏ I Gᴏ! Iғ Yᴏᴜ Wᴀɴɴᴀ Aᴅᴅ Mᴇ Aɢᴀɪɴ Cᴏɴᴛᴀᴄᴛ Mʏ Sᴜᴘᴘᴏʀᴛ Gʀᴏᴜᴘ.</b> \nRᴇᴀꜱᴏɴ : <code>{reason}</code>', reply_markup=InlineKeyboardMarkup(buttons))
        await bot.leave_chat(chat_)
    except Exception as e:
        await message.reply(f"Eʀʀᴏʀ: {e}")

  @Client.on_message(filters.command('ban') & filters.user(ADMINS))
async def ban_a_user(bot, message):
    if len(message.command) == 1: return await message.reply('Gɪᴠᴇ Mᴇ A Uꜱᴇʀ Iᴅ / Uꜱᴇʀɴᴀᴍᴇ')
    r = message.text.split(None)
    if len(r) > 2:
        reason = message.text.split(None, 2)[2]
        chat = message.text.split(None, 2)[1]
    else:
        chat = message.command[1]
        reason = "No reason Provided"
    try: chat = int(chat)
    except: pass
    try: k = await bot.get_users(chat)
    except PeerIdInvalid: return await message.reply("Tʜɪs Is Aɴ Iɴᴠᴀʟɪᴅ Usᴇʀ, Mᴀᴋᴇ Sᴜʀᴇ Iᴀ Hᴀᴠᴇ Mᴇᴛ Hɪᴍ Bᴇғᴏʀᴇ")
    except IndexError: return await message.reply("Tʜɪs Mɪɢʜᴛ Bᴇ A Cʜᴀɴɴᴇʟ, Mᴀᴋᴇ Sᴜʀᴇ Iᴛs A Usᴇʀ.")
    except Exception as e: return await message.reply(f'Eʀʀᴏʀ: {e}')
    else:
        jar = await db.get_ban_status(k.id)
        if jar['is_banned']: return await message.reply(f"{k.mention} Iꜱ Aʟʀᴇᴅʏ Bᴀɴɴᴇᴅ\nRᴇᴀꜱᴏɴ: {jar['ban_reason']}")
        await db.ban_user(k.id, reason)
        temp.BANNED_USERS.append(k.id)
        await message.reply(f"Sᴜᴄᴄᴇꜱꜰᴜʟʟʏ Bᴀɴɴᴇᴅ {k.mention}")

@Client.on_message(filters.command('unban_user') & filters.user(ADMINS))
async def unban_a_user(bot, message):
    if len(message.command) == 1: return await message.reply('Gɪᴠᴇ Mᴇ A Uꜱᴇʀ Iᴅ / Uꜱᴇʀɴᴀᴍᴇ')
    r = message.text.split(None)
    if len(r) > 2:
        reason = message.text.split(None, 2)[2]
        chat = message.text.split(None, 2)[1]
    else:
        chat = message.command[1]
        reason = "No reason Provided"
    try: chat = int(chat)
    except: pass
    try: k = await bot.get_users(chat)
    except PeerIdInvalid: return await message.reply("Tʜɪs Is Aɴ Iɴᴠᴀʟɪᴅ Usᴇʀ, Mᴀᴋᴇ Sᴜʀᴇ Iᴀ Hᴀᴠᴇ Mᴇᴛ Hɪᴍ Bᴇғᴏʀᴇ")
    except IndexError: return await message.reply("Tʜɪs Mɪɢʜᴛ Bᴇ A Cʜᴀɴɴᴇʟ, Mᴀᴋᴇ Sᴜʀᴇ Iᴛs A Usᴇʀ.")
    except Exception as e: return await message.reply(f'Eʀʀᴏʀ: {e}')
    else:
        jar = await db.get_ban_status(k.id)
        if not jar['is_banned']: return await message.reply(f"{k.mention} Iꜱ Nᴏᴛ Yᴇᴛ Bᴀɴɴᴇᴅ")
        await db.remove_ban(k.id)
        temp.BANNED_USERS.remove(k.id)
        await message.reply(f"Sᴜᴄᴄᴇꜱꜰᴜʟʟʏ Uɴʙᴀɴɴᴇᴅ {k.mention}")

@Client.on_message(filters.command('logs') & filters.user(ADMINS))
async def log_file(bot, msg):
    try: await message.reply_document('BotLog.txt')
    except Exception as e: await message.reply(str(e))


@Client.on_message(filters.command("restart") & filters.user(ADMINS))
async def restart_bot(bot, msg):
    await msg.reply("Rᴇꜱᴛᴀᴛɪɴɢ........")
    await asyncio.sleep(2)
    await sts.delete()
    os.execl(sys.executable, sys.executable, *sys.argv)
