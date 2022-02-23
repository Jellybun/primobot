from re import A
import discord
import pymongo
import json
import aiohttp
import datetime
import motor.motor_asyncio
from discord.ext import commands

coin = '<:coin:933027999299809380>'

client_user = motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://lilybrown:Lilybrown.0001@cluster0.ccjaa.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client_user['Discord']
collectionProfile = db['Profile']
collectionServers = db['Servers']
collectionChats = db['Chats']
blank = "<:blank:835155831074455622>"
inv = "<:inv:864984624052305961>"

clientcommands = ["servers", "service", "gift", "bag", "save", "wd", "xp", "rank", "level", "customcommands", "allcommands", "service", "selfrole", "suggest", "prefix", "ping", "help", "setuserlevel", "resetserverlevel", "lb", "leaderboard", "top", "Lb", "Top", "Leaderboard", "command", "tags", "tag", "commands", "customcommands", "lock", "unlock", "mute", "unmute", "kick", "ban", "unban", "warn", "post", "postedit", "role", "purge", "clear", "delete", "daily", "avatar", "av", "who", "whois", "userinfo", "note", "market", "shop", "buy", "purchase", "sell", "inv", "inventory", "bag", "balance", "bal", "cash", "coin", "cowoncy", "deposit", "dep", "dump", "place", "withdraw", "draw", "wd", "withd", "give", "marry", "divorce", "profile", "roll", "poke", "nasa"]

class Events(commands.Cog):
    def __init__(self, client):
        self.client = client
        super().__init__()
        self.cd_mapping = commands.CooldownMapping.from_cooldown(1, 60, commands.BucketType.member)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or message.guild == None:
            return
        if await collectionProfile.count_documents({"userId": message.author.id}) == 0:
            status = {
                "userId": message.author.id,
                "daily": False,
                "profile": {
                    "coin": [0, 1000],
                    "marriage": "Single",
                    "about": "instagram"
                },
                "inventory": {
                    "ring": 0
                },
                "servers": {
                    str(message.guild.id): {
                        "id": message.guild.id,
                        "level": 0,
                        "xp": 0
                    }
                }
            }
            await collectionProfile.insert_one(status)

    @commands.Cog.listener('on_message')
    async def xpsystem(self, message):
        if message.author.bot or message.guild == None:
            return
        member = message.author
        bucket = self.cd_mapping.get_bucket(message)
        retry_after = bucket.update_rate_limit()
        if retry_after:
            return
        else:
            profile = await collectionProfile.find_one({"userId": member.id})
            if str(message.guild.id) not in list(profile["servers"].keys()):
                oldlevel = 0
                oldxp = 0
            else:
                oldlevel = profile['servers'][str(message.guild.id)]['level']
                oldxp = profile['servers'][str(message.guild.id)]['xp']
            oldcoin = profile['profile']['coin'][1]
            bank = profile['profile']['coin'][0]
            newxp = oldxp + 17
            requiredxp = int(oldlevel**3 + 1000)
            if newxp >= requiredxp:
                newlevel  = oldlevel + 1
                xp = newxp - requiredxp
                newcoin = oldcoin + (newlevel*1000)
                await message.channel.send(f"{message.author.mention}\nТа **{newlevel}** level хүрлээ!🎉🎉🎉\Level урамшуулал **{newlevel*1000}**{coin} койн таны дансанд орлоо!")
            else:
                newlevel = oldlevel
                xp = newxp
                newcoin = oldcoin
            status = {
                "$set": {
                    "profile.coin": [bank, newcoin],
                    f"servers.{str(message.guild.id)}": {
                        "id": message.guild.id,
                        "level": newlevel,
                        "xp": xp
                    }
                }
            }
            await collectionProfile.update_one(profile, status)

    @commands.Cog.listener("on_message")
    async def chat(self, message):
        if message.author.bot:
            return
        if message.channel == message.author.dm_channel:
            if await collectionChats.count_documents({"userId": message.author.id}) == 0:
                if message.content.startswith("?"):
                    return
                else:
                    await message.channel.send('Танд тусламж хэрэгтэй бол **Primoverse** серверийн #help гэсэн channel дээрээс хэрэгтэй зүйлээ бичээрэй')
                    return
            else:
                profile = await collectionChats.find_one({"userId": message.author.id})
                partner = self.client.get_user(profile['partner'])
                await partner.send(f"**Stranger**:\n{message.content}")

    @commands.Cog.listener("on_message")
    async def commandimporting(self, message):
        if message.author.bot or message.guild == None:
            return
        with open("importcommands.json", "r") as f:
            data = json.load(f)
        profile = await collectionServers.find_one({"guildId": message.guild.id})
        prefix = profile['prefix']
        if message.content.lower().startswith(f"{prefix}") and str(message.guild.id) in data:
            commands = [key for key in data[str(message.guild.id)]]
            seekingmsg = message.content[1:].lower()
            if seekingmsg in clientcommands:
                return
            elif seekingmsg in commands:
                response = data[str(message.guild.id)][str(seekingmsg)]
                await message.channel.send(response)
                return


    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.bot:
            return
        welcome = await collectionServers.find_one({"guildId": member.guild.id})['welcome']
        oldHour = datetime.datetime.now(datetime.timezone.utc).strftime("%H")
        now = datetime.datetime.now(datetime.timezone.utc)
        newHour = int(oldHour) + 8
        if newHour >= 24:
            newHour = int(newHour - 24)
        new = str(now.replace(hour=newHour, microsecond=0))[:-6]
        raw_json = json.loads(welcome['embed'])
        desc = raw_json['description']
        dict_final = desc.format(member=member.mention, member_count=member.guild.member_count)
        raw_json['description'] = dict_final
        embed = discord.Embed.from_dict(raw_json)
        embed.set_footer(text=new)
        
        if welcome['webhook'] is None:
            welcome_channel = self.client.get_channel(int(welcome['channel']))
            await welcome_channel.send(embed=embed)
        else:
            new_url = welcome['webhook'][30:]
            index = 0
            webhook_id = ''
            webhook_token = ''
            for letter in new_url:
                if letter == '/':
                    index += 1
                elif index == 1:
                    webhook_id += letter
                elif index == 2:
                    webhook_token += letter
        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.partial(
                webhook_id,
                webhook_token,
                adapter=discord.AsyncWebhookAdapter(session)
            )              
            await webhook.send(embed=embed)
    
    @commands.Cog.listener("on_member_join")
    async def profilecreaterformember(self, member):
        if await collectionProfile.count_documents({"userId": member.id}) == 0:
            status = {
                "userId": member.id,
                "daily": False,
                "profile": {
                    "coin": [0, 1000],
                    "marriage": "Single",
                    "about": "instagram"
                },
                "inventory": {
                    "ring": 0
                },
                "servers": {
                    str(member.guild.id): {
                        "id": member.guild.id,
                        "level": 0,
                        "xp": 0
                    }
                }
            }
            await collectionProfile.insert_one(status)


    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        if await collectionServers.count_documents({"guildId": guild.id}) == 0:
            document = {
                "guildId": guild.id,
                "prefix": "?",
                "tags": {},
                "notes": {},
                "ga": [],
                "welcome": {'embed': None, 'channel': None, 'webhook': None}
            }
            await collectionServers.insert_one(document)
        else:
            return

def setup(client):
    client.add_cog(Events(client))