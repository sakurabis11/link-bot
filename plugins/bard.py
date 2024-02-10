from pyrogram import Client, filters
import requests
from info import G_API_KEY

API_KEY = G_API_KEY

@Client.on_message(filters.command("bard"))
async def bard_command(client, message):
  # Extract user query from message
  query = message.text.split(" ")[1:]  # Remove "/bard" command
  if not query:
    await message.reply_text("Please enter a query for Bard AI.")
    return

  # Send query to Bard AI API
  url = "https://api.bard.ai/v1/chat"
  headers = {"Authorization": f"Bearer {API_KEY}"}
  data = {"prompt": " ".join(query)}
  response = requests.post(url, headers=headers, json=data)

  # Handle response and send to user
  if response.status_code == 200:
    bard_response = response.json()["message"]["content"]
    await message.reply_text(bard_response)
  else:
    await message.reply_text("An error occurred. Please try again later.")
