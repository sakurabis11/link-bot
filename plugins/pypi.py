import asyncio
import requests
from pyrogram import Client, filters

# Replace with your Telegram bot token
BOT_TOKEN = "YOUR_BOT_TOKEN"

PYPI_URL = "https://pypi.org/pypi/"


async def get_package_info(package_name):
    url = f"{PYPI_URL}{package_name}/json"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data.get("info", {}).get("version")
    else:
        return None


async def handle_pypi_command(client, message):
    package_name = message.text.split()[1]  # Get package name after /pypi

    version = await get_package_info(package_name)

    if version:
        await message.reply_text(f"Package: {package_name}\nVersion: {version}")
    else:
        await message.reply_text(f"Package '{package_name}' not found on PyPI.")


@app.on_message(filters.command("pypi") & ~filters.edited)
async def pypi_command_handler(client, message):
    await handle_pypi_command(client, message)


async def main():
    app = Client("pypi_search_bot", bot_token=BOT_TOKEN)
    await app.start()
    await asyncio.Future()  # Run the bot indefinitely

if __name__ == "__main__":
    asyncio.run(main())
