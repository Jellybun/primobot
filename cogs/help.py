import discord
from discord.ext import commands
blank = "<:blank:835155831074455622>"
inv = "<:inv:864984624052305961>"

class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['clear', 'delete'])
    async def purge(self, ctx, amount=10):
        amount = amount + 1
        await ctx.channel.purge(limit=amount)

    @commands.command()
    async def help(ctx):
        embed = discord.Embed(description="**Moderating**\n> '?kick'\n> '?ban'\n> '?purge'")
        

    

def setup(client):
    client.add_cog(Help(client))