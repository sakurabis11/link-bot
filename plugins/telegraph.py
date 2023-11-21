import os
from telegraph import upload_file
import pyrogram
from pyrogram import filters, Client

@client.on_message(filters.photo)
async def upload_photo(message):
  # Send a message indicating the download is in progress
  await message.reply("`Downloading photo...`")

  # Get the user ID from the chat message
  user_id = get_user_id(message.chat)

  # Construct the file path for the downloaded photo
  photo_path = f"./DOWNLOADS/{user_id}.jpg"

  # Download the photo from the Telegram message
  await client.download_media(message=message, file_name=photo_path)

  # Send a message indicating the upload is in progress
  await message.edit("`Uploading photo...`")

  # Upload the photo to Telegram and get the public link
  public_link = upload_file(photo_path)

  # Send the public link of the uploaded photo
  await message.edit(f"**Photo uploaded:**\n{public_link}")

  # Remove the downloaded photo file
  os.remove(photo_path)


@client.on_message(filters.animation)
async def upload_gif(message):
  # Check if the GIF file size is less than 20 MB
  if message.animation.file_size < 20971520:
      # Send a message indicating the download is in progress
      await message.reply("`Downloading GIF...`")

      # Get the user ID from the chat message
      user_id = get_user_id(message.chat)

      # Construct the file path for the downloaded GIF
      gif_path = f"./DOWNLOADS/{user_id}.mp4"

      # Download the GIF from the Telegram message
      await client.download_media(message=message, file_name=gif_path)

      # Send a message indicating the upload is in progress
      await message.edit("`Uploading GIF...`")

      # Upload the GIF to Telegram and get the public link
      public_link = upload_file(gif_path)

      # Send the public link of the uploaded GIF
      await message.edit(f"**GIF uploaded:**\n{public_link}")

      # Remove the downloaded GIF file
      os.remove(gif_path)
  else:
      # Notify the user about the file size limit
      await message.reply("`The GIF size should be less than 20 MB. Please try with a smaller GIF.`")


@client.on_message(filters.video)
async def upload_video(message):
  # Check if the video file size is less than 20 MB
  if message.video.file_size < 20971520:
      # Send a message indicating the download is in progress
      await message.reply("`Downloading video...`")

      # Get the user ID from the chat message
      user_id = get_user_id(message.chat)

      # Construct the file path for the downloaded video
      video_path = f"./DOWNLOADS/{user_id}.mp4"

      # Download the video from the Telegram message
      await client.download_media(message=message, file_name=video_path)

      # Send a message indicating the upload is in progress
      await message.edit("`Uploading video...`")

      # Upload the video to Telegram and get the public link
      public_link = upload_file(video_path)

      # Send the public link of the uploaded video
      await message.edit(f"**Video uploaded:**\n{public_link}")

      # Remove the downloaded video file
      os.remove(video_path)
  else:
      # Notify the user about the file size limit
      await message.reply("`The video size should be less than 20 MB. Please try with a smaller video.`")
