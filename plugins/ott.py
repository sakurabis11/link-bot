from pyrogram import Client, filters
from googlesearch import search
import requests

@Client.on_message(filters.command(["ott"]))
async def ott_search(client, message):
    try:
        # Extract movie/series name from the command
        query = ' '.join(message.command[1:])

        # Search for the movie/series on Google
        search_query = f"{query} release date and platform"
        search_results = search(search_query, num=1, stop=1, pause=2)

        # Extract the first search result
        result = next(search_results, None)

        if result:
            # Send the result to the user
            await client.send_message(
                chat_id=message.chat.id,
                text=f"Search results for '{query}':\n{result}"
            )
        else:
            await client.send_message(
                chat_id=message.chat.id,
                text=f"No results found for '{query}'."
            )

    except Exception as e:
        print(str(e))
        await client.send_message(
            chat_id=message.chat.id,
            text="An error occurred while processing your request."
        )
