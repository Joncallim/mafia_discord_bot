#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 18:32:12 2020

@author: Jonathan
"""


import discord

class WerewolfPermissions():
    
    def __init__(self, bot):
        self.bot = bot
        
        self.NoText = discord.PermissionOverwrite()
        self.NoText.send_messages = False
        self.NoText.read_messages = False
        self.NoText.read_message_history = False
        
        self.AllText = discord.PermissionOverwrite()
        self.AllText.send_messages = True
        self.AllText.read_messages = True
        self.AllText.read_message_history = True
        
        self.ReadOnly = discord.PermissionOverwrite()
        self.ReadOnly.send_messages = False
        self.ReadOnly.read_messages = True
        self.ReadOnly.read_message_history = True
        
        self.Speak = discord.PermissionOverwrite()
        self.Speak.speak = True
        self.Speak.connect = True
        
        self.ListenOnly = discord.PermissionOverwrite()
        self.ListenOnly.speak = False
        self.ListenOnly.connect = True
        
    async def NewTextChannel(self, ctx, ChannelName, Public = False):
        channel = await ctx.guild.create_text_channel(ChannelName)
        # for member in ctx.guild.members:
            # if not member.bot:
        if Public:
            try:
                await channel.set_permissions(ctx.guild.default_role, overwrite = self.ReadOnly)
            except discord.Forbidden as Error:
                print("Failed to set permissions in {} due to {}".format(ctx.guild.name, Error))
        else:
            try:
                await channel.set_permissions(ctx.guild.default_role, overwrite = self.NoText)
            except discord.Forbidden as Error:
                print("Failed to set permissions in {} due to {}".format(ctx.guild.name, Error))
        return channel
    
    async def NewVoiceChannel(self, ctx, ChannelName):
        channel = await ctx.guild.create_voice_channel(ChannelName)
        try:
            await channel.set_permissions(ctx.guild.default_role, overwrite = self.ListenOnly)
        except discord.Forbidden as Error:
            print("Failed to set permissions in {} due to {}".format(ctx.guild.name, Error))
        return channel
    
    def GetPermission(self, PermissionName):
        if PermissionName == "textOK":
            return self.AllText
        elif PermissionName == "speak":
            return self.Speak
        
    async def Kill(self, GuildID, PlayerID):
        guild = self.bot.get_guild(GuildID)
        User = guild.get_member(PlayerID)
        general_text_channel = guild.get_channel(self.bot.game_list[GuildID]["channel_ids"]["general"])
        general_voice_channel = guild.get_channel(self.bot.game_list[GuildID]["channel_ids"]["general-voice"])
        werewolf_channel = guild.get_channel(self.bot.game_list[GuildID]["channel_ids"]["werewolf"])
        medic_channel = guild.get_channel(self.bot.game_list[GuildID]["channel_ids"]["medic"])
        detective_channel = guild.get_channel(self.bot.game_list[GuildID]["channel_ids"]["detective"])
        DeathMessage = discord.Embed(title="You Have Died...",
                                     description="You have been killed, and you can no longer communicate with the living in the Village-Ville Text and Voice channels...",
                                     color = 0xFF0000)
        try:
            await User.send(embed=DeathMessage)
            await werewolf_channel.set_permissions(User, overwrite = self.ReadOnly)
            await medic_channel.set_permissions(User, overwrite = self.ReadOnly)
            await detective_channel.set_permissions(User, overwrite = self.ReadOnly)
            await general_text_channel.set_permissions(User, overwrite = self.ReadOnly)
            await general_voice_channel.set_permissions(User, overwrite = self.ListenOnly)
        except discord.Forbidden as Error:
            print("Failed to set permissions in {} due to {}".format(guild.name, Error))
        return
        
        
        