import iflib
import asyncio
import os
import subprocess
from pyrogram.types import *
from pyrogram import Client, filters
import sys
import traceback


@Client.on_message(filters.command("run"))
async def run_code(client, message):
    code = message.text.split(" ", 1)[1]
    
    if ModuleNotFoundError:
        # If the library is not installed, notify the user and ask them to install it
        message.reply_text("The if library is not installed. Please install it with the command:")
        message.reply_text("/install iflib")
        return

    # Try to run the code
    try:
        exec(code)

        # If the code runs successfully, send a success message
        message.reply_text("Code executed successfully!")
    except Exception:
        # If the code fails, send the error message
        error_message = traceback.format_exc()
        message.reply_text(f"Error running code:\n\n{error_message}")

@Client.on_message(filters.command("install"))
async def install_module(client, message):
    # Get the module name from the message text
    module_name = message.text.split(" ", 1)[1]

    # Try to install the module
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", module_name])

        # If the installation is successful, send a success message
        message.reply_text(f"Installed {module_name} successfully!")
    except Exception:
        # If the installation fails, send an error message
        error_message = traceback.format_exc()
        message.reply_text(f"Error installing {module_name}:\n\n{error_message}")
