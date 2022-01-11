import pymongo
import motor.motor_asyncio
client_user = motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://lilybrown:Lilybrown.0001@cluster0.ccjaa.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client_user['Discord']
collectionProfile = db['Profile']

async def profilechecker(memberId):
    if collectionProfile.count_documents({"userId": int(memberId)}) == 0:
        status = {"userId": memberId, "about": None, "economy": {"wallet": 0, "golomt": 0, "khan": 0}, "career": None}
        await collectionProfile.insert_one(status)
    else:
        pass