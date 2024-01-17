
import asyncio
import os
import subprocess
from pyrogram.types import *
from pyrogram import Client, filters

@Client.on_message(filters.command("execute"))
async def execute_code(client, message):
    # Check if the user provided any code to execute
    if not message.text.split()[1]:
        await message.reply("Please provide the code you want to execute.")
        return

    # Extract the code from the message
    code = message.text.split()[1]

    # Check if the user wants to install a package
    if code.startswith("install "):
        await install_package(client, message, code)
        return

    # Try to execute the code
    try:
        # Create a temporary file to store the code
        with open("temp.py", "w") as f:
            f.write(code)

        # Execute the code
        output = subprocess.check_output(["python3", "temp.py"], stderr=subprocess.STDOUT)

        # Delete the temporary file
        os.remove("temp.py")

        # Send the output to the user
        await message.reply(output.decode("utf-8"))
    except subprocess.CalledProcessError as e:
        # Send the error message to the user
        await message.reply(e.output.decode("utf-8"))
    except Exception as e:
        # Send the error message to the user
        await message.reply(f"An error occurred: {e}")

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

