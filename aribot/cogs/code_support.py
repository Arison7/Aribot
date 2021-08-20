import discord
from discord.ext import commands
from itertools import cycle
import json
global to_delete
to_delete = []


class help_channel():

    all_channels = []

    def __init__(self, channel_id, guild_id):
        self.channel_id = channel_id
        self.Is_occupated = False
        self.all_channels.append(self)
        self.user = []
        self.guild_id = guild_id


with open(r"C:\Users\ariso\Desktop\Snake projects\aribot\cogs\data.json", "r") as f:
    data = json.load(f)
for x in data["serwers"]:
    for y in x:
        for helps in x[y]["help_channels"]:
            help_channel(helps, y)


def get_channel_for_guild(guild_id, wanted_channel):
    for x in data["serwers"]:
        for y in x:
            if int(y) == guild_id:
                return int(x[y][wanted_channel])


class coggs(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(brief="brief description of your problem")
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def get_help(self, ctx, *, info):
        await ctx.channel.purge(limit=1)
        await ctx.channel.send(f"{ctx.author} your request has been send")
        guild_id = ctx.guild.id
        for x in help_channel.all_channels:

            if x.Is_occupated == False and int(x.guild_id) == ctx.guild.id:
                print("Check")
                x.Is_occupated = True
                print(x.Is_occupated)
                channel = self.client.get_channel(int(x.channel_id))
                channel2 = self.client.get_channel(
                    get_channel_for_guild(guild_id, "helpers_channel"))
                await channel.set_permissions(ctx.author, send_messages=True)
                await channel.send(f"hi, {ctx.author} please describe your problem here\nSoon one of the helpers will come here to solve your problem  ")
                x.user.append(ctx.author)
                emb = discord.Embed(title=f"{ctx.author} is looking for help with:",
                                    description=f"{info}\n\n*Reat with ✅ to take request*\n*react with ❌ to close this request* ", color=0xFF0000)
                await channel2.send(embed=emb)
                break

    @commands.command(brief="mods only don't try it")
    @commands.has_permissions(manage_messages=True)
    async def close(self, ctx):
        for x in help_channel.all_channels:
            if self.client.get_channel(int(x.channel_id)) == ctx.channel:
                await ctx.channel.purge(limit=1000)
                await ctx.channel.set_permissions(x.user[0], send_messages=False)
                break

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):

        channel = self.client.get_channel(payload.channel_id)

        if channel == self.client.get_channel(get_channel_for_guild(payload.guild_id, "helpers_channel")):
            print("check0")
            msg = await channel.fetch_message(payload.message_id)
            msge = msg.embeds
            title = msge[0].title

            msg_splited = title.split(" ")
            for x in help_channel.all_channels:

                print(type(payload.guild_id))
                print(type(int(x.guild_id)))

                if len(x.user) != 0 and int(x.guild_id) == payload.guild_id:
                    print("check 1")
                    if str(x.user[0]) == msg_splited[0]:
                        print("check 2")
                        channel2 = self.client.get_channel(int(x.channel_id))
                        break

        if str(payload.emoji.name) == "❌":

            if channel == self.client.get_channel(get_channel_for_guild(payload.guild_id, "helpers_channel")):
                print(len(to_delete))
                for u in to_delete:
                    await channel2.set_permissions(u, send_messages=False)

                msg = await channel.fetch_message(payload.message_id)
                await msg.delete()
        elif str(payload.emoji.name) == "✅":
            if channel == self.client.get_channel(get_channel_for_guild(payload.guild_id, "helpers_channel")):
                user = await self.client.fetch_user(payload.user_id)
                print(user)
                print(type(user))
                to_delete.append(user)

                await channel2.set_permissions(user, send_messages=True)
                await channel2.send(f"It's your lucky day {user} is here to help you")


def setup(client):
    client.add_cog(coggs(client))
