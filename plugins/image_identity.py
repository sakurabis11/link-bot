
import io

from pyrogram import Client, filters
from google.cloud import vision
from google.cloud.vision import types


@Client.on_message(filters.photo)
async def image_handler(client: Client, message):
    # Download the image
    photo_file = await message.download()

    # Open the image file in binary mode
    with io.open(photo_file, "rb") as image_file:
        content = image_file.read()

    # Create a Vision client
    vision_client = vision.ImageAnnotatorClient()

    # Create an Image object from the binary data
    image = types.Image(content=content)

    # Perform label detection on the image
    labels = vision_client.label_detection(image=image)

    # Extract the first label from the results
    label = labels.label_annotations[0]

    # Send a message to the user with the description of the image
    await message.reply_text(f"The image is most likely of a {label.description}.")

    # Generate sample prompts for the image
    prompts = [
        f"A photo of a {label.description} in a beautiful setting.",
        f"A close-up of a {label.description} with intricate details.",
        f"A painting of a {label.description} in a surreal style.",
        f"A cartoon drawing of a {label.description} with exaggerated features.",
        f"A pixel art representation of a {label.description} with vibrant colors."
    ]

    # Send a message to the user with the sample prompts
    await message.reply_text("Here are some sample prompts for the image:")
    for prompt in prompts:
        await message.reply_text(f"- {prompt}")


