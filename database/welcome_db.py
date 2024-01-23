import pymongo
from pyrogram import enums
from info import DATABASE_URI, DATABASE_NAME
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

myclient = pymongo.MongoClient(DATABASE_URI)
mydb = myclient[DATABASE_NAME]

class Welcomedb:

    async def set_welcome(group_id, welcome_message):
        mycol = mydb[str(group_id)]
        mycol.update_one({"_id": group_id}, {"$set": {"file_id": welcome_message}})

    async def remove_welcome(group_id):
        mycol = mydb[str(group_id)]
        mycol.update_one({"_id": group_id}, {"$set": {"file_id": None}})

    async def set_welcome(self, group_id, welcome_message):
        await self.col.update_one({'_id': int(id)}, {'$set': {'file_id': welcome_message}})

    async def get_caption(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('caption', None)

wdb = Welcomedb(DATABASE_URI, DATABASE_NAME)
