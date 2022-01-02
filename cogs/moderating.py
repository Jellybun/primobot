import discord
from discord.ext import commands
blank = "<:blank:835155831074455622>"
inv = "<:inv:864984624052305961>"

class Moderating(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['clear', 'delete'])
    @commands.has_permissions(manage_messages = True)
    async def purge(self, ctx, amount=10):
        amount = amount + 1
        await ctx.channel.purge(limit=amount)

    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def kick(self, ctx, member : discord.Member=None, *, reason = None):
        if member is None and reason is None:
            await ctx.send("Please specify a member!")
            return
        embed = discord.Embed(description=f"Kicked a user {member.name}!")
        await member.kick(reason = reason)
        await member.send(f"You have been kicked from **{ctx.guild.name}** due to {reason} reason!")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def ban(self, ctx, member : discord.Member=None, *, reason = None):
        if member is None and reason is None:
            await ctx.send("Please specify a member!")
            return
        await member.ban(reason = reason)
        embed = discord.Embed(description=f"Banned a user {member.name}!")
        await member.send(f"You have been banned from **{ctx.guild.name}** due to {reason} reason!")
        await ctx.send(embed=embed)
        

    

def setup(client):
    client.add_cog(Moderating(client))