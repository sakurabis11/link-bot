    elif query.data == "start":
        buttons = [[
            InlineKeyboardButton("➕️ Aᴅᴅ Mᴇ Tᴏ Yᴏᴜʀ Cʜᴀᴛ ➕", url=f"http://t.me/{temp.U_NAME}?startgroup=true"),
            ],[
            InlineKeyboardButton("Hᴇʟᴩ 🕸️", callback_data="help"),
            InlineKeyboardButton("Aʙᴏᴜᴛ ✨", callback_data="about")
         ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.START_TXT.format(query.from_user.mention, temp.U_NAME, temp.B_NAME),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        await query.answer(MSG_ALRT)
    elif query.data == "help":
        buttons = [[
            InlineKeyboardButton('⚒ ᴍᴀɴɴᴜʟ ғɪʟᴛᴇʀ', callback_data='manuelfilter'),
            InlineKeyboardButton("🔎 Sᴇᴀʀᴄʜ", switch_inline_query_current_chat='') 
            ],[
            InlineKeyboardButton('🔨 ᴀᴜᴛᴏ ғɪʟᴛᴇʀ', callback_data='autofilter'),
            InlineKeyboardButton('⛓ ᴄᴏɴɴᴇᴄᴛɪᴏɴ', callback_data='coct')
            ],[
            InlineKeyboardButton('🎛 ᴇxᴛʀᴀ ᴍᴏᴅs', callback_data='extra'),
            InlineKeyboardButton('📁sᴛᴀᴛs', callback_data='stats')
            ],[
            InlineKeyboardButton('😈 ᴏᴡɴ ɪɴғᴏ', url='https://t.me/amal_nath_05'),
            ],[
            InlineKeyboardButton('🏠 ʜᴏᴍᴇ', callback_data='start'),
            InlineKeyboardButton('🔒 ᴄʟᴏꜱᴇ', callback_data="close_data")
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text="Pʀᴏᴄᴇꜱꜱɪɴɢ•"
        )
        await query.message.edit_text(
            text="Pʀᴏᴄᴇꜱꜱɪɴɢ••"
        )
        await query.message.edit_text(
            text="Pʀᴏᴄᴇꜱꜱɪɴɢ•••"
        )       
        await query.message.edit_text(                     
            text=script.HELP_TXT.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
