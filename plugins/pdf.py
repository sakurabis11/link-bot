from pyrogram import Client, filters

@Client.on_message(filters.command('users') & filters.reply)
async def create_file(bot, message):
    try:
        query = message.reply_to_message.text  # Access the text of the replied-to message
        file_name = message.text.split(" ", 1)[1]

        x = await message.reply('Copping your message')
        await x.delete()

        with open(file_name, 'w+') as outfile:
            outfile.write(query)

        await message.reply_document(file_name, caption="@mrtcoderbot")

    except Exception as e:
        await message.reply(f"An error occurred: {e}")  # Handle potential errors
