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
        if definer is None and text is None:
            await ctx.send("?tag create `<tagName>`")
            return
        elif definer.lower() == "create":
            if await collectionTags.count_documents({"tagName": text}) == 0:
                await ctx.send(f"What will be the content of the tag **{text}**?")
                def check(message):
                    return message.author == ctx.author and message.channel == ctx.channel
                try:
                    message = await self.client.wait_for('message', timeout=60.0, check=check)
                except asyncio.TimeoutError:
                    await ctx.send("Cooldown is up!")
                else:
                    document = {"tagName": str(text), "tagContent": str(message.content)}
                    await collectionTags.insert_one(document)
                    await ctx.send(f"Successfully created the tag: **{text}**")
            else:
                await ctx.send("Tag already exists!")
                return
        elif definer.lower() == "edit":
            if await collectionTags.count_documents({"tagName": text}) != 0:
                await ctx.send(f"What will be the content of the new tag **{text}**?")
                def check(message):
                    return message.author == ctx.author and message.channel == ctx.channel
                try:
                    message = await self.client.wait_for('message', timeout=60.0, check=check)
                except asyncio.TimeoutError:
                    await ctx.send("Cooldown is up!")
                else:
                    profile = await collectionTags.find_one({"tagName": str(text)})
                    document = {"tagName": text, "tagContent": message.content}
                    await collectionTags.update_one(profile, document)
                    await ctx.send(f"Successfully edited the tag: **{text}**")
            else:
                await ctx.send("Tag doesn't exists!")
                return
        elif text is None:
            tagName = definer.lower()
            if await collectionTags.count_documents({"tagName": tagName}) == 0:
                await ctx.send("Tag doesn't exist")
                return
            else:
                profile = await collectionTags.find_one({"tagName": tagName})
                await ctx.send(profile['tagContent'])
                

    

def setup(client):
    client.add_cog(Discordcode(client))