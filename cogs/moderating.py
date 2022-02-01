import discord
import asyncio
import json
import datetime
import asyncio
from typing import Union
from discord.ext import commands
blank = "<:blank:835155831074455622>"
inv = "<:inv:864984624052305961>"
blocked = ['create_instant_invite', 'add_reactions', 'priority_speaker', 'stream', 'read_messages', 'send_messages', 'send_tts_messages', 'embed_links', 'attach_files',  'read_message_history', 'external_emojis', 'view_guild_insights', 'connect', 'speak', 'mute_members', 'deafen_members', 'move_members', 'use_voice_activation', 'use_slash_commands', 'request_to_speak']

class Moderating(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(manage_messages = True)
    async def lock(self, ctx, channel: discord.TextChannel=None):
        if channel is None:
            channel = ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = False
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.send('Channel locked.')

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(manage_messages = True)
    async def unlock(self, ctx, channel: discord.TextChannel=None):
        if channel is None:
            channel = ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = True
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.send('Channel unlocked.')

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(manage_messages = True)
    async def mute(self, ctx, member: discord.Member=None):
        if member is None:
            await ctx.send("No user found!")
            return
        mutedrole = discord.utils.get(ctx.guild.roles, name="Muted")
        if mutedrole is None:
            await ctx.send("No role found named **Muted**")
            return
        await member.add_roles(mutedrole)
        await ctx.send(f'**{member.name}** has been muted!')

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(manage_messages = True)
    async def unmute(self, ctx, member: discord.Member=None):
        if member is None:
            await ctx.send("No user found!")
            return
        mutedrole = discord.utils.get(ctx.guild.roles, name="Muted")
        if mutedrole is None:
            await ctx.send("No role found named **Muted**")
            return
        await member.remove_roles(mutedrole)
        await ctx.send(f'**{member.name}** has been unmuted!')

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(manage_messages = True)
    async def warn(self, ctx, member: discord.Member=None, reason=None):
        if member is None and reason is None:
            await ctx.send("Wrong argument!")
            return
        elif reason is None:
            await ctx.send(f'**{member.name}** has been warned!')  
        else:
            await ctx.send(f'**{member.name}** has been warned for __{reason}__ reason!')  
        
    
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(manage_messages = True)
    async def post(self, ctx, channel: discord.TextChannel, *, text=None):
        if text is None:
            await ctx.send("Та message контентийг оруулж өгнө үү!")
            return
        else:
            if text.startswith("{"):
                try:
                    firstjson = json.loads(text)
                    rawJson = firstjson['embeds'][0]
                    embed = discord.Embed.from_dict(rawJson)
                except:
                    await ctx.send("Json текстийг хөрвүүлэхэд алдаа гарлаа")
                    return
                else:
                    await ctx.message.delete()
                    await ctx.send(embed=embed)
                    msg = await ctx.send(f"**{channel.name}** дотор амжилттай embed-post хийлээ!")
                    await asyncio.sleep(3)
                    await msg.delete()
                
            else:
                await ctx.message.delete()
                await channel.send(text)
                msg = await ctx.send(f"**{channel.name}** дотор амжилттай post хийлээ!")
                await asyncio.sleep(3)
                await msg.delete()

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(manage_messages = True)
    async def postedit(self, ctx, mchannel : discord.TextChannel, messageobj: discord.Message, *, text=None):
        if text is None:
            await ctx.send("Та message контентийг оруулж өгнө үү!")
            return
        else:
            if isinstance(mchannel, discord.TextChannel) and isinstance(messageobj, discord.Message):
                if text.startswith("{"):
                    try:
                        firstjson = json.loads(text)
                        rawJson = firstjson['embeds'][0]
                        embed = discord.Embed.from_dict(rawJson)
                    except:
                        await ctx.send(f"**{ctx.author.name}**! Json текстийг хөрвүүлэхэд алдаа гарлаа")
                        return
                    else:
                        await messageobj.edit(embed=embed)
                        await ctx.message.delete()
                        msg = await ctx.send(f"**{ctx.author.name}**! embed-post-ийг амжилттай шинэчлэлээ!")
                        await asyncio.sleep(3)
                        await msg.delete()
                    
                else:
                    await messageobj.edit(content=text)
                    msg = await ctx.send(f"**{ctx.author.name}**! Message-ийг амжилттай шинэчлэлээ!")
                    await asyncio.sleep(3)
                    await msg.delete()

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.has_permissions(manage_roles = True)
    async def role(self, ctx, define, arg1: Union[discord.Member, discord.Role, str, int]=None, arg2: Union[discord.Role, str, int]=None):
        deletecmd = ['delete', 'del']
        colorcmd = ['color', 'changecolor']
        if define.lower() == "create":
            rolename = arg1
            if isinstance(arg2, str):
                hexcode = int(arg2, 16)
            elif isinstance(arg2, int):
                hexcode = int(arg2)
            await ctx.guild.create_role(name=rolename, color=discord.Colour(hexcode))
            embed = discord.Embed(description=f"**{rolename}** role-ийг амжилттай шинээр үүсгэлээ!", color=65280)
            await ctx.send(embed=embed)
        elif define.lower() in deletecmd and arg2 == None:
            if isinstance(arg1, discord.Role):
                embed = discord.Embed(description=f"**{arg1.name}** role-ийг амжилттай устгалаа", color=65280)
                await ctx.send(embed=embed)
                await arg1.delete()
            if isinstance(arg1, str):
                role = discord.utils.get(ctx.guild.roles, name=arg1)
                if role is None:
                    await ctx.send(f"**{ctx.author.name}**! **{arg1}** нэртэй role олдсонгүй")
                    return
                else:
                    await role.delete()
                    embed = discord.Embed(description=f"**{arg1.name}** role-ийг амжилттай устгалаа", color=65280)
                    await ctx.send(embed=embed)
        elif define.lower() == "info" and arg2 == None:
            if isinstance(arg1, discord.Role):
                role = arg1
                rolename = arg1.name
                hex = str(arg1.color)[1:]
                rolecolor = int(hex, 16)
            elif isinstance(arg1, str):
                role = discord.utils.get(ctx.guild.roles, name=arg1)
                rolename = arg1
                hex = str(role.color)[1:]
                rolecolor = int(hex, 16)
                if role is None:
                    await ctx.send(f"**{ctx.author.name}**! **{arg1}** нэртэй role олдсонгүй")
                    return
            membersobj = role.members
            perms = role.permissions
            members = ""
            store = ""
            for perm in perms:
                if perm[1] == False or perm[0] in blocked:
                    pass
                else:
                    store += f"{perm[0]}, "
            index = 0
            for i in membersobj:
                members += f"{i.name}, "
                index += 1
            if len(store) == 0:
                store = 'None'
            if len(members) == 0:
                members = 'None'
            embed = discord.Embed(title=f"Role мэдээлэл:", color=rolecolor)
            embed.add_field(name="Name:", value=f"```{rolename}```", inline=True)
            embed.add_field(name="Id:", value=f"```{role.id}```", inline=True)
            embed.add_field(name="Creation date:", value=f"```{role.created_at.replace(microsecond=0)}```", inline=True)
            embed.add_field(name=f"Members({index}):", value=str(members), inline=True)
            embed.add_field(name="Permissions:", value=str(store), inline=True)
            await ctx.send(embed=embed)

        elif define.lower() in colorcmd:
            if isinstance(arg1, discord.Role) and isinstance(arg2, int):
                hex = int(arg2)
            elif isinstance(arg1, discord.Role) and isinstance(arg2, str):
                hex = int(arg2, 16)
            try:
                await arg1.edit(colour=discord.Colour(int(hex)))
            except:
                await ctx.send(f"**{ctx.author.name}**! Role өнгө өөрчлөхөд алдаа гарлаа. Hex/Int кодийг дахин шалгана уу!")
            else:
                embed = discord.Embed(description=f"**{arg1.mention}** role өнгийг амжилттай өөрчиллөө!", color=65280)
                await ctx.send(embed=embed)
        elif define.lower() == "add":
            if isinstance(arg1, discord.Member) and isinstance(arg2, discord.Role):
                await arg1.add_roles(arg2)
                embed = discord.Embed(description=f"**{arg1.name}-д {arg2.mention}** role-ийг амжилттай өглөө!", color=65280)
                await ctx.send(embed=embed)
        elif define.lower() == "remove":
            if isinstance(arg1, discord.Member) and isinstance(arg2, discord.Role):
                await arg1.remove_roles(arg2)
                embed = discord.Embed(description=f"**{arg1.name}-ээс {arg2.mention}** role-ийг амжилттай хурааж авлаа!", color=65280)
                await ctx.send()
            elif isinstance(arg1, str) and isinstance(arg2, discord.Role):
                if arg1 == 'all':
                    members = ''
                    index = 0
                    membersobj = arg2.members
                    for member in membersobj:
                        await member.remove_roles(arg2)
                        index += 1
                    embed = discord.Embed(description=f"**{index}** хэрэглэгчээс амжилттай **{arg2.mention}** role-ийг хурааж авлаа", color=65280)
                    await ctx.send(embed=embed)
                else:
                    await ctx.send(f"**{ctx.author.name}**! `all` argument дээр зөвхөн тухайн role дээрх бүх хэрэглэгчийн role-ийг хурааж авна")

        else:
            await ctx.send(f"**{ctx.author.name}**! Wrong argument!")



    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(manage_messages = True)
    async def kick(self, ctx, member : discord.Member=None, *, reason = None):
        if member is None and reason is None:
            await ctx.send(f"Хэрэглэгч олдсонгүй!")
            return
        embed = discord.Embed(description=f"{member.name}-ийг амжилттай гаргалаа!", color=65280)
        await member.kick(reason = reason)
        await member.send(f"You have been kicked from **{ctx.guild.name}** due to {reason} reason!")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(administrator = True)
    async def ban(self, ctx, member : discord.Member=None, *, reason = None):
        if member is None and reason is None:
            await ctx.send("Хэрэглэгч олдсонгүй!")
            return
        await member.ban(reason = reason)
        embed = discord.Embed(description=f"{member.name}ийг амжилттай ban хийлээ!", color=65280)
        await member.send(f"You have been banned from **{ctx.guild.name}** due to {reason} reason!")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(administrator = True)
    async def unban(self, ctx, member : discord.Member=None):
        if member is None:
            await ctx.send("Хэрэглэгч олдсонгүй!")
            return
        await member.unban()
        embed = discord.Embed(description=f"{member.name}ийг амжилттай unban хийлээ!", color=65280)
        await member.send(f"You have been unbanned from **{ctx.guild.name}**!")
        await ctx.send(embed=embed)

    @commands.command(aliases=['clear', 'delete'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(manage_messages = True)
    async def purge(self, ctx, typo: Union[discord.Member, str, int]=None, amount: int=None):
        if typo is None and amount is None:
            finalAmount = 2
            await ctx.channel.purge(limit=finalAmount)
        elif amount is None:
            try:
                typo = int(typo)
            except:
                finalAmount = 101
                await ctx.channel.purge(limit=finalAmount)
                alert = await ctx.send("100 message устгалаа!")
                await asyncio.sleep(2)
                await alert.delete()
            else:
                await ctx.channel.purge(limit=typo+1)
                alert = await ctx.send(f"{typo} message устгалаа!")
                await asyncio.sleep(2)
                await alert.delete() 
        else:
            if isinstance(typo, discord.Member):
                messages = await ctx.channel.history(limit=amount+1).flatten()
                for message in messages:
                    if message.author == typo:
                        await message.delete()
                    else:
                        pass
                await ctx.message.delete()
            else:
                await ctx.send("Wrong argument!")
                return
        

    

def setup(client):
    client.add_cog(Moderating(client))