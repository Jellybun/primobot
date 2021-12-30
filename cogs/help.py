import discord
from discord.ext import commands
blank = "<:blank:835155831074455622>"
inv = "<:inv:864984624052305961>"

class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(description="**Moderating**\n> '?kick'\n> '?ban'\n> '?purge'")
        await ctx.send(embed=embed)

    

def setup(client):
    client.add_cog(Help(client))