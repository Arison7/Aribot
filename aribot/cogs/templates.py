import discord
from discord.ext import commands
from itertools import cycle
import os
import json
import time
import string


def add_inmiddle(template, between, word):
    return template[:template.index(between[0])+1] + "\n\t" + word + template[template.index(between[0])+1:template.index(between[1])-1] + template[template.index(between[1])-1:]


class player:
    users = []

    def __init__(self, user, mod, ctx, c_channel):
        self.user = user
        self.c_channel = c_channel
        self.mod = mod
        self.users.append(self)
        self.anserws = []
        self.quastions = []
        self.item = 0
        with open(r"Pyprograms\aribot\cogs\templates\\{}".format(self.mod)+".txt") as f:
            for line in f:
                if line.startswith("!done!"):
                    break
                else:
                    self.quastions.append(line)

    def __call__(self):

        if self.item < len(self.quastions):
            ret = self.quastions[self.item]
            ret = ret.replace("$", "\n")
            self.item += 1
            return ret

        else:
            return "that's all"


class LuckofDash(Exception):
    pass


class coggs(commands.Cog):
    async def Is_it_done_yet(self, p):

        if len(p.anserws) == len(p.quastions):
            with open(r"Pyprograms\aribot\cogs\templates\\{}".format(p.mod)+".txt") as f:

                i = 0
                global template
                template = ""
                to_replace = ""
                to_exec = ""
                for line in f:
                    if line == "\n":
                        continue
                    if line.startswith("!R!"):
                        i = 2
                        to_exec = to_exec.format(
                            p.anserws, "add_inmiddle", "template")

                        exec(to_exec, globals())
                    elif i == 2:
                        to_replace = line.rstrip("\n").split(",")
                        for number, replacement in enumerate(to_replace):
                            template = template.replace(
                                str(replacement), p.anserws[number])
                        await p.c_channel.send("```\n" + template + "\n```")
                        p.users.remove(p)
                        del(p)
                    if line.startswith("!S!"):
                        i = 3
                    elif i == 3:
                        to_exec += line
                    if line.startswith("!done!"):
                        i = 1
                    elif i == 1:
                        template += line

    @commands.command()
    async def get_template(self, ctx, *, rest):
        await ctx.send("getting template")
        if rest.replace(" ", "") + ".txt" in os.listdir(r"Pyprograms\aribot\cogs\templates"):

            first = player(ctx.author, rest, ctx, ctx.channel)
            await ctx.send("your template is correct")
            await ctx.send("@"+str(ctx.author)+"\n"+first())
        else:
            await ctx.channel.send("I don't have such a template")

    @get_template.error
    async def get_template_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.channel.purge(limit=1)
            await ctx.send(f"{ctx.author}, you have to specify the template")
        else:
            print(error)

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            if message.content.startswith("aribot"):
                if not "-" in message.content and not "|" in message.content and not "+" in message.content:
                    raise LuckofDash
                elif not "-" in message.content and "|" in message.content and not "+" in message.content:
                    for p in player.users:
                        if p.user == message.author:
                            temp_dict = {}
                            for argumnet in message.content.replace(" ", "").split("|", 1)[1].split(","):
                                temp_dict.setdefault(argumnet.split(
                                    ":")[0], argumnet.split(":")[1])

                            for key in temp_dict.keys():
                                for l in key:
                                    if l not in string.ascii_lowercase + ["_"]:
                                        await message.channel.send(f"letter {l} isn't a valid character, please try again")
                                        break
                                for l in temp_dict[key]:
                                    if l not in string.ascii_lowercase + ["_"]:
                                        await message.channel.send(f"letter {l} isn't a valid character, please try again")
                                        break
                            else:

                                await p.c_channel.send("@"+str(message.author) + p())
                                p.anserws.append(temp_dict)

                            await self.Is_it_done_yet(p)
                elif not "-" in message.content and not "|" in message.content and "+" in message.content:
                    for p in player.users:
                        if p.user == message.author:
                            try:
                                float(message.content.replace(
                                    " ", "").split("+", 1)[1])
                                await p.c_channel.send("@"+str(message.author) + p())
                                p.anserws.append(message.content.replace(
                                    " ", "").split("+", 1)[1])
                            except ValueError:
                                await p.c_channel.send("@"+str(message.author) + "Your anserw must be a number")
                            await self.Is_it_done_yet(p)
                else:
                    for p in player.users:
                        if p.user == message.author:

                            for l in message.content.replace(" ", "").split("-", 1)[1].lower():
                                if l not in string.ascii_lowercase + ["_"]:
                                    await message.channel.send(f"letter {l} isn't a valid character, please try again")
                                    break
                            else:

                                await p.c_channel.send("@"+str(message.author) + p())
                                p.anserws.append(message.content.replace(
                                    " ", "").split("-", 1)[1].lower())

                            await self.Is_it_done_yet(p)

        except LuckofDash:
            await message.channel.send("You have to add \"- , | or +\" between aribot and your variable ")


def setup(client):
    client.add_cog(coggs(client))
