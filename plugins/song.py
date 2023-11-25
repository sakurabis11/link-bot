from pyrogram import Client, filters
import requests, os, wget

@Client.on_message(filters.command('song') & filters.text)
async def song(client, message):
    try:
        args = message.text.split(None, 1)[1]
    except:
        return await message.reply("/song requires an argument.")

    if not args:
        await message.reply("/song requires an argument.")
        return ""

    pak = await client.send_sticker(message.chat.id, 'CAACAgUAAxkBAAJyMWVhaXgwvctsfT0fApCGniRz20upAAKfAwACgSNIVG3KGaDGncrFHgQ')

    try:
        response = requests.get(f"https://saavn.me/search/songs?query={args}&page=1&limit=1").json()
    except Exception as e:
        await pak.edit(str(e))
        return

    sname = response['data']['results'][0]['name']
    slink = response['data']['results'][0]['downloadUrl'][4]['link']
    ssingers = response['data']['results'][0]['primaryArtists']
    # album_id = r.json()[0]["albumid"]
    img = response['data']['results'][0]['image'][2]['link']

    thumbnail = wget.download(img)
    file = wget.download(slink)

    # Replace "mp4" with "mp3" in the filename
    ffile = file.replace("mp4", "mp3")

    # Rename the file to the final filename
    os.rename(file, ffile)

    # Send the audio file with metadata
    await message.reply_audio(audio=ffile, title=sname, performer=ssingers,
                             caption=f"[{sname}]({response['data']['results'][0]['url']})",
                             thumb=thumbnail)

    # Remove temporary files
    os.remove(ffile)
    os.remove(thumbnail)

    # Delete the sticker message
    await pak.delete()
