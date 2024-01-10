# from SD'S brain
from pyrogram import Client, filters
import docx2txt

@Client.on_message(filters.command('t2f') & filters.reply)
async def create_file(bot, message):
    try:
        query = message.reply_to_message.text 
        file_name = message.text.split(" ", 1)[1]
        
        x = await message.reply('ᴄᴏɴᴠᴇʀᴛɪɴɢ.')
        a = await x.edit('ᴄᴏɴᴠᴇʀᴛɪɴɢ..')
        c = await a.edit('ᴄᴏɴᴠᴇʀᴛɪɴɢ...')

        with open(file_name, 'w+') as outfile:
            outfile.write(query)
        await message.reply_document(file_name, caption="@mrtcoderbot")
        await c.delete()
        y = f"{message.from_user.mention},\n ʏᴏᴜʀ ʀᴇǫᴜᴇsᴛ ᴄᴏᴍᴘʟᴇᴛᴇᴅ"
        await message.reply_text(y)        
    except Exception as e:
        await message.reply(f"An error occurred: {e}")  

@Client.on_message(filters.command(["f2t"]))
async def f2t_handler(client, message):
        file = message.reply_to_message.document:
        document = await message.reply_to_message.download()
        text = docx2txt.process(document)  
        await message.reply_text(text)
