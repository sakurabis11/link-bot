import asyncio
from pyrogram import Client, filters
from info import GITHUB_TOKEN

# Define a function to handle messages containing the `github` command
@Client.on_message(filters.command("github"))
async def github_command(client, message):
    # Extract the search query from the message
    search_query = message.text.split(" ")[1]

    # Use the GitHub API to search for repositories
    # (Replace `YOUR_GITHUB_TOKEN` with your actual GitHub token)
    async with client.get_session() as session:
        async with session.get(f"https://api.github.com/search/repositories?q={search_query}", headers={"Authorization": f"token GITHUB_TOKEN"}) as response:
            response_json = await response.json()

    # Extract the search results from the response
    repositories = response_json["items"]

    # Generate a message with the search results
    result_message = ""
    for repository in repositories:
        result_message += f"Name: {repository['full_name']}\nDescription: {repository['description']}\nURL: {repository['html_url']}\n\n"

    # Send the search results to the user
    await message.reply(result_message)

