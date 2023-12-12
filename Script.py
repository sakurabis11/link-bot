class script(object):  
    LOG_TEXT_G = """<b>#ɴᴇᴡ_ɢʀᴏᴜᴩ

◉ ɢʀᴏᴜᴩ: {}(<code>{}</code>)
◉ ᴍᴇᴍʙᴇʀꜱ: <code>{d}</code>
◉ ᴀᴅᴅᴇᴅ ʙʏ: {}"""
    
    LOG_TEXT_P = """#ɴᴇᴡ_ᴜꜱᴇʀ
    
◉ ᴜꜱᴇʀ-ɪᴅ: <code>{}</code>
◉ ᴀᴄᴄ-ɴᴀᴍᴇ: {}"""

    START_TXT = """Hᴇʟʟᴏ {}.
Mʏ Nᴀᴍᴇ Is <a href=https://t.me/{}>{}</a>. ɪ ᴀᴍ ᴀ sᴘᴇᴄɪᴀʟ ʙᴏᴛ"""

    HELP_TXT = """Hᴇʀᴇ ɪs Mʏ Hᴇʟᴩ.
ᴄʟɪᴄᴋ ᴛʜɪs /support"""

    ABOUT_TXT = """<b>✯ Mʏ ɴᴀᴍᴇ ɪs {} </>
✯ Dᴇᴠᴇʟᴏᴩᴇʀ: <a href='https://t.me/MrTG_Coder'>ᴍʀ.ʙᴏᴛ ᴛɢ</a>
✯ Lɪʙʀᴀʀʏ: <a href='https://docs.pyrogram.org/'>Pʏʀᴏɢʀᴀᴍ</a>
✯ Lᴀɴɢᴜᴀɢᴇ: <a href='https://www.python.org/download/releases/3.0/'>Pʏᴛʜᴏɴ 3</a>
✯ Mʏ Sᴇʀᴠᴇʀ: <a href='https://www.render.com'>ʀᴇɴᴅᴇʀ </a>
✯ Pʏʀᴏɢʀᴀᴍ ᴠᴇʀsɪᴏɴ: ᴠ2.0.30
✯ Mʏ ᴠᴇʀsɪᴏɴ: ᴠ1.8"""

    RRB_TXT = """ɪғ ᴀɴʏ ʙᴜɢs ɪɴ ᴛʜɪs ʙᴏᴛ ғᴏʀᴡᴀʀᴅ ᴛʜᴇ ᴍᴇssᴀɢᴇ ᴛᴏ sᴜᴘᴘᴏʀᴛ ᴀᴅᴍɪɴ. ᴛʜɪs ʙᴏᴛ ɪs ᴀ ᴏᴘᴇɴ sᴏᴜʀᴄᴇ ᴘʀᴏᴊᴇᴄᴛ"""

    SUPPORT_TXT = """ᴛʜᴇsᴇ ᴀʀᴇ ᴍʏ sᴜᴘᴘᴏʀᴛ ᴄʜᴀɴɴᴇʟ ᴀɴᴅ ɢʀᴏᴜᴘ. ɪғ ᴀɴʏ ᴘʀᴏʙʟᴇᴍ, ʀᴇᴘᴏʀᴛ ᴛᴏ ᴛʜᴇ ᴀᴅᴍɪɴ"""

    STATUS_TXT =  """<b>◉ ᴛᴏᴛᴀʟ ᴜꜱᴇʀꜱ: <code>{}</code></b>"""

    ADMIN_CMD_TXT = """/broadcast ᴛᴏ ʙʀᴏᴀᴅᴄᴀsᴛ ᴀ ᴍᴇssɢᴇ ᴛᴏ ʟʟ ᴜsᴇʀs\n/leave ᴛᴏ ʟᴇᴀᴠᴇ ғʀᴏᴍ ᴀ ɢʀᴏᴜᴘ\n/ban ᴛᴏ ʙᴀɴ ᴀ ᴜsᴇʀ\n/unban ᴛᴏ ᴜɴʙᴀɴ ᴛʜᴇ ʙᴀɴɴᴇᴅ ᴜsᴇʀ\n/users ᴛᴏ ɢᴇᴛ ᴛʜᴇ ʟɪsᴛ ᴏғ ᴜsᴇʀs\n.ping ғᴏʀ ᴛʜᴇ ᴘᴏɴɢ"""

    TELEGRAGH_TXT = """/telegraph Rᴇᴘʟʏ Tᴏ A Pʜᴏᴛᴏ Oʀ Vɪᴅᴇᴏ"""

    OPENAI_TXT = """/openai {ᴜʀ ǫᴜᴇsᴛɪᴏɴ}\n sᴏᴍᴇᴛɪᴍᴇs ɪᴛ ᴡɪʟʟ ɴᴏᴛ ᴡᴏʀᴋ ᴘʀᴏᴘᴇʀʟʏ"""

    SONG_TXT = """/song {song_name} .ᴅᴏᴡɴʟᴏᴀᴅ sᴏɴɢ ғʀᴏᴍ ʏᴏᴜᴛᴜʙᴇ
ᴄʀᴇᴅɪᴛs @MrTG_Coder"""

    RINGTUNE_TXT = """ʏᴏᴜ ᴄᴀɴ ᴀsᴋ ʀɪɴɢᴛᴜɴᴇ ɪɴ ᴛʜᴇ ғʀᴏᴍ ᴏғ /ringtune {sᴏɴɢ_ɴᴀᴍᴇ + ᴀʀᴛɪsᴛ_ɴᴀᴍᴇ} ᴏʀ {sᴏɴɢ_ɴᴀᴍᴇ}\n <a href='https://t.me/amal_nath_05/197'>ʀᴇᴀsᴏɴ</a>
ᴄʀᴇᴅɪᴛs @MrTG_Coder"""

    STICKER_TXT = """reply to the sticker as /sticker_id"""

    SPOTIFY_TXT = """/spotify {song_name}\nɴᴏᴡ ᴡᴇ ᴏɴʟʏ ᴀᴅᴅ ғɪɴᴅ ᴛʜᴇ sᴏɴɢ ᴅᴇᴛᴀɪʟs ʙʏ ᴜʀ ʀᴇǫᴜᴇsᴛ.
ᴄʀᴇᴅɪᴛs @MrTG_Coder"""

    REPO_TXT = """/repo ᴛᴏ sᴇᴀʀᴄʜ ᴛʜᴇ ʀᴇᴘᴏsɪᴛᴏʀʏ
ᴄʀᴇᴅɪᴛs @MrTG_Coder"""

    CREATOR_REQUIRED = """❗<b>You have To Be The Group Creator To Do That.</b>"""
      
    INPUT_REQUIRED = "❗ **Arguments Required**"
      
    KICKED = """✔️ Successfully Kicked {} Members According To The Arguments Provided."""
      
    START_KICK = """🚮 Removing Inactive Members This May Take A While..."""
      
    ADMIN_REQUIRED = """❗<b>എന്നെ Admin ആക്കത്ത സ്ഥലത്ത് ഞാൻ നിക്കില്ല പോകുവാ Bii..Add Me Again with all admin rights.</b>"""
      
    DKICK = """✔️ Kicked {} Deleted Accounts Successfully."""
      
    FETCHING_INFO = """<b>ഇപ്പൊ എല്ലാം അടിച്ചുമാറ്റി തരാം...</b>"""

    STATUS = """{}\n<b>Chat Member Status</b>**\n\n```<i>Recently``` - {}\n```Within Week``` - {}\n```Within Month``` - {}\n```Long Time Ago``` - {}\nDeleted Account - {}\nBot - {}\nUnCached - {}</i>
"""
