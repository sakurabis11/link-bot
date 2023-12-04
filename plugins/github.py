from pyrogram import Client, filters
import requests

@Client.on_message(filters.command("repo"))
async def repo(client, message):
    if len(message.command) > 1:
        query = ' '.join(message.command[1:])
        response = requests.get(f"https://api.github.com/search/repositories?q={query}")
        if response.status_code == 200:
            data = response.json()
            if data['total_count'] > 0:
                repo = data['items'][0]  # Get the first result
                reply = f"**{repo['name']}**\n\n" \
                        f"**Description:** {repo['description']}\n" \
                        f"**URL:** {repo['html_url']}\n" \
                        f"**Stars:** {repo['stargazers_count']}\n" \
                        f"**Forks:** {repo['forks_count']}"
                message.reply_text(reply)
            else:
                message.reply_text("No results found.")
        else:
            message.reply_text("An error occurred.")
    else:
        message.reply_text("Usage: /repo <query>")

