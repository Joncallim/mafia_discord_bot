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
import json


from discord.ext import commands
import os

import nest_asyncio
nest_asyncio.apply()


with open('../werewolf_secret/bot_codes.json', 'r') as file:
    codes = json.load(file)

TOKEN = codes.get('token')


bot = commands.Bot(command_prefix = '/')

bot.host_message_check = {}
bot.game_list = {}

# bot.test_player_list = {111: {'role': 'not_playing', 'name': 'test_player_1'}, 
#                         222: {'role': 'not_playing', 'name': 'test_player_2'}, 
#                         333: {'role': 'not_playing', 'name': 'test_player_3'}, 
#                         123: {'role': 'player', 'name': 'test_player_4'}, 
#                         234: {'role': 'player', 'name': 'test_player_5'}, 
#                         456: {'role': 'player', 'name': 'test_player_6'}, 
#                         786: {'role': 'player', 'name': 'test_player_7'}, 
#                         112: {'role': 'player', 'name': 'test_player_8'}, 
#                         874: {'role': 'player', 'name': 'test_player_9'}, 
#                         987: {'role': 'player', 'name': 'test_player_10'}, 
#                         445: {'role': 'player', 'name': 'test_player_11'}, 
#                         213: {'role': 'player', 'name': 'test_player_12'}, 
#                         334: {'role': 'player', 'name': 'test_player_13'}}

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    for guild in bot.guilds:
        print(f'Werewolf Bot is now connected to {guild.name}.')

# Clears stuff out from memory - cleans every file in the server. Will add a
# check to make sure only I can do this in a bit.
@bot.command(help = "Scrubs memory.")
@commands.is_owner()
async def scrub(ctx):
    bot.daytime = True
    bot.host_message_check = {}
    bot.player_list = {}
    print('Storage has been cleared')

@bot.command(help = "Loads extensions.")
@commands.is_owner()
async def load(ctx, extension):
    bot.load_extension(f"cogs.{extension}")
    print('{} has now been loaded.'.format(extension))
    
@bot.command(help = "Unloads extensions.")
@commands.is_owner()
async def unload(ctx, extension):
    bot.unload_extension(f"cogs.{extension}")
    print('{} has now been unloaded.'.format(extension))
    
@bot.command(help = "Reloads all extensions.")
@commands.is_owner()
async def reload(ctx, extension):
    bot.unload_extension(f"cogs.{extension}")
    bot.load_extension(f"cogs.{extension}")
    print('{} has now been reloaded.'.format(extension))

@bot.command(name='status', help='Checks if bot is active')
async def check_status(ctx):
    await ctx.send("```Werewolf Bot is active.```")
    
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.NotOwner):
        await ctx.send('```You do not have permission to execute that command, {}.```'.format(ctx.author.display_name))
        print(ctx.author.id, " attempted to execute an illegal command.")


# This just goes through all the .py files in the cogs directory and loads them
# at the first start of this bot.
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        # Splice to cut off last 3 characters -> .py removed
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(TOKEN)