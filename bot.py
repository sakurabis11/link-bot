from pyrogram import Client
from info import API_ID, API_HASH, BOT_TOKEN, PORT
import os, math, logging, datetime, pytz
import logging.config
from pyrogram.errors import BadRequest, Unauthorized
from aiohttp import web
from typing import Union, Optional, AsyncGenerator


logging.config.fileConfig("logging.conf")
logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)

class Bot(Client):

    def __init__(self):
        super().__init__(
            name="simple-renamer",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=100,
            plugins={"root": "plugins"},
            sleep_threshold=10,
        )
    async def start(self):
        await super().start()
        me = await self.get_me()
        temp.U_NAME = me.username
        temp.B_NAME = me.first_name
        app = web.AppRunner(await web_server())
        await app.setup()
        await web.TCPSite(app, "0.0.0.0", 8080).start()
        logger.info("Web Response Is Running......🕸️")
        print(f"{me.first_name} | @{me.username} 𝚂𝚃𝙰𝚁𝚃𝙴𝙳...⚡️")

       
    async def stop(self, *args):
       await super().stop()      
       print("Bot Restarting........")

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


bot = Bot()
bot.run()
