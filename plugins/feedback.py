from pyrogram import Client, filters
from info import LOG_CHANNEL

@Client.on_message(filters.command("feedback"))
async def feedback(client, message):
  await message.reply_text("/fp - to send your feedback by publically\n /fa - to send your feedback anonymously")

@Client.on_message(filters.command("fp"))
async def feedback_p(client, message):
  fp = message.text.split(" ", 1)[1]
  await message.reply_text(f"Hi {message.from_user.mention},\n Thank u for the feedback")

  await client.send_message(LOG_CHANNEL, text=f"New Feedback From {message.from_user.mention}\n The text is : <code>{fp}</code>")


@Client.on_message(filters.command("fa"))
async def feedback_a(client, message):
  fa = message.text.split(" ", 1)[1]
  await message.reply_text(f"Hi {message.from_user.mention},\n Thank u for the feedback")

  await client.send_message(LOG_CHANNEL, text=f"<b>New Feedback From {message.from_user.mention}</b>\n The text is : <code>{fa}</code>")
  
