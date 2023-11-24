import psutil

from pyrogram import Client, filters

@Client.on_message(filters.command("uptime"))
def uptime_status(client, message):
    uptime = psutil.boot_time()
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage("/")

    message.reply_text(
        f"Uᴩᴛɪᴍᴇ: {psutil.elapsed_time(uptime)}\\n"
        f"CPU Uꜱᴀɢᴇ: {cpu_usage:.1f}%\\n"
        f"RAM Uꜱᴀɢᴇ: {ram_usage:.1f}%\\n"
        f"Tᴏᴛᴀʟ Dɪꜱᴋ: {disk_usage.total:,} GB\\n"
        f"Uꜱᴇᴅ Dɪꜱᴋ: {disk_usage.used:,} GB ({disk_usage.percent:.1f}%)\\n"
        f"Fʀᴇᴇ Dɪꜱᴋ: {disk_usage.free:,} GB"
    )
    
  message.reply_text(uptime_status)

