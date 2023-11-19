import re
import os
from os import environ
from pyrogram import enums
from Script import script

import asyncio
import json
from pyrogram import Client

API_ID = int(os.environ.get('API_ID', '8914119'))
API_HASH = os.environ.get('API_HASH', '652bae601b07c928b811bdb310fdb4b0')
BOT_TOKEN = os.environ.get('BOT_TOKEN', '')
