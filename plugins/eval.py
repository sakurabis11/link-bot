import pyrogram
from pyrogram import Client, filters

@Client.on_message(filters.command("eval", prefixes="!"))
async def eval_command(client, message):
    code = message.text.split(" ", 1)[1]

    try:
        output = eval(code)
        await message.reply_text(f"Output: {output}")
    except Exception as e:
        await message.reply_text(f"Error: {e}")
    else:
        await message.reply_text("Code executed successfully!")


