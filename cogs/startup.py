#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 16 13:57:23 2020

@author: Jonathan
"""

import discord
from discord.ext import commands, tasks
import random
import collections.abc
import math

# Dictionary updating for nested dicts. Goes recursively through the list to get
# the appropriate key and update each dict.
# Source: https://stackoverflow.com/questions/3232943/update-value-of-a-nested-dictionary-of-varying-depth
def update(d = {}, u = {}):
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = update(d.get(k, {}), v)
        else:
            d[k] = v
    return d

class startup(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.initial_player_list = {}
        self.host_message = {}
        self.terminate_idle_game.start()
        self.NoPermission = discord.PermissionOverwrite()
        self.NoPermission.send_messages = False
        self.NoPermission.read_messages = False

    # Checks if a game has been idle for too long (24 hours) and kills it if
    # so.
    @tasks.loop(seconds = 86400.0)
    async def terminate_idle_game(self):
        print('Checking for idle games...')
        if self.bot.game_list == {}:
            pass
        else:
            for guild_id, game in self.bot.game_list.items():
                if game['idle'] == False:
                    self.bot.game_list[guild_id]['idle'] = True
                elif game['idle'] == True:
                    guild = self.bot.get_guild(guild_id)
                    for key, channelID in self.bot.game_list[guild_id]['channel_ids'].items():
                        channel = guild.get_channel(channelID)
                        # Simple check to ensure that the channel exists.
                        if channel:
                            # Deletes all channels except for the general channel.
                            if key != 'general':
                                try:
                                    await channel.delete()
                                except discord.Forbidden:
                                    print('Idle Terminator: Could not delete {} channel from server: {}'.format(key, guild.id))
                        else:
                            print("Idle Terminator: {} channel does not exist in server: {}".format(key, guild.id))
                        # Clears the memory of the rest of the dict holding the storage 
                        # for the particular server.
                    channel = guild.get_channel(self.bot.game_list[guild.id]['channel_ids']['general'])
                    embed = discord.Embed(title="Game deleted from server!",
                                          description="The game in this server has been idle for too long, and has been cleared from the system's memory.",
                                          color=self.bot.colours['admin'])
                    await channel.send(embed = embed)
                    # As the last thing done, clears the memory of this game.
                    self.bot.game_list.pop(guild.id)
                    print('Idle Terminator: Game terminated in server: {}, id: {}'.format(guild.name, guild.id))
        
    # Assigns the number of roles for villagers: Will add roles as this grows.
    def assign_roles(self, player_list):
        # Total number of active players in the game.
        num_players = len(player_list)
        # It is recommended by Andrew Plotkin that there are exactly 2 mafioso
        # (or werewolves), but in the original Davidoff rules there are 1/3 the
        # number of players. This bot respects the old rules.
        num_werewolves = round(num_players / 3)
        # i.e. For 10 players there will be 2 medics, 2 detectives, and 3
        # werewolves, meaning 7/10 will have roles. Otherwise, 5/9 will 
        # have roles. 
        num_medic = math.floor(num_players/5)
        num_detective = math.floor(num_players/5)
        if num_detective == 0:
            num_detective = 1
        num_villagers = num_players - (num_werewolves + num_medic + num_detective)
        # This is an array to store all the roles. They're appended on to the 
        # array so that they can be passed through and used. I would have used
        # integers, but this is just more readable and makes for easier maintenance
        # later on...
        roles = []
        # Appends the role onto the end of the list...
        for i in range(num_werewolves):
            roles.append('Werewolf')
        for i in range(num_villagers):
            roles.append('Villager')
        for i in range(num_medic):
            roles.append('Medic')
        for i in range(num_detective):
            roles.append('Detective')
        # random.shuffle shuffles the original list, as is done here, since it
        # has a go at the data being pointed at.
        random.shuffle(roles)
        return roles
    
    @commands.Cog.listener()
    async def on_reaction_add(self, react: discord.Reaction, person: discord.User):
        # This should check that the react is for the correct server AND the
        # correct message, since the discord.message type has all the right
        # values stored in it.
        if not person.bot:
            # Iterates through each of the dicts in the host_message_check dict,
            # stops quickly on the one that matches the right message in the 
            # right server. Basically stops a reaction to any old message from
            # bringing the rest of the function up.
            for key, message in self.host_message.items():
                # This section is only called if both the message and server
                # match the appropriate message. (So, should work across multiple
                # servers.)
                if (react.message.guild.id == key) & (react.message.id == message['message']):
                    # Removes the original author's vote - basically prevents
                    # double-votes, and is just fairly useful to keep the visuals
                    # streamlined
                    await react.remove(person)
                    # Checkbox Tick emoji - sets the player as "player"
                    if react.emoji == '\u2705':
                        self.initial_player_list[react.message.guild.id].update({person.id: {"role": "player", 
                                                                                             "name": person.display_name}})                        
                    elif react.emoji == '\u274e':
                        self.initial_player_list[react.message.guild.id].update({person.id: {"role": "not_playing", 
                                                                                             "name": person.display_name}})
                    numPlayers = sum(value['role'] == "player" for value in self.initial_player_list[react.message.guild.id].values())
                    await react.message.edit(embed = self.bot.AdminText.StartUp(react.message.guild.name, numPlayers))
                    pass
    
    @commands.command(help = "[/werewolf] initialises a game, and brings up a message that lets players opt into the game.")
    async def werewolf(self, ctx):
        message = await ctx.send(embed = self.bot.AdminText.StartUp(ctx.guild.name, 0))
        message_info = {message.guild.id: {"message": message.id}}
        self.host_message.update(message_info)
        self.initial_player_list.update({ctx.guild.id: {}})
        await message.add_reaction('\u2705')
        await message.add_reaction('\u274e')
        
        
    async def new_channelText(self, ctx, channel_name):
        channel = await ctx.guild.create_text_channel(channel_name)
        # overwrite = discord.PermissionOverwrite()
        # overwrite.send_messages = False
        # overwrite.read_messages = False
        # # overwrite = Permissions()
        # # overwrite.none()
        print(self.NoPermission)
        for member in ctx.guild.members:
            if not member.bot:
                print(member)
                await channel.set_permissions(member, overwrite = self.NoPermission)#send_messages = False, read_messages = False, read_message_history = False)
        return channel

    @commands.command(help = "[/ready] starts a game once all players who are participating in the game are ready to play.")
    async def ready(self, ctx):
        InitialEmbed = discord.Embed(title="Game Starting Up!",
                                     description="Please wait while I allocate resources.",
                                     color = 0xFF0000)
        await ctx.send(embed = InitialEmbed)
        # Removes the entry for this server from the storage dictionary - the
        # start message won't be needed any more. Sets a default value in case
        # there is no item.
        self.host_message.pop(ctx.guild.id, None)
        # Gets the dictionary for the current server (by ctx.guild.id), and 
        # removes it from the original storage list, so it doesn't store it 
        # forever.
        all_player_list = self.initial_player_list.pop(ctx.guild.id, None)
        # Quick check to see if a dict has actually been popped, or if no dict
        # exists in the database.
        if all_player_list == None:
            await ctx.send(embed = self.bot.ErrorText.NoGame(ctx.guild.name))
            pass
        else:
            active_player_list = {}
            observer_list = {}
            for playerID, player in all_player_list.items():
                # Any player with the role of "player" is added to this dict
                # for the "players. Anyone not playing... Gets added to the 
                # other list.
                if player["role"] == "player":
                    active_player_list.update({playerID: player})
                else:
                    observer_list.update({playerID: player})
            # Creates a channel for the werewolves to chat in - this channel 
            # will be set so only werewolves can see inside it.
            # werewolf_channel = await ctx.guild.create_text_channel("werewolves")
            werewolf_channel = await self.bot.WWChannels.NewTextChannel(ctx, "werewolves")
            medic_channel = await self.bot.WWChannels.NewTextChannel(ctx, "medics")
            detective_channel = await self.bot.WWChannels.NewTextChannel(ctx, "detectives")
            general_text = await self.bot.WWChannels.NewTextChannel(ctx, "village-ville", Public = True)
            general_voice = await self.bot.WWChannels.NewVoiceChannel(ctx, "village-ville")
            i = 0
            playerString = ""
            roles = self.assign_roles(active_player_list)
            for playerID, player in active_player_list.items():
                # Gets the user using the player id. I really should have used
                # this to get the display name all along, but I've now written
                # the code to store the display name too.
                user = ctx.guild.get_member(playerID)
                self.bot.dm_id = user
                # Sets permissions for the particular user in specific channels.
                # If you're not meant to be in a particular channel, you can't
                # see it. Unfortunately you can't take permissions away from a
                # channel owner, so this needs a better workaround in a bit.
                try:
                    await general_text.set_permissions(user, overwrite = self.bot.WWChannels.GetPermission("textOK") )
                    await general_voice.set_permissions(user, overwrite = self.bot.WWChannels.GetPermission("speak") )
                except discord.Forbidden as Error:
                    print("Failed to set permissions in {} due to {}".format(ctx.guild.name, Error))
                if roles[i] == 'Werewolf':
                    await werewolf_channel.set_permissions(user, overwrite = self.bot.WWChannels.GetPermission("textOK") )
                    alignment = 'Werewolf'
                elif roles[i] == 'Medic':
                    await medic_channel.set_permissions(user, overwrite = self.bot.WWChannels.GetPermission("textOK") )
                    alignment = 'Human'
                elif roles[i] == 'Detective':
                    await detective_channel.set_permissions(user, overwrite = self.bot.WWChannels.GetPermission("textOK") )
                    alignment = 'Human'
                else:
                    alignment = 'Human'
                # Updates the role for active players so their roles in the dict
                # now reflects their in-game roles. Starts up the players as all
                # alive, and starts a turn counter for each player.
                player.update({'role': roles[i], 
                               'status': 'alive',
                               'turns': 0,
                               'alignment': alignment})
                # Sends a formatted message to the player, specifying their role
                # and alignment in the game.
                await user.send(embed = self.bot.AdminText.PlayerPersonalInfo(ctx.guild.name, roles[i], alignment))
                # creates a long string with all the players in the game, listed
                # from 1 to whatever.
                playerString = "{}{}. {}\n".format(playerString, i+1, player['name'])
                i = i + 1
            # Updates the game's storage so it holds values for the various 
            # channels and players. Manually creating this list, so every 
            # variable can be seen clearly -- Mods will be made to different 
            # roles as this goes along, so it's fairly important...
            self.bot.game_list.update({ctx.guild.id: {"active": active_player_list, 
                                                      "observer": observer_list,
                                                      "player_numbers": {"alive": len(active_player_list),
                                                                         "dead": 0,
                                                                         "werewolves_total": roles.count('Werewolf'),
                                                                         "werewolves_live": roles.count('Werewolf'),
                                                                         "villagers_total": roles.count('Villager'),
                                                                         "villagers_live": roles.count('Villager'),
                                                                         "medics_total": roles.count('Medic'),
                                                                         "medics_live": roles.count('Medic'),
                                                                         "detectives_total": roles.count('Detective'),
                                                                         "detectives_live": roles.count('Detective'),
                                                                         "humans_live": (roles.count('Detective') + roles.count('Medic') + roles.count('Villager')),
                                                                         "total": len(active_player_list),},
                                                      "turn_complete": {"werewolves": False,
                                                                        "medics": False,
                                                                        "detectives": False },
                                                      "idle": False,
                                                      "day": True,
                                                      "playing": True,
                                                      "turn": 0,
                                                      "channel_ids": {"admin": ctx.channel.id,
                                                                      "general": general_text.id,
                                                                      "general-voice": general_voice.id,
                                                                      "werewolf": werewolf_channel.id,
                                                                      "medic": medic_channel.id,
                                                                      "detective": detective_channel.id} }})
            print('Game started in server: {}, id: {}'.format(ctx.guild.name, ctx.guild.id))
            TextInvite = await general_text.create_invite()
            TextInviteEmbed = discord.Embed(name="Join the Village-Ville Text Channel!",
                                            description="Click on the 'Joined' button to go straight to the text channel, where the rest of the game will be played.",
                                            color=0xFF0000)
            VoiceInvite = await general_voice.create_invite()
            VoiceInviteEmbed = discord.Embed(name="Join the Village-Ville Voice Chat!",
                                             description="Click on the 'Join Voice' button to go straight to the voice channel.",
                                             color=0xFF0000)
            try:
                await ctx.send(VoiceInvite, embed = VoiceInviteEmbed)
                await ctx.send(TextInvite, embed = TextInviteEmbed)
                await general_text.send(embed = self.bot.AdminText.GameStarting(ctx.guild.name, roles, playerString))
            except discord.Forbidden as Error:
                print("Could not send startup message in {} due to {}".format(ctx.guild.name, Error))

    @commands.command(help = "[/end] terminates the session, and clears the current game from memory. Use this if you're experiencing and issues and would like to clear the game from memory completely.")
    async def end(self, ctx):
        if await self.bot.PlayerChecks.IsValidPlayer(ctx):
            # For the different channel IDs that were created by the bot, goes
            # through them one at a time and deletes all of them.
            for key, channelID in self.bot.game_list[ctx.guild.id]['channel_ids'].items():
                channel = ctx.guild.get_channel(channelID)
                # Simple check to ensure that the channel exists.
                if channel:
                    # Deletes all channels except for the general channel.
                    if key != 'admin':
                        try:
                            await channel.delete()
                        except discord.Forbidden:
                            print('Could not delete {} channel from server: {}'.format(key, ctx.guild.id))
                else:
                    print("{} channel does not exist in server: {}".format(key, ctx.guild.id))
                # Clears the memory of the rest of the dict holding the storage 
                # for the particular server.
            channel = ctx.guild.get_channel(self.bot.game_list[ctx.guild.id]['channel_ids']['admin'])
            await channel.send(embed = self.bot.AdminText.GameDeleted(ctx.guild.name))
            # As the last thing done, clears the memory of this game.
            self.bot.game_list.pop(ctx.guild.id)
            if ctx.guild.id in self.bot.DetectiveClass.Investigations:
                self.bot.DetectiveClass.Investigations.pop(ctx.guild.id)
            print('Game terminated in server: {}, id: {}'.format(ctx.guild.name, ctx.guild.id))

        
def setup(bot):
    bot.add_cog(startup(bot))