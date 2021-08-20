import discord
from discord.ext import commands
from itertools import cycle
import json
with open(r"C:\Users\ariso\Desktop\Snake projects\aribot\cogs\data.json", "r") as f:
    data = json.load(f)

#gets id for a artist channel for a guild it's used in 
def get_channel_for_guild(guild_id, wanted_channel):
    for x in data["serwers"]:
        for y in x:
            if int(y) == guild_id:
                return int(x[y][wanted_channel])


class coggs(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.colors = cycle([0xF39E06, 0x00ff00, 0xF305FF, 0xFF0014, 0x1FB28D])

    @commands.command(brief='Title, description')
    @commands.cooldown(1, 30, commands.BucketType.user)
    #sending emded request to a artist channel for easier work
    #takes title of a project and it's description seperated by a ","
    async def art_request(self, ctx,  *, rest):
        
        if ctx.channel == self.client.get_channel(get_channel_for_guild(ctx.guild.id, "art_request_channel")):
            await ctx.channel.send(f"{ctx.author} your request has been sent")
            if rest == "":
                raise commands.MissingRequiredArgument
            else:
                channel = self.client.get_channel(
                    get_channel_for_guild(ctx.guild.id, "artists_channel"))
                splited_rest = rest.split(",")
                z = " "
                for x in range(len(splited_rest)-1):
                    y = splited_rest[x+1]
                    z += y + " "
                emb = discord.Embed(title=f"art {splited_rest[0]} \nhas be requested by {ctx.author} ",
                                    description=f'**Description:**\n{z}\n\n *Reat with :thumbsup: to let know other you are doing it*\n*react with ❌ to close this request* ', color=next(self.colors))
                await channel.send(embed=emb)
        else:
            await ctx.channel.purge(limit=1)
            await ctx.channel.send(f"This command is accesable only in {self.client.get_channel(get_channel_for_guild(ctx.guild.id,'art_request_channel'))}")

            #f"art {splited_rest[0]} has be requested by {ctx.author} \n with following description{z} \n reat with :thumbsup: to let know other you are doing it"
    #Deleting requested after they are fulfilled with ❌ emote
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        channel = self.client.get_channel(payload.channel_id)
        if channel == get_channel_for_guild(payload.guild_id,"artists_channel"): 
            if str(payload.emoji.name) == "❌":
                msg = await channel.fetch_message(payload.message_id)
                await msg.delete()

    @art_request.error
    async def art_request_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument) and ctx.channel != self.client.get_channel(get_channel_for_guild(ctx.guild.id, "art_request_channel")):
            await ctx.channel.purge(limit=1)
            await ctx.send(f"Wrong channel buddy, also add description to your request (channel should be {self.client.get_channel(get_channel_for_guild(ctx.guild.id,'art_request_channel'))})")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.channel.purge(limit=1)
            await ctx.send("You need to add description to your request")


def setup(client):
    client.add_cog(coggs(client))
