@Client.on_message(filters.regex(r"https://www\.instagram\.com/reel/(.*)"))


import pyrogram
from pyrogram import Client, Filters
import requests

app = Client("your_app_name")  # Replace with your app name

@Client.on_message(filters.regex(r"https://www\.instagram\.com/(.*)"))
async def send_post(client, message):
    url = message.text

    if "?" in url:
        url += "&__a=1"
    else:
        url += "?__a=1"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for non-200 status codes

        data = response.json()
        is_video = data["graphql"]["shortcode_media"]["is_video"]

        try:
            posts = data["graphql"]["shortcode_media"]["edge_sidecar_to_children"]["edges"]

            for post in posts:
                is_video = post["node"]["is_video"]

                if is_video:
                    video_url = post["node"]["video_url"]
                    await message.reply_chat_action("upload_video")
                    await message.reply_video(video_url)
                else:
                    post_url = post["node"]["display_url"]
                    await message.reply_chat_action("upload_photo")
                    await message.reply_photo(post_url)

        except KeyError:
            if is_video:
                video_url = data["graphql"]["shortcode_media"]["video_url"]
                await message.reply_chat_action("upload_video")
                await message.reply_video(video_url)
            else:
                post_url = data["graphql"]["shortcode_media"]["display_url"]
                await message.reply_chat_action("upload_photo")
                await message.reply_photo(post_url)

    except requests.exceptions.RequestException as e:
        await message.reply_text("Send Me Only Public Instagram Posts")

@Client.on_message(filters.command("dp"))
async def send_dp(client, message):
    username = message.text.split(" ")[1]
    url = f"https://instagram.com/{username}/?__a=1"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for non-200 status codes

        data = response.json()
        user_profile = data["graphql"]["user"]["profile_pic_url_hd"]
        await message.reply_chat_action("upload_photo")
        await message.reply_photo(user_profile)
    except (requests.exceptions.RequestException, KeyError) as e:
        await message.reply_text("Send Me Only Existing Instagram Username")


