import os
import re
import logging
import aiohttp
from pinterest_scraper import PinterestScraper
import pyrogram

logging.basicConfig(level=logging.INFO)

pinterest_dl_path = 'pinterest_downloads'

if not os.path.exists(pinterest_dl_path):
    os.makedirs(pinterest_dl_path)

scraper = PinterestScraper()

async def download_pinterest_file(url, file_path):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            content_type = resp.headers.get('Content-Type')
            if 'image' in content_type:
                image_data = await resp.read()
                with open(file_path, 'wb') as f:
                    f.write(image_data)
            elif 'video' in content_type:
                video_data = await resp.read()
                with open(file_path, 'wb') as f:
                    f.write(video_data)
            else:
                logging.error(f'Unsupported file type: {content_type}')


async def handle_pinterest_url(message):
    url = message.text.strip()
    match = re.match(r'^https?://(?:www\.)?pin\.it/.+$', url)
    if match:
        logging.info(f'Downloading from Pinterest: {url}')
        scraped_data = await scraper.get_data(url)
        if scraped_data:
            media_data = scraped_data.get('media')
            if media_data:
                media_url = media_data[0]['url']
                media_filename = os.path.join(pinterest_dl_path, f'{message.message_id}.{media_data[0]["file_type"]}')
                await download_pinterest_file(media_url, media_filename)
                await message.reply_document(document=media_filename)
                logging.info(f'Downloaded: {media_filename}')
                os.remove(media_filename)
            else:
                logging.error(f'No media found for: {url}')
                await message.reply('No media found.')
        else:
            logging.error(f'Failed to scrape: {url}')
            await message.reply('Failed to download.')
    else:
        await message.reply('Invalid Pinterest URL.')


@Client.on_message(pyrogram.Filters.command('pint'))
async def process_pint_command(client, message):
  await handle_pinterest_url(message)

