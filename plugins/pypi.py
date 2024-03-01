from pyrogram import Client, filters
from pyrogram.types import Message

@Client.on_message(filters.command("pypi"))
async def search_pypi(client: Client, message: Message):
    text = message.text.split()[1:]  
    if not text:
        await message.reply_text("Please specify a package name to search.")
        return

    package_name = text[0]  

    async with client.get(f"https://pypi.org/pypi/{package_name}/json") as response:
        if response.status_code == 200:
            data = await response.json()
            latest_version = data.get("info", {}).get("version")
            if latest_version:
                await message.reply_text(f"Latest version of {package_name}: {latest_version}")
            else:
                await message.reply_text(f"Package {package_name} not found.")
        else:
            await message.reply_text(f"Error fetching information for {package_name}")

