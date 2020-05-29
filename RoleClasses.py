#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 29 15:47:51 2020

@author: Jonathan

RoleClasses has some specific functions for each Role - it includes the checks
for selecting a target during each night phase, and can also store some specific
error text for each case.
"""

import discord

class DetectiveClass():
    def __init__(self, bot):
        self.bot = bot
        self.Investigations = {}
        self.colour = 0xA569BD
        self.ErrorText = {0: "No player identified! Type `/investigate x` to investigate a player, with x as the number next to the player's name. You can also investigate yourself, but that won't really do you any good!",
                          1: "You can only investigate one player per night. Re-enter the `/investigate` command!",
                          2: "That player does not exist! Pick a number on the list shown.",
                          3: "You have already investigated a player, and cannot perform another investigation!"}
        pass
    
    def ThrowError(self, code):
        # Unknown error should never show up, but if the code passed to the 
        # function is not held in ErrorText, it will default to this.
        ErrorDescription = self.ErrorText.get(code, "Unknown Error")
        embed = discord.Embed(title="Invalid selection",
                              description=ErrorDescription,
                              color=self.colour)
        return embed
    
    def TargetSelected(self, Detective, Target):
        embed = discord.Embed(title="Target chosen!",
                              description="{} is investigating {} tonight!".format(Detective, Target),
                              color=self.colour)
        return embed
    
    # This is the big one - makes sure that the selection is valid, and performs
    # the kill this way.
    async def CheckSelection(self, ctx, Target, TargetList):
        # First check to make sure the investigation has not yet been performed
        # by this particular detective
        if ctx.author.id in self.Investigations[ctx.guild.id]:
            await ctx.send( embed = self.ThrowError(3) )
            return False
        # First iteration here is the valid one, throws up an appropriate error
        # for any issue that's not within the right bit.
        elif len(Target) == 1:
            # Reassigns the target to an integer value, and the first instance
            # of the Target array.
            Target = int(Target[0])
            # Unlike with the werewolves, you must pick someone to save every
            # night.
            if (Target > len(TargetList)) | (Target == 0):
                await ctx.send( embed = self.ThrowError(2) )
                return False
            else:
                await ctx.send( embed = self.TargetSelected(ctx.author.mention, TargetList[Target - 1]) )
                # Add's the detective's ID to the Investigations list for this
                # game, meaning he cannot make another search.
                self.Investigations[ctx.guild.id].append(ctx.author.id)
                return True
        # Can only target ONE player -- any more than that is going to not work
        # well. Throws the error here. Less also doesn't work... Uses the else
        # statement to catch any other errors too.
        elif len(Target) > 1:
            await ctx.send( embed = self.ThrowError(1) )
            return False
        else:
            await ctx.send( embed = self.ThrowError(0) )
            return False
        
    async def SendInvestigationResults(self, ctx, TargetID):
        # Generating the private message that reveals the alignment of the target
        # player. First, get the Target's alignment and Name
        TargetAlignment = self.bot.game_list[ctx.guild.id]["active"][TargetID]["alignment"]
        TargetName = self.bot.game_list[ctx.guild.id]["active"][TargetID]["name"]
        embed = discord.Embed(title="Investigation complete!",
                              description="{} is a {}!".format(TargetName, TargetAlignment),
                              color=self.colour)
        self.bot.dm_id = ctx.author
        await ctx.author.send( embed = embed )
        # This is a check for the number of investigations matching the number
        # of detectives active in the game.
        if len(self.Investigations[ctx.guild.id]) == self.bot.game_list[ctx.guild.id]["player_numbers"]["detectives_live"]:
            return True
        else:
            return False

class MedicClass():
    def __init__(self, bot):
        self.bot = bot
        self.colour = 0xDC7633
        self.ErrorText = {0: "No player identified! Type `/save x` to save a player, with x as the number next to the player's name. You can also save yourself if you're not sure who to pick!",
                          1: "You can only save one player every night. Re-enter the `/save` command!",
                          2: "That player does not exist! Pick a number on the list shown."}
        pass
    
    def ThrowError(self, code):
        # Unknown error should never show up, but if the code passed to the 
        # function is not held in ErrorText, it will default to this.
        ErrorDescription = self.ErrorText.get(code, "Unknown Error")
        embed = discord.Embed(title="Invalid selection",
                              description=ErrorDescription,
                              color=self.colour)
        return embed
    
    def TargetSelected(self, Medic, Patient):
        embed = discord.Embed(title="Patient chosen!",
                              description="{} will protect {} from the wolves tonight!".format(Medic, Patient),
                              color=self.colour)
        return embed
    
    # This is the big one - makes sure that the selection is valid, and performs
    # the kill this way.
    async def CheckSelection(self, ctx, Patient, PatientList):
        # First iteration here is the valid one, throws up an appropriate error
        # for any issue that's not within the right bit.
        if len(Patient) == 1:
            # Reassigns the target to an integer value, and the first instance
            # of the Target array.
            Patient = int(Patient[0])
            # Unlike with the werewolves, you must pick someone to save every
            # night.
            if (Patient > len(PatientList)) | (Patient == 0):
                await ctx.send( embed = self.ThrowError(2) )
                return False
            else:
                await ctx.send( embed = self.TargetSelected(ctx.author.mention, PatientList[Patient - 1]) )
                return True
        # Can only target ONE player -- any more than that is going to not work
        # well. Throws the error here. Less also doesn't work... Uses the else
        # statement to catch any other errors too.
        elif len(Patient) > 1:
            await ctx.send( embed = self.ThrowError(1) )
            return False
        else:
            await ctx.send( embed = self.ThrowError(0) )
            return False



class WerewolfClass():
    def __init__(self, bot):
        self.bot = bot
        self.colour = 0xE74C3C
        self.ErrorText = {0: "No player identified! Type `/kill x` to target a player, with x as the number next to the player's name. Use `/kill 0` if you want to avoid killing anyone.",
                          1: "You can only target one player to be killed each night. Re-enter the `/kill` command!",
                          2: "That target does not exist! Pick a number on the list shown."}
        pass
    
    def ThrowError(self, code):
        # Unknown error should never show up, but if the code passed to the 
        # function is not held in ErrorText, it will default to this.
        ErrorDescription = self.ErrorText.get(code, "Unknown Error")
        embed = discord.Embed(title="Invalid selection",
                              description=ErrorDescription,
                              color=self.colour)
        return embed
    
    def TargetSelected(self, Wolf, Target):
        embed = discord.Embed(title="Target chosen!",
                              description="{} wants to attack {}!".format(Wolf, Target),
                              color=self.colour)
        return embed
    
    def NoKill(self, Wolf):
        embed = discord.Embed(title="No bloodshed tonight!",
                              description="{} has decided to stay in tonight and have a nice cup to tea, instead of causing death and destruction.".format(Wolf),
                              color=self.colour)
        return embed
    
    # This is the big one - makes sure that the selection is valid, and performs
    # the kill this way.
    async def CheckSelection(self, ctx, Target, TargetList):
        # First iteration here is the valid one, throws up an appropriate error
        # for any issue that's not within the right bit.
        if len(Target) == 1:
            # Reassigns the target to an integer value, and the first instance
            # of the Target array.
            Target = int(Target[0])
            if Target > len(TargetList):
                await ctx.send( embed = self.ThrowError(2) )
                return False
            else:
                if Target != 0:
                    await ctx.send( embed = self.TargetSelected(ctx.author.mention, TargetList[Target - 1]) )
                    return True
                else:
                    await ctx.send( embed = self.NoKill(ctx.author.mention) )
                    return True
        # Can only target ONE player -- any more than that is going to not work
        # well. Throws the error here. Less also doesn't work... Uses the else
        # statement to catch any other errors too.
        elif len(Target) > 1:
            await ctx.send( embed = self.ThrowError(1) )
            return False
        else:
            await ctx.send( embed = self.ThrowError(0) )
            return False
    