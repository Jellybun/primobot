import discord
import random
import asyncio
from discord.ext import commands
blank = "<:blank:835155831074455622>"
inv = "\u200b \u200b"
imgcoin = '<:coin:933027999299809380>'
limit = 140

horses = ['<a:horse_green:941686663111913552>', '<a:horse_orange:941686662784762036>', '<a:horse_white:941686662252089354>', '<a:horse_blue:941686661748785162>', '<a:horse_red:941686663061590096>', '<a:horse_purple:941686662046576680>', '<a:horse_yellow:941686661937504277>']
slotChoices = ['<:slots_777:941618295168180224>', '<:slots_die:941618534084132874>', '<:slots_money:941617788357865482>', '<:slots_wm:941618733162594334>']
slotMapping = {
    "<:slots_wm:941292987353301022>": 1,
    "<:slots_die:941618534084132874>": 2,
    "<:slots_money:941617788357865482>": 4,
    "<:slots_777:941618295168180224>": 10
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

    @commands.command(aliases=['hr'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def horserace(self, ctx, bet: int=None):
        if bet is None:
            bet = 1
        status = {
                "0": {"horse": "<a:horse_green:941686663111913552>", "pts": 0},
                "1": {"horse": "<a:horse_orange:941686662784762036>", "pts": 0},
                "2": {"horse": "<a:horse_white:941686662252089354>", "pts": 0},
                "3": {"horse": "<a:horse_blue:941686661748785162>", "pts": 0},
                "4": {"horse": "<a:horse_red:941686663061590096>", "pts": 0},
                "5": {"horse": "<a:horse_purple:941686662046576680>", "pts": 0},
                "6": {"horse": "<a:horse_yellow:941686661937504277>", "pts": 0}
            }
        jump = [5, 5, 5, 10, 10, 20]
        winners = []
        desc = f"{inv*status['0']['pts']}<a:horse_green:941686663111913552>{inv*(limit-status['0']['pts'])}🏁\n{inv*status['1']['pts']}<a:horse_orange:941686662784762036>{inv*(limit-status['1']['pts'])}🏁\n{inv*status['2']['pts']}<a:horse_white:941686662252089354>{inv*(limit-status['2']['pts'])}🏁\n{inv*status['3']['pts']}<a:horse_blue:941686661748785162>{inv*(limit-status['3']['pts'])}🏁\n{inv*status['4']['pts']}<a:horse_red:941686663061590096>{inv*(limit-status['4']['pts'])}🏁\n{inv*status['5']['pts']}<a:horse_purple:941686662046576680>{inv*(limit-status['5']['pts'])}🏁\n{inv*status['6']['pts']}<a:horse_yellow:941686661937504277>{inv*(limit-status['6']['pts'])}🏁"
        embed = discord.Embed(title=f"{ctx.author.name} bet {bet} coins on horse race!", description=f"`Бооцоо тавих морио сонгоно уу`\n\n{desc}", color=16777215)
        msg = await ctx.send(embed=embed)
        def check(m):
                return m.content.lower() in ["1", "2", "3", "4", "5", "6", "7"] and m.channel == ctx.channel
        await ctx.send("`Бооцоо тавих морио сонгоно уу`\n__1, 2, 3, 4, 5, 6, 7__")
        try:
            message = await self.client.wait_for('message', check=check, timeout=20)
        except asyncio.TimeoutError:
            await ctx.send(f"**{ctx.author.name}!**, Морио сонгох цаг дууслаа")
            await msg.delete
            return
        else:
            if message.content == "1":
                userhorse = "<a:horse_green:941686663111913552>"
            elif message.content == "2":
                userhorse = "<a:horse_orange:941686662784762036>"
            elif message.content == "3":
                userhorse = "<a:horse_white:941686662252089354>"
            elif message.content == "4":
                userhorse = "<a:horse_blue:941686661748785162>"
            elif message.content == "5":
                userhorse = "<a:horse_red:941686663061590096>"
            elif message.content == "6":
                userhorse = "<a:horse_purple:941686662046576680>"
            elif message.content == "7":
                userhorse = "<a:horse_yellow:941686661937504277>"
            embed2 = discord.Embed(title=f"{ctx.author.name} bet {bet} coins on horse race!", description=f"`Таны сонгосон морь:` {str(userhorse)}\n\n<a:horse_green:941686663111913552>{inv*limit}🏁\n<a:horse_orange:941686662784762036>{inv*limit}🏁\n<a:horse_white:941686662252089354>{inv*limit}🏁\n<a:horse_blue:941686661748785162>{inv*limit}🏁\n<a:horse_red:941686663061590096>{inv*limit}🏁\n<a:horse_purple:941686662046576680>{inv*limit}🏁\n<a:horse_yellow:941686661937504277>{inv*limit}🏁", color=16777215)
            await msg.edit(embed=embed2)
            while True:
                await asyncio.sleep(1)
                for i in range(7):
                    if status[str(i)]['horse'] not in winners:
                        status[str(i)]['pts'] += int(random.choice(jump))
                    if status[str(i)]['pts'] >= limit and status[str(i)]['horse'] not in winners:
                        status[str(i)]['pts'] = limit
                        winners.append(status[str(i)]['horse'])
                embed3 = discord.Embed(title=f"{ctx.author.name} bet {bet} coins on horse race!", description=f"`Таны сонгосон морь:` {userhorse}\n\n{inv*status['0']['pts']}<a:horse_green:941686663111913552>{inv*(limit-status['0']['pts'])}🏁\n{inv*status['1']['pts']}<a:horse_orange:941686662784762036>{inv*(limit-status['1']['pts'])}🏁\n{inv*status['2']['pts']}<a:horse_white:941686662252089354>{inv*(limit-status['2']['pts'])}🏁\n{inv*status['3']['pts']}<a:horse_blue:941686661748785162>{inv*(limit-status['3']['pts'])}🏁\n{inv*status['4']['pts']}<a:horse_red:941686663061590096>{inv*(limit-status['4']['pts'])}🏁\n{inv*status['5']['pts']}<a:horse_purple:941686662046576680>{inv*(limit-status['5']['pts'])}🏁\n{inv*status['6']['pts']}<a:horse_yellow:941686661937504277>{inv*(limit-status['6']['pts'])}🏁", color=16777215)
                await msg.edit(embed=embed3)
                if len(winners) == 7:
                    if winners[0] == userhorse:
                        titlemsg = f"{ctx.author.name} won {bet*10} coins on horse race!"
                        color = 65280
                    else:
                        index = 1
                        for item in winners:
                            if item != userhorse:
                                index += 1
                            else:
                                break
                        titlemsg = f"{ctx.author.name} lost {bet} coins on horse race!"
                        color = 16711680
                    desc = f"{inv*status['0']['pts']}<a:horse_green:941686663111913552>{inv*(limit-status['0']['pts'])}🏁\n{inv*status['1']['pts']}<a:horse_orange:941686662784762036>{inv*(limit-status['1']['pts'])}🏁\n{inv*status['2']['pts']}<a:horse_white:941686662252089354>{inv*(limit-status['2']['pts'])}🏁\n{inv*status['3']['pts']}<a:horse_blue:941686661748785162>{inv*(limit-status['3']['pts'])}🏁\n{inv*status['4']['pts']}<a:horse_red:941686663061590096>{inv*(limit-status['4']['pts'])}🏁\n{inv*status['5']['pts']}<a:horse_purple:941686662046576680>{inv*(limit-status['5']['pts'])}🏁\n{inv*status['6']['pts']}<a:horse_yellow:941686661937504277>{inv*(limit-status['6']['pts'])}🏁"
                    embedlast = discord.Embed(title=titlemsg, description=f"`Таны сонгосон морь:` {userhorse} **|** `Эзэлсэн байр:` **{index}**\n\n{desc}", color=color)
                    await msg.edit(embed=embedlast)
                    break

    @commands.command(aliases=['slots'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def slot(self, ctx, amount: int=None):
        if amount is None:
            amount = 1
        if amount < 0:
            await ctx.send(f"**{ctx.author.name}!**, Оруулах хэмжээ **0**-ээс бага байж болохгүй!")
            return
        desc = f"\u2800 <a:slots:941291012410728460> | <a:slots:941291012410728460> | <a:slots:941291012410728460> \u2800"
        embed = discord.Embed(title=f"{ctx.author.name} bet {amount}{imgcoin} coins!", description=desc, color=16776960)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        msg = await ctx.send(embed=embed)
        hasWon = random.choice((True, False))
        if hasWon:
            which = random.choice(slotChoices)
            result = (which, which, which)
            color = 65280
            prize = slotMapping[which]
            titlemsg = f"{ctx.author.name} won {prize*amount}{imgcoin} coins!"
        else:
            result = (random.choice(slotChoices), random.choice(slotChoices), random.choice(slotChoices))
            color = 16711680
            if result[0] == result[1] == result[2]:
                prize = slotMapping(result[0])
                titlemsg = f"{ctx.author.name} won {prize*amount}{imgcoin} coins!"
            else:
                titlemsg = f"{ctx.author.name} lost {amount}{imgcoin} coins!"
        await asyncio.sleep(1)
        embed1 = discord.Embed(title=f"{ctx.author.name} bet {amount}{imgcoin} coins!", description=f"**\u2800 {result[0]} | <a:slots:941291012410728460> | <a:slots:941291012410728460> \u2800**", color=16776960)
        embed1.set_thumbnail(url=ctx.author.avatar_url)
        await msg.edit(embed=embed1)
        await asyncio.sleep(1)
        embed2 = discord.Embed(title=f"{ctx.author.name} bet {amount}{imgcoin} coins!", description=f" **\u2800 {result[0]} | {result[1]} | <a:slots:941291012410728460> \u2800**", color=16776960)
        embed2.set_thumbnail(url=ctx.author.avatar_url)
        await msg.edit(embed=embed2)
        await asyncio.sleep(1.3)
        embed3 = discord.Embed(title=titlemsg, description=f" **\u2800 {result[0]} | {result[1]} | {result[2]} \u2800**", color=color)
        embed3.set_thumbnail(url=ctx.author.avatar_url)
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