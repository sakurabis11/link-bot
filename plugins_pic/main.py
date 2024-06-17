import pyrogram
from pyrogram import Client , filters , enums
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import *
from pyrogram.types import InlineKeyboardButton , InlineKeyboardMarkup
from pyrogram.errors import UserNotParticipant
from utils import get_size
from Script import script
from pyrogram.errors import PeerIdInvalid
from pyrogram.errors.exceptions.bad_request_400 import MessageTooLong
from info import DATABASE_URI , DATABASE_NAME , LOG_CHANNEL , ADMINS
from database.users_db import sd

HELP_TXT = """How to play ⚡️

Full version of the guide.

💰 Tap to earn
Tap the screen and collect coins.

⛏ Mine
Upgrade bot,card  that will give you passive income opportunities.

👥 Friends
Invite your friends and you’ll get bonuses. Help a friend move to the next leagues and you'll get even more bonuses.

🪙Do daily task and earn 💸

Daily update will be given on community group"""

ABOUT_TXT = """
✯ Developer: <a href='https://t.me/N_A_V_I_P_A_V_I'>꧁࿗༒⚔️ 𝕄𝕣 ℙ𝕣𝕠𝕗𝕖𝕤𝕤𝕠𝕣⚔️༒࿗꧂</a>
✯ Library: <a href='https://docs.pyrogram.org/'>Pyrogram</a>
✯ Language: <a href='https://www.python.org/download/releases/3.0/'>Python 3</a>
✯ Community group: <a href='https://t.me/+5K73cpDNZAY0ZGI1'>Group</a>
"""


@Client.on_message(filters.command("start") & filters.private)
async def start(client , message):
    user_id = message.from_user.id
    if not await sd.is_user_exist(message.from_user.id):
        await sd.add_user(message.from_user.id , message.from_user.first_name)
        await client.send_message(PIC_LOG_CHANNEL ,
                                  script.LOG_TEXT_PI.format(message.from_user.id , message.from_user.mention ,
                                                            message.from_user.id))
    buttons = [[
        InlineKeyboardButton("link" , callback_data="link")
    ] , [
        InlineKeyboardButton("️Help" , callback_data="help") ,
        InlineKeyboardButton("About" , callback_data="about")
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    await message.reply_text(
        text=f"Hello! {message.from_user.mention}\nYou are now the member of a crypto exchange.💰Just tap and earn 💸🤑\nFor more bot link 🖇️ click link 🔗" ,
        reply_markup=reply_markup)


@Client.on_message(filters.command('stats') & filters.private)
async def get_stats(bot , message):
    try:
        user_id = message.from_user.id
        msg = await message.reply('Fetching stats..')
        total_users = await sd.total_users_count()
        totl_chats = await sd.total_chat_count()
        total_count = collection.count_documents({})
        user_count = collection.count_documents({"user_id": user_id})
        size = await sd.get_db_size()
        free = 536870912 - size
        size = get_size(size)
        free = get_size(free)
        await msg.edit(script.STATS_TXT.format(total_users , total_count , user_count , size , free))
    except Exception as e:
        await msg.edit(e)


@Client.on_message(filters.command('users') & filters.user(ADMINS) & filters.private)
async def list_users(bot , message):
    msg = await message.reply('ɢᴇᴛᴛɪɴɢ ᴛʜᴇ ᴜsᴇʀs')
    users = await sd.get_all_users()
    out = "Users Saved In DB Are:\n\n"
    async for user in users:
        out += f"<a href=tg://user?id={user['id']}>{user['name']}</a>"
        if user['ban_status']['is_banned']:
            out += '( Banned User )'
        out += '\n'
    try:
        await msg.edit_text(out)
    except MessageTooLong:
        with open('users.txt' , 'w+') as outfile:
            outfile.write(out)
        await message.reply_document('users.txt' , caption="List Of Users")


@Client.on_message(filters.command("link") & filters.private)
async def link_session(client , message):
    buttons = [[
        InlineKeyboardButton("Hamster Kombat 🐹" ,
                             url="https://t.me/hamsTer_kombat_bot/start?startapp=kentId5450544747") ,
        InlineKeyboardButton("Wave wallet 🔷" , url="https://t.me/waveonsuibot/walletapp?startapp=4858876")
    ] , [
        InlineKeyboardButton("Memefi 🪙" , url="https://t.me/memefi_coin_bot?start=r_3497d11788") ,
        InlineKeyboardButton("Pixelverse 👾" , url="https://t.me/pixelversexyzbot?start=1296817425")
    ] , [
        InlineKeyboardButton("Yescoin💰" , url="https://t.me/theYescoin_bot/Yescoin?startapp=Yt5izz")
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    await message.reply_text(
        text="These are the top crypto bots Earn money 🤑💰" ,
        disable_web_page_preview=True ,
        reply_markup=reply_markup)


@Client.on_callback_query()
async def callback_handle(client , query):
    if query.data == "start":
        buttons = [[
            InlineKeyboardButton("link" , callback_data="link")
        ] , [
            InlineKeyboardButton("️Help" , callback_data="help") ,
            InlineKeyboardButton("About" , callback_data="about")
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=f"Hello! {query.from_user.mention}\nYou are now the member of a crypto exchange.💰Just tap and earn 💸🤑\nFor more bot link 🖇️ click link 🔗" ,
            reply_markup=reply_markup)

    elif query.data == "help":
        buttons = [[
            InlineKeyboardButton("Community Group" , url="https://t.me/+5K73cpDNZAY0ZGI1") ,
            InlineKeyboardButton("Back" , callback_data="start")
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=HELP_TXT ,
            reply_markup=reply_markup)

    elif query.data == "about":
        buttons = [[
            InlineKeyboardButton("Back" , callback_data="start")
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=ABOUT_TXT ,
            disable_web_page_preview=True ,
            reply_markup=reply_markup)

    elif query.data == "link":
        buttons = [[
            InlineKeyboardButton("Hamster Kombat 🐹" ,
                                 url="https://t.me/hamsTer_kombat_bot/start?startapp=kentId5450544747") ,
            InlineKeyboardButton("Wave wallet 🔷" , url="https://t.me/waveonsuibot/walletapp?startapp=4858876")
        ] , [
            InlineKeyboardButton("Memefi 🪙" , url="https://t.me/memefi_coin_bot?start=r_3497d11788") ,
            InlineKeyboardButton("Pixelverse 👾" , url="https://t.me/pixelversexyzbot?start=1296817425")
        ] , [
            InlineKeyboardButton("Yescoin💰" , url="https://t.me/theYescoin_bot/Yescoin?startapp=Yt5izz")
        ] , [
            InlineKeyboardButton("Back" , callback_data="start")
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text="These are the top crypto bots Earn money 🤑💰" ,
            disable_web_page_preview=True ,
            reply_markup=reply_markup)

