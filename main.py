import discord
import json
import os
import datetime
import asyncio
import requests
import pymongo
import motor.motor_asyncio
from timeConverter import time_converter
from discord.ext import commands, tasks
from difflib import get_close_matches
userBlackList = []

client_user = motor.motor_asyncio.AsyncIOMotorClient(...)
db = client_user['Discord']
collectionServers = db['Servers']
collectionProfile = db['Profile']
collectionCommands = db['Commands']
collectionPrimoverse = db['Primoverse']

async def get_prefix(client, message):
  if message.channel == message.author.dm_channel:
    return "?"
  else:
    server = await collectionServers.find_one({"guildId": message.guild.id})
    prefix = server["prefix"]
    return prefix, "?"   

client = commands.Bot(command_prefix = get_prefix, activity=discord.Game("?help"), intents = discord.Intents.all())
client.remove_command('help')

@client.command()
async def load(ctx, ext):
  client.load_extension(f"cogs.{ext}")

@client.command()
async def unload(ctx, ext):
  client.unload_extension(f"cogs.{ext}")

for file in os.listdir('./cogs'):
  if file.endswith("py"):
    client.load_extension(f'cogs.{file[:-3]}')

async def run_once_when_ready():
    await client.wait_until_ready()
    print('Bot is ready')

client.loop.create_task(run_once_when_ready())


@client.command()
async def ping(ctx):
    embed = discord.Embed(description=f"Current ms: `{int(client.latency * 1000)}`", color=16777215)
    await ctx.send(embed=embed)


class Blacklist(commands.CheckFailure):
    pass

@client.check
async def userblacklist(ctx):
    if ctx.author.id in userBlackList:
        raise Blacklist('You are temporarily blacklisted from using this bot.')
        return
    else:
        return True

# On Command Error
@client.event
async def on_command_error(ctx, error):
  if isinstance(error, Blacklist):
    await ctx.send(error)
  elif isinstance(error, commands.CommandOnCooldown):
    time = time_converter(error.retry_after)
    embed = discord.Embed(description=f"**{ctx.author.name}**! Коммандын cooldown дуусахад **{time}** дутуу байна", color=16711680)
    mainmsg = await ctx.send(embed=embed)
    await asyncio.sleep(int(error.retry_after))
    await mainmsg.delete()
  elif isinstance(error, commands.CommandNotFound):
    cmd = ctx.invoked_with
    cmds = [cmd.name for cmd in client.commands]
    matches = get_close_matches(cmd, cmds)
    if len(matches) > 0:
      embed = discord.Embed(description=f'`{cmd}` гэх command алга байна, төстэй илэрц: `{matches[0]}`', color=16711680)
      await ctx.send(embed=embed)
    else:
      return
  elif isinstance(error, commands.MissingPermissions):
    msg = ''
    perms = error.missing_perms
    for perm in perms:
      msg += f"{perm}\n"
    embed = discord.Embed(description=f"**{ctx.author.name}**! Танд уг коммандыг гүйцэтгэх permission алга байна.\n__Missing permissions__:\n```{msg}```", color=16711680)
    await ctx.send(embed=embed)


  elif isinstance(error, commands.BotMissingPermissions):
    embed = discord.Embed(description=f'**{ctx.author.name}!**, Надад энэ коммандыг гүйцэтгэх permission алга байна!\nMissing Permissions: `{", ".join(error.missing_perms)}`', color=16711680)
    await ctx.channel.send(embed=embed)
  elif isinstance(error, commands.MemberNotFound):
    embed = discord.Embed(description=f"**{ctx.author.name}!**, Тухайн хэрэглэгч (`{error.argument}`) энэ серверт олдсонгүй", color=16711680)
    await ctx.channel.send(embed=embed)
  elif isinstance(error, commands.MissingRequiredArgument):
    embed = discord.Embed(description=f"**{ctx.author.name}!**, Уг коммандыг гүйцэтгэхэд шаардлах утгууд дутуу байна!", color=16711680)
    await ctx.send(embed=embed)


TOKEN = os.getenv("TOKEN")

client.run("OTIxMDQ1MTgyNjcyMTY2OTQy.YbtMKw.8vtuahezVapNLQNw4T7Gk8uzDs8")
