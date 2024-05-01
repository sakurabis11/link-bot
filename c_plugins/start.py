from pyrogram import enums , filters , Client
from pyrogram.types import InlineKeyboardButton , InlineKeyboardMarkup , CallbackQuery , Message
from info import DATABASE_URI, DATABASE_NAME, LOG_CHANNEL_INFORM, LOG_CHANNEL_ERROR
from pymongo import MongoClient
from pyrogram.errors.exceptions.bad_request_400 import ButtonUserPrivacyRestricted

client = MongoClient(DATABASE_URI)
db = client[DATABASE_NAME]
collection = db["clone_bots"]


@Client.on_message(filters.command("start"))
async def start(client , message: Message):
    try:
        me = await client.get_me()
        user_id = message.from_user.id
        first_name = message.from_user.first_name or "Unknown"
        button = [[
            InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ" , url="https://t.me/sd_bots") ,
        ] , [
            InlineKeyboardButton("ʜᴇʟᴘ" , callback_data="help") ,
            InlineKeyboardButton("ᴀʙᴏᴜᴛ" , callback_data="about") ,
        ]]
        reply_markup = InlineKeyboardMarkup(button)
        await message.reply_text(f"ʜɪ {message.from_user.mention}\nᴄʟɪᴄᴋ ʜᴇʟᴘ ʙᴜᴛṭᴏɴs" , reply_markup=reply_markup)
    except Exception as e:
        await client.send_message(LOG_CHANNEL_ERROR, text=f"#Error_in_start_cmd\n\nBot: @{me.username}\n\nError: {e}")

@Client.on_message(filters.command("help"))
async def help(client, message: Message):
    try:
        me = await client.get_me()
        buttons = [[
            InlineKeyboardButton('ɢᴏᴏɢʟᴇ ᴀɪ' , callback_data='google') ,
        ] , [
            InlineKeyboardButton('sᴏɴɢ' , callback_data='song') ,
            InlineKeyboardButton('ɪɴsᴛᴀ' , callback_data='insta') ,
            InlineKeyboardButton('ᴠɪᴅᴇᴏ ᴛᴏ ᴀᴜᴅɪᴏ' , callback_data='convert')
        ] , [
            InlineKeyboardButton('ᴅᴏɴᴀᴛᴇ' , callback_data='donate')
        ] , [
            InlineKeyboardButton('ʜᴏᴍᴇ' , callback_data='start') ,
            InlineKeyboardButton('ᴄʟᴏsᴇ' , callback_data='close')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_text("ᴛʜᴇsᴇ ᴀʀᴇ ʜᴇʟᴘ ʙᴜᴛᴛᴏɴs" , reply_markup=reply_markup ,
                                      parse_mode=enums.ParseMode.HTML) 
    except Exception as e:
        await client.send_message(LOG_CHANNEL_ERROR, text=f"#Error_in_help_cmd\n\nBot: @{me.username}\n\nError: {e}")

@Client.on_message(filters.command("about"))
async def about(client, message: Message):
        try:
                me = await client.get_me()
                bot_username = me.username
                bot_info = collection.find_one({"username": bot_username.strip("@")})
                buttons = [[
                    InlineKeyboardButton("ᴄʟᴏɴᴇ ʟᴏɢ ᴄʜᴀɴɴᴇʟ" , url="https://t.me/+nAFYw7r7C8xiMzU1"),
                    InlineKeyboardButton("ᴇʀʀᴏʀs ғʀᴏᴍ ᴄʟᴏɴᴇ ʙᴏᴛ" , url="https://t.me/+cKp_xa58vxZhNWE1")
                    ],[
                    InlineKeyboardButton('Home' , callback_data='start') ,
                    InlineKeyboardButton('close' , callback_data='close')
                ]]
                reply_markup = InlineKeyboardMarkup(buttons)
                await message.reply_text(
                    f"✯ᴍʏ ɴᴀᴍᴇ: {me.first_name}\n\n✯ Lɪʙʀᴀʀʏ: <a href='https://docs.pyrogram.org/'>Pʏʀᴏɢʀᴀᴍ</a>\n✯ Lᴀɴɢᴜᴀɢᴇ: <a href='https://www.python.org/download/releases/3.0/'>Pʏᴛʜᴏɴ 3</a>\n\n✯ ᴄʟᴏɴᴇᴅ ғʀᴏᴍ: @mrtgcoderbot" ,
                    reply_markup=reply_markup , parse_mode=enums.ParseMode.HTML , disable_web_page_preview=True)

        except Exception as e:
            await client.send_message(LOG_CHANNEL_ERROR, text=f"#Error_in_about_cmd\n\nBot: @{me.username}\n\nError: {e}")    

@Client.on_callback_query()
async def callback_handle(client , query):
    if query.data == 'start':
        buttons = [[
            InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ" , url="https://t.me/sd_bots") ,
        ] , [
            InlineKeyboardButton("ʜᴇʟᴘ" , callback_data='help') ,
            InlineKeyboardButton("ᴀʙᴏᴜᴛ" , callback_data='about')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(f"Hello {query.from_user.mention}\nᴄʟɪᴄᴋ ʜᴇʟᴘ ʙᴜᴛᴛᴏɴs" ,
                                      reply_markup=reply_markup ,
                                      parse_mode=enums.ParseMode.HTML)

    elif query.data == 'help':
        buttons = [[
            InlineKeyboardButton('ɢᴏᴏɢʟᴇ ᴀɪ' , callback_data='google') ,
        ] , [
            InlineKeyboardButton('sᴏɴɢ' , callback_data='song') ,
            InlineKeyboardButton('ɪɴsᴛᴀ' , callback_data='insta') ,
            InlineKeyboardButton('ᴠɪᴅᴇᴏ ᴛᴏ ᴀᴜᴅɪᴏ' , callback_data='convert')
        ] , [
            InlineKeyboardButton('ᴅᴏɴᴀᴛᴇ' , callback_data='donate')
        ] , [
            InlineKeyboardButton('ʜᴏᴍᴇ' , callback_data='start') ,
            InlineKeyboardButton('ᴄʟᴏsᴇ' , callback_data='close')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text("ᴛʜᴇsᴇ ᴀʀᴇ ʜᴇʟᴘ ʙᴜᴛᴛᴏɴs" , reply_markup=reply_markup ,
                                      parse_mode=enums.ParseMode.HTML)

    elif query.data == 'google':
        buttons = buttons = [[
            InlineKeyboardButton('ʜᴏᴍᴇ' , callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text("/ai {ᴜʀ ǫᴜᴇsᴛɪᴏɴ}" , reply_markup=reply_markup , parse_mode=enums.ParseMode.HTML)

    elif query.data == 'song':
        buttons = buttons = [[
            InlineKeyboardButton('ʜᴏᴍᴇ' , callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            "/song {song_name} .ᴅᴏᴡɴʟᴏᴀᴅ sᴏɴɢ ғʀᴏᴍ ʏᴏᴜᴛᴜʙᴇ ᴏʀ ᴜsᴇ /song {ʏᴛ_ʟɪɴᴋ} ᴏʀ ᴊᴜsᴛ sᴇɴᴅ ᴛʜᴇ ʏᴛ ʟɪɴᴋ" ,
            reply_markup=reply_markup , parse_mode=enums.ParseMode.HTML)

    elif query.data == 'insta':
        buttons = buttons = [[
            InlineKeyboardButton('ʜᴏᴍᴇ' , callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            "sᴇɴᴅ ɪɴsᴛᴀɢʀᴀᴍ ʀᴇᴇʟ,sᴛᴏʀɪᴇs ᴀɴᴅ ᴘᴏsᴛ ʟɪɴᴋ ᴛᴏ ᴛʜɪs ʙᴏᴛ, ғᴏʀ ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ, ᴘᴜʙʟɪᴄ ᴏɴʟʏ" ,
            reply_markup=reply_markup , parse_mode=enums.ParseMode.HTML)

    elif query.data == 'donate':
        buttons = buttons = [[
            InlineKeyboardButton('ʜᴏᴍᴇ' , callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            f"ʜᴇʏ {query.from_user.mention}\nᴅᴏɴᴀᴛᴇ ɪғ ʏᴏᴜ ᴄᴀɴ, ᴜᴘɪ ɪᴅ:- <code>zenistu@ibl</code>" ,
            reply_markup=reply_markup , parse_mode=enums.ParseMode.HTML)

    elif query.data == 'convert':
        buttons = buttons = [[
            InlineKeyboardButton('ʜᴏᴍᴇ' , callback_data='next')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            f"ʜᴇʏ {query.from_user.mention}\nɪ ᴄᴀɴ ᴄᴏɴᴠᴇʀᴛ ᴠɪᴅᴇᴏ ᴛᴏ ᴀᴜᴅɪᴏ.\nᴊᴜsᴛ sᴇɴᴅ ᴀ ᴠɪᴅᴇᴏ ᴛᴏ ᴛʜᴇ ʙᴏᴛ ᴀɴᴅ sᴇɴᴅ /convert ᴛᴏ ᴛʜᴇ ᴠɪᴅᴇᴏ.sᴜᴘᴘᴏᴛ ᴏɴʟʏ ᴠɪᴅᴇᴏ" ,
            reply_markup=reply_markup , parse_mode=enums.ParseMode.HTML)

    elif query.data == 'about':
        try:
            me = await client.get_me()
            bot_username = me.username

            bot_info = collection.find_one({"username": bot_username.strip("@")})
            if bot_info:
                user_fname = bot_info.get("user_fname")
                user_id = bot_info.get("user_id")
                user_f_name = user_fname[0]
                user_id_str = str(user_id)
                user = user_id_str.replace("(" , "").replace("," , "").replace(")" , "")
                u_bot = bot_username.strip("@")
                try:
                    buttons = [[
                        InlineKeyboardButton('owner' , user_id=int(user)) ,
                        ],[
                        InlineKeyboardButton("ᴄʟᴏɴᴇ ʟᴏɢ ᴄʜᴀɴɴᴇʟ" , url="https://t.me/+nAFYw7r7C8xiMzU1"),
                        InlineKeyboardButton("ᴇʀʀᴏʀs ғʀᴏᴍ ᴄʟᴏɴᴇ ʙᴏᴛ" , url="https://t.me/+cKp_xa58vxZhNWE1")
                        ],[
                        InlineKeyboardButton('Home' , callback_data='start') ,
                        InlineKeyboardButton('close' , callback_data='close')
                    ]]
                    reply_markup = InlineKeyboardMarkup(buttons)
                    await query.message.edit_text(
                        f"✯ᴍʏ ɴᴀᴍᴇ: <a href='https://t.me/{u_bot}'>{me.first_name}</a>\n\n"
                        f"✯ ᴏᴡɴᴇʀ: <a href='tg://user?id={user}'><b>{user_f_name}</b></a>\n"
                        f"✯ Lɪʙʀᴀʀʏ: <a href='https://docs.pyrogram.org/'>Pʏʀᴏɢʀᴀᴍ</a>\n"
                        f"✯ Lᴀɴɢᴜᴀɢᴇ: <a href='https://www.python.org/download/releases/3.0/'>Pʏᴛʜᴏɴ 3</a>\n\n"
                        f"✯ ᴄʟᴏɴᴇᴅ ғʀᴏᴍ: @mrtgcoderbot" ,
                        reply_markup=reply_markup , parse_mode=enums.ParseMode.HTML , disable_web_page_preview=True)
                except ButtonUserPrivacyRestricted:
                    buttons = [[
                        InlineKeyboardButton("ᴄʟᴏɴᴇ ʟᴏɢ ᴄʜᴀɴɴᴇʟ" , url="https://t.me/+nAFYw7r7C8xiMzU1"),
                        InlineKeyboardButton("ᴇʀʀᴏʀs ғʀᴏᴍ ᴄʟᴏɴᴇ ʙᴏᴛ" , url="https://t.me/+cKp_xa58vxZhNWE1")
                        ],[
                        InlineKeyboardButton('Home' , callback_data='start') ,
                        InlineKeyboardButton('close' , callback_data='close')
                    ]]
                    reply_markup = InlineKeyboardMarkup(buttons)
                    await query.message.edit_text(
                        f"✯ᴍʏ ɴᴀᴍᴇ: <a href='https://t.me/{u_bot}'>{me.first_name}</a>\n\n"
                        f"✯ ᴏᴡɴᴇʀ: <a href='tg://user?id={user}'><b>{user_f_name}</b></a>\n"
                        f"✯ Lɪʙʀᴀʀʏ: <a href='https://docs.pyrogram.org/'>Pʏʀᴏɢʀᴀᴍ</a>\n"
                        f"✯ Lᴀɴɢᴜᴀɢᴇ: <a href='https://www.python.org/download/releases/3.0/'>Pʏᴛʜᴏɴ 3</a>\n\n"
                        f"✯ ᴄʟᴏɴᴇᴅ ғʀᴏᴍ: @mrtgcoderbot" ,
                        reply_markup=reply_markup , parse_mode=enums.ParseMode.HTML , disable_web_page_preview=True)
            else:
                await query.message.edit_text("Sorry, couldn't retrieve bot information. Please try again later.")
        except Exception as e:
            print(f"Error processing about query: {e}")

    elif query.data == 'close':
        await query.message.delete()
        edited_keyboard = InlineKeyboardMarkup([])
        await query.answer()
        await query.message.edit_reply_markup(edited_keyboard)
