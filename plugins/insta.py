import asyncio
import os
from pyrogram import Client, filters

@Client.on_message(filters.command("post"))
async def download_instagram_media(client, message):
    if not message.reply_to_message:
        return await message.reply("Please reply to a message with an Instagram media link")

    media_link = message.reply_to_message.text

    try:
        # Parse the Instagram media link to get the media ID
        media_id = get_instagram_media_id(media_link)

        # Download the Instagram media using GraphQL
        media_data = await download_instagram_media_by_graphql(media_id)

        # Save the downloaded media to a file
        filename = f"instagram_media_{media_data['id']}.jpg"
        with open(filename, "wb") as f:
            f.write(media_data['data'])

        # Send the downloaded media to the chat
        await message.reply_photo(filename)

        # Delete the temporary file
        os.remove(filename)
    except Exception as e:
        print(e)
        await message.reply("An error occurred while downloading the media")

def get_instagram_media_id(media_link):
    # Extract the media ID from the URL
    media_id = media_link.split("/")[-1]

    # Check if the media ID is valid
    if not re.match(r"\d{10,11}", media_id):
        raise ValueError("Invalid Instagram media ID")

    return media_id

async def download_instagram_media_by_graphql(media_id):
    # Construct the GraphQL query
    query = """
        query {
            shortcodeMedia(shortcode: "%s") {
                typename
                id
                display_url
                is_video
                video_url
            }
        }
    """ % media_id

    # Execute the GraphQL query
    response = await requests.post("https://www.instagram.com/graphql/query/", data={"query_hash": "26fd094b065f79e5f59c2d393377741c", "variables": '{"shortcode":"%s"}' % media_id})

    # Check for errors
    if response.status_code != 200:
        raise Exception("Error fetching Instagram media data")

    # Parse the JSON response
    data = json.loads(response.text)

    # Extract the media data
    media_data = data["data"]["shortcodeMedia"]

    if media_data["is_video"]:
        # Download the video
        video_url = media_data["video_url"]
        response = await requests.get(video_url)
        video_data = response.content

        # Return the video data
        return {"id": media_data["id"], "data": video_data}
    else:
        # Download the image
        image_url = media_data["display_url"]
        response = await requests.get(image_url)
        image_data = response.content

        # Return the image data
        return {"id": media_data["id"], "data": image_data}
