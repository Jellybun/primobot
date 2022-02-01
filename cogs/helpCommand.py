import discord
import datetime
from discord.ext import commands
blank = "<:blank:835155831074455622>"
inv = "<:inv:864984624052305961>"

class Helpcommand(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def service(self, ctx):
        embed = discord.Embed(title='Танилцуулга:', description="Primoverse нь Discord Bot хийх болон серверт freelancing moderator хийж өгөх үйлчилгээ үзүүлдэг. Та хэрвээ сервертээ өөрийн хүссэн маягаар bot хийлгэх эсвэл Bot болон Third-party website-уудтай ажиллаж чадах туршлагатай үйлчилгээ хэрэгтэй бол манай серверт нэгдэж илүү дэлгэрэнгүй мэдээллийг аваарай\n[Нэгдэх](https://www.discord.gg/X3YRdPNSZu)", color=16777215)
        embed.set_image(url="https://cdn.discordapp.com/attachments/832245157889441855/936253173428015154/Screen_Shot_2021-12-30_at_19.20.02.png")
        embed.set_thumbnail(url=self.client.user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def help(self, ctx, category=None):        
        if category is None:
            desc = f'Комманд тус бүрийн талаар `?help <command>` гэж дэлгэрэнгүй мэдээлэл аваарай\n\n__**Main commands:**__\n> `profile` `leaderboard`\n\n__**Economy:**__\n> `daily` `balance` `give` `shop` `buy` `sell` `inventory` `deposit` `withdraw` `marry`\n\n__**Moderation:**__\n> `command` `role` `post` `clear` `mute` `lock` `warn` `kick` `ban` `setuserlevel` `resetserverlevel`\n\n__**Utility:**__\n> `tag` `note` `avatar` `userinfo`\n\n__**Fun:**__\n> `roll` `poke`\n\n__**Education:**__\n> `nasa` *more features coming soon...*\n\n__**Service:**__\n> `service`'
        elif category.lower() == "profile":
            desc = '```?profile```\n**Тайлбар:**\n```Primobot дээрх өөрийн үзүүлэлт болон тухайн серверт хэдэн левелтэй байгаагаа харах```\n**Авах утгууд:**\n`?profile` – Өөрийн profile-ийг харах\n`?profile <user>` – Бусад хэрэглэгчийн profile-ийг харах\n\n**Aliases:**\n```rank, xp, level```\n**Cooldown:**\n```10 seconds```'
        elif category.lower() == "leaderboard":
            desc = '```?leaderboard```\n**Тайлбар:**\n```Сервер дахь хамгийн их level болон coin-тэй хэрэглэгчдийг харах```\n**Авах утгууд:**\n`?leaderboard <level/xp> <index>` – Өөрийн profile-ийг харах\n`?leaderboard <cash/money/rich/coin> {quantity}` – Бусад хэрэглэгчийн profile-ийг харах\n\n**Aliases:**\n```lb```\n**Cooldown:**\n```10 seconds```'
        elif category.lower() == "daily":
            desc = '```?daily```\n**Тайлбар:**\n```Primobot дээрх өдөр тутмын daily авах```\n**Авах утгууд:**\n`?daily` – Нэмэлт утга авахгүй\n\n**Aliases:**\n```None```\n**Cooldown:**\n```10 seconds```'
        elif category.lower() == "balance":
            desc = '```?balance```\n**Тайлбар:**\n```Primobot дээрх өөрийн дансны мэдээлэл харах```\n**Авах утгууд:**\n`?balance` – Нэмэлт утга авахгүй\n\n**Aliases:**\n```cash, coin, bal, money```\n**Cooldown:**\n```5 seconds```'
        elif category.lower() == "give":
            desc = '```?give```\n**Тайлбар:**\n```Primobot ашигладаг өөр хэрэглэгчид coin шилжүүлэх```\n**Авах утгууд:**\n`?give <user>` – Ямар хэрэглэгчид өгөхөө тодотгох\n\n**Aliases:**\n```gift```\n**Cooldown:**\n```5 seconds```'
        elif category.lower() == "shop":
            desc = '```?shop```\n**Тайлбар:**\n```Primobot-ийн shop харах```\n**Авах утгууд:**\n`?shop – Shop дээрх item харах\n`?shop sell <item>` – Хэрвээ та өөрөө shop дээр зар оруулах бол зарах зүйлийн мэдээллийг оруулна\n\n**Aliases:**\n```None```\n**Cooldown:**\n```5 seconds```'
        elif category.lower() == "buy":
            desc = '```?buy```\n**Тайлбар:**\n```Primobot дээрх албан ёсны item-уудаас худалдаж авах```\n**Авах утгууд:**\n`?buy <item>` – Авах зүйлийн нэр\n\n**Aliases:**\n```None```\n**Cooldown:**\n```5 seconds```'
        elif category.lower() == "sell":
            desc = '```?sell```\n**Тайлбар:**\n```Өөрийн inventory дотор байгаа зүйлийг зарах. Үнэ нь авсан үнээс 2 дахин бага болно```\n**Авах утгууд:**\n`?sell <item>` – Зарах зүйлийн нэр\n\n**Aliases:**\n```None```\n**Cooldown:**\n```5 seconds```'
        elif category.lower() == "inventory":
            desc = '```?inventory```\n**Тайлбар:**\n```Өөрийн inventory дотор байгаа зүйлсийг харах```\n**Авах утгууд:**\n`?inventory` – Өөрт байгаа зүйлс\n`?inventory <user>` – Бусад хэрэглэгчийн inventory-г харах\n\n**Aliases:**\n```inv, bag```\n**Cooldown:**\n```5 seconds```'
        elif category.lower() == "deposit":
            desc = '```?deposit```\n**Тайлбар:**\n```Өөрийн дансанд wallet-аас мөнгө хийх\n**Авах утгууд:**\n`?deposit <amount>` – Шилжүүлэх хэмжээ\n\n**Aliases:**\n```dep, dump, save```\n**Cooldown:**\n```5 seconds```'
        elif category.lower() == "withdraw":
            desc = '```?withdraw```\n**Тайлбар:**\n```Өөрийн данснаас wallet-руу мөнгө татах\n**Авах утгууд:**\n`?withdraw <amount>` – Татах хэмжээ\n\n**Aliases:**\n```withd, wd, draw```\n**Cooldown:**\n```5 seconds```'
        elif category.lower() == "marry":
            desc = '```?marry```\n**Тайлбар:**\n```Primobot ашигладаг бусад хэрэглэгчтэй гэрлэх. Гэрлэсэн тохиолдол хэнтэй гэрлэсэнээ харах\n**Авах утгууд:**\n`?marry` – Өөрийн гэрлэлтийн статусыг харах\n`?marry <user>` – Гэрлэх саналаа тавих хүн\n\n**Aliases:**\n```propose, marriage, husband, wife```\n**Cooldown:**\n```10 seconds```\n**Sub command:** `?divorce <user>` – Гэрлэсэн хүнээсээ салах'
        elif category.lower() == "command":
            desc = '```?command```\n__Note: Зөвхөн admin permission-тэй хүмүүс гүйцэтгэх комманд__\n**Тайлбар:**\n```Серверийн custom command хянах\n**Авах утгууд:**\n`?command create <name> <content>` – Шинээр custom command хийх. Hэр болон контентийг оруулж өгнө\n`?command edit <name> <new_content>` – Custom command-ийн контентийг өөрчлах\n`?command delete <name> – Custom command-ийг устгах`\n\n**Aliases:**\n```customcommand```\n**Cooldown:**\n```10 seconds```'
        elif category.lower() == "role":
            desc = '```?command```\n**Тайлбар:**\n```Серверийн role хянах\n**Авах утгууд:**\n`?role create <name> <hex color code>` – Шинээр role хийх. Hэр болон hex code оруулж өгнө\n`?role delete <@role>` – Role устгах\n`?role info <@role>` – Role-ийн мэдээлэл харах\n`?role add <@user> <@role>` – Хэрэглэгчид role өгөх\n`?role remove <@user/all> <@role>` – Хэрэглэгчээс role хурааж авах\n`?role changecolor/color <@role> <hex code> – Role өнгө солих`\n\n**Aliases:**\n```None```\n**Cooldown:**\n```3 seconds```\n**Required permissions:**\n```Manage roles```'
        elif category.lower() == "post":
            desc = '```?post```\n**Тайлбар:**\n```Серверийн аль нэг channel-д Primobot-oop message бичих\nХэрвээ Primobot-oop бичсэн message-ийг өөрчлөх бол ?help postedit гэж бичин мэдээлэл авна уу```\n**Авах утгууд:**\n`?post <channel> <message/json>` – Ямар channel-д бичихээ тодотгох\nХэрвээ embed-message бичих бол Discohook дээрээс Json format-ийг хуулж буулган бичнэ\n\n**Aliases:**\n```None```\n**Cooldown:**\n```5 seconds```\n**Required permissions:**\n```Manage messages```'
        elif category.lower() == "postedit":
            desc = '```?postedit```\n**Тайлбар:**\n```Серверт Primobot-oop бичсэн message-ийг өөрчлөх```\n**Авах утгууд:**\n`?postedit <channel> <messageId> <message/json>` – Тухайн message-ийн channel, message id болон шинэ message контент\nХэрвээ embed-message бичих бол Discohook дээрээс Json format-ийг хуулж буулган бичнэ\n\n**Aliases:**\n```None```\n**Cooldown:**\n```5 seconds```\n**Required permissions:**\n```Manage messages```'
        elif category.lower() == "clear":
            desc = '```?clear```\n**Тайлбар:**\n```Channel дахь message устгах```\n**Авах утгууд:**\n`?clear <amount/all>` – Устгах message-ийн хэмжээ\n`?purge <user> <amount>` – Зөвхөн тухайн хэрэглэгчийн message-ийг устгах\n\n**Aliases:**\n```purge```\n**Cooldown:**\n```5 seconds```\n**Required permissions:**\n```Manage messages```'
        elif category.lower() == "mute":
            desc = '```?mute```\n**Тайлбар:**\n```Хэрэглэгчид mute role өгөх\nЭнэ комманд нь сервэрээс зөвхөн Muted гэсэн нэртэй role өгнө. Тухайн нэртэй role олдоогүй тохиолдолд хүчингүй болно```\n**Авах утгууд:**\n`?mute <user>` – Mute хийх хэрэглэгч\n\n**Aliases:**\n```None```\n**Cooldown:**\n```5 seconds```\n**Sub command:** `?unmute` – Mute хийсэн хэрэглэгээс muted role авах\n**Required permissions:**\n```Manage messages```'
        elif category.lower() == "lock":
            desc = '```?lock```\n**Тайлбар:**\n```Сервэрийн channel lock хийх```\n**Авах утгууд:**\n`?lock <channel>` – Lock хийх channel\n\n**Aliases:**\n```None```\n**Cooldown:**\n```5 seconds```\n**Sub command:** `?unlock` – Lock хийсэн channel-ийг unlock хийх\n**Required permissions:**\n```Manage messages```'
        elif category.lower() == "warn":
            desc = '```?warn```\n**Тайлбар:**\n```Хэрэглэгчид анхааруулга өгөх```\n**Авах утгууд:**\n`?warn <user>` – Анхааруулга өгөх хэрэглэгч\n\n**Aliases:**\n```None```\n**Cooldown:**\n```5 seconds```\n**Required permissions:**\n```Manage messages```'
        elif category.lower() == "kick":
            desc = '```?kick```\n**Тайлбар:**\n```Хэрэглэгчийг серверээс гаргах```\n**Авах утгууд:**\n`?kick <user>` – Kick-лэх хэрэглэгч\n\n\n**Aliases:**\n```None```\n**Cooldown:**\n```5 seconds```\n**Required permissions:**\n```Manage messages```'
        elif category.lower() == "ban":
            desc = '```?ban```\n**Тайлбар:**\n```Хэрэглэгчийг серверээс бан хийх```\n**Авах утгууд:**\n`?ban <user>` – Бан хийх хэрэглэгч\n\n**Aliases:**\n```None```\n**Cooldown:**\n```5 seconds```\n**Sub command:**  `?unban <user>` – Бан хийсэн хэрэглэгчийг unban хийх\n**Required permissions:**\n```Manage messages```'
        elif category.lower() == "setuserlevel":
            desc = '```?setuserlevel```\n__Note: Зөвхөн admin permission-тэй хүмүүс гүйцэтгэх комманд__\n**Тайлбар:**\n```Хэрэглэгчийн тухайн сервэр дэх level-ийг өөрчлөх```\n**Авах утгууд:**\n`?setuserlevel <user>` – Level-ийг нь өөрчлөх хэрэглэгч\n\n**Aliases:**\n```None```\n**Cooldown:**\n```5 seconds```'
        elif category.lower() == "resetserverlevel":
            desc = '```?resetserverlevel```\n__Note: Зөвхөн admin permission-тэй хүмүүс гүйцэтгэх комманд__\n**Тайлбар:**\n```Тухайн сервэрийн level-ийг дахин шинээр эхлэх```\n**Авах утгууд:**\n`?setuserlevel` – Нэмэлт утга авахгүй\n\n**Aliases:**\n```None```\n**Cooldown:**\n```5 seconds```'
        elif category.lower() == "tag":
            desc = '```?tag```\n**Тайлбар:**\n```Сервердэх tag харах```\n**Авах утгууд:**\n`?tag <name>` – Тухайн серверээс tag нэрээр нь хайх\n`?tags` – Тухайн сервер дэх бүх tag-ийг харах\n**Server moderation**(Шаардах permissions: __manage_messages__):\n`?tag <create> <name> – Tag шинээр үүсгэхn\n`?tag edit <name>` – Өмнө нь байсан tag-ийн контентийг өөрчлөх\n`?tag delete <name>` – Tag устгах\n\n**Aliases:**\n```None```\n**Cooldown:**\n```5 seconds```'
        elif category.lower() == "note":
            desc = '```?note```\n**Тайлбар:**\n```Өөртөө сануулга үлдээх эсвэл тэмдэглэл хийх```\n**Авах утгууд:**\n`?note <content>` – Тэмдэглэл хадгалах\n`?note` – Хадгалсан тэмдэглэлээ хадгалах\n\n**Aliases:**\n```None```\n**Cooldown:**\n```5 seconds```'
        elif category.lower() == "avatar":
            desc = '```?avatar```\n**Тайлбар:**\n```Хэрэглэгчийн avatar picture харах```\n**Авах утгууд:**\n`?avatar <user>` – Avatar-ийг нь харах хэрэглэгч\n\n**Aliases:**\n```av```\n**Cooldown:**\n```5 seconds```'
        elif category.lower() == "userinfo":
            desc = '```?avatar```\n**Тайлбар:**\n```Хэрэглэгчийн тухайн сервэр дэх мэдээллийг харах```\n**Авах утгууд:**\n`?userinfo <user>` – Мэдээллийг нь харах хэрэглэгч\n\n**Aliases:**\n```whois, who```\n**Cooldown:**\n```5 seconds```'
        elif category.lower() == "poke":
            desc = '```?poke```\n**Тайлбар:**\n```Сервер дэх хэрэглэгчрүү өөрт нь мэдэгдэхгүйгээр Primobot-oop message бичих\nAlternative secret.me```\n**Авах утгууд:**\n`?poke <user>` – Poke хийх хэрэглэгч\n\n**Aliases:**\n```None```\n**Cooldown:**\n```5 seconds```'
        elif category.lower() == 'roll':
            desc = '```?roll```\n**Тайлбар:**\n```Шоо хаях```\n**Авах утгууд:**\n`?roll <amount>` – Шоон талуудын тоо\n\n**Aliases:**\n```None```\n**Cooldown:**\n```5 seconds```'
        elif category.lower() == "nasa":
            desc = '```?nasa```\n**Тайлбар:**\n```Өдөр тутмын сонирхолтой Nasa-ийн зураг```\n**Авах утгууд:**\n`?nasa` – Нэмэлт утга авахгүй\n\n**Aliases:**\n```None```\n**Cooldown:**\n```10 seconds```'
        elif category.lower() == "service":
            desc = '```?service```\n**Тайлбар:**\n```Primoverse нь Discord Bot хийх болон серверт freelancing moderator хийж өгөх үйлчилгээ үзүүлдэг. Та хэрвээ сервертээ өөрийн хүссэн маягаар bot хийлгэх эсвэл Bot болон Third-party website-уудтай ажиллаж чадах туршлагатай үйлчилгээ хэрэгтэй бол манай серверт нэгдэж илүү дэлгэрэнгүй мэдээллийг аваарай```\n[Нэгдэх](https://www.discord.gg/X3YRdPNSZu)'

        embed = discord.Embed(
                title='Комманд зааварчилгаа:',
                description=desc,
                color=16777215
            )
        embed.set_thumbnail(url=self.client.user.avatar_url)
        await ctx.send(embed=embed)

    

def setup(client):
    client.add_cog(Helpcommand(client))