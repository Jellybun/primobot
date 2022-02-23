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
collectionChats = db['Chats']
blank = "<:blank:835155831074455622>"
inv = "<:inv:864984624052305961>"
coinimg = "<:coin:933027999299809380>"

class Tasks(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.dailyTask.start()
        self.checkboosters.start()
        self.commandimporter.start()
        self.quizmo.start()

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
                amount = 2000
                desc = f"**{ctx.author.name}**! Та өнөөдрийн daily reward-аа авч танд **{1000}{coinimg}** болон сервер boost-ийн **{1000}{coinimg}** coins нэмэгдэж орлоо"
            else:
                amount = 1000
                desc = f"**{ctx.author.name}**! Та өнөөдрийн daily reward-аа авч танд **{amount}{coinimg}** coins нэмэгдэж орлоо"
            newbal = oldbal + amount
            status = {
                "$set": {
                    "daily": True,
                    "profile.coin": [bank, newbal]
                }
            }
            await collectionProfile.update_one(profile, status)
            await ctx.send(desc)
        else:
            await ctx.send(f"**{ctx.author.name}**! Та нэг өдөрт нэг л удаа daily reward авч болно")
            return

    @tasks.loop(seconds=60)
    async def quizmo(self):
        profile = await collectionChats.find_one({"room": "room"})
        lining = profile['lining']
        users = []
        i = 0
        length = int(len(lining)/2)
        while i < length:
            user1 = lining[0]
            user2= lining[1]
            for i in range(len(lining)):
                if i in [0, 1]:
                    pass
                else:
                    users = users + [lining[i]]
            i += 1
            doc1 = {"userId": user1, "partner": user2}
            doc2 = {"userId": user2, "partner": user1}

            await collectionChats.insert_one(doc1)
            await collectionChats.insert_one(doc2)
            user1 = self.client.get_user(user1)
            if user1 != None:
                await user1.send("Tантай xэрэглэгч холбогдлоо. Таны бичсэн зүйлс тухайн хэрэглэгчид bot dm message-ээр очих болно.")                
            user2 = self.client.get_user(user2)
            if user2 != None:
                await user2.send("Tантай xэрэглэгч холбогдлоо. Таны бичсэн зүйлс тухайн хэрэглэгчид bot dm message-ээр очих болно.")                
        await collectionChats.update_one(profile, {"$set": {"lining": users}})

    @quizmo.before_loop
    async def until_next_run_quizmo(self):
        await self.client.wait_until_ready()

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
            if str(key) not in boosters:
                roleid = profile['boosters'][str(key)]
                if roleid == False:
                    pass
                else:
                    role = guild.get_role(roleid)
                    await role.delete()
                user = self.client.get_user(int(key))
                await user.send("Primoverse server-ийг boost хийсэнд баярлалаа! Tа Primoverse server дэх **Server booster** perk-ийг алдаж хувийн role-оо алдлаа")
            else:
                value = profile['boosters'][str(key)]
                store[str(key)] = value
        for booster in boosters:
            if booster not in keys:
                user = self.client.get_user(int(booster))
                await user.send("Primoverse server-ийг boost хийсэнд баярлалаа!\nЭнэ хугацаанд та `?selfrole <name> <hexcode>` command-ийг ашиглан зөвхөн өөртөө хүссэн нэр өнгөөр хувийн role хийлгэж болно. Мөн өдөр тутмын **Daily** дээрээс 2 дахин их койн авна.")
                store[str(booster)] = False
        status = {"$set": {"boosters": store}}
        await collectionPrimoverse.update_one(profile, status)

    @checkboosters.before_loop
    async def until_next_run_1(self):
        await self.client.wait_until_ready()


    @tasks.loop(hours=24)
    async def dailyTask(self):
        async for profile in collectionProfile.find():
            bank = profile['profile']['coin'][0]
            bal = int(profile['profile']['coin'][1])
            newbank = int(bank*1.03)
            status = {
                "$set": {
                    "daily": False,
                    "profile.coin": [newbank, bal]
                }
            }
            await collectionProfile.update_one(profile, status)

    @dailyTask.before_loop
    async def until_next_run(self):
        now = datetime.datetime.now(datetime.timezone.utc)
        later = now.replace(hour=8, minute=0, second=00)
        if later < now:
            later += datetime.timedelta(days=1)
        await discord.utils.sleep_until(later)
        
def setup(client):
    client.add_cog(Tasks(client))
