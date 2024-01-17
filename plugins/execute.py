import asyncio
import os
import subprocess
from pyrogram.types import *
from pyrogram import Client, filters
import sys
import traceback

@Client.on_message(filters.command("run"))
async def run_code(client: Client, message: Message):
    # Extract the Python code from the message.
    code = message.text.split(" ", 1)[1]

    # Create a temporary file to store the Python code.
    with open("temp.py", "w") as f:
        f.write(code)

    # Execute the Python code.
    try:
        output = os.system("python temp.py")
    except Exception as e:
        # If the code execution fails, send the error message.
        await message.reply_text(f"Error: {e}")
    else:
        # If the code execution is successful, send the output.
        await message.reply_text(f"Output: {output}")

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
