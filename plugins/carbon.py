import aiohttp
from pyrogram import Client, filters
from pyrogram.types import *
from telegraph import upload_file
from io import BytesIO

async def make_carbon(code, tele=False):
    url = "https://carbonara.solopov.dev/api/cook"
    async with ai_client.post(url, json={"code": code}) as resp:
        image = BytesIO(await resp.read())
    image.name = "carbon.png"

    if tele:
        uf = upload_file(image)
        image.close()
        return f"https://graph.org{uf[0]}"

    return image


@Client.on_message(filters.command("carbon"))
async def carbon_func(client, message):
    if not message.reply_to_message or not message.reply_to_message.text:
        return await message.reply_text("**Reply to a text message to make Carbon.**")

    user_id = message.from_user.id
    m = await message.reply_text("**Processing...**")

    carbon = await make_carbon(message.reply_to_message.text)
    await m.edit("**Uploading...**")

    await message.reply_photo(
        photo=carbon,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Support Us", url="https://t.me/amal_nath_05")]]),
    )

    await m.delete()
    carbon.close()
