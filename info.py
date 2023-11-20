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
