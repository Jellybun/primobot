import discord
import pymongo
import asyncio
import json
import datetime
import motor.motor_asyncio
from discord.ext import commands, tasks
client_user = motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://lilybrown:Lilybrown.0001@cluster0.ccjaa.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client_user['Discord']
collectionServers = db['Servers']
collectionCommands = db['Commands']
collectionPrimoverse = db['Primoverse']
collectionProfile = db['Profile']
blank = "<:blank:835155831074455622>"
inv = "<:inv:864984624052305961>"
coinimg = "<:coin:933027999299809380>"

class Tasks(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.dailyTask.start()
        self.checkboosters.start()
        self.commandimporter.start()

    @commands.command()
    async def daily(self, ctx):
        profile = await collectionProfile.find_one({"userId": ctx.author.id})
        if profile['daily'] == False:
            bank = profile['profile']['coin'][0]
            oldbal = profile['profile']['coin'][1]

            guild = self.client.get_guild(906153176414183475)
            boosterrole = guild.get_role(927487106840940546)
            membersobj = boosterrole.members
            boosters = []
            for obj in membersobj:
                boosters.append(obj.id)

            if ctx.author.id in boosters:
                amount = 2500
            else:
                amount = 1000
            newbal = oldbal + amount
            status = {
                "$set": {
                    "daily": True,
                    "profile.coin": [bank, newbal]
                }
            }
            await collectionProfile.update_one(profile, status)
            await ctx.send(f"**{ctx.author.name}**! Та өнөөдрийн daily reward-аа авч танд **1000{coinimg}** coins нэмэгдэж орлоо\nМөн **server booster**-ийн **1500{coinimg}** coins бонус авлаа")
        else:
            await ctx.send(f"**{ctx.author.name}**! Та нэг өдөрт нэг л удаа daily reward авч болно")
            return


    @tasks.loop(minutes=1)
    async def commandimporter(self):
        data = {}
        async for profile in collectionCommands.find():
            guildId = profile['guildId']
            data[str(guildId)] = {}
            keys = profile['commands'].keys()
            for key in keys:
                value = profile['commands'][str(key)]
                data[str(guildId)][str(key)] = str(value)
        with open("importcommands.json", "w") as f:
            json.dump(data, f)


    @tasks.loop(hours=1)
    async def checkboosters(self):
        profile = await collectionPrimoverse.find_one({"guildName": "Primoverse"})
        guild = self.client.get_guild(906153176414183475)
        boosterrole = guild.get_role(927487106840940546)
        membersobj = boosterrole.members
        boosters = []
        store = {}
        for obj in membersobj:
            boosters.append(str(obj.id))
    
        keys = profile['boosters'].keys()
        for key in keys:
            if str(key) in boosters:
                roleid = profile['boosters'][str(key)]
                store[str(key)] = roleid
            else:
                roleid = profile['boosters'][str(key)]
                if roleid == False:
                    pass
                else:
                    role = guild.get_role(roleid)
                    await role.delete()
                user = self.client.get_user(int(key))
                await user.send("Primoverse server-ийг boost хийсэнд баярлалаа! гэхдээ та Primoverse server дэх **Server booster** perk-ийг алдаж хувийн role-оо алдлаа")
        status = {"$set": {"boosters": store}}
        for booster in boosters:
            if booster not in keys:
                print(int(booster))
                user = self.client.get_user(int(booster))
                await user.send("Primoverse server-ийг boost хийсэнд баярлалаа!\nЭнэ хугацаанд та `?selfrole <name> <hexcode>` command-ийг ашиглан зөвхөн өөртөө хүссэн нэр өнгөөр хувийн role хийлгэж болно. Мөн өдөр тутмын **Daily** дээрээс 2 дахин их койн авна.")
        await collectionPrimoverse.update_one(profile, status)

    @checkboosters.before_loop
    async def until_next_run_1(self):
        await self.client.wait_until_ready()


    @tasks.loop(hours=24)
    async def dailyTask(self):
        async for profile in collectionProfile.find():
            bank = profile['profile']['coin'][0]
            bal = profile['profile']['coin'][1]
            newbank = bank * 1.03
            status = {
                '$set:': {
                    "daily": False,
                    "profile.coin": [newbank, bal]
                }
            }
            await collectionProfile.update_one(profile, status)
        print("Successfully reset the daily status!")

    @dailyTask.before_loop
    async def until_next_run(self):
        now = datetime.datetime.now(datetime.timezone.utc)
        later = now.replace(hour=8, minute=0, second=00)
        if later < now:
            later += datetime.timedelta(days=1)
        await discord.utils.sleep_until(later)
        
def setup(client):
    client.add_cog(Tasks(client))
