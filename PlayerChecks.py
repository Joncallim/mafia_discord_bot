#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 29 13:14:32 2020

@author: Jonathan

PlayerChecks() performs the if-else checks that would otherwise make for very 
long, weird-looking concave code, and streamlines it into a series of True/False
boolean returns. It will throw errors as needed, and there should be only one
True return in each function, even if there are multiple False returns. 

The class is used so that the bot can be passed through to all the functions 
without being repeated all over the place.
"""


import discord
from discord.ext import commands

class PlayerChecks():
    
    def __init__(self, bot):
        self.bot = bot
    
    # Basic checks for all players if they send a command in-game.
    async def IsValidPlayer(self, ctx):
        # Check 1: Making sure that the guild is actually in the game list.
        if ctx.guild.id not in self.bot.game_list:
            await ctx.send( embed = self.bot.ErrorText.NoGame(ctx.guild.name) )
            return False
        # Check 2: Making sure the game is not still in the preparation phase -
        # i.e. the first night has started.
        elif self.bot.game_list[ctx.guild.id]['turn'] == 0:
            await ctx.send(embed = self.bot.ErrorText.GenericError())
            return False
        # Check 3: Author is actually active within the current game.
        elif ctx.author.id not in self.bot.game_list[ctx.guild.id]['active'].keys():
            await ctx.send(embed = self.bot.ErrorText.NotJoined(ctx.author))
            return False
        # Check 4: Ensures author is actually alive in the current game.
        elif self.bot.game_list[ctx.guild.id]['active'][ctx.author.id]['status'] != 'alive':
            await ctx.send(embed = self.bot.ErrorText.PlayerDead(ctx.author))
            return False
        # If none of the errors thrown are False, then returns true and allows
        # the program to continue.
        else:
            return True
    
    # This checks that the properties for voting to lynch a player are all valid.
    # If any of them are not valid, it will throw the appropriate error message.
    async def IsValidVote(self, ctx, Nomination):
        # Check 1: Must be Daytime.
        if not self.bot.game_list[ctx.guild.id]["day"]:
            await ctx.send(embed = self.bot.ErrorText.GenericError())
            return False
        # Check 2: Must have a valid Nomination. These only go through if the
        # earlier check passes, 
        else:
            if len(Nomination) == 1:
                return True
            elif len(Nomination) > 1:
                await ctx.send(embed = self.bot.ErrorText.TooManyNominations())
                return False
            else:
                await ctx.send(embed = self.bot.ErrorText.NoNomination())
                return False
    
    # Checks that the werewolf message author is valid to be sending the message.
    async def IsValidWerewolf(self, ctx):
        # Check 1: Makes sure that the command is being sent in the correct channel
        if ctx.channel.id != self.bot.game_list[ctx.guild.id]["channel_ids"]["werewolf"]:
            await ctx.send(embed = self.bot.ErrorText.WrongChannel())
            return False
        # Check 2: Making sure it's the right time-of-day (Only Night phases 
        # are allowed for Werewolf kills)
        elif self.bot.game_list[ctx.guild.id]["day"]:
            await ctx.send(embed = self.bot.ErrorText.GenericError())
            return False
        # Check 3: Making sure the player who has proposed is actually a werewolf
        elif self.bot.game_list[ctx.guild.id]['active'][ctx.author.id]['role'] != 'Werewolf':
            await ctx.send(embed = self.bot.ErrorText.PlayerInWrongChannel(ctx.author))
            return False
        # Now if the player passes all checks, allows the program to continue.
        else:
            return True
    
    # Checks that the medic message author is valid to be sending the message.
    # Almost identical to werewolves.
    async def IsValidMedic(self, ctx):
        # Check 1: Correct channel
        if ctx.channel.id != self.bot.game_list[ctx.guild.id]["channel_ids"]["medic"]:
            await ctx.send(embed = self.bot.ErrorText.WrongChannel())
            return False
        # Check 2: Making sure it's the right time-of-day (Only Night phases 
        # are allowed for Werewolf kills)
        elif self.bot.game_list[ctx.guild.id]["day"]:
            await ctx.send(embed = self.bot.ErrorText.GenericError())
            return False
        # Check 3: Making sure the player who has proposed is actually a werewolf
        elif self.bot.game_list[ctx.guild.id]['active'][ctx.author.id]['role'] != 'Medic':
            await ctx.send(embed = self.bot.ErrorText.PlayerInWrongChannel(ctx.author))
            return False
        # Now if the player passes all checks, allows the program to continue.
        else:
            return True
        
    # Checks that the medic message author is valid to be sending the message.
    # Almost identical to werewolves.
    async def IsValidDetective(self, ctx):
        # Check 1: Correct channel
        if ctx.channel.id != self.bot.game_list[ctx.guild.id]["channel_ids"]["detective"]:
            await ctx.send(embed = self.bot.ErrorText.WrongChannel())
            return False
        # Check 2: Making sure it's the right time-of-day (Only Night phases 
        # are allowed for Werewolf kills)
        elif self.bot.game_list[ctx.guild.id]["day"]:
            await ctx.send(embed = self.bot.ErrorText.GenericError())
            return False
        # Check 3: Making sure the player who has proposed is actually a werewolf
        elif self.bot.game_list[ctx.guild.id]['active'][ctx.author.id]['role'] != 'Detective':
            await ctx.send(embed = self.bot.ErrorText.PlayerInWrongChannel(ctx.author))
            return False
        # Now if the player passes all checks, allows the program to continue.
        else:
            return True
    
    async def ReadyToStartGame(self, ctx):
        # first, check that game is ready, and this is the right channel.
        if ctx.guild.id not in self.bot.game_list.keys():
            await ctx.send(embed = self.ErrorText.GameNotStarted(ctx.guild.name))
            return False
        elif ctx.author.id not in self.bot.game_list[ctx.guild.id]['active'].keys():
            await ctx.send(embed = self.ErrorText.NotJoined(ctx.author))
            return False
        else:
            return True
            