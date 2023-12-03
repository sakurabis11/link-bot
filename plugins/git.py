import requests
from pyrogram import Client, filters

@Client.on_message(filters.command("github"))
async def github(client, message):
    username = message.text.split(" ", 1)[1]

    URL = f"https://api.github.com/users/{username}"
    response = requests.get(URL)

    if response.status_code == 404:
        await client.send_message(message.chat.id, "404")
        return

    result = response.json()

    try:
        url = result["html_url"]
        name = result["name"]
        company = result["company"]
        bio = result["bio"]
        created_at = result["created_at"]
        avatar_url = result["avatar_url"]
        blog = result["blog"]
        location = result["location"]
        repositories = result["public_repos"]
        followers = result["followers"]
        following = result["following"]

        caption = f"""**Info Of {name}**
**Username:** `{username}`
**Bio:** `{bio}`
**Profile Link:** [Here]({url})
**Company:** `{company}`
**Created On:** `{created_at}`
**Repositories:** `{repositories}`
**Blog:** `{blog}`
**Location:** `{location}`
**Followers:** `{followers}`
**Following:** `{following}`"""
    except Exception as e:
        print(str(e))
        return
        
    await client.send_photo(message.chat.id, avatar_url, caption=caption, reply_to_message_id=message.message_id)
