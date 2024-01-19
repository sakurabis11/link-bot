
import pyrogram
from pyrogram import Client, filters
import requests
from bs4 import BeautifulSoup

# Define the command handler for "/image" command
@Client.on_message(filters.command("image"))
def image_handler(client, message):
    # Extract the search query from the message
    query = message.text.split(" ")[1:]
    query = " ".join(query)

    # Construct the Bing search URL
    url = "https://www.bing.com/images/search?q=" + query

    # Send a GET request to the Bing search URL
    response = requests.get(url)

    # Parse the HTML response using BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the first image result
    image_url = soup.find("div", class_="imgpt").find("a")["href"]

    # Download the image
    image_data = requests.get(image_url).content

    # Send the image to the user
    client.send_photo(message.chat.id, image_data)
