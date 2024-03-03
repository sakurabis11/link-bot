from pyrogram import Client, filters
from pyrogram.types import Message
from utils import temp

@Client.on_messag(filters.command("chatbot"))
async def chatbot(client: Client, message: Message):
    try:
        user_id = message.from_user.id
        user_query = message.text.split()[1:]
        if not user_query:
            await message.reply_text("please provide a movie name, <code>/torent your name</code>")
            return 
        encoded_query = " ".join(user_query).replace(" ", "")
        response = requests.get(f"https://api.safone.dev/chatbot?query={encoded_query}&user_id={user_id}&bot_name={temp.U_NAME}&bot_master=mrtg")
        if response.status_code == 200:
            data = response.json()
            response = data["response"][0]
    
            await client.send_message(message.chat.id, response)
    except Exception as e:
            await message.reply_text(f"{e}")
        
