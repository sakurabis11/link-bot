import pyrogram 
from pyrogram import Client, filters
from pyrogram.types import *

@Client.on_message(filters.command("start"))
