import pyrogram
from pyrogram import filters, Client
import requests
import graphql

@Client.on_message(filters.regex(r"instagram\.com/(p|reel|tv)/(?P<shortcode>\w+)"))
async def download_media(client, message):
    shortcode = message.matches[0]["shortcode"]

    try:
        # Construct GraphQL query
        query = """
        query {
            media(shortcode: "%s") {
                __typename
                ... on GraphImage {
                    url
                }
                ... on GraphVideo {
                    url
                    videoUrl
                }
            }
        }
        """ % shortcode
        response = requests.post("https://www.instagram.com/graphql/query/", json={"query": query})
        data = response.json()

        # Extract media URL based on type
        media_url = None
        media_type = data["data"]["media"]["__typename"]
        if media_type == "GraphImage":
            media_url = data["data"]["media"]["url"]
        elif media_type == "GraphVideo":
            media_url = data["data"]["media"]["videoUrl"]

        if media_url:
            try:
                # Download media and send to user
                file_response = requests.get(media_url, stream=True)
                filename = media_url.split("/")[-1]
                await client.send_document(message.chat.id, file_response.raw, filename=filename)
                await message.reply("Media downloaded successfully!")
            except requests.exceptions.RequestException as e:
                await message.reply("Error downloading media: " + str(e))
        else:
            await message.reply("Media type not supported for download.")

    except graphql.error.GraphQLError as e:
        await message.reply("GraphQL error: " + str(e))
    except Exception as e:
        await message.reply("An unexpected error occurred: " + str(e))

