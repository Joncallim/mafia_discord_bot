#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 16 13:57:23 2020

@author: Jonathan
"""

import discord
from discord.ext import commands
import random
import collections.abc

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
        
    # Assigns the number of roles for villagers: Will add roles as this grows.
    def assign_roles(self, player_list):
        # Total number of active players in the game.
        num_players = len(player_list)
        # It is recommended by Andrew Plotkin that there are exactly 2 mafioso
        # (or werewolves), but in the original Davidoff rules there are 1/3 the
        # number of players. This bot respects the old rules.
        if num_players > 7:
            num_werewolves = round(num_players / 3)
            num_villagers = num_players - num_werewolves
        elif num_players > 4:
            num_werewolves = 2
            num_villagers = num_players - num_werewolves
        # For games of <4 players, there will be 1 werewolf. Probably not a great
        # games, but I assume someone is going to try to break this.
        else:
             num_werewolves = 1
             num_villagers = num_players - num_werewolves
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
                    await react.message.edit(content = '```Click \u2705 to join the game, or \u274e to cancel.\n\nPlayers: {}```'.format(numPlayers))
                    pass
    
    @commands.command(help = "[/werewolf] initialises a game, and brings up a message that lets players opt into the game.")
    async def werewolf(self, ctx):
        message = await ctx.send('```Click \u2705 to join the game, or \u274e to cancel.\n\nPlayers: 0```')
        message_info = {message.guild.id: {"message": message.id}}
        self.host_message.update(message_info)
        self.initial_player_list.update({ctx.guild.id: {}})
        await message.add_reaction('\u2705')
        await message.add_reaction('\u274e')

    @commands.command(help = "[/ready] starts a game once all players who are participating in the game are ready to play.")
    async def ready(self, ctx):
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
            await ctx.send("```You haven't started the Werewolf bot! Type '/werewolf' to get started!```")
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
            werewolf_channel = await ctx.guild.create_text_channel("werewolves")
            i = 0
            playerString = ""
            roles = self.assign_roles(active_player_list)

            # Iterates through all the players in the active player list, and 
            # applies a specific set of operations to each of them.
            for playerID, player in active_player_list.items():
                # Gets the user using the player id. I really should have used
                # this to get the display name all along, but I've now written
                # the code to store the display name too.
                user = ctx.guild.get_member(playerID)
                self.bot.dm_id = user
                await user.send('```Your role for the game in {} is "{}!"```'.format(ctx.guild.name, roles[i]))
                # Sets permissions for the particular user in specific channels.
                # If you're not meant to be in a particular channel, you can't
                # see it. Unfortunately you can't take permissions away from a
                # channel owner, so this needs a better workaround in a bit.
                if roles[i] == 'Werewolf':
                    overwrite = discord.PermissionOverwrite()
                    overwrite.send_messages = True
                    overwrite.read_messages = True
                    overwrite.read_message_history = True
                    await werewolf_channel.set_permissions(user, 
                                                           overwrite = overwrite)
                else:
                    overwrite = discord.PermissionOverwrite()
                    overwrite.send_messages = False
                    overwrite.read_messages = False
                    overwrite.read_message_history = False
                    await werewolf_channel.set_permissions(user, 
                                                           overwrite = overwrite)
                # Updates the role for active players so their roles in the dict
                # now reflects their in-game roles. Starts up the players as all
                # alive, and starts a turn counter for each player.
                player.update({'role': roles[i], 
                               'status': 'alive',
                               'turns': 0 })
                # creates a long string with all the players in the game, listed
                # from 1 to whatever.
                playerString = "{}{}. {}\n".format(playerString, i+1, player['name'])
                i = i + 1
            # Updates the game's storage so it holds values for the various 
            # channels and players.
            self.bot.game_list.update({ctx.guild.id: {"active": active_player_list, 
                                                      "observer": observer_list,
                                                      "player_numbers": {"alive": len(active_player_list),
                                                                         "dead": 0,
                                                                         "werewolves_total": roles.count('Werewolf'),
                                                                         "werewolves_live": roles.count('Werewolf'),
                                                                         "villagers_total": roles.count('Villager'),
                                                                         "villagers_live": roles.count('Villager'),
                                                                         "total": len(active_player_list)},
                                                      "day": True,
                                                      "playing": True,
                                                      "turn": 0,
                                                      "channel_ids": {"general": ctx.channel.id,
                                                                      "werewolf": werewolf_channel.id} }})
            print('Game started in server: {}'.format(ctx.guild.id))
            await ctx.send('```Game Starting with {} Players and {} Observers!\nPlayers:\n{}\nThere are {} Werewolves and {} Villagers!\nCheck your DMs for your roles, then type [/start] to begin the first night!```'.format(len(roles), len(observer_list), playerString, roles.count('Werewolf'), roles.count('Villager')))

    @commands.command(help = "[/end] terminates the session, and clears the current game from memory. Use this if you're experiencing and issues and would like to clear the game from memory completely.")
    async def end(self, ctx):
        if ctx.guild.id in self.bot.game_list.keys():
            # For the different channel IDs that were created by the bot, goes
            # through them one at a time and deletes all of them.
            for key, channelID in self.bot.game_list[ctx.guild.id]['channel_ids'].items():
                channel = ctx.guild.get_channel(channelID)
                # Simple check to ensure that the channel exists.
                if channel:
                    # Deletes all channels except for the general channel.
                    if key != 'general':
                        try:
                            await channel.delete()
                        except discord.Forbidden:
                            print('Could not delete {} channel from server: {}'.format(key, ctx.guild.id))
                else:
                    print("{} channel does not exist in server: {}".format(key, ctx.guild.id))
                # Clears the memory of the rest of the dict holding the storage 
                # for the particular server.
            channel = ctx.guild.get_channel(self.bot.game_list[ctx.guild.id]['channel_ids']['general'])
            await channel.send('```Memory cleared of this game```')
            # As the last thing done, clears the memory of this game.
            self.bot.game_list.pop(ctx.guild.id)
            print('Game terminated in server: {}'.format(ctx.guild.id))
        else:
            print("No Storage Found")
        
def setup(bot):
    bot.add_cog(startup(bot))