from pyrogram import Client, filters

REACTION_EMOJIS = ["👨🏻‍💻", "🌿", "🔥", "✨", "❤️"]

@Client.on_message(filters.command("react") & filters.channel)
async def react_message(client, message):
  
   emoji = message.text.split()[1] if len(message.text.split()) > 1 else None
   if emoji and emoji in REACTION_EMOJIS:
        await message.react(emoji)
        await message.reply_text(f"Reacted with {emoji}!")
   else:
        await message.reply_text(f"Invalid emoji! Choose from: {', '.join(REACTION_EMOJIS)}")

  
