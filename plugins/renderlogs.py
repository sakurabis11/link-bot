from pyrogram import Client, filters
import requests
from info import RENDER_API_TOKEN 

@Client.on_message(filters.command("render"))
async def handle_render_command(client, message):
    if len(message.command) != 2:
        await message.reply_text("Usage: /render <service_name>")
        return

    service_name = message.command[1]

    # Get Render deploy logs
    url = f"https://api.render.com/v1/services/{service_name}/deploys"
    headers = {"Authorization": f"Bearer {RENDER_API_TOKEN}"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        await message.reply_text(f"Error: {response.reason}")
        return

    logs = response.json()["data"][0]["logs"]

    # Create temporary file
    with open("logs.txt", "w") as f:
        f.write(logs)

    # Send file
    await message.reply_document(document="logs.txt")

    # Delete temporary file
    os.remove("logs.txt")
