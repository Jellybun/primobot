import discord
import aiohttp
import pymongo
from typing import Union
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from functools import partial
from discord.ext import commands

client_user = pymongo.MongoClient("mongodb+srv://lilybrown:Lilybrown.0001@cluster0.ccjaa.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client_user['Discord']
collectionProfile = db['Profile']

coin = '<:coin:933027999299809380>'

blank = "<:blank:835155831074455622>"
inv = "<:inv:864984624052305961>"

class Membersetting(commands.Cog):
    def __init__(self, client):
        self.client = client            

    @staticmethod
    def processing(avatar_bytes: bytes, author, partner, rank, profile) -> BytesIO:
        level = int(profile['servers'][str(author.guild.id)]['level'])
        xp_asint = int(profile['servers'][str(author.guild.id)]['xp'])
        requiredxp = level**3 + 1000
        xp = f"{xp_asint}/{requiredxp}"
        size = int(1055*(xp_asint/requiredxp))
        balance = str(profile['profile']['coin'][1])
        desc = profile['profile']['about']
        marry = str(partner.name)
        rank = str(rank)
        with Image.open(BytesIO(avatar_bytes)) as mainImage:
            pfp = mainImage.resize((377,377))
            buffer = BytesIO()
            premainbar = Image.open("images/mainBar.png")
            background = Image.open('images/background.png')
   
            xpBar = premainbar.resize((size, 55))

            background.paste(pfp, (32, 32))
            background.paste(xpBar, (485, 273))

            draw = ImageDraw.Draw(background)
            size1 = ImageFont.truetype("arial.ttf", 100)
            size2 = ImageFont.truetype("arial.ttf", 70)
            size3 = ImageFont.truetype("arial.ttf", 55)
            name = str(author.name)
            draw.text((670, 173), str(level), (255, 255, 255), font=size2)
            draw.text((1170, 173), str(rank), (255, 255, 255), font=size2)
            draw.text((463, 45), str(name), (255, 255, 255), font=size1)
            draw.text((315, 575), str(balance), (255, 255, 255), font=size2)
            draw.text((1200, 353), str(xp), (255, 255, 255), font=size3)
            draw.text((840, 530), str(desc), (255, 255, 255), font=size2)
            draw.text((165, 695), str(marry), (255, 255, 255), font=size2)

            background.save(buffer, "png")
            buffer.seek(0)
            
            return buffer


    @commands.command(aliases=['rank', 'xp', 'level'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def profile(self, ctx, typo: Union[discord.Member, str]=None, section=None, *, desc=None):
        if typo is None and section is None and desc is None:
            async with ctx.channel.typing():
                profile = collectionProfile.find_one({'userId': ctx.author.id})
                avatar_url = ctx.author.avatar_url_as(format = 'png')
                pfp = await avatar_url.read()
                author = ctx.author
                partner = self.client.get_user(int(profile['profile']['marriage']))
                dex = 1
                for pro in collectionProfile.find().sort(f"servers.{str(ctx.guild.id)}", -1):
                    if pro['userId'] == int(ctx.author.id):
                        rank = dex
                        break
                    else:
                        dex += 1
                        pass
                fn = partial(self.processing, pfp, author, partner, rank, profile)

                final_buffer = await self.client.loop.run_in_executor(None, fn)
                file = discord.File(filename='test.png', fp=final_buffer)
                await ctx.send(file=file)
        elif section is None and desc is None:
            if isinstance(typo, discord.Member):
                profile = collectionProfile.find_one({'userId': typo.id})
                avatar_url = typo.avatar_url_as(format = 'png')
                pfp = await avatar_url.read()
                author = typo
                partner = self.client.get_user(int(profile['profile']['marriage']))
                dex = 1
                for pro in collectionProfile.find().sort(f"servers.{str(ctx.guild.id)}", -1):
                    if pro['userId'] == int(typo.id):
                        rank = dex
                        break
                    else:
                        dex += 1
                        pass
                fn = partial(self.processing, pfp, author, partner, rank, profile)
                final_buffer = await self.client.loop.run_in_executor(None, fn)
                file = discord.File(filename='test.png', fp=final_buffer)
                await ctx.send(file=file)
        else:
            if isinstance(typo, str) and typo == "set" and section == "about":
                if len(desc) > 18:
                    await ctx.send(f"**{ctx.author.name}**! Таны оруулсан text хэтэрхий урт байна!")
                    return
                profile = collectionProfile.find_one({"userId": ctx.author.id})
                status = {
                    "$set": {
                        "profile.about": str(desc)
                    }
                }
                collectionProfile.update_one(profile, status)
                await ctx.send(f"**{ctx.author.name}**! Таны **About me** хэсгийг **{desc}** болгож өөрчиллөө")


def setup(client):
    client.add_cog(Membersetting(client))