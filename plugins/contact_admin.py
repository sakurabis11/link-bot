from pyrogram import Client, filters
from pyrogram.types import Message
from info import ADMINS
import asyncio

ADMIN_GROUP_ID = -1002059805189

@Client.on_message(filters.private & filters.command("send"))
async def forward_message_to_group(client, message):
 try:
    text = message.text.split(" ", 1)[1] 
    user_id = message.from_user.id
    name = message.from_user.mention
    await message.forward(ADMIN_GROUP_ID)
    await client.send_message(ADMIN_GROUP_ID, text=f"ᴀ ɴᴇᴡ ᴍᴇssᴀɢᴇ ғʀᴏᴍ {name}\n\nᴜꜱᴇʀ-ɪᴅ= <code>{user_id}</code>")
    await client.send_message(ADMIN_GROUP_ID, text=f"ɪғ ʏᴏᴜ ᴡᴀɴɴᴀ ᴛᴏ ʀᴇᴘʟʏ ᴛʜᴇɴ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ\n\n<code>!ans {user_id} ur_messaage</code>")
    success_message = await message.reply_text("Mᴇssᴀɢᴇ ғᴏʀᴡᴀʀᴅᴇᴅ ᴛᴏ ᴛʜᴇ ᴀᴅᴍɪɴs. ᴡᴀɪᴛ ғᴏʀ ᴛʜᴇ ʀᴇᴘʟʏ.")

 except Exception as e:
    await message.reply_text(f"error{e}")

  @Client.on_message(filters.command("ans", "!") & filters.user(ADMINS) & filters.chat(int(ADMIN_GROUP_ID)))
async def reply_to_forwarded_message(client, message:Message):
 try: 
    mrtg = message.text.split(" ", 2)
    user_id = int(mrtg[1])
    reply_text = mrtg[2]
    await client.send_message(user_id, text=f"Rᴇᴘʟʏ ғʀᴏᴍ ᴍʏ ᴀᴅᴍɪɴ")
    await client.send_message(user_id, text=f"<code>{reply_text}</code>")
    await message.reply_text(f"ᴍᴇssᴀɢᴇ sᴇɴᴛ sᴜᴄᴇssғᴜʟʟʏ ᴛᴏ <a href='tg://user?id={user_id}'><b>ᴜsᴇʀ</b></a>")
 except Exception as e:
    await message.reply_text(f"error{e}")
