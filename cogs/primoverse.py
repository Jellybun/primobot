import discord
import datetime
import asyncio
import motor.motor_asyncio
from typing import Union
from discord.ext import commands
blank = "<:blank:835155831074455622>"
inv = "<:inv:864984624052305961>"

client_user = motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://lilybrown:Lilybrown.0001@cluster0.ccjaa.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client_user['Discord']
collectionServers = db['Servers']
collectionProfile = db['Profile']
collectionCommands = db['Commands']
collectionPrimoverse = db['Primoverse']

class Primoverse(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def servers(self, ctx):
        guilds = self.client.guilds
        x = 1
        for i in guilds:
            await ctx.send(f"{x}) **Guild name**: {i.name} {blank} **|** {blank} **Member count**: `{i.member_count}`")
            x += 1

    @commands.command()
    async def suggest(self, ctx, *, messag = None):
        if ctx.guild.id != 906153176414183475:
            return
        if messag == None:
            await ctx.send("No suggestion was found!")
        else:
            await ctx.send("Та хүсэлт бичихдээ итгэлтэй байна уу?\n`yes`/`no`")

            def check(m):
                return m.content.lower() in ["yes", 'no'] and m.channel == ctx.channel
            
            embed = discord.Embed(description=f"{messag}", color=3447003)
            embed.set_author(name=f"{ctx.author.name}'s suggestion:", icon_url=f"{ctx.author.avatar_url}")
            pchannel = self.client.get_channel(934100539187273849)
            try:
                message = await self.client.wait_for('message', timeout=60.0, check=check)
            except asyncio.TimeoutError:
                await ctx.send('Request timeout!')
            else:
                if message.content.lower() == 'yes':
                    await ctx.send("Таны хүсэлтийг амжилттай нийтлэлээ")
                    msg = await pchannel.send(embed=embed)
                    await msg.add_reaction("👍")
                    await msg.add_reaction("👎")
                else:
                    await ctx.send("Request closed!")


    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def selfrole(self, ctx, name, color: Union[str, int]):
        if ctx.guild.id == 906153176414183475:
            profile = await collectionPrimoverse.find_one({"guildName": "Primoverse"})
            keys = profile['boosters'].keys()
            rolename = name

            boosters = []
            boosterrole = ctx.guild.get_role(927487106840940546)
            memberojb = boosterrole.members
            for obj in memberojb:
                boosters.append(obj.id)

            if ctx.author.id not in boosters:
                await ctx.send("Танд **Server booster** role алга байна")
                return
            else:
                if isinstance(color, str):
                    hexcode = int(color, 16)
                elif isinstance(color, int):
                    hexcode = int(color)
                if str(ctx.author.id) not in keys:
                    await ctx.guild.create_role(name=rolename, color=discord.Colour(hexcode))
                    selfrole = discord.utils.get(ctx.guild.roles, name=rolename)
                    await ctx.author.add_roles(selfrole)
                    await ctx.send(f"Та амжилттай **{rolename}** role-ийг хийлээ")
                    status = {"$set": {
                        f"boosters.{str(ctx.author.id)}": selfrole.id
                    }}
                    await collectionPrimoverse.update_one(profile, status)
                else:
                    roleid = profile['boosters'][str(ctx.author.id)]
                    role = ctx.guild.get_role(roleid)
                    await role.edit(name=rolename, color=discord.Colour(hexcode))
                    await ctx.send(f"Та амжилттай **{rolename}** role-ийг шинэчлэлээ")
        else:
            pass

    @commands.command()
    async def commit(self, ctx, *, text):
        if ctx.channel == ctx.author.dm_channel:
            now = datetime.datetime.now().strftime("%x")
            channel = self.client.get_channel(932535601977262132)
            store = ""
            word = ""
            i = 0
            while True:
                if text[i] == "," and text[i+1] == " ":
                    store += f"`–{word}`\n\n"
                    word = ""
                    i += 2
                else:
                    word += text[i]
                    i += 1
                    if i == len(text):
                        store += f"`–{word}`\n\n"
                        break
            embed = discord.Embed(title='New bot commits', description=store, color=15548997)
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            embed.set_footer(text=now)
            await channel.send(embed=embed)
    

def setup(client):
    client.add_cog(Primoverse(client))