import os 
from pyrogram import Client, filters
from info import BOT_TOKEN

token = os.environ.get('TOKEN',BOT_TOKEN)
botid = token.split(':')[0]

from from database.r_database import botdata, find_one, total_user
from plugins.Rename.r_utils import *
@Client.on_message(filters.private & filters.command(["r_stats"]))
async def start(client,message):
	botdata(int(botid))
	data = find_one(int(botid))
	total_rename = data["total_rename"]
	total_size = data["total_size"]
	await message.reply_text(f"Total Renamed File :-{total_rename}\nTotal Size Renamed :- {humanbytes(int(total_size))} ",quote=True)
