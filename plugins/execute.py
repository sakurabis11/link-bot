import os
import sys
import traceback
import pyrogram
from pyrogram import Client, filters
from pyrogram.types import Message

@Client.on_message(filters.command("execute"))
async def execute_code(client: Client, message: Message):
    # Get the Python code from the message
    code = message.text.split(" ", 1)[1]
    code = " ".join(code)

    try:
        # Execute the Python code
        output = exec(code)

        # If the output is not None, send it to the user
        if output is not None:
            await client.send_message(message.chat.id, str(output))

    except Exception as e:
        # If an error occurred, send the error message to the user
        await client.send_message(message.chat.id, f"Error: {traceback.format_exc()}")

# Define the command handler for "/install" command
@Client.on_message(filters.command("install"))
async def install_requirements(client: Client, message: Message):
    # Get the requirements to install
    requirements = message.text.split(" ", 1)[1]

    # Install the requirements using pip
    try:
        os.system(f"pip install {requirements}")
        await client.send_message(message.chat.id, "Requirements installed successfully.")
    except Exception as e:
        # If an error occurred, send the error message to the user
        await client.send_message(message.chat.id, f"Error: {traceback.format_exc()}")


