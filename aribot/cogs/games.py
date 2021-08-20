
import discord
from discord.ext import commands 
import random
import time



class coggs(commands.Cog):
    def __init__(self, client ):
        self.client = client
        self.hiding_spots = {}
    @commands.command()
    async def hide(self,ctx):
        await ctx.message.delete(delay = 5)
        good_channels = []
        for channel in ctx.guild.channels:
            if ctx.author.permissions_in(channel) and str(channel.type) == "text":
                good_channels.append(channel)
        self.hiding_spots[ctx.author.id] = [random.choice(good_channels),len(ctx.guild.channels) //4]
        message = await ctx.send(f"find me using '.ari find' on a channel you think i am hiding in! you have {self.hiding_spots[ctx.author.id][1]} guesses" )
        
        await message.delete(delay= 5)
    @commands.command()
    async def find(self,ctx):
        await ctx.message.delete(delay = 5)
        if ctx.author.id in self.hiding_spots.keys():
            if self.hiding_spots[ctx.author.id][1] > 0 and self.hiding_spots[ctx.author.id][0] == ctx.channel:
                msg = await ctx.send(":partying_face: YOU FOUND ME!!! :partying_face: ")
                self.hiding_spots.pop(ctx.author.id,None)
                
                await msg.delete(delay= 5)
            else:
                self.hiding_spots[ctx.author.id][1] -= 1
                message = await ctx.send(f"nope {self.hiding_spots[ctx.author.id][1]} guess left")

                await message.delete(delay = 4)
                if self.hiding_spots[ctx.author.id][1] == 0:
                    
                    channel = discord.utils.get(ctx.guild.channels, name =  str(self.hiding_spots[ctx.author.id][0]))
                    channel_id = channel.id
                    channel = await self.client.fetch_channel(channel_id)
                    
                    m = await channel.send("I was here! " + ctx.author.mention + ":stuck_out_tongue_closed_eyes:")
                    self.hiding_spots.pop(ctx.author.id,None)
                    
                    await m.delete(delay= 15)
        else:
            msg = await ctx.send("You are not curretly seeking Shhhh!")
            msg.delete(delay = 5)
            
            
    



def setup(client):
    client.add_cog(coggs(client))