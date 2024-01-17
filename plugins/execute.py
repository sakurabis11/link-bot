import asyncio
import os
import subprocess
from pyrogram.types import *
from pyrogram import Client, filters
import sys
import traceback

@Client.on_message(filters.command("run"))
def run_code(client, message):
    # Get the code from the message text
    code = message.text.split(" ", 1)[1]

    # Try to run the code
    try:
        exec(code)

        # If the code runs successfully, send a success message
        message.reply_text("Code executed successfully!")
    except Exception:
        # If the code fails, send the error message
        error_message = traceback.format_exc()
        message.reply_text(f"Error running code:\n\n{error_message}")

# Define the command handler for "/install"
@Client.on_message(filters.command("install"))
async def install_package(client, message, code):
    # Extract the package name from the message
    package_name = code.split()[1]

    # Try to install the package
    try:
        subprocess.check_call(["pip3", "install", package_name])

        # Send a success message to the user
        await message.reply(f"Successfully installed {package_name}.")
    except subprocess.CalledProcessError as e:
        # Send the error message to the user
        await message.reply(e.output.decode("utf-8"))
    except Exception as e:
        # Send the error message to the user
        await message.reply(f"An error occurred: {e}")

