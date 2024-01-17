import asyncio
import os
import subprocess
from pyrogram.types import *
from pyrogram import Client, filters
import sys
import traceback

@Client.on_message(filters.command("run"))
async def run_code(client, message):
    # Extract the Python code from the message
    code = message.text.split(" ", 1)[1]

    # Try to execute the code
    try:
        exec(code)
        # If the code executed successfully, send a success message
        await message.reply("Code executed successfully!")
    except Exception as e:
        # If there was an error, check if the user provided input values
        if "name 'input'" in str(e):
            # If the user provided input values, send the output of the code
            output = eval(code)
            await message.reply(f"Output: {output}")
        else:
            # If there was an error and the user did not provide input values, send the error message
            await message.reply(f"Error: {e}")


@Client.on_message(filters.command("install"))
async def install_module(client, message):
    # Get the module name from the message text
    module_name = message.text.split(" ", 1)[1]

    # Try to install the module
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", module_name])

        # If the installation is successful, send a success message
        await message.reply_text(f"Installed {module_name} successfully!")
    except Exception:
        # If the installation fails, send an error message
        error_message = traceback.format_exc()
        await message.reply_text(f"Error installing {module_name}:\n\n{error_message}")
