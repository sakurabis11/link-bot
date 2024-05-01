from pyrogram import enums, filters, Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message
from datetime import datetime  # Import datetime for timestamps
from pymongo import MongoClient

# Replace with your actual MongoDB connection details
DATABASE_URI = "mongodb://localhost:27017/"  # Connection string (replace with yours)
DATABASE_NAME = "your_database_name"  # Database name (replace with yours)

client = MongoClient(DATABASE_URI)
db = client[DATABASE_NAME]
collection = db["clone_bots"]  

@Client.on_message(filters.command("start"))
async def start(client, message: Message):
  try:
    user_id = message.from_user.id
    first_name = message.from_user.first_name or "Unknown"
    button = [[
        InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ", url="https://t.me/sd_bots"),
    ], [
        InlineKeyboardButton("ʜᴇʟᴘ", callback_data="help"),
        InlineKeyboardButton("ᴀʙᴏᴜᴛ", callback_data="about"),
    ]]
    reply_markup = InlineKeyboardMarkup(button)
    await message.reply_text(f"ʜɪ {message.from_user.mention}\nᴄʟɪᴄᴋ ʜᴇʟᴘ ʙᴜᴛṭᴏɴs", reply_markup=reply_markup)
  except Exception as e:
    print(e)

@Client.on_callback_query()
async def callback_handle(client, query):
    if query.data == 'start':
        buttons = [[ 
         InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ", url="https://t.me/sd_bots"),
        ],[
        InlineKeyboardButton("ʜᴇʟᴘ" , callback_data='help') ,
        InlineKeyboardButton("ᴀʙᴏᴜᴛ" , callback_data='about')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(f"Hello {query.from_user.mention}\nᴄʟɪᴄᴋ ʜᴇʟᴘ ʙᴜᴛᴛᴏɴs",
                                       reply_markup=reply_markup,
                                       parse_mode=enums.ParseMode.HTML)
        
    elif query.data == 'help':
        buttons = [[
         InlineKeyboardButton('ɢᴏᴏɢʟᴇ ᴀɪ', callback_data='google'),
         ],[
         InlineKeyboardButton('sᴏɴɢ', callback_data='song'),
         InlineKeyboardButton('ɪɴsᴛᴀ', callback_data='insta'),
         InlineKeyboardButton('ᴠɪᴅᴇᴏ ᴛᴏ ᴀᴜᴅɪᴏ', callback_data='convert')
         ],[
         InlineKeyboardButton('ᴅᴏɴᴀᴛᴇ', callback_data='donate')
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
        await query.message.edit_text(f"ʜᴇʏ {query.from_user.mention}\nᴅᴏɴᴀᴛᴇ ɪғ ʏᴏᴜ ᴄᴀɴ, ᴜᴘɪ ɪᴅ:- <code>zenistu@ibl</code>", reply_markup=reply_markup, parse_mode=enums.ParseMode.HTML)

    elif query.data == 'convert':
        buttons = buttons = [[
            InlineKeyboardButton('ʜᴏᴍᴇ', callback_data='next')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(f"ʜᴇʏ {query.from_user.mention}\nɪ ᴄᴀɴ ᴄᴏɴᴠᴇʀᴛ ᴠɪᴅᴇᴏ ᴛᴏ ᴀᴜᴅɪᴏ.\nᴊᴜsᴛ sᴇɴᴅ ᴀ ᴠɪᴅᴇᴏ ᴛᴏ ᴛʜᴇ ʙᴏᴛ ᴀɴᴅ sᴇɴᴅ /convert ᴛᴏ ᴛʜᴇ ᴠɪᴅᴇᴏ.sᴜᴘᴘᴏᴛ ᴏɴʟʏ ᴠɪᴅᴇᴏ", reply_markup=reply_markup, parse_mode=enums.ParseMode.HTML)
        
   
elif query.data == 'about':
  try:
    me = await client.get_me()
    bot_username = me.username
    bot_info = collection.find_one({"username": bot_username.strip("@")})

    if bot_info:
      me = client.get_me()
      user_fname = bot_info.get("user_fname"),
      user_id = bot_info.get("user_id")
      user_f_name = user_fname[0]
      user_id_str = str(user_id)
      user = user_id_str.replace("(", "").replace(",", "").replace(")", "")

      buttons = [[
          InlineKeyboardButton('Home', callback_data='start'),
          InlineKeyboardButton('close', callback_data='close')
      ]]
      reply_markup = InlineKeyboardMarkup(buttons)
      await query.message.edit_text(f"✯ ᴏᴡɴᴇʀ: <a href='tg://user?id={user}'><b>{user_f_name}</b></a>\n✯ Lɪʙʀᴀʀʏ: <a href='https://docs.pyrogram.org/'>Pʏʀᴏɢʀᴀᴍ</a>\n✯ Lᴀɴɢᴜᴀɢᴇ: <a href='https://www.python.org/download/releases/3.0/'>Pʏᴛʜᴏɴ 3</a>\n\n✯ ᴄʟᴏɴᴇᴅ ғʀᴏᴍ: @mrtgcoderbot", reply_markup=reply_markup, parse_mode=enums.ParseMode.HTML, disable_web_page_preview=True)
    else:
      buttons = [[
        InlineKeyboardButton('Home' , callback_data='start') ,
        InlineKeyboardButton('close' , callback_data='close')
      ]]
      reply_markup = InlineKeyboardMarkup(buttons)
      await query.message.edit_text(f"✯ᴍʏ ɴᴀᴍᴇ: {me.first_name}\n\n✯ Lɪʙʀᴀʀʏ: <a href='https://docs.pyrogram.org/'>Pʏʀᴏɢʀᴀᴍ</a>\n✯ Lᴀɴɢᴜᴀɢᴇ: <a href='https://www.python.org/download/releases/3.0/'>Pʏᴛʜᴏɴ 3</a>\n\n✯ ᴄʟᴏɴᴇᴅ ғʀᴏᴍ: @mrtgcoderbot", reply_markup=InlineKeyboardMarkup([]))

  except Exception as e:
    print(f"Error processing about query: {e}")
    
    elif query.data == 'close':
        await query.message.delete()
        edited_keyboard = InlineKeyboardMarkup([])
        await query.answer()
        await query.message.edit_reply_markup(edited_keyboard)
