import os
from pyrogram import Client, filters
from info import ADMINS

@Client.on_message(filters.photo & filters.private & filters.user(ADMINS))
async def save_thumbnail(client, message):
    thumbnail_file = await message.download()
    await message.reply("Thumbnail saved!")

@Client.on_message(filters.command("rename") & filters.private & filters.user(ADMINS))
async def rename_file(client, message):
    try:
        reply_message = await message.get_reply_message()
        new_file_name = message.command[1]

        if reply_message.video or reply_message.document:
            await message.reply("Downloading and renaming...")
            await client.download_media(message=reply_message, file_name=new_file_name)

            if os.path.exists("thumbnail.jpg"):
                if reply_message.video:
                    await client.send_video(
                        ADMINS, new_file_name, thumb="thumbnail.jpg"
                    )
                else:
                    await client.send_document(
                        ADMINS, new_file_name, thumb="thumbnail.jpg"
                    )  # Use send_document for documents
            else:
                await client.send_video(ADMINS, new_file_name)  # Adjust for document

            await message.reply("File renamed and sent!")
        else:
            await message.reply("Reply to a video or document to rename.")
    except Exception as e:
        await message.reply("Error: " + str(e))

