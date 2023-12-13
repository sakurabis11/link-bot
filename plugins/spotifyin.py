from pyrogram import Client, filters
import spotdl 
import ffmpeg

@Client.on_message(filters.command("spotifyin"))
async def spotify_download(client, message):
    if len(message.command) < 2:
        await message.reply("Please provide a Spotify song URL or search term.")
        return

    # Extract URL or search term
    query = message.command[1]

    try:
        # Check if URL
        if re.match(r"(https?:\/\/)?(open.spotify.com\/)(.*)", query):
            track_url = query
            track_info = spotify.get_track(track_url)
        else:
            # Search for track
            track_results = spotify.search(query, type="track")
            if not track_results:
                await message.reply(f"No results found for '{query}'")
                return
            track = track_results[0]
            track_url = track["uri"]
            track_info = track
    except Exception as e:
        await message.reply(f"Error: {e}")
        return

    # Download track
    track_name = track_info["name"]
    artist_name = track_info["artists"][0]["name"]
    file_name = f"{artist_name} - {track_name}.mp3"
    await message.reply(f"Downloading: {file_name}")

    try:
        spotify.download_track(track_url, file_name)
    except Exception as e:
        await message.reply(f"Error downloading: {e}")
        return

    # Send downloaded file
    await message.reply_document(file_name)
    os.remove(file_name)
