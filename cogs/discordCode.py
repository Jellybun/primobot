import discord
import asyncio
import motor
from discord.ext import commands
blank = "<:blank:835155831074455622>"
inv = "<:inv:864984624052305961>"

client_user = motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://lilybrown:Lilybrown.0001@cluster0.ccjaa.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client_user['Discord']
collectionPrefix = db['Prefix']
collectionTags = db['Tags']

class Discordcode(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def tag(self, ctx, definer=None, *, text=None):
        if definer.lower() == "create":
            if await collectionTags.count_documents({"tagName": text}) == 0:
                def check(message):
                    return message.author == ctx.author and message.channel == ctx.channel
                await ctx.send(f"What will be the content of the tag **{text}**?")
                try:
                    message = await commands.wait_for('message', timeout=30.0, check=check)
                except asyncio.TimeoutError:
                    await ctx.send("Cooldown is up!")
                else:
                    document = {"tagName": text, "tagContent": message.content}
                    await collectionTags.insert_one(document)
                    await ctx.send(f"Successfully created the tag: **{text}**")
            else:
                await ctx.send("Tag already exists!")
                return
        else:
            if await collectionTags.count_documents({"tagName": text}) == 0:
                await ctx.send("Tag doesn't exist")
                return
            else:
                profile = await collectionTags.find_one({"tagName": text})
                await ctx.send(profile['tagContent'])
                

    

def setup(client):
    client.add_cog(Discordcode(client))