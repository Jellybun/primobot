import discord
import asyncio
import json
import aiohttp
from discord.ext import commands
blank = "<:blank:835155831074455622>"
inv = "<:inv:864984624052305961>"

async def get_apod():
    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://api.nasa.gov/planetary/apod?api_key=FHlnYmh56cpv8KVLOdW8k2mCdKhAYT47A6XEKZCG') as r:
            json_data = await r.json()
            return json_data


class Api(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def nasa(self, ctx):
        data = await get_apod()
        image = data["hdurl"]
        if image is None:
            await ctx.send("Өнөөдөр **NASA**-аас шинэ зураг ороогүй байна\nТа дараа дахин шалгана уу")
            return

        title = data['title']
        if title is None:
            title = "Today's post"
        date = data['date']
        if date is None:
            date = 'Today'
        explanation = data['explanation']
        if explanation is None:
            explanation = 'No description'
        author = data['copyright']
        if author is None:
            author = 'Anonymous'
        embed = discord.Embed(title=title, description=str(explanation), color=16777215)
        embed.set_thumbnail(url=self.client.user.avatar_url)
        embed.set_author(name=str(author))
        embed.set_image(url=str(image))
        embed.set_footer(text=str(date))
        await ctx.send(embed = embed)

    

def setup(client):
    client.add_cog(Api(client))