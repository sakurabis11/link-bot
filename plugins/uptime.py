from pyrogram import Client, filters
import psutil
import time
import os

def format_uptime(seconds):
    days = seconds // (24*60*60)
    seconds %= (24*60*60)
    hours = seconds // (60*60)
    seconds %= (60*60)
    minutes = seconds // 60
    seconds %= 60
    return f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds"

@bot.on_message(filters.command("system"))
def system_info(client, message):
    uptime = format_uptime(time.time() - psutil.boot_time())
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    total_disk = psutil.disk_usage('/').total / (1024.0 ** 3)
    used_disk = psutil.disk_usage('/').used / (1024.0 ** 3)
    used_disk_percent = psutil.disk_usage('/').percent
    free_disk = psutil.disk_usage('/').free / (1024.0 ** 3)
    client.send_message(chat_id=message.chat.id, text=f"Uᴩᴛɪᴍᴇ: {uptime}\nCPU Uꜱᴀɢᴇ: {cpu_usage}%\nRAM Uꜱᴀɢᴇ: {ram_usage}%\nTᴏᴛᴀʟ Dɪꜱᴋ: {total_disk} GB\nUꜱᴇᴅ Dɪꜱᴋ: {used_disk} GB ({used_disk_percent}%)\nFʀᴇᴇ Dɪꜱᴋ: {free_disk} GB")


