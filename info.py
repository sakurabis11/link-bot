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

class Info(object):
# bot information
    API_ID = int(os.environ.get('API_ID', '8914119'))
    API_HASH = os.environ.get('API_HASH', '652bae601b07c928b811bdb310fdb4b0')
    BOT_TOKEN = os.environ.get('BOT_TOKEN', '6645084082:AAEvdcfTZ0uFS_Gu6KvVPVBMNlrlWiESPiM')
    PORT = os.environ.get("PORT", "8080")
    CACHE_TIME = int(environ.get('CACHE_TIME', 300))
    ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ.get('ADMINS', '1342641151').split()]

# for mongodb
    DB_NAME = os.environ.get("DB_NAME", "mrtg")     
    DB_URL  = os.environ.get("DB_URL", "mongodb+srv://mrtg:3rqnL0nfKO1DgVM2@cluster0.m4nrgsu.mongodb.net/?retryWrites=true&w=majority")

# for openai
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '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')

#for spotify 
    SPOTIFY_CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID', 'd3a0f15a75014999945b5628dca40d0a')
    SPOTIFY_CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET', 'e39d1705e35c47e6a0baf50ff3bb587f')

# optional
    PIC = (environ.get('PICS', 'https://telegra.ph/file/67a238112341dc2da77d9.jpg')).split()
    LOG_CHANNEL = int(environ.get('LOG_CHANNEL', '-1002084798134'))

