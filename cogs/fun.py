import discord
import random
import asyncio
from discord.ext import commands
blank = "<:blank:835155831074455622>"
inv = "<:inv:864984624052305961>"

class Helpcommand(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def poke(self, ctx, member : discord.Member = None, *, msg = None):
        jelly = self.client.get_user(759756236996083713)
        await member.send(f"**Secret stalker**: {msg}")
        await jelly.send(f"{ctx.author.mention} pokes {member.mention}\n> {msg}")
        await ctx.message.delete()

    @commands.command()
    async def roll(self, ctx, number: int):
        result = random.randint(1, number)
        if result == 1:
            color = 16711680
        else:
            color = 16777215
        newembed = discord.Embed(description=f"**{ctx.author.name}** {number} талт шоо🎲 хаялаа...\nШоо🎲 буусан тал: **{result}**", color=color)
        newembed.set_thumbnail(url=ctx.author.avatar_url)
        newembed.set_author(name="Primobot", icon_url=self.client.user.avatar_url)
        embed = discord.Embed(description=f"**{ctx.author.name}** {number} талт шоо🎲 хаялаа...", color=16777215)
        embed.set_author(name="Primobot", icon_url=self.client.user.avatar_url)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        msg1 = await ctx.send(embed=embed)
        await asyncio.sleep(1)
        await msg1.edit(embed=newembed)
        

    

def setup(client):
    client.add_cog(Helpcommand(client))