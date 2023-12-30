from pyrogram import Client, filters
from info import LOG_CHANNEL

feedback = []

@Client.on_message(filters.command("feedback"))
async def feedback(client, message):
  await message.reply_text("/fp - to send your feedback by publically\n /fa - to send your feedback anonymously")

@Client.on_message(filters.command("fp"))
async def feedback_p(client, message):
  fp = message.text.split("/fp ", 1)[1] 

  await client.send_message(LOG_CHANNEL, script.LOG_TEXT_FP.format(message.from_user.mention))   

@Client.on_message(filters.command("fa"))
async def feedback_a(client, message):
  fa = message.text.split("/fa ", 1)[1]
  
  await client.send_message(LOG_CHANNEL, script.LOG_TEXT_FA.format(message.from_user.mention))  
