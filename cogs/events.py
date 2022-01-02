import discord
import pymongo
from discord.ext import commands

client_user = pymongo.MongoClient("mongodb+srv://lilybrown:Lilybrown.0001@cluster0.ccjaa.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client_user['Discord']
collectionPrefix = db['Prefix']
blank = "<:blank:835155831074455622>"
inv = "<:inv:864984624052305961>"

class Events(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        welcomeChannel = member.guild.get_channel(927195673684750336)
        embed = discord.Embed(description=f'Welcome to our server! {member.mention}\nYou are our {member.guild.member_count}th member')
        await welcomeChannel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        status = {"guild": str(guild.id), "prefix": "?"}
        collectionPrefix.insert_one(status)

def setup(client):
    client.add_cog(Events(client))