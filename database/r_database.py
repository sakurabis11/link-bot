import pymongo 
import motor.motor_asyncio
import os
from info import DATABASE_NAME, DATABASE_URI

mongo = pymongo.MongoClient(DATABASE_URI)
db = mongo[DATABASE_NAME]
dbcol = db["user"]
      
#insert bot Data 
async def botdata(chat_id):
	bot_id = int(chat_id)
	try:
		bot_data = {"_id":bot_id,"total_rename":0,"total_size":0}
		dbcol.insert_one(bot_data)
	except:
		pass


async def total_rename(chat_id,renamed_file):
	now = int(renamed_file) + 1
	dbcol.update_one({"_id":chat_id},{"$set":{"total_rename":str(now)}})
	
async def total_size(chat_id,total_size,now_file_size):
	now = int(total_size) + now_file_size
	dbcol.update_one({"_id":chat_id},{"$set":{"total_size":str(now)}})


async def addthumb(chat_id, file_id):
	dbcol.update_one({"_id":chat_id},{"$set":{"file_id":file_id}})
	
async def delthumb(chat_id):
	dbcol.update_one({"_id":chat_id},{"$set":{"file_id":None}})

async def find_one(id):
	return dbcol.find_one({"_id":id})

async def def find(chat_id):
	id =  {"_id":chat_id}
	x = dbcol.find(id)
	for i in x:
             file = i["file_id"]
             try:
                 caption = i["caption"]
             except:
                 caption = None
                 
             return [file, caption]

