import discord
import pymongo
import datetime
import motor.motor_asyncio
from discord.ext import commands
from profileChecker import profilechecker


client_user = motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://lilybrown:Lilybrown.0001@cluster0.ccjaa.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client_user['Discord']
collectionPrefix = db['Prefix']
collectionProfile = db['Profile']
blank = "<:blank:835155831074455622>"
inv = "<:inv:864984624052305961>"

class Events(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        oldHour = datetime.datetime.now(datetime.timezone.utc).strftime("%H")
        now = datetime.datetime.now(datetime.timezone.utc)
        newHour = int(oldHour) + 8
        new = now.replace(hour=newHour)
        
        welcomeChannel = self.client.get_channel(927195673684750336)
        welcomeMessage = await welcomeChannel.fetch_message(927256713999040532)
        embed = discord.Embed(description=f'Welcome to our server! {member.mention}\nYou are our {member.guild.member_count}th member', color=16777215)
        embed.set_image(url='https://cdn.discordapp.com/attachments/832245157889441855/930055311887323206/Screen_Shot_2021-12-30_at_19.22.44.png')
        embed.set_author(name=member.name, icon_url=member.avatar_url)
        embed.set_footer(text=new)
        profilechecker(member.id)
        await welcomeMessage.edit(embed=embed)


    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        status = {"guild": str(guild.id), "prefix": "?"}
        await collectionPrefix.insert_one(status)

def setup(client):
    client.add_cog(Events(client))