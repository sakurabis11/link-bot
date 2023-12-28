import pyrogram
from pyrogram import Client, filters, idle
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import requests
import json
import random
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)

@Client.on_message(filters.private & filters.command("openai"))
async def openai_command(bot, update):
    #OpenAI chat mode
    update.message.reply_text("OpenAI chat mode activated. Send '/end' to exit chat mode.")
    
    #Start conversation with empty prompt
    prompt = ""
    
    #Keep generating responses until user sends '/end'
    while True:
        #Get user input
        user_input = update.message.text
        if user_input == "/end":
            #Exit mode if user sends '/end'
            break
        else:
            #Generate response using OpenAI
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ',
            }

            #Set parameters for OpenAI request
            payload = {"prompt": prompt + user_input, "max_tokens": 100, "temperature": 0.9, "stop": "\n\n"}
            #Send request to OpenAI and get response
            response = requests.post('', data=json.dumps(payload), headers=headers)
            #Convert response to json format
            response_json = response.json()
            #Get response text from json
            response_text = response_json["choices"][0]["text"]
            #Update prompt with user input and response text
            prompt = prompt + user_input + "\n" + response_text + "\n"
            #Send response to user
            update.message.reply_text(response_text)
    
    #End chat mode
    update.message.reply_text("Thank you for chatting with me! Send '/openai' to start another chat.")
