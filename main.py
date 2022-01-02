import discord
import json
import os
import datetime
import asyncio
import requests
import pymongo
from discord.ext import commands, tasks
userBlackList = []

client_user = pymongo.MongoClient("mongodb+srv://lilybrown:Lilybrown.0001@cluster0.ccjaa.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client_user['Discord']
collectionPrefix = db['Prefix']
collectionStatus = db['Status']

def get_prefix(client, message):
  if message.channel == message.author.dm_channel:
    return "?"
  else:
    server = collectionPrefix.find_one({"guild": str(message.guild.id)})
    prefix = server["prefix"]
    return prefix, "?"   

client = commands.Bot(command_prefix = "?", activity=discord.Game("?help"), intents = discord.Intents.all())
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

@client.event
async def on_ready():
    profile = collectionStatus.find_one({"guild": "primoverse"})
    status = profile['status']
    text = profile['text']
    url = profile['url']
    if status == 'play':
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=text))
    elif status == 'watch':
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=text))
    elif status == 'compet':
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.competing, name=text))
    elif status == 'listen':
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=text))
    elif status == 'stream':
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.streaming, name=text, url=url))
    print('Bot is ready!')


@client.command()
async def ping(ctx):
    embed = discord.Embed(description=f"Current ms: `{round(client.latency * 100)}`")
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


TOKEN = os.getenv("TOKEN")
client.run(TOKEN)