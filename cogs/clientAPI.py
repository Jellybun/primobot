import discord
import requests
import json
from discord.ext import commands
blank = "<:blank:835155831074455622>"
inv = "<:inv:864984624052305961>"

def get_apod():
    response = requests.get("https://api.nasa.gov/planetary/apod?api_key=FHlnYmh56cpv8KVLOdW8k2mCdKhAYT47A6XEKZCG")
    json_data = json.loads(response.text)
    return json_data

class Api(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def nasa(self, ctx):
        data = get_apod()
        image = data["hdurl"]
        title = data['title']
        date = data['date']
        explanation = data['explanation']
        author = data['copyright']
        embed = discord.Embed(title=title, description=str(explanation))
        embed.set_author(name=str(author))
        embed.set_image(url=str(image))
        embed.set_footer(text=str(date))
        await ctx.send(embed = embed)

    

def setup(client):
    client.add_cog(Api(client))