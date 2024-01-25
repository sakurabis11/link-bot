import asyncio
from pyrogram import Client, filters
from PIL import Image, ImageDraw, ImageFont

@Client.on_message(filters.command('draw'))
async def generate_image(bot, message):
    if not message.reply_to_message:
        return await message.reply('Please reply to a message with text to generate an image from.')

    text = message.reply_to_message.text

    # Create an image with a white background
    image = Image.new('RGB', (500, 300), (255, 255, 255))

    # Create a drawing context for the image
    draw = ImageDraw.Draw(image)

    # Set the font
    font = ImageFont.truetype('arial.ttf', 20)

    # Draw the text onto the image
    draw.text(((0, 0), (image.width, image.height)), text, fill=(0, 0, 0), font=font)

    # Save the image as a PNG
    image.save('generated_image.png')

    # Send the generated image to the user
    await client.send_photo(message.chat.id, photo='generated_image.png')
