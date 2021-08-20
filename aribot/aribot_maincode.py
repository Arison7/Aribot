import discord
from discord.ext import commands, tasks
from itertools import cycle
import os
import json
import random

client = commands.Bot(command_prefix=".ari ")
# used on_guild_join to easier put data into json file (i putted here for no reason)
tamplate = {}


# opens json file and loads it data in data variable
with open(r"C:\Users\ariso\Desktop\Snake projects\aribot\cogs\data.json", "r") as f:
    data = json.load(f)
# when bots is entering the serwer it's used to get all nessesary channels ids


@client.event
async def on_guild_join(guild):
    # checks if guild is already in our database , technicly impossible to fail, but it's just in case
    if guild.id in data["serwers"]:
        return
    else:
        # ask owner in serwer to fill this if all nessesart ids
        await guild.text_channels[0].send('''hello!
I will need you to complete some spets before we can work together
pls use command *.ari add_channels*
id of helpers_channels one or more seperated by "|" ,  
id of channel that you want to users to send art_requests ,
id of channel you want to artists only channel,
id of chanel that would helpers only channel [note id Has to be write without spaces and have to be saperated by ,] ''')
        # commands for setting up bot

        @client.command()
        @commands.is_owner()
        async def add_channels(ctx, *, rest):
            help_channels = []
            splited_rest = rest.split(",")
            for x in splited_rest[0].split("|"):
                help_channels.append(x)
                for x in help_channels:
                    # checks if channels exits in serwer
                    if int(x)not in guild.text_channel:
                        await ctx.send("one of channels doesn't exists in your serwer")
            for x in range(len(splited_rest)-1):
                if int(splited_rest[x+1]) not in guild.text_channel:
                    await ctx.send("one of channels doesn't exists in your serwer")
            # adds modified template to data.json
            tamplate.setdefault(guild.id, {"help_channels": help_channels, "art_request_channel":
                               splited_rest[1], "artists_channel": splited_rest[2], "helpers_channel": splited_rest[3]})
            data["serwers"].append(tamplate)
            with open(r"C:\Users\ariso\Desktop\Snake projects\aribot\cogs\data.json", "w") as f:
                json.dump(data, f, indent=2)
            await ctx.send('''cool, everything seems to be working. Last thing are channel permisions
helpers_channels should be visable for everyone and mods/helpers should be allow to manage them
art_request channel should be public
artists only channel i think speaks for it self
same with helpers only ''')
            
# removing all of data about the guild after leaving

@client.event
async def on_guild_remove(guild):
    for x in data["serwers"]:
        if guild.id == int(x):
            del x

#indicator after bot is ready for use 

@client.event
async def on_ready():
    print("i am ready")

# realoding cogs 

@client.command()
@commands.has_permissions(manage_messages=True)
async def reload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    client.load_extension(f"cogs.{extension}")

#deleting said amount of messages from a channel

@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, ammout):
    await ctx.channel.purge(limit=int(ammout))

@client.event
async def on_message(message):
    #my interactions with bot XD
    if "hi aribot" in str(message.content) and message.author.id == 384350694905217034:
        await message.channel.send("Hi creator! ❤️")
    if "bad aribot" in str(message.content) and message.author.id == 384350694905217034:
        await message.channel.send("I am so sorry, creator 😭")
    #those to may not work since they are links to image that were sent in discord which could be deleted.
    #Better would be to set them to images sent in private channels on your server instead.
    #Should to be addable by command <- to do
    if ":hipnotize:" in str(message.content):
        await message.channel.purge(limit=1)
        await message.channel.send("https://cdn.discordapp.com/attachments/798653357660045333/813708811721768970/ezgif.com-video-to-gif.gif ")
    if ":'merica:" in str(message.content):
        await message.channel.purge(limit=1)
        await message.channel.send("https://cdn.discordapp.com/attachments/809656965063507998/811570670332543016/llama_marica.gif ")
    await client.process_commands(message)

#mixins 
@client.command()
async def mixin(ctx):
    msg =  await ctx.send("https://github.com/SpongePowered/Mixin/wiki")
    await msg.delete()


for f in os.listdir(r"C:\Users\ariso\Desktop\Snake projects\aribot\cogs"):
    if f.endswith(".py"):
        client.load_extension(f"cogs.{f[:-3]}")


client.run('ODE0MTkwMjM1MzY5NDcyMDIw.YDaPvw.DkRADfHf9yPYXNXxJE9tD5r3AAA')
