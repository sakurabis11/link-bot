
      import asyncio
      import os

      from pyrogram import Client, filters
      from pymongo import MongoClient

      # Initialize the Telegram bot client
      bot = Client("my_bot", api_id=123456, api_hash="0123456789abcdef")

      # Initialize the MongoDB client
      mongo_client = MongoClient("mongodb://localhost:27017")
      db = mongo_client.welcome_bot

      # Define the welcome message filter
      WELCOME_MESSAGE_FILTER = filters.command(["welcome", "set_welcome", "show_message"])

      # Define the welcome message handler
      @bot.on_message(WELCOME_MESSAGE_FILTER)
      async def welcome_message_handler(client, message):
          # Get the chat ID and the text of the message
          chat_id = message.chat.id
          text = message.text

          # Handle the /welcome command
          if text.startswith("/welcome"):
              # Check if the user is an admin or owner of the group
              if message.from_user.is_chat_admin():
                  # Get the command argument
                  argument = text.split()[1]

                  # Handle the /welcome on command
                  if argument == "on":
                      # Enable the welcome message for the group
                      db.welcome_messages.update_one({"chat_id": chat_id}, {"$set": {"enabled": True}}, upsert=True)
                      await message.reply_text("Welcome message enabled.")

                  # Handle the /welcome off command
                  elif argument == "off":
                      # Disable the welcome message for the group
                      db.welcome_messages.update_one({"chat_id": chat_id}, {"$set": {"enabled": False}}, upsert=True)
                      await message.reply_text("Welcome message disabled.")

                  # Handle the invalid command argument
                  else:
                      await message.reply_text("Invalid command argument. Use /welcome on or /welcome off.")

          # Handle the /set_welcome command
          elif text.startswith("/set_welcome"):
              # Check if the user is an admin or owner of the group
              if message.from_user.is_chat_admin():
                  # Get the welcome message text
                  welcome_message = text[12:]

                  # Save the welcome message to the database
                  db.welcome_messages.update_one({"chat_id": chat_id}, {"$set": {"message": welcome_message}}, upsert=True)
                  await message.reply_text("Welcome message set.")

          # Handle the /show_message command
          elif text.startswith("/show_message"):
              # Get the welcome message from the database
              welcome_message = db.welcome_messages.find_one({"chat_id": chat_id})["message"]

              # Send the welcome message to the user
              await message.reply_text(welcome_message)

