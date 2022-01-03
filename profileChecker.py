import pymongo
client_user = pymongo.MongoClient("mongodb+srv://lilybrown:Lilybrown.0001@cluster0.ccjaa.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client_user['Discord']
collectionProfile = db['Profile']

def profilechecker(memberId):
    if collectionProfile.count_documents({"userId": int(memberId)}) == 0:
        status = {"userId": memberId, "about": None, "economy": {"wallet": 0, "golomt": 0, "khan": 0}, "career": None}
        collectionProfile.insert_one(status)
    else:
        pass