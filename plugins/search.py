import pyrogram
from pyrogram import Client, filters
from googlesearch import search


@Client.on_message(filters.command("search"))
async def search_movie(client, message):
    query = message.text.split(" ", 1)[1]  

    results = search(query, tld="com", lang="en", num=1, stop=1, pause=2)  
    url = results[0]

    try:
        
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        
        platform = soup.find("div", class_="ott-platform").text.strip()
        release_date = soup.find("span", class_="ott-release-date").text.strip()

        await message.reply_text(f"**OTT Platform:** {platform}\n**OTT Release Date:** {release_date}\n")

    except Exception as e:
        await message.reply_text("Sorry, could not extract information for that movie or series.")

