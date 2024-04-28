from pyrogram import enums, filters, Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message

@Client.on_message(filters.command("start"))
async def start(client, message: Message):
    mine = await client.get_me()
    button = [[ InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ", url="https://t.me/sd_bots"),
                ],[
                InlineKeyboardButton("ʜᴇʟᴘ" , callback_data='help') ,
                InlineKeyboardButton("ᴀʙᴏᴜᴛ" , callback_data='about')
            ]]
    await client.send_message(chat_id=message.chat.id, text=f"**__Hello {message.from_user.mention}__**", reply_markup=InlineKeyboardMarkup(button), disable_web_page_preview=True)

@Client.on_callback_query()
async def callback_handle(client, query):
    if query.data == 'start':
            button = [[ InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ", url="https://t.me/sd_bots"),
                ],[
                InlineKeyboardButton("ʜᴇʟᴘ" , callback_data='help') ,
                InlineKeyboardButton("ᴀʙᴏᴜᴛ" , callback_data='about')
            ]]
            reply_markup = InlineKeyboardMarkup(buttons)
            await query.message.edit_text(chat_id=message.chat.id, text=f"**__Hello {message.from_user.mention}__**", reply_markup=reply_markup, parse_mode=enums.ParseMode.HTML)
        
    elif query.data == 'help':
        buttons = [[
         InlineKeyboardButton('ɢᴏᴏɢʟᴇ ᴀɪ', callback_data='google'),
         ],[
         InlineKeyboardButton('sᴏɴɢ', callback_data='song'),
         InlineKeyboardButton('ɪɴsᴛᴀ', callback_data='insta'),
         InlineKeyboardButton('ᴅᴏɴᴀᴛᴇ', callback_data='donate'),
         ],[
         InlineKeyboardButton('ʜᴏᴍᴇ', callback_data='start'),
         InlineKeyboardButton('ᴄʟᴏsᴇ', callback_data='close')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text("ᴛʜᴇsᴇ ᴀʀᴇ ʜᴇʟᴘ ʙᴜᴛᴛᴏɴs", reply_markup=reply_markup, parse_mode=enums.ParseMode.HTML)

    elif query.data == 'google':
        buttons = buttons = [[
            InlineKeyboardButton('ʜᴏᴍᴇ', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text("/ai {ᴜʀ ǫᴜᴇsᴛɪᴏɴ}", reply_markup=reply_markup, parse_mode=enums.ParseMode.HTML)

    elif query.data == 'song':
        buttons = buttons = [[
            InlineKeyboardButton('ʜᴏᴍᴇ', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text("/song {song_name} .ᴅᴏᴡɴʟᴏᴀᴅ sᴏɴɢ ғʀᴏᴍ ʏᴏᴜᴛᴜʙᴇ ᴏʀ ᴜsᴇ /song {ʏᴛ_ʟɪɴᴋ} ᴏʀ ᴊᴜsᴛ sᴇɴᴅ ᴛʜᴇ ʏᴛ ʟɪɴᴋ", reply_markup=reply_markup, parse_mode=enums.ParseMode.HTML)

    elif query.data == 'insta':
        buttons = buttons = [[
            InlineKeyboardButton('ʜᴏᴍᴇ', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text("sᴇɴᴅ ɪɴsᴛᴀɢʀᴀᴍ ʀᴇᴇʟ,sᴛᴏʀɪᴇs ᴀɴᴅ ᴘᴏsᴛ ʟɪɴᴋ ᴛᴏ ᴛʜɪs ʙᴏᴛ, ғᴏʀ ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ, ᴘᴜʙʟɪᴄ ᴏɴʟʏ", reply_markup=reply_markup, parse_mode=enums.ParseMode.HTML)

    elif query.data == 'donate':
        buttons = buttons = [[
            InlineKeyboardButton('ʜᴏᴍᴇ', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(f"ʜᴇʏ {message.from_user.mention}\nᴅᴏɴᴀᴛᴇ ɪғ ʏᴏᴜ ᴄᴀɴ, ᴜᴘɪ ɪᴅ:- <code>zenistu@ibl</code>", reply_markup=reply_markup, parse_mode=enums.ParseMode.HTML)

    elif query.data == 'close':
        await query.message.delete()
        edited_keyboard = InlineKeyboardMarkup([])
        await query.answer()
        await query.message.edit_reply_markup(edited_keyboard)
