import selfcord
from selfcord.ext import commands, tasks
from pathlib import Path
import os
import subprocess
import asyncio
import requests
import base64

#intents = selfcord.Intents.default()
#intents.members = True
bot = commands.Bot(command_prefix=".", self_bot=True)
token = open(Path("token.txt"), "r").read() #reads the token.txt file

@bot.event
async def on_ready():
    print("Hello world!")
    print(bot.user)

@bot.command()
async def hello(ctx):
    await ctx.channel.send("hello!")

@bot.command(aliases=["debug"])
async def schizo(ctx, *, msg):
    print(msg)
    await ctx.channel.send(msg)

@bot.command()
async def pingall(ctx):
    messages = []
    current_message = ""
    print(ctx.guild.members)
    for index, member in enumerate(ctx.guild.members):
        formatted_ping = member.mention
        if len(current_message) < 1900:
            current_message += f"{formatted_ping} "
            if index == len(ctx.guild.members) - 1:
                messages.append(current_message)
        else:
            messages.append(current_message)
            current_message = ""
            already =  True
    for message in messages:
        await ctx.channel.send(message) 

@bot.command()
async def dmall(ctx, *, msg):
    for member in ctx.guild.members:
        member.send(msg)

@bot.command()
async def dm(ctx, *, username):
    mention_string = username.split()[0]
    user_id = int(mention_string[2:-1])
    user = await bot.fetch_user(user_id)
    if len(username.split()) > 1:
        message = username.split(" ", 1)[1]
        await user.send(message)

@bot.command()
async def clone(ctx, person): #can only be done twice an hour
    user_id = int(person[2:-1])
    user = await bot.fetch_user(user_id)
    avatar_url = user.avatar.url
    image = requests.get(avatar_url).content
    await bot.user.edit(avatar=image, username=user.name, password="Bat4Drill")

if __name__ == "__main__":   
    bot.run(token)