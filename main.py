#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 15 21:33:02 2020

@author: Jonathan
This is the Mafia bot source code.
"""

import sys
# Needed to make sure the going up a level in the file manager works.
sys.path.append('../')
import discord
import random
import json


from discord.ext import commands
import os

import nest_asyncio
nest_asyncio.apply()


with open('../secret/bot_codes.json', 'r') as file:
    codes = json.load(file)

TOKEN = codes.get('token')


bot = commands.Bot(command_prefix = '/')

bot.daytime = True

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    for guild in bot.guilds:
        print(f'Mafia Bot is now connected to {guild.name}.')

@bot.command(help = "Loads extensions.")
async def load(ctx, extension):
    bot.load_extension(f"cogs.{extension}")
    print('{} has now been loaded.'.format(extension))
    
@bot.command(help = "Unloads extensions.")
async def unload(ctx, extension):
    bot.unload_extension(f"cogs.{extension}")
    print('{} has now been unloaded.'.format(extension))
    
@bot.command(help = "Unloads extensions.")
async def reload(ctx, extension):
    bot.unload_extension(f"cogs.{extension}")
    bot.load_extension(f"cogs.{extension}")
    print('{} has now been reloaded.'.format(extension))
    
@bot.command(name='status', help='Checks if bot is active')
async def check_status(ctx):
    await ctx.send("```Mafia Bot is active.```")


# This just goes through all the .py files in the cogs directory and loads them
# at the first start of this bot.
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        # Splice to cut off last 3 characters -> .py removed
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(TOKEN)

# Send data to DM
# user = bot.get_user(ctx.author.id)
# bot.dm_id = user
# await user.send('Initiative Starts!')