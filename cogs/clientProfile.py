import discord
import pymongo
import asyncio
from discord.ext import commands

client_user = pymongo.MongoClient("mongodb+srv://lilybrown:Lilybrown.0001@cluster0.ccjaa.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client_user['Discord']
collectionPrefix = db['Prefix']
collectionStatus = db['Status']

blank = "<:blank:835155831074455622>"
inv = "<:inv:864984624052305961>"

class Clientprofile(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def prefix(self, ctx, prefix = None):
        server = collectionPrefix.find_one({"guild": str(ctx.guild.id)})
        guildPrefix = server["prefix"]
        if prefix == None:
            await ctx.send(f"Одоогийн prefix: `{guildPrefix}`\nPrefix солих заавар:\n> {guildPrefix}prefix `<new prefix>`")
        else:
            new = {"$set": {"prefix": str(prefix)}}
            collectionPrefix.update_one(server, new)
            await ctx.send(f"The prefix for this server was changed to `{prefix}`")

    @commands.command()
    async def changestatus(self, ctx, arg = None, *, text = None):
        if arg is None and text is None:
            embed = discord.Embed(title = "Command description:", description='!changestatus `<type>` `<title>`\ntype = `watch`, `listen`, `play`, `compet`, `stream`\ntitle = Anything you want\n> !changestatus compet Owm competition')
            await ctx.send(embed = embed)
            return
        elif text == None:
            await ctx.send("Please indicate the activity type\n`watch`, `listen`, `play`, `compet`, `stream`")
            return
        elif arg == 'watch':
            await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=text))
            profile = collectionStatus.find_one({"guild": "primoverse"})
            status = {"$set": {"status": "watch", "text": text}}
            collectionStatus.update_one(profile, status)
        elif arg == 'listen':
            await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=text))
            profile = collectionStatus.find_one({"guild": "primoverse"})
            status = {"$set": {"status": "listen", "text": text}}
            collectionStatus.update_one(profile, status)
        elif arg == 'play':
            await self.client.change_presence(activity=discord.Game(name=text))
            profile = collectionStatus.find_one({"guild": "primoverse"})
            status = {"$set": {"status": "play", "text": text}}
            collectionStatus.update_one(profile, status)
        elif arg == 'compet':
            await self.client.change_presence(activity = discord.Activity(type=discord.ActivityType.competing, name=text))
            profile = collectionStatus.find_one({"guild": "primoverse"})
            status = {"$set": {"status": "compet", "text": text}}
            collectionStatus.update_one(profile, status)
        elif arg == 'stream':
            await ctx.send("Enter the url of __twitch__ stream:")
            def check(message):
                return message.author == ctx.author and message.channel == ctx.channel
            try:
                message = await commands.wait_for('message', timeout=60.0, check=check)
            except asyncio.TimeoutError:
                await ctx.send("Cooldown is up!")
            else:
                profile = collectionStatus.find_one({"guild": "primoverse"})
                status = {"$set": {"status": "stream", "text": text, "url": message.content}}
                collectionStatus.update_one(profile, status)
                await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.streaming, name=text, url=message.content)) 
        await ctx.send(f"Changed the bot presence status as **{arg}ing {text}**!")

def setup(client):
    client.add_cog(Clientprofile(client))