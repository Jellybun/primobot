import discord
import pymongo
import asyncio
import motor.motor_asyncio
from discord.ext import commands

client_user = motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://lilybrown:Lilybrown.0001@cluster0.ccjaa.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client_user['Discord']
collectionServers = db['Servers']

blank = "<:blank:835155831074455622>"
inv = "<:inv:864984624052305961>"

class Clientprofile(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(manage_messages = True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def prefix(self, ctx, prefix: str = None):
        server = await collectionServers.find_one({"guildId": ctx.guild.id})
        guildPrefix = server["prefix"]
        if prefix == None:
            embed = discord.Embed(title="Command заавар", description=f"Одоогийн prefix: ```{guildPrefix}```\n\nPrefix солих:\n> {guildPrefix}prefix `<new prefix>`", color=16777215)
            await ctx.send(embed=embed)
        else:
            new = {"$set": {"prefix": prefix}}
            await collectionServers.update_one(server, new)
            await ctx.send(f"Серверийн prefix-ийг амжилттай`{prefix}` болгож өөрчиллөө")

def setup(client):
    client.add_cog(Clientprofile(client))