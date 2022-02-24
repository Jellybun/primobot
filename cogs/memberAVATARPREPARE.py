import discord
import aiohttp
import motor.motor_asyncio
from typing import Union
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from functools import partial
from discord.ext import commands

client_user = motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://lilybrown:Lilybrown.0001@cluster0.ccjaa.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client_user['Discord']
collectionProfile = db['Profile']

coin = '<:coin:933027999299809380>'

blank = "<:blank:835155831074455622>"
inv = "<:inv:864984624052305961>"

class Membersetting(commands.Cog):
    def __init__(self, client):
        self.client = client            

    @staticmethod
    def processing(avatar_bytes: bytes, name: str, level: int, xp: int, rank: str) -> BytesIO:
        requiredxp = level**3 + 1000
        footer = f"{xp}/{requiredxp}"
        size = int(445*(xp/requiredxp))
        if size < 28:
            size = 1
        with Image.open(BytesIO(avatar_bytes)) as pfp:
            buffer = BytesIO()
            premainbar = Image.open("images/bar.png")
            background = Image.open('images/background.png')
            xpBar = premainbar.resize((size, 29))
            pfp = pfp.resize((70, 70))

            background.paste(pfp, (16, 15))
            background.paste(xpBar, (30, 128))

            draw = ImageDraw.Draw(background)
            size2 = ImageFont.truetype("quicksand.ttf", 30)

            draw.text((15, 90), f'Level: {level}     Rank: {rank}            {footer}', (0, 0, 0), font=size2)
            draw.text((110, 20), str(name), (0, 0, 0), font=size2)
            background.save(buffer, "png")
            buffer.seek(0)
            
            return buffer


    @commands.command(aliases=['rank', 'xp', 'level'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def profile(self, ctx, typo: Union[discord.Member, str]=None, *, desc=None):
        if typo is None and desc is None:
            async with ctx.channel.typing():
                profile = await collectionProfile.find_one({'userId': ctx.author.id})
                avatar_url = ctx.author.avatar_url_as(format='png')
                pfp = await avatar_url.read()
                name = ctx.author.name
                level = profile['servers'][str(ctx.guild.id)]['level']
                xp = profile['servers'][str(ctx.guild.id)]['xp']
                dex = 1
                async for pro in collectionProfile.find().sort(f"servers.{str(ctx.guild.id)}.level", -1):
                    if pro['userId'] == int(ctx.author.id):
                        rank = dex
                        break
                    else:
                        dex += 1
                        pass
                fn = partial(self.processing, pfp, name, level, xp, rank)
                final_buffer = await self.client.loop.run_in_executor(None, fn)
                file = discord.File(filename='test.png', fp=final_buffer)
                await ctx.send(file=file)
        elif desc is None:
            if isinstance(typo, discord.Member):
                profile = await collectionProfile.find_one({'userId': typo.id})
                avatar_url = typo.avatar_url_as(format='png')
                pfp = await avatar_url.read()
                name = typo.name
                level = profile['servers'][str(ctx.guild.id)]['level']
                xp = profile['servers'][str(ctx.guild.id)]['xp']
                dex = 1
                async for pro in collectionProfile.find().sort(f"servers.{str(ctx.guild.id)}.level", -1):
                    if pro['userId'] == int(typo.id):
                        rank = dex
                        break
                    else:
                        dex += 1
                        pass
                fn = partial(self.processing, pfp, name, level, xp, rank)
                final_buffer = await self.client.loop.run_in_executor(None, fn)
                file = discord.File(filename='test.png', fp=final_buffer)
                await ctx.send(file=file)
        else:
            if isinstance(typo, str) and typo == "set":
                if len(desc) > 18:
                    await ctx.send(f"**{ctx.author.name}**! Таны оруулсан text хэтэрхий урт байна!")
                    return
                profile = await collectionProfile.find_one({"userId": ctx.author.id})
                status = {
                    "$set": {
                        "profile.about": str(desc)
                    }
                }
                collectionProfile.update_one(profile, status)
                await ctx.send(f"**{ctx.author.name}**! Таны description хэсгийг **{desc}** болгож өөрчиллөө")


def setup(client):
    client.add_cog(Membersetting(client))