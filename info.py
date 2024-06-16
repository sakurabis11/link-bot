import re
import os
from os import environ
from pyrogram import enums
import asyncio
import json
from pyrogram import Client

id_pattern = re.compile(r'^.\d+$')
def is_enabled(value, default):
    if value.strip().lower() in ["on", "true", "yes", "1", "enable", "y"]: return True
    elif value.strip().lower() in ["off", "false", "no", "0", "disable", "n"]: return False
    else: return default

API_ID = int(os.environ.get('API_ID', '8914119'))
API_HASH = os.environ.get('API_HASH', '652bae601b07c928b811bdb310fdb4b0')

BOT_TOKEN_2 = os.environ.get('BOT_TOKEN', '7149161535:AAFpWT16IXiIFuscFdAwtthXozr_GKcudEQ')
PORT = os.environ.get("PORT", "8080")
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ.get('ADMINS', "1342641151 6624136826").split()]

PIC_LOG_CHANNEL = int(os.environ.get("PIC_LOG_CHANNEL", "-1002078419108"))

# important information for your bot
S_GROUP = environ.get('S_GROUP', "https://t.me/sdbots_support")
S_CHANNEL = environ.get('S_CHANNEL', "https://t.me/sd_bots")

DATABASE_NAME_2 = os.environ.get("DATABASE_NAME_2", "4QaG3MFKFOxz9xfS")
DATABASE_URI_2 = os.environ.get("DATABASE_URI_2", "mongodb+srv://4QaG3MFKFOxz9xfS:e!axPczC-zPF9MK@cluster0.ybcaemg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

