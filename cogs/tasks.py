import discord
import pymongo
import asyncio
from discord.ext import commands, tasks
client_user = pymongo.MongoClient("mongodb+srv://lilybrown:Lilybrown.0001@cluster0.ccjaa.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client_user['Discord']
collectionPrefix = db['Prefix']
collectionStatus = db['Status']
blank = "<:blank:835155831074455622>"
inv = "<:inv:864984624052305961>"

class Tasks(commands.Cog):
    def __init__(self, client):
        self.client = client
        

def setup(client):
    client.add_cog(Tasks(client))
