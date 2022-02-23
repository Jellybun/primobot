import discord
import asyncio
import datetime
import json
import motor.motor_asyncio
from difflib import get_close_matches
from discord.ext import commands
blank = "<:blank:835155831074455622>"
inv = "<:inv:864984624052305961>"

client_user = motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://lilybrown:Lilybrown.0001@cluster0.ccjaa.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client_user['Discord']
collectionServers = db['Servers']
collectionCommands = db['Commands']
collectionProfile = db['Profile']
class Botguilds(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(administrator =True)
    async def setuserlevel(self, ctx, member: discord.Member, level: int):
        if await collectionProfile.count_documents({"userId": member.id}) == 0:
            await ctx.send(f"**{ctx.author.name}**! Хэрэглэгчийн profile олдсонгүй!")
            return
        else:
            profile = await collectionProfile.find_one({"userId": member.id})
            if str(ctx.guild.id) not in profile['servers'].keys():
                await ctx.send(f"**{ctx.author.name}**! Хэрэглэгчийн profile **энэ server дотор** олдсонгүй!")
                return
            else:
                status = {
                    "$set": {
                        f"servers.{str(ctx.guild.id)}": {"id": ctx.guild.id, "level": level, "xp": 0}
                    }
                }
                await collectionProfile.update_one(profile, status)
                embed = discord.Embed(description=f"**{member.name}** xэрэглэгчийн level-ийг амжилттай **{level}** болгож өөрчиллөө!", color=65280)
                await ctx.send(embed=embed)
                return

    @commands.command(aliases=['wlcm', ' welcome'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(manage_messages =True)
    async def welcome(self, ctx, define: str, info: str = None, *, content: str = None):
        guild = await collectionServers.find_one({"guildId": ctx.guild.id})
        if content is None and info is None and define.lower() == 'status':
            embed = discord.Embed(
                title=f'{ctx.guild.name}-ийн welcome message status',
                description='**Түлхүүр үгc**:\nШинэ гишүүн – `{member}`\nСерверийн гишүүдийн тоо – `{member_count}`\nЖишээ: Сайн байна уу {member}. Та манай {member_count}-дэх гишүүн боллоо = Сайн байна уу **User**. Та манай **1**-дэх гишүүн боллоо\n**Санамж**: Дээрх түлхүүр үгсийг discohook дээрх json-ий зөвхөн __description__ хэсэгт оруулна!',
                color=16777215
            )
            if guild['welcome']['embed'] is None:
                guild_status = "Идэвхигүй"
            else:
                guild_status = 'Идэвхитэй'
            if guild['welcome']['webhook'] is None:
                guild_type = 'Primobot'
                guild_url = '–'
            else:
                guild_type = 'Webhook'
                guild_url = str(guild['welcome']['webhook'])
            embed.add_field(name='Status:', value=f"```{guild_status}```", inline=True)
            embed.add_field(name='Channel id:', value=f"```{guild['welcome']['channel']}```", inline=True)
            embed.add_field(name='Webhook/Bot:', value=f"```{guild_type}```", inline=True)
            embed.add_field(name='Webhook url:', value=f"```{guild_url}```", inline=False)
            await ctx.send(embed=embed)
            return
        elif content is None and info is None and define.lower() in ['display', 'show']:
            if len(guild['welcome']) >= 1:
                embed = discord.Embed.from_dict(guild['welcome'])
            else:
                embed = discord.Embed(description=f'**{ctx.author.name}**!, Энэ серверт одоогоор welcome message идэвхижээгүй байна!', color=16711680)
            await ctx.send(embed=embed)
            return
        elif content is None and info is None and define.lower() == 'disable':
            status = {"$set": {"welcome.embed": None}}
            await collectionServers.update_one(guild, status) 
            await ctx.send('Welcome message-ийг амжилттай идэвхгүй болголоо!')
            return
        elif define.lower() == 'set' and info.lower() == "message":
            to_json = json.loads(content)
            raw_json = to_json['embeds'][0]
            embed = discord.Embed.from_dict(raw_json)
            status = {"$set": {"welcome.embed": raw_json}}
            await collectionServers.update_one(guild, status) 
            await ctx.send(embed=embed)
            await ctx.send("Welcome message-ийг амжилттай шинэчлэлээ")
        elif define.lower() == 'set' and info.lower() == "channel":
            status = {"$set": {"welcome.channel": int(content)}}
            await collectionServers.update_one(guild, status)
            await ctx.send("Welcome message-ийн channel-ийг амжилттай шинэчлэлээ")
        elif define.lower() == 'set' and info.lower() == "client":
            if content.lower() == 'bot':
                status = {"$set": {"welcome.webhook": None}}
            else:
                status = {"$set": {"welcome.webhook": str(content)}}
            await collectionServers.update_one(guild, status)
            await ctx.send("Welcome message-ийн client-ийг амжилттай шинэчлэлээ")
             


    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(administrator =True)
    async def resetserverlevel(self, ctx):
        await ctx.send(f"Та **{ctx.guild.name}** server-ийн бүх хэрэглэгчийн level-ийг бүхэлд нь шинэчлэхдээ итгэлтэй байна уу?\n`yes`/`no`")
        def check(m):
            return m.content.lower() in ["yes", 'no'] and m.channel == ctx.channel
        try:
            message = await self.client.wait_for('message', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send('Request timeout!')
        else:
            if message.content.lower() == "yes":
                embed = discord.Embed(description="Серверийн датаг шинэчлэж байна<a:loading1:919916989990965248>\nХэрвээ комманд дундаасаа ажиллахаа болисон тохиолдолд та коммандийг дахин ачааллуулнуу!", color=16711680)
                embed.set_thumbnail(url=self.client.user.avatar_url)
                msg1 = await ctx.send(embed=embed)
                async for profile in collectionProfile.find({f"servers.{ctx.guild.id}id": ctx.guild.id}):
                    status = {
                        "$set": {
                            f"servers.{str(ctx.guild.id)}": {"id": ctx.guild.id, "level": 0, "xp": 0}
                        }
                    }
                    await collectionProfile.update_one(profile, status)
                newembed = discord.Embed(description="Серверийн data-г амжилттай шинэчлэж дууслаа!", color=65280)
                newembed.set_thumbnail(url=self.client.user.avatar_url)
                await msg1.edit(embed=newembed)
            else:
                await ctx.send(f"**{ctx.author.name}**! Хүсэлтийг цуцаллаа!")
                
    @commands.command(aliases=['leaderboard', 'top', 'Lb', 'Top', 'Leaderboard'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def lb(self, ctx, definer: str=None, many: int=None):
        if definer is None and many is None:
            await ctx.send(f"**{ctx.author.name}**! `level/cash` аль категорийн самбарыг хархаа тодорхойлно уу\n> ?lb `<level>/<cash>` `<index>`")
            return
        else:
            footer = datetime.datetime.now().strftime("%x")
            if many is None:
                many = 10
            asset = ['money', 'cash', 'bal', 'balance', 'coin', 'coins', 'rich', 'richest']
            if definer.lower() in asset:           
                desc = ""
                index = 1
                async for profile in collectionProfile.find({f"servers.{ctx.guild.id}.id": ctx.guild.id}).sort("profile.coin", -1):
                    username = self.client.get_user(profile['userId'])
                    desc += f"\n```{index}) {username}: {profile['profile']['coin'][0]+profile['profile']['coin'][1]}```"
                    index += 1
                embed = discord.Embed(title=f'{ctx.guild.name} серверийн хамгийн баян {many} хэрэглэгч', description=desc, color=16777215)
                embed.set_thumbnail(url=self.client.user.avatar_url)
                embed.set_footer(text=footer)
                await ctx.send(embed=embed)
            else:
                desc = ""
                index = 1
                async for profile in collectionProfile.find({f"servers.{str(ctx.guild.id)}.id": ctx.guild.id}).sort(f"servers.{str(ctx.guild.id)}.level", -1):
                    username = self.client.get_user(profile['userId'])
                    desc += f"```{index}) {username}: {profile['servers'][str(ctx.guild.id)]['level']}\n```"
                    index += 1
                embed = discord.Embed(title=f'{ctx.guild.name} серверийн хамгийн их левелтэй {many} хэрэглэгч', description=desc, color=16777215)
                embed.set_thumbnail(url=self.client.user.avatar_url)
                embed.set_footer(text=footer)
                await ctx.send(embed=embed)

    @commands.command(aliases=['customcommand'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(administrator = True)
    async def command(self, ctx, definer: str, name: str, *, text: str):
        if definer.lower() == "create":
            if await collectionCommands.count_documents({"guildId": ctx.guild.id}) == 0:
                status = {
                    "guildId": ctx.guild.id, 
                    "commands": {
                        str(name): str(text)
                    }
                }
                await collectionCommands.insert_one(status)
                await ctx.send(f"**{ctx.author.name}!** __{name}__ command-ийг амжилттай шинээр үүсгэлээ. Таны хийсэн command 1 минутын дараа идэвхижэх болно!")
            else:
                profile = await collectionCommands.find_one({"guildId": ctx.guild.id})
                keys = profile['commands'].keys()
                if str(name) in keys:
                    status = {
                        "$set": {
                            f"commands.{str(name)}": str(text)
                            }
                        }
                    await collectionCommands.update_one(profile, status)
                    await ctx.send(f"**{ctx.author.name}!** __{name}__ command-ийг амжилттай шинээр үүсгэлээ. Таны хийсэн command 1 минутын дараа идэвхижэх болно!")
                else:
                    status = {
                        "$set": {
                            f"commands.{str(name)}": str(text)
                        }
                    }
                    await collectionCommands.update_one(profile, status)
                    await ctx.send(f"**{ctx.author.name}!** __{name}__ command-ийг амжилттай шинээр үүсгэлээ. Таны хийсэн command 1 минутын дараа идэвхижэх болно!")
        elif definer.lower() == "edit":
            if await collectionCommands.count_documents({"guildId": ctx.guild.id}) == 0:
                await ctx.send("Энэ server-т command хийгдээгүй байна.")
            else:
                profile = await collectionCommands.find_one({"guildId": ctx.guild.id})
                keys = profile['commands'].keys()
                if str(name) in keys:
                    status = {
                        "$set": {
                            f"commands.{str(name)}": str(text)
                            }
                        }
                    await collectionCommands.update_one(profile, status)
                    await ctx.send(f"**{ctx.author.name}!** __{name}__ command-ийг амжилттай шинэчлэлээ. Таны шинэчлэсэн command 1 минутын дараа идэвхижэх болно!")
                    
                else:
                    await ctx.send("Тухайн нэртэй command олдсонгүй")
        elif definer.lower() == "delete":
            if await collectionCommands.count_documents({"guildId": ctx.guild.id}) == 0:
                await ctx.send("Энэ server-т command хийгдээгүй байна.")
            else:
                profile = await collectionCommands.find_one({"guildId": ctx.guild.id})
                keys = profile['commands'].keys()
                if str(name) in keys:
                    status = {
                        "$set": {
                            f"commands.{str(name)}": "Тухайн нэртэй command олдсонгүй"
                            }
                        }
                    await collectionCommands.update_one(profile, status)
                    await ctx.send(f"**{ctx.author.name}!** __{name}__ command-ийг амжилттай устгалаа")
                else:
                    await ctx.send("Тухайн нэртэй command олдсонгүй")


    @commands.command(aliases=['allcommands'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def customcommands(self, ctx):
        profile = await collectionCommands.find_one({"guildId": ctx.guild.id})
        keys = profile['commands'].keys()
        allcommands = ''
        for key in keys:
            allcommands += str(key)
        embed = discord.Embed(title=f'All commands for {ctx.guild.name} ({len(keys)})', description=allcommands, color=16777215)
        embed.set_thumbnail(url=self.client.user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def tags(self, ctx):
        async with ctx.channel.typing():
            allTags = ''
            status = 0
            profile = await collectionServers.find_one({"guildId": ctx.guild.id})
            amount = len(profile['tags'].keys())
            if amount == 0:
                await ctx.send("Энэ серверт одоогоор хадгалагдсан tag алга байна")
                return
            else:
                for tag in profile['tags'].keys():
                    allTags += f"{tag}, "
                embed = discord.Embed(title=f'All tags for {ctx.guild.name} ({amount})', description=allTags, color=16777215)
                embed.set_thumbnail(url=self.client.user.avatar_url)
                await ctx.send(embed=embed)

            

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def tag(self, ctx, definer: str, *, text: str=None):
        async with ctx.channel.typing():
            profile = await collectionServers.find_one({"guildId": ctx.guild.id})
            keys = profile['tags'].keys()
            if definer.lower() == "create":
                def check(message):
                    return message.author == ctx.author and message.channel == ctx.channel
                if text not in keys:
                    await ctx.send(f"**{text}** tag нь ямар контент агуулах вэ?")
                    
                    try:
                        message = await self.client.wait_for('message', timeout=60.0, check=check)
                    except asyncio.TimeoutError:
                        await ctx.send("Коммандын хүлээх хугацаа дууслаа")
                    else:
                        status = {
                            "$set": {
                                f"tags.{str(text)}": str(message.content)

                            }
                        }
                        await collectionServers.update_one(profile, status)
                        await ctx.send(f"**{text}** tag-ийг амжилттай шинээр нээлээ")
                else:
                    content = profile['tags'][str(text)]
                    if content.startswith("Тухайн"):
                        await ctx.send(f"**{text}** tag нь ямар контент агуулах вэ?")
                        try:
                            message = await self.client.wait_for('message', timeout=60.0, check=check)
                        except asyncio.TimeoutError:
                            await ctx.send("Коммандын хүлээх хугацаа дууслаа")
                        else:
                            status = {
                                "$set": {
                                    f"tags.{str(text)}": str(message.content)
                                }
                            }
                        await collectionServers.update_one(profile, status)
                        await ctx.send(f"**{text}** tag-ийг амжилттай шинээр нээлээ")
                    else:
                        await ctx.send("Тухайн tag нь нээгдсэн байна!")
                        return
            elif definer.lower() == "edit":
                if str(text.lower()) in keys:
                    await ctx.send(f"**{text}** tag нь ямар контент агуулах вэ?")
                    def check(message):
                        return message.author == ctx.author and message.channel == ctx.channel
                    try:
                        message = await self.client.wait_for('message', timeout=60.0, check=check)
                    except asyncio.TimeoutError:
                        await ctx.send("Коммандын хүлээх хугацаа дууслаа")
                    else:
                        document = {
                            "$set": {
                                f"tags.{str(text)}": str(message.content)
                            }
                        }
                        await collectionServers.update_one(profile, document)
                        await ctx.send(f"**{text}** tag-ийг амжилттай өөрчиллөө")
                else:
                    await ctx.send("Тухайн нэртэй tag алга байна!")
                    return
            elif definer.lower() == 'delete':
                if str(text.lower()) not in keys:
                    await ctx.send("Тухайн нэртэй tag алга байна!")
                    return
                else:
                    profile = await collectionServers.find_one({"guildId": ctx.guild.id})
                    status = {
                        "$set": {
                            f"tags.{str(text)}": "Тухайн нэртэй tag алга байна!"
                        }
                    }
                    await collectionServers.update_one(profile, status)
                    await ctx.send(f"**{text}** tag-ийг амжилттай устгалаа!")

            elif text is None:
                tagName = definer.lower()
                if str(tagName.lower()) not in keys:
                    cmd = tagName
                    cmds = [cmd for cmd in profile['tags'].keys()]
                    matches = get_close_matches(cmd, cmds)
                    if len(matches) > 0:
                        await ctx.send(f'`{cmd}` гэх tag алга байна, төстэй илэрц: `{matches[0]}`')
                    return
                else:
                    await ctx.send(profile['tags'][str(tagName)])
                

    

def setup(client):
    client.add_cog(Botguilds(client))