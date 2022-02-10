import motor.motor_asyncio

client_user = motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://lilybrown:Lilybrown.0001@cluster0.ccjaa.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client_user['Discord']
collectionProfile = db['Profile']
collectionServers = db['Servers']

async def createprofile(member):
    if await collectionProfile.count_documents({"userId": member.id}) == 0:
        status = {
            "userId": id,
            "daily": False,
            "profile": {
                "coin": [0, 1000],
                "marriage": "Single",
                "about": "instagram"
            },
            "inventory": {
                "ring": 0
            },
            "servers": {
                str(member.guild.id): {
                    "id": member.guild.id,
                    "level": 0,
                    "xp": 17
                }
            }
        }
        await collectionProfile.insert_one(status)
    else:
        pass