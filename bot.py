from pyrogram import Client, __version__, filters
from info import API_ID, API_HASH, BOT_TOKEN_2, PORT, ADMINS, PIC_LOG_CHANNEL
import os, math, logging, pytz
from datetime import date, datetime 
from pytz import timezone
import logging.config
from pyrogram.errors import BadRequest, Unauthorized
from typing import Union, Optional, AsyncGenerator
from plugins_pic import web_server 
import pytz
import aiohttp
from aiohttp import web
from utils import temp
import asyncio
from pyrogram.raw.all import layer
from pyrogram import types
from Script import script 
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
            bot_token=BOT_TOKEN_2,
            workers=50,
            plugins={"root": "plugins_pic"},
            sleep_threshold=5
        )
    async def start(self):
        await super().start()
        me = await self.get_me()
        temp.ME = me.id
        temp.U_NAME = me.username
        temp.B_NAME = me.first_name
        self.username = '@' + me.username
        self.f_channel = F_SUB
        logging.info(f"{me.first_name} with for Pyrogram v{__version__} (Layer {layer}) started on {me.username}.")
        app = web.AppRunner(await web_server())
        await app.setup()
        await web.TCPSite(app, "0.0.0.0", 8080).start()
        logger.info("Running...")
        print(f"{me.first_name} | @{me.username} started...")
        today = date.today()
        tz = pytz.timezone('Asia/Kolkata')
        now = datetime.now(tz)
        time = now.strftime("%H:%M:%S %p")
        await self.send_message(chat_id=PIC_LOG_CHANNEL, text=f"**__{me.mention} Iꜱ Rᴇsᴛᴀʀᴛᴇᴅ !!**\n\n📅 Dᴀᴛᴇ : `{today}`\n⏰ Tɪᴍᴇ : `{time}`\n🌐 Tɪᴍᴇᴢᴏɴᴇ : `Asia/Kolkata`\n\n🉐 Vᴇʀsɪᴏɴ : `v{__version__} (Layer {layer})`</b>")
        tz = pytz.timezone('Asia/Kolkata')
 
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
