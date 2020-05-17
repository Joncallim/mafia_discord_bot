#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 17 12:51:55 2020

@author: Jonathan
"""

import discord
from discord.ext import commands
import numpy as np

class turns(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.kill_message = {}
        self.target_list = {}
        
        
    async def game_end(self, guild_id, werewolf_victory = True):
        if werewolf_victory:
            firstString = "Werewolves win!"
        else:
            firstString = "Villagers win!"
        initStatString = "Number of Turns: {}\n\nPlayers Remaining: {}\n - Werewolves: {}\n - Villagers: {}\n\nTotal Players: {}\n - Werewolves: {}\n - Villagers: {}".format(self.bot.game_list[guild_id]["turn"],
                                                                                                                                                                              self.bot.game_list[guild_id]["player_numbers"]["alive"],
                                                                                                                                                                              self.bot.game_list[guild_id]["player_numbers"]["werewolves_live"],
                                                                                                                                                                              self.bot.game_list[guild_id]["player_numbers"]["villagers_live"],
                                                                                                                                                                              self.bot.game_list[guild_id]["player_numbers"]["total"],
                                                                                                                                                                              self.bot.game_list[guild_id]["player_numbers"]["werewolves_total"],
                                                                                                                                                                              self.bot.game_list[guild_id]["player_numbers"]["villagers_total"])
        liveString = ""
        deadString = ""
        for player in self.bot.game_list[guild_id]['active'].values():
            if player['status'] == "alive":
                liveString = "{} - {} ({})\n".format(liveString,
                                                                player['name'],
                                                                player['role'])
            else:
                deadString = "{} - {} ({}), Turns: {}\n".format(deadString,
                                                                player['name'],
                                                                player['role'],
                                                                player['turns'])
        playerListString = "Live Players:\n{}\n Dead Players:\n{}".format(liveString, deadString)
        outputString = "```{}\n{}\n\n{}\n\nThanks for Playing!```".format(firstString, initStatString, playerListString)
        guild = self.bot.get_guild(guild_id)
        general_channel = guild.get_channel(self.bot.game_list[guild_id]["channel_ids"]["general"])
        await general_channel.send(outputString)
        # Now purging the game from memory.
        for key, channelID in self.bot.game_list[guild_id]['channel_ids'].items():
            channel = guild.get_channel(channelID)
            # Simple check to ensure that the channel exists.
            if channel:
                # Deletes all channels except for the general channel.
                if key != 'general':
                    try:
                        await channel.delete()
                    except discord.Forbidden:
                        print('Could not delete {} channel from server: {}'.format(key, guild_id))
            else:
                print("{} channel does not exist in server: {}".format(key, guild_id))
        # As the last thing done, clears the memory of this game.
        self.bot.game_list.pop(guild_id)
        print('Game terminated in server: {}'.format(guild_id))
        
    async def kill_player(self, guild_id, player_id):
        # Updates the player's status to dead, and changes the counters
        # that store the number of live and dead players.
        self.bot.game_list[guild_id]["active"][player_id]["status"] = 'dead'
        self.bot.game_list[guild_id]["active"][player_id]["turns"] = self.bot.game_list[guild_id]['turn']
        self.bot.game_list[guild_id]["player_numbers"]["alive"] = self.bot.game_list[guild_id]["player_numbers"]["alive"] - 1
        self.bot.game_list[guild_id]["player_numbers"]["dead"] = self.bot.game_list[guild_id]["player_numbers"]["dead"] + 1
        # Also if the player who has just been lynched is the last
        # werewolf, goes to success screen.
        if self.bot.game_list[guild_id]["active"][player_id]["role"] == "Werewolf":
            self.bot.game_list[guild_id]["player_numbers"]["werewolves_live"] = self.bot.game_list[guild_id]["player_numbers"]["werewolves_live"] - 1
            if self.bot.game_list[guild_id]["player_numbers"]["werewolves_live"] == 0:
                self.bot.game_list[guild_id]["playing"] = False
                await self.game_end(guild_id, werewolf_victory = False)
                pass
        elif self.bot.game_list[guild_id]["active"][player_id]["role"] == "Villager":
            self.bot.game_list[guild_id]["player_numbers"]["villagers_live"] = self.bot.game_list[guild_id]["player_numbers"]["villagers_live"] - 1
            if self.bot.game_list[guild_id]["player_numbers"]["villagers_live"] == 0:
                self.bot.game_list[guild_id]["playing"] = False
                await self.game_end(guild_id)
                pass
        return
        
    async def set_night(self, guild):
        # Updating the current time-of-day and turn counter.
        self.bot.game_list[guild.id]["day"] = False
        self.bot.game_list[guild.id]["turn"] = self.bot.game_list[guild.id]["turn"] + 1
        general_channel = guild.get_channel(self.bot.game_list[guild.id]["channel_ids"]["general"])
        await general_channel.send("```It is now night time...```")
        await self.werewolf_victim_send(guild)
        pass
    
    async def set_day(self, guild):
        self.bot.game_list[guild.id]["day"] = True
        general_channel = guild.get_channel(self.bot.game_list[guild.id]["channel_ids"]["general"])
        
        live_list = []
        # Getting the status of each player, and if they're alive, moving them
        # into this list of live players.
        for key, player in self.bot.game_list[guild.id]['active'].items():
            if (player['status'] == 'alive'):
                live_list.append(player['name'])
        # Creating a string to print all live targets to display for werewolves
        # to pick...
        live_string = ""
        for i, target in enumerate(live_list):
            live_string = "{} {}. {}\n".format(live_string, i+1, target)
        await general_channel.send("```It is now daytime. Turn Number: {}. Total players remaining: {}\n{}\nYou can now nominate one player to kill, by typing [/kill @player], by mentioning the player in general chat. You can only nominate one player, so choose well.```".format(self.bot.game_list[guild.id]["turn"], self.bot.game_list[guild.id]["player_numbers"]["alive"], live_string))
        pass
    
    async def update_werewolf_victims(self, guild_id, werewolf_name, target_number):
        target_id = self.target_list[guild_id]["target_ids"][target_number]
        # Pushing the new vote into the array. It should update everytime, so
        # will only keep your last vote.
        self.target_list[guild_id].update({"votes": {werewolf_name: target_id}})
        # Checks if the total number of votes match the number of live werewolves
        # in the game. Once they match, takes the majority vote, or 
        if len(self.target_list[guild_id]['votes']) == self.bot.game_list[guild_id]["player_numbers"]["werewolves_live"]:
            werewolf_votes = list(self.target_list[guild_id]['votes'].values())
            # Gets rid of storage for this instance of the werewolf votes.
            self.target_list.pop(guild_id)
            victims, victim_votes = np.unique(werewolf_votes, return_counts = True)
            guild = self.bot.get_guild(guild_id)
            general_channel = guild.get_channel(self.bot.game_list[guild_id]["channel_ids"]["general"])
            for victim, votes in zip(victims, victim_votes):
                if (self.bot.game_list[guild_id]["player_numbers"]["werewolves_live"] > 3) & (votes > 2):
                    await general_channel.send("```The werewolves killed {} in the night!```".format(self.bot.game_list[guild_id]["active"][victim]['name']))
                    await self.kill_player(guild_id, target_id)
                elif (self.bot.game_list[guild_id]["player_numbers"]["werewolves_live"] == 2) & (self.bot.game_list[guild_id]["player_numbers"]["werewolves_live"] == 3) & (votes > 1):
                    await general_channel.send("```The werewolves killed {} in the night!```".format(self.bot.game_list[guild_id]["active"][victim]['name']))
                    await self.kill_player(guild_id, target_id)
                elif (self.bot.game_list[guild_id]["player_numbers"]["werewolves_live"] == 1):
                    await general_channel.send("```The werewolves killed {} in the night!```".format(self.bot.game_list[guild_id]["active"][victim]['name']))
                    await self.kill_player(guild_id, target_id)
                else:
                    await general_channel.send("```Werewolves really need to get their act together...```")
            if guild_id in self.bot.game_list:
                if self.bot.game_list[guild_id]["playing"] == True:
                    await self.set_day(guild)
            
    async def werewolf_victim_send(self, guild):
        general_channel = guild.get_channel(self.bot.game_list[guild.id]["channel_ids"]["general"])
        await general_channel.send("```Werewolves are choosing who to kill!```")
        live_target_list = []
        live_target_id_list = []
        # Getting the status of each player, and if they're alive, moving them
        # into this list of live players.
        for key, player in self.bot.game_list[guild.id]['active'].items():
            if (player['status'] == 'alive'):
                live_target_list.append(player['name'])
                live_target_id_list.append(key)
        self.target_list.update({guild.id: {"names": live_target_list,
                                            "target_ids": live_target_id_list}})
        # Creating a string to print all live targets to display for werewolves
        # to pick...
        live_target_string = ""
        for i, target in enumerate(live_target_list):
            live_target_string = "{} {}. {}\n".format(live_target_string, i+1, target)
        werewolf_channel = guild.get_channel(self.bot.game_list[guild.id]["channel_ids"]["werewolf"])
        await werewolf_channel.send("```Pick who to kill! Each werewolf must type /kill [number] to target someone. You can vote to kill different players, but a majority (or minimum of 3 votes, whichever is lower) must be reached in order to successfully kill a player.\nLive targets:\n{}```".format(live_target_string))
    
    def get_mob_kill_string(self, initialString, player_name, kill_votes, no_kill_votes, kill_details):
        # Just putting together all the names that voted.
        killString = '\n - '.join(kill_details['vote_kill'])
        noKillString = '\n - '.join(kill_details['vote_no_kill'])
        # Slightly different message if a decision was unanimous.
        if (kill_votes > 0) & (no_kill_votes > 0):
            finalString = '```{}\nVoted to Kill: {}\n - {}\n\nVoted not to Kill: {}\n - {}```'.format(initialString, kill_votes, killString, no_kill_votes, noKillString)
        elif (kill_votes > 0) & (no_kill_votes == 0):
            finalString = '```{}\nNobody voted not to Kill {}!```'.format(initialString, player_name)
        elif (kill_votes == 0) & (no_kill_votes > 0): 
            finalString = '```{}\nNobody voted to kill {}!```'.format(initialString, player_name)
        return finalString
        
        
    
    async def end_voting(self, guild_id):
        kill_details = self.kill_message.pop(guild_id, None)
        # Just checking that the kill dictionary exists. Prevents a whole host
        # of errors flooding the log if this isn't here - also helps me more
        # easily identify the server causing the issue.
        if kill_details == None:
            print('Error occured in server {}: No kill dictionary found to remove.'.format(guild_id))
        else:
            # Pulls the lengths of each array - just makes for slightly easier
            # reading here, in case some changes need to be made along the way.
            kill_votes = len(kill_details['vote_kill'])
            no_kill_votes = len(kill_details['vote_no_kill'])
            total_votes = kill_votes + no_kill_votes
            # Quick pull of player details: again makes reading in the next 
            # section a bit easier for anyone going through this, or if I'm 
            # making any changes.
            player_name = kill_details["player_to_kill_name"]
            player_id = kill_details["player_to_kill_id"]
            # Getting the guild object, to get the channel object, to send a
            # nice little message. This needs to be here because the original 
            # structure of the code meant that the async operator for ending the
            # game was happening simultaneously to printing the lynch text. This
            # just sorts that out a little.
            guild = self.bot.get_guild(guild_id)
            general_channel = guild.get_channel(self.bot.game_list[guild_id]["channel_ids"]["general"])
            # needs a majority of votes to kill a player, so the greater than
            # operator is used.
            if kill_votes > no_kill_votes:
                # String for a lynched person (ignores role, doesn't tell the
                # game how many werewolves left).
                initialString = 'The mob voted to execute {}, and killed him!\nTotal Votes: {}'.format(player_name, total_votes)
                finalString = self.get_mob_kill_string(initialString, player_name, kill_votes, no_kill_votes, kill_details)
                # printing the lynch text.
                await general_channel.send(finalString)
                # Kills player - Can end game here if needed!
                await self.kill_player(guild_id, player_id)
                pass
            else:
                # String for a failed lynch.
                initialString = 'The mob voted to execute {}, but there were not enough votes!\nTotal Votes: {}'.format(player_name, total_votes)
                finalString = self.get_mob_kill_string(initialString, player_name, kill_votes, no_kill_votes, kill_details)
                # printing the no-lynch text. These were initially outside the
                # if-else statements, but have moved inside to stop the async
                # operation for game ending from being run at the same time.
                await general_channel.send(finalString)
                pass
    
    @commands.command()
    async def start(self, ctx, *arg):
        # first, check that game is ready, and this is the right channel.
        if ctx.guild.id in self.bot.game_list.keys():
            if ctx.author.id in self.bot.game_list[ctx.guild.id]['active'].keys():
                self.bot.game_list[ctx.guild.id]['day'] = False
                self.bot.game_list[ctx.guild.id]['turn'] = 1
                await ctx.send("```Beginning the first night phase!```")
                await self.werewolf_victim_send(ctx.guild)
            else:
                await ctx.send("```You are not part of the game, {}!```".format(ctx.author.display_name))
        else:
            await ctx.send("```You don't have a game started in this server!```")
        
    @commands.Cog.listener()
    async def on_reaction_add(self, react: discord.Reaction, person: discord.User):
        # Lines were getting ridiculously long, this is just to shorten them.
        guildID = react.message.guild.id
        # This should check that the react is for the correct server AND the
        # correct message, since the discord.message type has all the right
        # values stored in it.
        if not person.bot:
            # Iterates through each of the dicts in the kill_message dict,
            # stops quickly on the one that matches the right message in the 
            # right server. Basically stops a reaction to any old message from
            # bringing the rest of the function up.
            if self.kill_message.items():
                for key, message in self.kill_message.items():
                    # This section is only called if both the message and server
                    # match the appropriate message. (So, should work across multiple
                    # servers.)
                    if (guildID == key) & (react.message.id == message['message']):
                        # Check that the person making the react is listed as an
                        # active player within the current guild.
                        if person.id in self.bot.game_list[guildID]['active']:
                            # Now check if the person is alive.
                            if self.bot.game_list[guildID]['active'][person.id]['status'] == 'alive':
                                # Checkbox tick react.
                                kill_list = self.kill_message[guildID]['vote_kill']
                                no_kill_list = self.kill_message[guildID]['vote_no_kill']
                                if react.emoji == '\u2705':
                                    # If player has previously voted for something,
                                    # remove that vote from the other list
                                    if person.display_name in no_kill_list:
                                        no_kill_list.remove(person.display_name)
                                    # Append player to appropriate vote list.
                                    if person.display_name not in kill_list:
                                        kill_list.append(person.display_name)
                                elif react.emoji == '\u274e':
                                    # If player has previously voted for something,
                                    # remove that vote from the other list
                                    if person.display_name in self.kill_message[guildID]['vote_kill']:
                                        self.kill_message[guildID]['vote_kill'].remove(person.display_name)
                                    # Append player to appropriate vote list.
                                    if person.display_name not in no_kill_list:
                                        no_kill_list.append(person.display_name)
                        await react.remove(person)
                        # Updates the screen to show how many votes have been
                        # cast, and how many should be cast in total.
                        total_votes = len(kill_list) + len(no_kill_list)
                        await react.message.edit(content = '```You nominated {} to be executed!\nClick on \u2705 to kill, or \u274e to spare.\n\n{} Players have voted out of {}.```'.format(self.kill_message[guildID]["player_to_kill_name"], total_votes, self.bot.game_list[guildID]["player_numbers"]["alive"]) )
                self.kill_message[guildID].update({"vote_kill": kill_list})
                self.kill_message[guildID].update({"vote_no_kill": no_kill_list})
                # Check if the total number of votes now matches the total
                # number of live players in the game.
                if self.bot.game_list[guildID]['player_numbers']['alive'] == (len(self.kill_message[guildID]['vote_no_kill']) + len(self.kill_message[guildID]['vote_kill'])):
                    # Gets the channel ID using the rection, and sends it
                    # on through to the end_voting parameter.
                    await self.end_voting(guildID)
                    if react.message.guild.id in self.bot.game_list:
                        if self.bot.game_list[react.message.guild.id]["playing"] == True:
                            await self.set_night(react.message.guild)
                pass
                    
        
    @commands.command(help = "[/kill] let you nominate players to kill. Follow the instructions in the game dialogue to kill players.")
    async def kill(self, ctx, *arg):
        # Checking that the server that this is called in has a game running!
        if ctx.guild.id in self.bot.game_list:
            # Making sure we're not still in the setup phase of the game!
            if self.bot.game_list[ctx.guild.id]['turn'] > 0:
                # Check for the message server: werewolf votes are handled slightly
                # differently from other votes.
                if (ctx.channel.id == self.bot.game_list[ctx.guild.id]["channel_ids"]["werewolf"]) & (self.bot.game_list[ctx.guild.id]["day"] == False):
                    # Check the player is, indeed, a werewolf...
                    if self.bot.game_list[ctx.guild.id]['active'][ctx.author.id]['role'] == 'Werewolf':
                        # This does different stuff fom the general actions below.
                        if len(arg) == 1:
                            if (int(arg[0]) > len(self.target_list[ctx.guild.id]['names'])) | (int(arg[0]) == 0):
                                await ctx.send("```That target does not exist, pick a number on the list!```")
                            else:
                                await ctx.send("```{} is targetting {} to be killed!```".format(ctx.author.display_name, self.target_list[ctx.guild.id]["names"][int(arg[0]) - 1]))
                                await self.update_werewolf_victims(ctx.guild.id, ctx.author.name, int(arg[0]) - 1)
                        # You should only be allowed to target 1 player, so anything that
                        # means you typed in more than 1 gets you disallowed.
                        elif len(arg) > 1:
                            await ctx.send('```You can only target one player to be killed!```')
                        # Again, if no player mentioned, tells you off.
                        else:
                            await ctx.send('```You have to mention player to be killed!\nType /kill @[player] to mention him/her chat!```')
                    else:
                        await ctx.send("```You're not supposed to be in this channel, {}!```".format(ctx.author.display_name))
                else:
                    # Makes sure lynching only happens during the daytime...
                    if self.bot.game_list[ctx.guild.id]["day"] == True:
                        # Checking if the author of the text is actually within the game.
                        # If not... Doesn't really help anyone. Also checks if
                        # this author is alive...
                        if ctx.author.id in self.bot.game_list[ctx.guild.id]['active'].keys():
                            if self.bot.game_list[ctx.guild.id]['active'][ctx.author.id]['status'] == 'alive':
                                # This is to determine who was mentioned in the vote-to-kill sequence.
                                # You should only mention 1 player, so this also does a quick check
                                # on that and throws up appropriate errors.
                                mentioned_player = ctx.message.mentions
                                if len(mentioned_player) == 1:
                                    # Generating message, and adding reaction "buttons".
                                    message = await ctx.send('```You nominated {} to be executed!\nClick on \u2705 to kill, or \u274e to spare.\n\n0 Players have voted out of {}.```'.format(mentioned_player[0].display_name, self.bot.game_list[ctx.guild.id]["player_numbers"]["alive"]))
                                    await message.add_reaction('\u2705')
                                    await message.add_reaction('\u274e')
                                    # Populates an interim storage solution - stores the message
                                    # id within the guild, and keeps details about the player to 
                                    # be killed, and who has voted to kill or not kill.
                                    message_info = {message.guild.id: {"message": message.id,
                                                                       "player_to_kill_id": mentioned_player[0].id,
                                                                       "player_to_kill_name": mentioned_player[0].display_name,
                                                                       "vote_kill": [],
                                                                       "vote_no_kill": []}}
                                    self.kill_message.update(message_info)
                                # If more than 1 player mentioned, tells you off.
                                elif len(mentioned_player) > 1:
                                    await ctx.send('```You can only nominate one player to be killed!```')
                                # Again, if no player mentioned, tells you off.
                                else:
                                    await ctx.send('```You have to mention player to be killed!\nType /kill @[player] to mention him/her in the Discord chat!```')
                            else:
                                await ctx.send("```You're dead, {}. You can't try to lynch anybody.```".format(ctx.author.display_name))
                        else:
                            await ctx.send("```You're not part of this game, {}!```".format(ctx.author.display_name))
                    else:
                        await ctx.send("```It's not time to do that!```")
            else:
                await ctx.send("```It's not time to do that!```")
        # This is if the guild.id cannot be found in the game_list dictionary.
        else:
            await ctx.send('```You do not have a game started!```')
                           
def setup(bot):
    bot.add_cog(turns(bot))