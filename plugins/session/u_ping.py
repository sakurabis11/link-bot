import time
import random
from pyrogram.types import Message
from pyrogram import Client, filters

session_string = "BQFfGLgAj8xENk_tfWYlYlMh5SUoF7rkDWLChb8h6R3TntOlhsJs2zWkEpCx011U7q98hReI9CA-0DVqCJRpc-xI6YArLif0z9sCuMvcutBcLmLm6t7AqoVQL8MeTJexNjzge6xf4FPZsbWcwBn_iUUR0zkofhhjWjFjGZTwDnn4JdIOvz0U-oeuQj2VcF0xzLgei7uZ_hZ0muFEo9S_Dc7ABqcsNhckh9IUbGynPPSFphkMxs6r9nkBe-FoooGITH0eUD_rRytksx3W9o_isAF5kc8LtIkISJDZ3js1E3HpKbfy3wXRRdoCh51edFCReFGLcX4fe4lli3TR0SwcqidwN36OEQAAAAEqYqWoAA"   

@Client.on_message(filters.command("ping", "!"))
async def ping_me(client, message: Message):
    """Ping the assistant"""
    start = time.time()
    reply = await message.reply_text("...")
    delta_ping = time.time() - start
    await reply.edit_text(f"**Pong!**\n`{delta_ping * 1000:.3f} ms`")
