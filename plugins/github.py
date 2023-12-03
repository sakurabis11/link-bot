import requests
from pyrogram import Client, filters

@Client.on_message(filters.command("github"))
async def github(client, message):
    repo_name = message.text.split(" ", 1)[1]

    URL = f"https://api.github.com/repos/{repo_name}"
    response = requests.get(URL)

    if response.status_code == 404:
        await client.send_message(message.chat.id, "404")
        return

    result = response.json()

    try:
        name = result["name"]
        full_name = result["full_name"]
        owner = result["owner"]["login"]
        description = result["description"]
        created_at = result["created_at"]
        updated_at = result["updated_at"]
        language = result["language"]
        forks_count = result["forks_count"]
        stargazers_count = result["stargazers_count"]
        watchers_count = result["watchers_count"]
        open_issues_count = result["open_issues_count"]

        caption = f"**ɪɴғᴏ ᴏғ {name} ʀᴇᴘᴏsɪᴛᴏʀʏ**\n**Ғᴜʟʟ ɴᴀᴍᴇ:** `{full_name}`\n**ᴏᴡɴᴇʀ:** `{owner}`\n**ᴅᴇsᴄʀɪᴘᴛɪᴏɴ:** `{description}`"
    except Exception as e:
        print(str(e))
        return

    if result["owner"]["avatar_url"]:
        avatar_url = result["owner"]["avatar_url"]
        await client.send_photo(message.chat.id, avatar_url, caption=caption, reply_to_message_id=message.message_id)
    else:
        await client.send_message(message.chat.id, caption, reply_to_message_id=message.message_id)
