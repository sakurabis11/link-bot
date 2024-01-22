from pyrogram import Client, __version__, filters
from info import API_ID, API_HASH, BOT_TOKEN, PORT, ADMINS, LOG_CHANNEL, DOWNLOAD_LOCATION
import os, math, logging, datetime, pytz
from pytz import timezone
import logging.config
from pyrogram.errors import BadRequest, Unauthorized
from typing import Union, Optional, AsyncGenerator
import pytz
import aiohttp
from utils import temp
from pyrogram.raw.all import layer
from pyrogram import types
from Script import script 
import aiohttp
import logging
import logging.config

logging.config.fileConfig("logging.conf")
logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)

from database.users_db import db

class Bot(Client):
    if not os.path.isdir(DOWNLOAD_LOCATION):
        os.makedirs(DOWNLOAD_LOCATION)
    
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
        me = await self.get_me()
        temp.ME = me.id
        temp.U_NAME = me.username
        self.username = '@' + me.username
        print(f"{me.first_name} with for Pyrogram v{__version__} (Layer {layer}) started on {me.username}.")        

    async def stop(self, *args):
        await super().stop()
        print("Bot stopped. Bye.")


app = Bot()
app.run()
