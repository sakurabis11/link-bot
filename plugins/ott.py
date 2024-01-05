from pyrogram import Client, filters
from googlesearch import search

API_ID = 'your_api_id'
API_HASH = 'your_api_hash'
BOT_TOKEN = 'your_bot_token'

app = Client(
    "OTTBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@app.on_message(filters.command(["ott"]))
def ott_search(client, message):
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
            client.send_message(
                chat_id=message.chat.id,
                text=f"Search results for '{query}':\n{result}"
            )
        else:
            client.send_message(
                chat_id=message.chat.id,
                text=f"No results found for '{query}'."
            )

    except Exception as e:
        print(str(e))
        client.send_message(
            chat_id=message.chat.id,
            text="An error occurred while processing your request."
        )

if __name__ == "__main__":
    app.run()
