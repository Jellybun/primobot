import discord
import pymongo
import asyncio
import datetime
import motor.motor_asyncio
from discord.ext import commands, tasks
client_user = motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://lilybrown:Lilybrown.0001@cluster0.ccjaa.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client_user['Discord']
collectionPrefix = db['Prefix']
collectionStatus = db['Status']
blank = "<:blank:835155831074455622>"
inv = "<:inv:864984624052305961>"

class Tasks(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.dailyTask.start()


    @commands.command()
    async def time(self, ctx):
        await ctx.send(datetime.datetime.now(datetime.timezone.utc))

    @tasks.loop(hours=24)
    async def dailyTask(self):
        print("Got in the daily tasks")
        mChannel = self.client.get_channel(928563610408607774)
        jelly = self.client.get_user(759756236996083713)
        await mChannel.send(f"Works\n{jelly.mention}")

    @dailyTask.before_loop
    async def until_next_run(self):
        now = datetime.datetime.now(datetime.timezone.utc)
        later = now.replace(hour=8, minute=33, second=00)
        if later < now:
            later += datetime.timedelta(days=1)
        await discord.utils.sleep_until(later)
        print(f"Sleeping until {later}")
        
def setup(client):
    client.add_cog(Tasks(client))
