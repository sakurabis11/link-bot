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
BOT_TOKEN = os.environ.get('BOT_TOKEN', '6645084082:AAG0CA3ObIx5AFJrpsHjt7n0vEJKDu1aNQo')
BOT_TOKEN_2 = os.environ.get('BOT_TOKEN', '7149161535:AAFpWT16IXiIFuscFdAwtthXozr_GKcudEQ')
PORT = os.environ.get("PORT", "8080")
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ.get('ADMINS', "1342641151 6624136826").split()]
LOG_CHANNEL = int(environ.get('LOG_CHANNEL', '-1002084798134'))
REQUESTED_CHANNEL = int(os.environ.get("REQUESTED_CHANNEL", "-1002079640571"))
MELCOW_NEW_USERS = is_enabled((environ.get('MELCOW_NEW_USERS', "False")), False)
ADMIN_CHANNEL_ID = int(os.environ.get("ADMIN_CHANNEL_ID", "-1002001268584"))
EVAL_ID = int(os.environ.get("EVAL_ID", "-1002002636126"))
PIC_LOG_CHANNEL = int(os.environ.get("PIC_LOG_CHANNEL", "-1002078419108"))

# important information for your bot
S_GROUP = environ.get('S_GROUP', "https://t.me/sdbots_support")
S_CHANNEL = environ.get('S_CHANNEL', "https://t.me/sd_bots")

F_SUB = os.environ.get("FORCE_SUB", "sd_bots") 

# for mongodb
DATABASE_NAME = os.environ.get("DB_NAME", "mrtg")     
DATABASE_URI  = os.environ.get("DB_URL", "mongodb+srv://mrtg:3rqnL0nfKO1DgVM2@cluster0.m4nrgsu.mongodb.net/?retryWrites=true&w=majority")
MONGO_URL = os.environ.get('MONGO_URL', "")

DATABASE_NAME_2 = os.environ.get("DATABASE_NAME_2", "4QaG3MFKFOxz9xfS")
DATABASE_URI_2 = os.environ.get("DATABASE_URI_2", "mongodb+srv://4QaG3MFKFOxz9xfS:e!axPczC-zPF9MK@cluster0.ybcaemg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

#for spotify 
SPOTIFY_CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID', 'd3a0f15a75014999945b5628dca40d0a')
SPOTIFY_CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET', 'e39d1705e35c47e6a0baf50ff3bb587f')

#for google
G_API_KEY = os.environ.get('G_API_KEY','AIzaSyAGv5kIu2-E0N9eTdK7lzevl2nr3sOk6is')


