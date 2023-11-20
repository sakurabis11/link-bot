import re
import os
from os import environ
from pyrogram import enums

import asyncio
import json
from pyrogram import Client

API_ID = int(os.environ.get('API_ID', '8914119'))
API_HASH = os.environ.get('API_HASH', '652bae601b07c928b811bdb310fdb4b0')
BOT_TOKEN = os.environ.get('BOT_TOKEN', '6866077251:AAGMOU-l84Qe_PIZFQ_pH5M7BALyhqbqK_E')
PORT = os.environ.get("PORT", "8080")

CACHE_TIME = int(environ.get('CACHE_TIME', 300))
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ.get('ADMINS', '1342641151').split()]

# MongoDB information
DATABASE_URL = environ.get('DATABASE_URL', "mongodb+srv://Gojo:gojo@cluster0.cn6dtat.mongodb.net/?retryWrites=true&w=majority&appName=AtlasApp")
DATABASE_NAME = environ.get('DATABASE_NAME', "gojo")

LOG_CHANNEL = int(environ.get('LOG_CHANNEL', '-1002084798134'))
