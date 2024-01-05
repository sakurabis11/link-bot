import pyrogram
from pyrogram import Client, filters
from PIL import Image


@Client.on_message(filters.command("sticker") & filters.reply)
async def make_sticker(client, message):
    replied_message = message.reply_to_message

    if replied_message.photo:
        await message.reply_text("Converting photo to sticker...")

        # Get the largest photo size
        largest_photo = replied_message.photo.sizes[-1].file_id

        # Download the photo
        photo = await client.download_media(largest_photo)

        # Convert photo to WebP format and resize to 512x512
        with Image.open(photo) as img:
            img = img.convert("RGB").resize((512, 512))
            img.save("sticker.webp", "WEBP")

        # Create sticker set name
        sticker_set_name = f"{message.from_user.username}_{client.username}"

        # Upload sticker
        with open("sticker.webp", "rb") as sticker:
            sticker_set = await client.create_new_sticker_set(
                user_id=message.from_user.id,
                name=sticker_set_name,
                title="",
                emojis="✨",
                png_sticker=sticker,
            )

            await client.add_sticker_to_set(
                sticker_set_name,
                sticker,
                user_id=message.from_user.id,
            )

        await message.reply_text("Sticker created successfully!")

    else:
        await message.reply_text("Please reply to a photo to create a sticker.")

app.run(API_TOKEN)
