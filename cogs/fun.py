import discord
import random
import asyncio
from discord.ext import commands
blank = "<:blank:835155831074455622>"
inv = "<:inv:864984624052305961>"
imgcoin = '<:coin:933027999299809380>'
slotChoices = ['<:slots_777:941292949101219930>', '<:slots_die:941292879878434838>', '<:slots_money:941293026955919382>', '<:slots_wm:941292987353301022>']
slotMapping = {
    "<:slots_wm:941292987353301022>": 1,
    "<:slots_die:941292879878434838>": 2,
    "<:slots_money:941293026955919382>": 4,
    "<:slots_wm:941292987353301022>": 10
}

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

    @commands.command(aliases=['slots'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def slot(self, ctx, amount: int=None):
        if amount < 0:
            await ctx.send("Оруулах хэмжээ 0-ээс бага байж болохгүй")
            return
        elif amount is None:
            amount = 1
        desc = f"<a:slots:941291012410728460> | <a:slots:941291012410728460> | <a:slots:941291012410728460>"
        embed = discord.Embed(title=f"{ctx.author.name} bet {amount}{imgcoin} coins!", description=desc, color=16776960)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        msg = await ctx.send(embed=embed)
        output = []
        for i in range(2):
            await asyncio.sleep(1)
            if i == 0:
                final = random.choice(slotChoices)
                output.append(final)
                embed1 = discord.Embed(title=f"{ctx.author.name} bet {amount}{imgcoin} coins!", description=f"**{final} | <a:slots:941291012410728460> | <a:slots:941291012410728460>**", color=16776960)
                embed1.set_thumbnail(url=ctx.author.avatar_url)
                await msg.edit(embed=embed1)
            elif i == 1:
                final = random.choice(slotChoices)
                output.append(final)
                embed2 = discord.Embed(title=f"{ctx.author.name} bet {amount}{imgcoin} coins!", description=f"**{output[0]} | {final} | <a:slots:941291012410728460>**", color=16776960)
                embed2.set_thumbnail(url=ctx.author.avatar_url)
                await msg.edit(embed=embed2)
        final = random.choice(slotChoices)
        if final == output[0] == output[1]:
            multiplier = slotMapping[str(final)]
            prize = amount*multiplier
            titlemsg = f"{ctx.author.name}!, you've won {prize}{imgcoin} coins!"
            color = 65280
        else:
            titlemsg = f"{ctx.author.name}!, you've lost {amount}{imgcoin} coins!"
            color = 16711680
        embed3 = discord.Embed(title=titlemsg, description=f"**{output[0]} | {output[1]} | {final}**", color=color)
        embed3.set_thumbnail(url=ctx.author.avatar_url)
        await asyncio.sleep(2)
        await msg.edit(embed=embed3)
        
        

    @commands.command()
    async def roll(self, ctx, number: int):
        if number < 0:
            await ctx.send("Оруулах хэмжээ 0-ээс бага байж болохгүй")
            return
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