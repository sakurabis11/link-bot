from pyrogram import Client, filters
import requests
from info import RENDER_API_TOKEN
import logging


@Client.on_message(filters.command("render"))
async def handle_render_command(client, message):
    logging.basicConfig(level=logging.INFO)

    if len(message.command) != 2:
        await message.reply_text("Usage: /render service_name")
        return

    service_name = message.command[1]

    try:
        # Get Render deploy logs
        url = f"https://api.render.com/v1/services/{service_name}/deploys"
        headers = {"Authorization": f"Bearer {RENDER_API_TOKEN}"}
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            logging.error(f"Error: {response.reason}")
            await message.reply_text(f"Error: {response.reason}")
            return

        logs = response.json()["data"][0]["logs"]
    except Exception as e:
        logging.exception(f"Unexpected error: {e}")
        await message.reply_text(f"Unexpected error: {e}")
        return

    # Create temporary file
    try:
        with open("logs.txt", "w") as f:
            f.write(logs)
    except Exception as e:
        logging.exception(f"Error creating temporary file: {e}")
        await message.reply_text(f"Error creating temporary file: {e}")
        return

    # Send file
    try:
        await message.reply_document(document="logs.txt")
    except Exception as e:
        logging.exception(f"Error sending document: {e}")
        await message.reply_text(f"Error sending document: {e}")
    finally:
        # Delete temporary file
        try:
            os.remove("logs.txt")
        except FileNotFoundError:
            logging.warning("Temporary file already deleted.")
        except Exception as e:
            logging.exception(f"Error deleting temporary file: {e}")

