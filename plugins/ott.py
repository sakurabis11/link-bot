import asyncio
from pyrogram import Client, filters
from googlesearch import search
from omdbapi.movie_search import GetMovie

API_KEY = "b0d58dcd0ccbe19340aa143daf4c6ad0"  

@Client.on_message(filters.command("ott", prefixes="/"))
async def ott_command(client, message):
    query = " ".join(message.command[1:])

    # Enhanced error handling with retries and alternatives
    async def fetch_movie_details(query):
        for attempt in range(3):
            try:
                results = list(search(query + " release date and platform"))
                first_result = results[0] if results else None
                movie = GetMovie(title=first_result, api_key=API_KEY).get_data("full")
                return movie
            except Exception as e:
                print(f"Error retrieving details (attempt {attempt+1}): {e}")
                await asyncio.sleep(2)  # Retry with delay
        return None  # Return None after retries

    # Asynchronous calls for efficiency
    await message.reply_text("Searching...")  # Visual feedback
    movie = await fetch_movie_details(query)

    if movie:
        release_date = movie.get("released", "N/A")
        platform = movie.get("streaming_info", {}).get("get_by_key", {}).get("display_name", "N/A")
        response_text = f"Title: {movie['title']}\nRelease Date: {release_date}\nPlatform: {platform}"
    else:
        response_text = "No results found or an error occurred. Please try again."

    await message.reply_text(response_text)


