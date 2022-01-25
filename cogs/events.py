import discord
import pymongo
import json
import datetime
import motor.motor_asyncio
from discord.ext import commands

coin = '<:coin:933027999299809380>'

client_user = motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://lilybrown:Lilybrown.0001@cluster0.ccjaa.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client_user['Discord']
collectionProfile = db['Profile']
collectionServers = db['Servers']
blank = "<:blank:835155831074455622>"
inv = "<:inv:864984624052305961>"

clientcommands = ["service", "gift", "bag", "save", "wd", "xp", "rank", "level", "customcommands", "allcommands", "service", "selfrole", "suggest", "prefix", "ping", "help", "setuserlevel", "resetserverlevel", "lb", "leaderboard", "top", "Lb", "Top", "Leaderboard", "command", "tags", "tag", "commands", "customcommands", "lock", "unlock", "mute", "unmute", "kick", "ban", "unban", "warn", "post", "postedit", "role", "purge", "clear", "delete", "daily", "avatar", "av", "who", "whois", "userinfo", "note", "market", "shop", "buy", "purchase", "sell", "inv", "inventory", "bag", "balance", "bal", "cash", "coin", "cowoncy", "deposit", "dep", "dump", "place", "withdraw", "draw", "wd", "withd", "give", "marry", "divorce", "profile", "roll", "poke", "nasa"]

class Events(commands.Cog):
    def __init__(self, client):
        self.client = client
        super().__init__()
        self.cd_mapping = commands.CooldownMapping.from_cooldown(1, 60, commands.BucketType.member)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or message.guild == None:
            return
        with open("importcommands.json", "r") as f:
            data = json.load(f)
        profile = await collectionServers.find_one({"guildId": message.guild.id})
        prefix = profile['prefix']
        if message.content.lower().startswith(f"{prefix}") and str(message.guild.id) in data:
            commands = [key for key in data[str(message.guild.id)]]
            seekingmsg = message.content[1:].lower()
            for cmd in clientcommands:
                if seekingmsg.startswith(cmd):
                    return
                else:
                    pass
            if seekingmsg in commands:
                response = data[str(message.guild.id)][str(seekingmsg)]
                await message.channel.send(response)
                return
            else:
                await message.channel.send(f"**{message.author.name}!** **{seekingmsg}** нэртэй custom command олдсонгүй")
                return
        member = message.author
        bucket = self.cd_mapping.get_bucket(message)
        retry_after = bucket.update_rate_limit()
        if retry_after:
            pass
        else:
            if await collectionProfile.count_documents({"userId": member.id}) == 0:
                status = {
                    "userId": member.id,
                    "daily": False,
                    "profile": {
                        "coin": [0, 1000],
                        "marriage": "Single",
                        "about": "I am a human being"
                    },
                    "inventory": {
                        "ring": 0
                    },
                    "servers": {
                        str(member.guild.id): [0, 17]
                    },
                    "serverinfo": {
                        str(member.guild.name): member.guild.name
                    }
                }
                await collectionProfile.insert_one(status)
            else:
                profile = await collectionProfile.find_one({"userId": member.id})
                if str(message.guild.id) not in list(profile["servers"].keys()):
                    oldlevel = 0
                    oldxp = 0
                else:
                    oldlevel = profile['servers'][str(message.guild.id)][0]
                    oldxp = profile['servers'][str(message.guild.id)][1]
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
                        f"servers.{str(message.guild.id)}": [newlevel, xp],
                        f"serverinfo.{str(member.guild.name)}": member.guild.name
                    }
                }
                await collectionProfile.update_one(profile, status)



    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.bot:
            return
        if await collectionProfile.count_documents({"userId": member.id}) == 0:
            status = {
                "userId": member.id,
                "daily": False,
                "profile": {
                    "coin": [0, 1000],
                    "marriage": "Single",
                    "about": "I am a human being"
                },
                "inventory": {
                    "ring": 0
                },
                "servers": {
                    str(member.guild.id): [0, 0]
                },
                "serverinfo": {
                    str(member.guild.name): member.guild.name
                }
            }
            await collectionProfile.insert_one(status)
        if member.guild.id != 906153176414183475:
            return
        oldHour = datetime.datetime.now(datetime.timezone.utc).strftime("%H")
        now = datetime.datetime.now(datetime.timezone.utc)
        newHour = int(oldHour) + 8
        new = now.replace(hour=newHour, microsecond=0)
        
        welcomeChannel = self.client.get_channel(927195673684750336)
        welcomeMessage = await welcomeChannel.fetch_message(927256713999040532)
        embed = discord.Embed(description=f'Welcome to our server! {member.mention}\nYou are our {member.guild.member_count}th member', color=16777215)
        embed.set_image(url='https://cdn.discordapp.com/attachments/832245157889441855/930055311887323206/Screen_Shot_2021-12-30_at_19.22.44.png')
        embed.set_author(name=member.name, icon_url=member.avatar_url)
        embed.set_footer(text=new)
        await welcomeMessage.edit(embed=embed)


    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        if await collectionServers.count_documents({"guildId": guild.id}) == 0:
            document = {
                "guildId": guild.id,
                "prefix": "?",
                "tags": {},
                "notes": {},
                "ga": []
            }
            await collectionServers.insert_one(document)
        else:
            return

def setup(client):
    client.add_cog(Events(client))