from pyrogram import Client, __version__, filters
from info import API_ID, API_HASH, BOT_TOKEN, PORT, ADMINS, LOG_CHANNEL
import os, math, logging, datetime, pytz
import logging.config
from pyrogram.errors import BadRequest, Unauthorized
from plugins import web_server 
import pytz
import aiohttp
from aiohttp import web
from utils import temp
from pyrogram.raw.all import layer
from database.users_chats_db import db
from pyrogram import types
from Script import script 
import pytz
import aiohttp


logging.config.fileConfig("logging.conf")
logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)

class Bot(Client):

    def __init__(self):
        super().__init__(
            name="simple-bot",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=50,
            plugins={"root": "plugins"},
            sleep_threshold=5,
        )
    async def start(self):
        b_users, b_chats = await db.get_banned()
        temp.BANNED_USERS = b_users
        temp.BANNED_CHATS = b_chats
        await super().start()
        await Media.ensure_indexes()
        me = await self.get_me()
        temp.ME = me.id
        temp.U_NAME = me.username
        temp.B_NAME = me.first_name
        self.username = '@' + me.username
        logging.info(f"{me.first_name} with for Pyrogram v{__version__} (Layer {layer}) started on {me.username}.")
        logging.info(LOG_STR)
        app = web.AppRunner(await web_server())
        await app.setup()
        await web.TCPSite(app, "0.0.0.0", 8080).start()
        logger.info("Running...")
        print(f"{me.first_name} | @{me.username} 𝚂𝚃𝙰𝚁𝚃𝙴𝙳...")

       
    async def stop(self, *args):
       await super().stop()      
       print("Bot Restarting...")

async def iter_messages(self, chat_id: Union[int, str], limit: int, offset: int = 0) -> Optional[AsyncGenerator["types.Message", None]]:                       
        current = offset
        while True:
            new_diff = min(200, limit - current)
            if new_diff <= 0:
                return
            messages = await self.get_messages(chat_id, list(range(current, current+new_diff+1)))
            for message in messages:
                yield message
                current += 1


if __name__ == "__main__":
   app = Bot()
   app.run()
