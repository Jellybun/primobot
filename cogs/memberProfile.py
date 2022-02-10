import discord
import datetime
import asyncio
import random
import motor.motor_asyncio
from typing import Union
from discord.ext import commands
from profilechecker import createprofile
coin = '<:coin:933027999299809380>'

client_user = motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://lilybrown:Lilybrown.0001@cluster0.ccjaa.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client_user['Discord']
collectionProfile = db['Profile']
collectionServers = db['Servers']
collectionMarket = db['Market']
blank = "<:blank:835155831074455622>"
inv = "<:inv:864984624052305961>"
coin = '<:coin:933027999299809380>'

marrygifs = ['https://c.tenor.com/UnSlrdcbV9kAAAAC/anime-ring.gif', 'https://c.tenor.com/WCeJaacSAecAAAAM/anime-wedding.gif', 'https://c.tenor.com/kftblVYVuSsAAAAM/anime-incest.gif', 'https://c.tenor.com/an0diNvfSSwAAAAM/marriage-anime-sailor-moon.gif', 'https://c.tenor.com/9_DMhvo7FCAAAAAM/anime-wedding.gif', 'https://c.tenor.com/3OYmSePDSVUAAAAM/black-clover-licht.gif', 'https://c.tenor.com/I59-iJUDG2kAAAAM/anime-love.gif', 'https://c.tenor.com/DrH3mGoFTGAAAAAM/anww-hug.gif', 'https://c.tenor.com/KD__SewDxK0AAAAM/horimiya-izumi-miyamura.gif']

market = {
    "ring": 5000
}

class Helpcommand(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['av'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def avatar(self, ctx, member: discord.Member=None):
        if member is None:
            user = ctx.author
        else:
            user = member
        embed = discord.Embed(title=f'User avatar for {user.name}', color=16777215)
        embed.set_image(url=user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(aliases=['whois', 'userinfo'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def who(self, ctx, member: discord.Member=None):
        footer = datetime.datetime.now().strftime("%x")
        if member is None:
            user = ctx.author
        else:
            user = member
        blocked = ['create_instant_invite', 'add_reactions', 'priority_speaker', 'stream', 'read_messages', 'send_messages', 'send_tts_messages', 'embed_links', 'attach_files',  'read_message_history', 'external_emojis', 'view_guild_insights', 'connect', 'speak', 'mute_members', 'deafen_members', 'move_members', 'use_voice_activation', 'use_slash_commands', 'request_to_speak']
        perms = ''
        roles = ''
        info = ctx.channel.permissions_for(user)
        vertical = 0
        for role in user.roles:
            if role.id == ctx.guild.id:
                pass
            elif vertical == 0:
                roles += f"{role.name}"
                vertical = 1
            else:
                roles += f", {role.name}"
        index = 0
        for perm in info:
            if perm[1] == False or perm[0].lower() in blocked:
                pass 
            else:
                perms += f"{perm[0]}\n"
                index += 1
        embed = discord.Embed(color=16777215)
        embed.add_field(name="**Нэр:**", value=f"```{user.name}```", inline=True)
        embed.add_field(name="**ID:**", value=f"```{user.id}```", inline=True)
        embed.add_field(name="\u200b", value=f"\u200b", inline=False)
        embed.add_field(name="**Серверт нэгдсэн огноо:**", value=f"```{user.joined_at.replace(microsecond=0)}```", inline=True)
        embed.add_field(name="**Хэрэглэгч нээсэн огноо:**", value=f"```{user.created_at.replace(microsecond=0)}```", inline=True)
        embed.add_field(name="\u200b", value=f"\u200b", inline=False)
        embed.add_field(name="**Roles:**", value=f"**{roles}**", inline=True)
        embed.add_field(name="**Permissions:**", value=f"__**{perms}**__", inline=True)
        embed.set_thumbnail(url=user.avatar_url)
        embed.set_footer(text=footer)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def note(self, ctx, *, text=None):
        await createprofile(ctx.author)
        if text is None:
            profile = await collectionServers.find_one({"guildId": ctx.guild.id})
            if str(ctx.author.id) not in profile['notes'].keys():
                await ctx.send(f"**{ctx.author.name}**! Танд ямар нэг тэмдэглэл алга байна")
                return
            else:
                content = profile['notes'][str(ctx.author.id)]
                await ctx.send(content)
        else:
            profile = await collectionServers.find_one({"guildId": ctx.guild.id})
            status = {
                "$set": {
                    f"notes.{str(ctx.author.id)}": str(text)
                }
            }
            await collectionServers.update_one(profile, status)
            embed = discord.Embed(description=f"**{ctx.author.name}**! Таны тэмдэглэлийг амжилттай хадгаллаа", color=65280)
            await ctx.send(embed=embed)

    @commands.command(aliases=['shop'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def market(self, ctx, definer: str=None, * ,info=None):
        await createprofile(ctx.author)
        if definer == None and info == None:
            items = ""
            index = 0
            async for sale in collectionMarket.find():
                items += f"**{sale['userName']}**: {sale['item']}\n\n"
                index += 1
                if index == 10:
                    break
            embed = discord.Embed(title='Market:', description=f"> **Ring💍**`[ring]` : **5000**{coin} coins\n\n`Та ?market sell command ашиглан энэ самбар дээр өөрийн зарыг нэмж болно`\n```Хэрэглэгчидийн зар:```\n{items}", color=16777215)
            embed.set_thumbnail(url=self.client.user.avatar_url)
            await ctx.send(embed=embed)
        elif definer.lower() == "sell":
            if info is None:
                await ctx.send(f"**{ctx.author.name}**! Та оруулах зар юуны талаар гэдгийг оруулна уу")
                return
            status = {"userName": ctx.author.name, "item": info}
            await collectionMarket.insert_one(status)
            await ctx.send(f"**{ctx.author.name}**!, Таны зарыг амжилттай нэмлээ!")

    @commands.command(aliases=['purchase'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def buy(self, ctx, good: str=None, quan: int=1):
        await createprofile(ctx.author)
        if good is None and quan is None:
            await ctx.send("Юу авах гэж байгаагаа оруулна уу")
            return
        else:
            try:
                amount = quan * market[str(good)]
            except:
                await ctx.send(f"**{ctx.author.name}**! Алдаа гарлаа!\nТа авах гэж байгаа зүйлийхээ нэрийг дахин шалгана уу")
            else:
                profile = await collectionProfile.find_one({"userId": ctx.author.id})
                bank = profile["profile"]["coin"][0]
                oldbal = profile["profile"]["coin"][1]
                newbal = int(oldbal - amount)
                if newbal < 0:
                    await ctx.send(f"**{ctx.author.name}**!, Таны үлдэгдэл хүрэлцэхгүй байна!")
                    return
                status = {
                    "$set": {
                        "profile.coin": [bank, newbal],
                        "inventory.ring": profile['inventory']['ring'] + quan

                    }
                }
                await collectionProfile.update_one(profile, status)
                await ctx.send(f"**{ctx.author.name}**! Та **{quan}** {good}💍 **{amount}{coin}** coin-оор худалдаж авлаа!")

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def sell(self, ctx, good: str=None):
        await createprofile(ctx.author)
        if good is None:
            await ctx.send("**{ctx.author.name}**! Юу зарах гэж байгаагаа оруулна уу")
            return
        else:
            try:
                amount = market[str(good)]
            except:
                await ctx.send(f"**{ctx.author.name}**! Алдаа гарлаа!\nТа зарах гэж байгаа зүйлийхээ нэрийг дахин шалгана уу")
            else:
                profile = collectionProfile.find_one({"userId": ctx.author.id})
                oldbal = profile['profile']['coin'][1]
                bank = profile['profile']['coin'][0]
                newbal = int(oldbal + amount/2)
                status = {
                    "$set": {
                        "coin": [bank, newbal]
                    }
                }
                await collectionProfile.update_one(profile, status)
                await ctx.send(f"**{ctx.author.name}**! Та {good}-ийг **{amount/2}{coin}** coin-оор зарлаа")


    
    @commands.command(aliases=['inventory', 'bag'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def inv(self, ctx, member: discord.Member=None):
        await createprofile(ctx.author)
        if member is None:
            member = ctx.author
        if await collectionProfile.count_documents({"userId": member.id}) == 0:
            await ctx.send(f"**{member.name}**!, Танд хэрэглэгчийн profile нээгдээгүй байна")
        else:
            profile = await collectionProfile.find_one({"userId": member.id})
            rings = profile['inventory']['ring']
            if rings == 0:
                response = "`Empty`"
            else:
                response = f"> **Ring💍**: **{rings}**x"
            embed = discord.Embed(title=f"{member.name}'s inventory:", description=response, color=16777215)
            await ctx.send(embed=embed)

    @commands.command(aliases=['bal', 'cash', 'coin', 'cowoncy'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def balance(self, ctx):
        await createprofile(ctx.author)
        footer = datetime.datetime.now().strftime("%x")
        profile = await collectionProfile.find_one({"userId": ctx.author.id})
        bank = profile['profile']['coin'][0]
        bal = profile['profile']['coin'][1]
        embed = discord.Embed(title=f"{ctx.author.name}-ийн үлдэгдэл:", description='Банкний хадгаламж дээр өдөр тутамд +__3%__-ийн хүү нэмэгдэнэ',color=16777215)
        embed.add_field(name="Bank:", value=f"```{bank}```", inline=True)
        embed.add_field(name="Wallet:", value=f"```{bal}```", inline=True)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.set_footer(text=footer)
        await ctx.send(embed=embed)

    @commands.command(aliases=['dep', 'dump', 'save'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def deposit(self, ctx, amount: Union[str, int]=None):
        await createprofile(ctx.author)
        if amount is None:
            await ctx.send("**{ctx.author.name}**! Та coin хадгалах хэмжээгээ оруулна уу")
            return
        else:
            profile = await collectionProfile.find_one({"userId": ctx.author.id})
            bank = profile['profile']['coin'][0]
            bal = profile['profile']['coin'][1]
            if isinstance(amount, str) and amount.lower() == "all":
                newbank = bal + bank
                newbal = 0
                finalamount = bal
                status = {
                    "$set": {
                        "profile.coin": [newbank, newbal]
                    }
                }
            elif isinstance(amount, int):
                if amount > bal:
                    await ctx.send(f"**{ctx.author.name}**! Таны үлдэгдэл хүрэлцэхгүй байна")
                    return
                else:
                    finalamount = amount
                    newbank = bank + amount
                    newbal = bal - amount
                    status = {
                    "$set": {
                        "profile.coin": [newbank, newbal]
                    }
                }
            await collectionProfile.update_one(profile, status)
            await ctx.send(f"**{ctx.author.name}**! Таны bank account-д **{finalamount}**{coin} coin нэмэгдэж орлоо")

    
    @commands.command(aliases=['withd', 'wd', 'draw'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def withdraw(self, ctx, amount: Union[int, str]=None):
        await createprofile(ctx.author)
        if amount is None:
            await ctx.send("**{ctx.author.name}**! Та coin авах хэмжээгээ оруулна уу")
            return
        else:
            profile = await collectionProfile.find_one({"userId": ctx.author.id})
            bank = profile['profile']['coin'][0]
            bal = profile['profile']['coin'][1]
            if isinstance(amount, str) and amount.lower() == "all":
                print("amount as all")
                newbank = 0
                newbal = bal + bank
                finalamount = bank
                status = {
                    "$set": {
                        "profile.coin": [newbank, newbal]
                    }
                }
            elif isinstance(amount, int):
                if amount > bank:
                    await ctx.send(f"**{ctx.author.name}**! Таны банкин дахь үлдэгдэл хүрэлцэхгүй байна")
                    return
                else:
                    finalamount = amount
                    newbank = bank - amount
                    newbal = bal + amount
                    status = {
                    "$set": {
                        "profile.coin": [newbank, newbal]
                    }
                }
            await collectionProfile.update_one(profile, status)
            await ctx.send(f"**{ctx.author.name}**! Танд **{finalamount}**{coin} coin нэмэгдэж орлоо")

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def give(self, ctx, member: discord.Member=None, amount: int=None):
        await createprofile(ctx.author)
        if member is None and amount is None:
            await ctx.send("Хэрэглэгч олдсонгүй!")
        else:
            profile = await collectionProfile.find_one({"userId": ctx.author.id})
            current = profile['profile']['coin'][1]
            if amount > current:
                await ctx.send(f"**{ctx.author.name}**! Таны үлдэгдэл хүрэлцэхгүй байна")
                return
            else:
                userprofile = await collectionProfile.find_one({"userId": member.id})
                new = int(current - amount)
                print(f"my new:{new}")
                usernew = int(userprofile['profile']['coin'][1]) + int(amount)
                print(f"user new:{usernew}")
                await collectionProfile.update_one(profile, {"$set": {"profile.coin": new}})
                await collectionProfile.update_one(userprofile, {"$set": {"profile.coin": usernew}})
                await ctx.send(f"**{ctx.author.name}**! Та **{member.name}**-т **{amount}**{coin} coin шилжүүллээ!")

    @commands.command(aliases=['marriage', 'husband', 'wife', 'propose'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def marry(self, ctx, member: discord.Member=None):
        await createprofile(ctx.author)
        profile = await collectionProfile.find_one({"userId": ctx.author.id})
        if member is None:
            status = profile['profile']['marriage']
            if isinstance(status, int):
                partner = self.client.get_user(int(status))
                embed = discord.Embed(title='Гэрлэлтийн гэрчилгээ', description=f'💗**{ctx.author.name}** 👫 **{partner.name}** нэг гэр бүл!💗\n\n*"Сэтгэл итгэлээрээ хайраа тэтгэж\nХазайсан газар нь нэгнээ түшиж\nХальтарсан газар биесээ тулаж\nНэгэн бие мэт нийлсэн сэтгэлээрээ\nНасан буянаа тэгшитгэж яваарай..."*', color=16738740)
                embed.set_thumbnail(url=ctx.author.avatar_url)
                embed.set_image(url=random.choice(marrygifs))
                embed.set_footer(text="Хүчинтэй хугацаа байхгүй")
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"**{ctx.author.name}**! Та хүнтэй гэрлээгүй байна")

        else:
            if member == ctx.author:
                await ctx.send(f"**{ctx.author.name}**! Та өөрөө өөртэйгээ гэрлэж болохгүй")
                return
            ring = profile['inventory']['ring']
            if ring == 0:
                await ctx.send(f"**{ctx.author.name}**! Танд гэрлэх бөгж алга байна. Shop дээрээс бөгж худалдан авч хүнтэй гэрлээрэй")
                return
            newring = ring-1
            userprofile = await collectionProfile.find_one({"userId": member.id})
            status = profile['profile']['marriage']
            userstatus = userprofile['profile']['marriage']
            if isinstance(status, str) and isinstance(userstatus, str):
                await ctx.send(f"**{member.name}**! Танд {ctx.author.name} гэрлэх санал тавилаа Та `yes` эсвэл `no` гэж хариугаа бичнэ үү")
                def check(message):
                    return message.content.lower() in ["yes", 'no'] and message.author == member and message.channel == ctx.channel
                try:
                    message = await self.client.wait_for('message', timeout=60.0, check=check)
                except asyncio.TimeoutError:
                    await ctx.send('Request timeout!')
                else:
                    if message.content.lower() == "yes":
                        document = {
                            "$set": {
                                "profile.marriage": member.id,
                                "inventory.ring": newring
                            }
                        }
                        userdocument = {
                            "$set": {
                                "profile.marriage": ctx.author.id
                            }
                        }
                        await collectionProfile.update_one(profile, document)
                        await collectionProfile.update_one(userprofile, userdocument)
                        await ctx.send(f"**{ctx.author.name}** 💑 **{member.name}** гэрлэсэнд тань баяр хүргэе❣️!")
                        return
                    else:
                        await ctx.send(f"**{ctx.author.name}**! Хүсэлтийг цуцаллаа")
                        return

            else:
                await ctx.send("Алдаа гарлаа!\nГэрлэхийн тулд тухайн 2 хүн аль аль нь гэрлээгүй байх ёстой")
                return

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def divorce(self, ctx):
        await createprofile(ctx.author)
        profile = await collectionProfile.find_one({"userId": ctx.author.id})
        status = profile['profile']['marriage']
        if isinstance(status, int):
            await ctx.send(f"**{ctx.author.name}**! Та салахдаа итгэлтэй байна уу?\n`yes`/`no`")
            def check(message):
                return message.author == ctx.author and message.channel == ctx.channel
            try:
                message = await self.client.wait_for('message', timeout=60.0, check=check)
            except asyncio.TimeoutError:
                await ctx.send('Request timeout!')
            else:
                if message.content.lower() == "yes":
                    partner = self.client.get_user(int(status))
                    userprofile = await collectionProfile.find_one({"userId": partner.id})
                    doc1 = {
                        "$set": {
                            "profile.marriage": "Single"
                        }
                    }
                    await collectionProfile.update_one(profile, doc1)
                    await collectionProfile.update_one(userprofile, doc1)
                    await ctx.send(f"**{ctx.author.name}**! Та **{partner.name}**-с саллаа!")
                elif message.content.lower() == "no":
                    await ctx.send("Таны салах хүсэлтийг цуцаллаа!")
        else:
            await ctx.send(f"**{ctx.author.name}**! Та хүнтэй гэрлээгүй байна")


    

def setup(client):
    client.add_cog(Helpcommand(client))