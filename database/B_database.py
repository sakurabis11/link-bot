from info import DATABASE_NAME, DATABASE_URI
from pymongo import MongoClient

myclient = MongoClient(DATABASE_NAME)
mydb = myclient[DATABASE_URI]
usrcol = mydb['users']
botcol = mydb['Bots']

class B_database:

    async def add_bot(self, user_id, owner, bot_id, bot_token, username):
        bot = {'_id': user_id, 'owner': first_name, 'bot_token': bot_token, 'bot_id': bot_id, 'username': username}
        botcol.insert_one(bot)

    async def is_bot_token(self, token):
        bot = botcol.find_one({'bot_token': token})
        return bool(bot)

bdb = B_database()
