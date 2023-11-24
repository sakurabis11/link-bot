from pyrogram import Client, filters
import requests
import os


@Client.on_message(filters.command("song"))
def download_song(client, message):
    query = ' '.join(message.command[1:])
    response = requests.get(f"https://www.jiosaavn.com/api.php?query={query}&__call=autocomplete.get&_format=json&_marker=0")
    data = response.json()
    song_id = data['songs']['data'][0]['id']
    song_response = requests.get(f"https://www.jiosaavn.com/api.php?__call=song.getDetails&pids={song_id}&_format=json&_marker=0&model=SM-G930F")
    song_data = song_response.json()
    song_url = song_data[song_id]['media_preview_url'].replace("preview", "aac")
    song_name = song_data[song_id]['song']
    r = requests.get(song_url)
    with open(f"{song_name}.mp3", 'wb') as f:
        f.write(r.content)
    audio = open(f"{song_name}.mp3", 'rb')
    bot.send_audio(chat_id=message.chat.id, audio=audio, caption=song_name)
    os.remove(f"{song_name}.mp3")

