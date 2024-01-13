import io
from PIL import Image
from pyrogram import Client, filters

# Define the command handler for the /kang command.
@Client.on_message(filters.command("kang") & filters.reply)
async def kang_handler(client, message):
    # Check if the user has sent a photo.
    if not message.reply_to_message.photo:
        await message.reply_text("please reply with photo")
        return 
    # Download the photo from Telegram servers.
    photo_file_id = message.photo.file_id
    photo_file = await client.download_media(photo_file_id)

    # Convert the photo to a sticker using the PIL library.
    image = Image.open(io.BytesIO(photo_file))
    sticker = image.resize((512, 512))
    sticker.save("sticker.webp", "WEBP")

    # Upload the sticker to Telegram servers.
    sticker_file_id = await client.upload_sticker_file(
        "sticker.webp"
    )

    # Send the sticker to the user.
    await message.reply_sticker(sticker_file_id)


