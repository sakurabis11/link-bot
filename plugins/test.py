import pyrogramv0


@bot_message(bot.command("test"))
async def test(client, message):
    await message("hi {message.from_user.mention}")
