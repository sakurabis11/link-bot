from pyrogram import Client, filters, enums
from pyrogram.types import Message
from pyrogram.errors import *

SESSION = "BQFfGLgAOEVHO5SMtutxL_-hK_Oq9SvQ8A-aJwjXfChqxkfj6ftuLp0mwizMFhu0U0lL1XII-BB8vgCrCUBTevCKbFZBtILBUAwv-LOoQ5j5JXq5buGyXcoNWbOhVbDdsVatZylKV8ObtqQwQhSe-dQK7IKaFOUmkNpkX9oz4Eosw4JMqI-axj0Vopc3e9ZucUUuy0dOqgsRANwCYrcNPr1hoWXrAZ6QDQ1KhTzgZ4qrsi-JIfXv-yoXlAEW_F9Zd1Ql6e9LtBeF-b7KVjg1gDNvKqnU5TvqPoVXRNlbDhGJRskJzXAOmku70EwzvIt9hGK-3XPZcZHFA4_gzW5YD23HSQFmWQAAAAEqYqWoAA"

CMD = "!, ., /, $"

@Client.on_message(filters.command("alive" ,CMD))
async def ping(client, message):
    start_t = time.time()
    rm = await message.reply_text("...")
    end_t = time.time()
    time_taken_s = (end_t - start_t) * 1000
    uptime = format_uptime(time.time() - psutil.boot_time())
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    used_disk = psutil.disk_usage('/').percent
    used_disk_percent = psutil.disk_usage('/').percent
    await rm.edit(f"<b>🏓 Pong!\n<code>{time_taken_s:.3f} ms</code>\n</b>\n\n\nUᴩᴛɪᴍᴇ: <code>{uptime}</code>\nCPU Uꜱᴀɢᴇ: <code>{cpu_usage}%</code>\nRAM Uꜱᴀɢᴇ: <code>{ram_usage}%</code>\nUꜱᴇᴅ Dɪꜱᴋ: <code>{used_disk} GB </code>(<code>{used_disk_percent}%</code>)\n")
