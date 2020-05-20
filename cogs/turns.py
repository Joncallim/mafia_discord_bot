#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 17 12:51:55 2020

@author: Jonathan
"""

import discord
from discord.ext import commands
import numpy as np
import random

class turns(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.kill_message = {}
        self.target_list = {}
        # Format for the strings:
        # Night phase: [night_scene_setting] [werewolf_hunting] [night_advice]
        # Werewolf Kill: [night_initial] victim [victim_action_desc] when [werewolf_desc] [werewolf_attack_desc]
        # Werewolf no-Kill:  [night_initial] [no_kill_desc][no_kill_variant]
        # daybreak: [daybreak] [other details (next line)]
        self.scenes = {"night_initial": ["It was a dark and stormy night.",
                                         "The moon was high in the sky."],
                       # werewolf descriptor will be appended onto after the 
                       # victim descriptor, so no punctuation at the end.
                       "werewolf_desc": ["a pack of wild werewolves",
                                         "a vicious pack of wild animals"],
                       "victim_action_desc": ["was out for a midnight stroll",
                                              "had just left home to visit grandma"],
                       "werewolf_attack_desc": ["attacked!",
                                                "ambushed!"],
                       "no_kill_desc": ["The village was really serene",
                                        "Nothing really happened last night"],
                       "no_kill_variant": ["...",
                                           ", except for the blacksmith working till midnight.",
                                           ", and everyone got lots of sleep."],
                       "daybreak": ["The sun rises over the little village.",
                                    "The village rooster crows on time, as usual."],
                       "werewolf_hunting": ["The werewolves are on the hunt!",
                                            "Wild creatures roam the night!"],
                       "night_advice": ["Lock your doors!",
                                        "Stay inside!"],
                       "night_scene_setting": ["It is now night-time...",
                                               "The sun sets on another day in village-ville..."],
                       "saving_identity": ["Thankfully, a kind soul was passing by, ",
                                           "Luckily, there was a helpful neighbour, "],
                       "saving_scene": ["who averted near-certain death!",
                                        "who acted quickly to save the life of a fellow villager!"]
                       
                       }
    
    # This creates a nice little random sequence of text for werewolf kills.
    async def werewolf_kill(self, guild_id, kill_list):
        # First check for more than 1 victim:
        initString = random.choice(self.scenes['night_initial'])
        # Sets the status of stop_game so that the game won't just kill itself
        # if no victory conditions are met in this function.
        stop_game = False
        kill_str = "{}\n\n".format(initString)
        formal_kills = ""
        # As long as at least one person was killed, creates a random sequence
        # of strings that should make sense. It'll append each victim's name to
        # the kill.
        if len(kill_list) > 0:
            for victim_id in kill_list:
                kill_str = "{}{} {}, when {} {}".format(kill_str,
                                                        self.bot.game_list[guild_id]["active"][victim_id]['name'],
                                                        random.choice(self.scenes['victim_action_desc']),
                                                        random.choice(self.scenes['werewolf_desc']),
                                                        random.choice(self.scenes['werewolf_attack_desc']))
                # The two checks here make sure that the saves is not an empty
                # list, and the victim has not been saved. If either condition
                # is true, the victim is saved.
                if (self.target_list[guild_id]['saves'] != []):
                    if (victim_id in self.target_list[guild_id]['saves'].values()):
                        kill_str = "{} {}{}".format(kill_str,
                                                    random.choice(self.scenes['saving_identity']),
                                                    random.choice(self.scenes['saving_scene']))
                    else:
                        # Initial kill string. Also then kills the player later, with
                        # some fancy text.
                        kill_str = "{}\n\n".format(kill_str)
                        # Kills the player and returns two booleans: The first tells
                        # you if it's a game-ending kill, the second tells you who's
                        # victory it is. A small flaw is that 
                        game_end, werewolf_victory = await self.kill_player(guild_id, victim_id)
                        # Saves the game-ending values here. The final player killed 
                        # could be a werewolf, for example, and that wouldn't trigger
                        # the game ending conditions the same way.
                        if (game_end == True) & (stop_game == False):
                            stop_game = True
                            ww_vic = werewolf_victory
                        # Just an itemized list of players who have been killed. Shows up
                        # every time in case you don't want to read the long text above it.
                        formal_kills = "{}\n - {}".format(formal_kills,
                                                          self.bot.game_list[guild_id]["active"][victim_id]['name'])   
                else:
                    # Initial kill string. Also then kills the player later, with
                    # some fancy text.
                    kill_str = "{}\n\n".format(kill_str)
                    # Kills the player and returns two booleans: The first tells
                    # you if it's a game-ending kill, the second tells you who's
                    # victory it is. A small flaw is that 
                    game_end, werewolf_victory = await self.kill_player(guild_id, victim_id)
                    # Saves the game-ending values here. The final player killed 
                    # could be a werewolf, for example, and that wouldn't trigger
                    # the game ending conditions the same way.
                    if (game_end == True) & (stop_game == False):
                        stop_game = True
                        ww_vic = werewolf_victory
                    # Just an itemized list of players who have been killed. Shows up
                    # every time in case you don't want to read the long text above it.
                    formal_kills = "{}\n - {}".format(formal_kills,
                                                      self.bot.game_list[guild_id]["active"][victim_id]['name'])
        # Nobody killed - brings up some normal-ish text
        elif len(kill_list) == 0:
            kill_str = "{}{}{}".format(kill_str,
                                       random.choice(self.scenes['no_kill_desc']),
                                       random.choice(self.scenes['no_kill_variant']))
        # If the game is finished from a werewolf kill, moves into the end-of-
        # game sequence, sending two messages (one for the werewolf kill, another
        # for the EOG).
        if stop_game:
            outputString = "```{}The following players have been killed:{}```".format(kill_str,
                                                                                      formal_kills)
            await self.send_message_general(guild_id, outputString)
            await self.game_end(guild_id, ww_vic)
        else:
            dayString = "{}{}\n\n".format(kill_str,
                                          random.choice(self.scenes['daybreak']))
            # Changes status to day, prints some info on what to do now.
            live_player_string = self.set_day(guild_id)
            if len(formal_kills) > 0:    
                outputString = "```{}The following players have been killed:\n - {}\n\n{}```".format(dayString,
                                                                                           formal_kills,
                                                                                           live_player_string)
            else:
                outputString = "```{}\n\n{}```".format(dayString,
                                                       live_player_string)
            # Gets rid of storage for this instance of the night-phase storage.
            self.target_list.pop(guild_id)
            await self.send_message_general(guild_id, outputString)
    
    def check_turns_complete(self, guild_id):
        return self.bot.game_list[guild_id]['turn_complete']['werewolves'] & self.bot.game_list[guild_id]['turn_complete']['medics'] & self.bot.game_list[guild_id]['turn_complete']['detectives']
    
    # Small function to send a message on the general channel, from just the 
    # guild id.
    async def send_message_general(self, guild_id, message):
        guild = self.bot.get_guild(guild_id)
        general_channel = guild.get_channel(self.bot.game_list[guild_id]["channel_ids"]["general"])
        await general_channel.send(message)
        pass
    
    # Game ending. Prints all the important EOG info, and clears memory of the
    # game.    
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
                print("{} channel did not exist in server: {}".format(key, guild_id))
        # As the last thing done, clears the memory of this game.
        self.bot.game_list.pop(guild_id)
        print('Game terminated in server: {}'.format(guild_id))
    
    # Return True for game ending, False for game continuing. Second condition
    # is the werewolf victory. True means the werewolves win.
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
                return True, False
                pass
        elif self.bot.game_list[guild_id]["active"][player_id]["role"] == "Villager":
            self.bot.game_list[guild_id]["player_numbers"]["villagers_live"] = self.bot.game_list[guild_id]["player_numbers"]["villagers_live"] - 1
            self.bot.game_list[guild_id]["player_numbers"]["humans_live"] = self.bot.game_list[guild_id]["player_numbers"]["humans_live"] - 1
            if self.bot.game_list[guild_id]["player_numbers"]["humans_live"] == 0:
                self.bot.game_list[guild_id]["playing"] = False
                return True, True
                pass
        elif self.bot.game_list[guild_id]["active"][player_id]["role"] == "Medic":
            self.bot.game_list[guild_id]["player_numbers"]["medics_live"] = self.bot.game_list[guild_id]["player_numbers"]["medics_live"] - 1
            self.bot.game_list[guild_id]["player_numbers"]["humans_live"] = self.bot.game_list[guild_id]["player_numbers"]["humans_live"] - 1
            if self.bot.game_list[guild_id]["player_numbers"]["humans_live"] == 0:
                self.bot.game_list[guild_id]["playing"] = False
                return True, True
                pass
        elif self.bot.game_list[guild_id]["active"][player_id]["role"] == "Detective":
            self.bot.game_list[guild_id]["player_numbers"]["detectives_live"] = self.bot.game_list[guild_id]["player_numbers"]["detectives_live"] - 1
            self.bot.game_list[guild_id]["player_numbers"]["humans_live"] = self.bot.game_list[guild_id]["player_numbers"]["humans_live"] - 1
            if self.bot.game_list[guild_id]["player_numbers"]["humans_live"] == 0:
                self.bot.game_list[guild_id]["playing"] = False
                return True, True
                pass
        return False, False
        
    async def set_night(self, guild):
        # Updating the current time-of-day and turn counter.
        self.bot.game_list[guild.id]["day"] = False
        self.bot.game_list[guild.id]["turn"] = self.bot.game_list[guild.id]["turn"] + 1
        self.bot.game_list[guild.id]["turn_complete"] = {"werewolves": False,
                                                         "medics": False,
                                                         "detectives": False }
        if self.bot.game_list[guild.id]["player_numbers"]["detectives_live"] == 0:
            self.bot.game_list[guild.id]["turn_complete"]["detectives"] = True
        if self.bot.game_list[guild.id]["player_numbers"]["medics_live"] == 0:
            self.bot.game_list[guild.id]["turn_complete"]["medics"] = True
        general_channel = guild.get_channel(self.bot.game_list[guild.id]["channel_ids"]["general"])
        await general_channel.send("```{} {} {}```".format(random.choice(self.scenes['night_scene_setting']),
                                                           random.choice(self.scenes['werewolf_hunting']),
                                                           random.choice(self.scenes['night_advice'])))
        await self.send_prompt(guild)
        pass
    
    def set_day(self, guild_id):
        self.bot.game_list[guild_id]["day"] = True
        self.bot.game_list[guild_id]["idle"] = False
        live_list = []
        # Getting the status of each player, and if they're alive, moving them
        # into this list of live players.
        for key, player in self.bot.game_list[guild_id]['active'].items():
            if (player['status'] == 'alive'):
                live_list.append(player['name'])
        # Creating a string to print all live targets to display for werewolves
        # to pick...
        live_string = ""
        for i, target in enumerate(live_list):
            live_string = "{} {}. {}\n".format(live_string, i+1, target)
        live_player_string = ("Turn Number: {}. Total players remaining: {}\n{}\nYou can now nominate one player to kill, by typing [/kill @player], by mentioning the player in general chat. You can only nominate one player, so choose well.".format(self.bot.game_list[guild_id]["turn"], self.bot.game_list[guild_id]["player_numbers"]["alive"], live_string))
        return live_player_string
    
    async def end_night_phase(self, guild_id):
        werewolf_votes = list(self.target_list[guild_id]['votes'].values())
        # Creates and empty werewolf kill list. This will be populated with
        # successful kills, and passed to another function to create a nice
        # string for printing. This uses player_ids, so no confusion and
        # quick indexing.
        werewolf_kill_list = []
        # Gets the number of each vote made by the werewolves, and counts
        # the number of unique votes. Repeated votes obviously get counted
        # multiple times.
        victims, victim_votes = np.unique(werewolf_votes, return_counts = True)
        # Getting the guild and general channel to send. May not need.
        for victim, votes in zip(victims, victim_votes):
            if (self.bot.game_list[guild_id]["player_numbers"]["werewolves_live"] > 3) & (votes > 2):
                werewolf_kill_list.append(victim)
            elif ((self.bot.game_list[guild_id]["player_numbers"]["werewolves_live"] == 2) | (self.bot.game_list[guild_id]["player_numbers"]["werewolves_live"] == 3)) & (votes > 1):
                werewolf_kill_list.append(victim)
            elif (self.bot.game_list[guild_id]["player_numbers"]["werewolves_live"] == 1):
                werewolf_kill_list.append(victim)
        await self.werewolf_kill(guild_id, werewolf_kill_list)
    
    # This function is called when a werewolf picks someone to kill. Werewolf
    # kills are fairly nuanced, so it might help to have a 2-input NN with a
    # few layers and a sigmoid activation function to train it against what you'd
    # decide to be "kills," but this needs lots of data, and will probably slow
    # down the overall speed of the program.
    async def update_werewolf_victims(self, guild_id, werewolf_id, target_number):
        target_id = self.target_list[guild_id]["target_ids"][target_number]
        # Pushing the new vote into the array. It should update everytime, so
        # will only keep your last vote.
        self.target_list[guild_id].update({"votes": {werewolf_id: target_id}})
        # Checks if the total number of votes match the number of live werewolves
        # in the game. Once they match, takes the majority vote according to a
        # specified list in the README.
        if len(self.target_list[guild_id]['votes']) == self.bot.game_list[guild_id]["player_numbers"]["werewolves_live"]:
            # Setting a boolean so that we can really easily check if all the 
            # roles have finished their night-time turn.
            self.bot.game_list[guild_id]["turn_complete"]["werewolves"] = True
            # This function returns True when all the markers have been set to
            # true. Then ends the night phase by calculating kills and generating
            # some text.
            if self.check_turns_complete(guild_id):
                await self.end_night_phase(guild_id)
                pass
    
    # Similar to killing victims, but medics and patients, not werewolves and
    # victims.
    async def save_patients(self, guild_id, medic_id, target_number):
        patient_id = self.target_list[guild_id]["target_ids"][target_number]
        # Pushing the new vote into the array. It should update everytime, so
        # will only keep your last vote.
        self.target_list[guild_id].update({"saves": {medic_id: patient_id}})
        # Checks if the total number of votes match the number of live medics
        if len(self.target_list[guild_id]['votes']) == self.bot.game_list[guild_id]["player_numbers"]["medics_live"]:
            # Setting a boolean so that we can really easily check if all the 
            # roles have finished their night-time turn.
            self.bot.game_list[guild_id]["turn_complete"]["medics"] = True
            # This function returns True when all the markers have been set to
            # true. Then ends the night phase by calculating kills and generating
            # some text.
            if self.check_turns_complete(guild_id):
                await self.end_night_phase(guild_id)
            
    # Send prompts sends the initial batch of prompts to the various night-time
    # channels for the different night-time roles. As new roles are added this
    # will of course have to expand, and be handled manually in order to change
    # the output text.
    async def send_prompts(self, guild):
        live_target_list = []
        live_target_id_list = []
        saves = []
        # Getting the status of each player, and if they're alive, moving them
        # into this list of live players.
        for key, player in self.bot.game_list[guild.id]['active'].items():
            if (player['status'] == 'alive'):
                live_target_list.append(player['name'])
                live_target_id_list.append(key)
        self.target_list.update({guild.id: {"names": live_target_list,
                                            "target_ids": live_target_id_list,
                                            "saves": saves,
                                            "investigations": 0}})
        # Creating a string to print all live targets to display for werewolves
        # to pick...
        live_target_string = ""
        for i, target in enumerate(live_target_list):
            live_target_string = "{} {}. {}\n".format(live_target_string, i+1, target)
        werewolf_channel = guild.get_channel(self.bot.game_list[guild.id]["channel_ids"]["werewolf"])
        await werewolf_channel.send("```Pick who to kill! Each werewolf must type /kill [number] to target someone. You can vote to kill different players, but a majority (or minimum of 3 votes, whichever is lower) must be reached in order to successfully kill a player.\nLive targets:\n{}```".format(live_target_string))
        medic_channel = guild.get_channel(self.bot.game_list[guild.id]["channel_ids"]["medic"])
        await medic_channel.send("```Pick who to save! Each medic must type /save [number] to save someone from being mauled by the werewolves. Each medic can save a different person, so use your save well!\nLive players:\n{}```".format(live_target_string))
        detective_channel = guild.get_channel(self.bot.game_list[guild.id]["channel_ids"]["detective"])
        await detective_channel.send("```Pick who to investigate! Each detective can type /investigate [number] to investigate someone. Each detective can investigate a different person, and the results will be delivered to you via DM!\nLive players:\n{}```".format(live_target_string))
        pass
        
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
                # Kills player - Can end game here if needed!
                game_end, werewolf_victory = await self.kill_player(guild_id, player_id)
                # Only one iteration of this will happen, so no need to save the
                # value of game_end earlier.
                if game_end:
                    # printing the lynch text.
                    await general_channel.send(finalString)
                    await self.game_end(guild_id, werewolf_victory)
                else:
                    await general_channel.send(finalString)
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
                # Sets the markers for detectives and medics if not present in
                # this particular game.
                if self.bot.game_list[ctx.guild.id]["player_numbers"]["detectives_live"] == 0:
                    self.bot.game_list[ctx.guild.id]["turn_complete"]["detectives"] = True
                if self.bot.game_list[ctx.guild.id]["player_numbers"]["medics_live"] == 0:
                    self.bot.game_list[ctx.guild.id]["turn_complete"]["medics"] = True
                # Day turns to night, turn one starts, etc.
                self.bot.game_list[ctx.guild.id]['day'] = False
                self.bot.game_list[ctx.guild.id]['turn'] = 1
                # This is the bit that starts the first night, visually. All the
                # appropriate markers have been set (and are very readable).
                await ctx.send("```Beginning the first night! {} {}```".format(random.choice(self.scenes['werewolf_hunting']),
                                                                               random.choice(self.scenes['night_advice'])))
                await self.send_prompts(ctx.guild)
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
            
    @commands.command(help = '[/investigate] lets the detectives check if a player is of a particular alignment, but not their specific roles.')
    async def investigate(self, ctx, *arg):
        # Checking that the server that this is called in has a game running!
        if ctx.guild.id in self.bot.game_list:
            # Check if author exists within the current game.
            if ctx.author.id in self.bot.game_list[ctx.guild.id]['active'].keys():
                # Performs a few checks:
                #   1. It is not the first night (i.e. not Turn 0)
                #   2. It is being received in the correct channel. (Detective)
                #   3. The game is in night phase.
                #   4. The player sending the request has the "Detective" class.
                if (self.bot.game_list[ctx.guild.id]['turn'] > 0) & (ctx.channel.id == self.bot.game_list[ctx.guild.id]["channel_ids"]["medic"]) & (self.bot.game_list[ctx.guild.id]["day"] == False) & (self.bot.game_list[ctx.guild.id]['active'][ctx.author.id]['role'] == 'Detective'):
                    if len(arg) == 1:
                        if (int(arg[0]) > len(self.target_list[ctx.guild.id]['names'])) | (int(arg[0]) == 0):
                            await ctx.send("```That player does not exist, pick a number on the list!```")
                        else:
                            # Sets a ticker to go off if all detectives
                            # have investigated.
                            self.target_list[ctx.guild.id]["investigations"] = self.target_list[ctx.guild.id]["investigations"] + 1
                            if self.target_list[ctx.guild.id]["investigations"] == self.bot.game_list[ctx.guild.id]["player_numbers"]["detectives_live"]:
                                self.bot.game_list[ctx.guild.id]["turn_complete"]["detectives"] = True
                            await ctx.send("```{} is investigating {}!```".format(ctx.author.display_name, self.target_list[ctx.guild.id]["names"][int(arg[0]) - 1]))
                            # First pulls the player ID of the player that
                            # has been chosen.
                            target_id = self.target_list[ctx.guild.id]["target_ids"][int(arg[0]) - 1]
                            # Puts the string together informing the detective
                            # about the player in question.
                            infoString = "Results of your investigation: {} is a {}!".format(self.target_list[ctx.guild.id]["names"][int(arg[0]) - 1], self.bot.game_list[ctx.guild.id]["active"][target_id]["alignment"])
                            self.bot.dm_id = ctx.author
                            await ctx.author.send(infoString)
                            # This function returns True when all the markers 
                            # have been set to true. Then ends the night phase 
                            # by calculating kills and generating some text.
                            if self.check_turns_complete(ctx.guild.id):
                                await self.end_night_phase(ctx.guild.id)
                                pass
                    # You should only be allowed to target 1 player, so anything that
                    # means you typed in more than 1 gets you disallowed.
                    elif len(arg) > 1 :
                        await ctx.send('```You can only investigate one player!```')
                    # Again, if no player mentioned, tells you off.
                    else:
                        await ctx.send('```You have to identify a player to investigate!\nType /save [number] to pick!```')
                else:
                    await ctx.send("```You can't do that!```")
            else:
                await ctx.send("```You're not part of this game, {}!```".format(ctx.author.display_name))
        # This is if the guild.id cannot be found in the game_list dictionary.
        else:
            await ctx.send('```You do not have a game started!```')
            
    @commands.command(help = '[/save] allows a medic to save a player from inevitable death at the hands of the brutal werewolves.')
    async def save(self, ctx, *arg):
        # Checking that the server that this is called in has a game running!
        if ctx.guild.id in self.bot.game_list:
            # Check if author exists within the current game.
            if ctx.author.id in self.bot.game_list[ctx.guild.id]['active'].keys():
                # Performs a few checks:
                #   1. It is not the first night (i.e. not Turn 0)
                #   2. It is being received in the correct channel. (Medics)
                #   3. The game is in night phase.
                #   4. The player sending the request has the "Medic" class.
                if (self.bot.game_list[ctx.guild.id]['turn'] > 0) & (ctx.channel.id == self.bot.game_list[ctx.guild.id]["channel_ids"]["medic"]) & (self.bot.game_list[ctx.guild.id]["day"] == False) & (self.bot.game_list[ctx.guild.id]['active'][ctx.author.id]['role'] == 'Medic'):
                    if len(arg) == 1:
                        if (int(arg[0]) > len(self.target_list[ctx.guild.id]['names'])) | (int(arg[0]) == 0):
                            await ctx.send("```That player does not exist, pick a number on the list!```")
                        else:
                            await ctx.send("```{} is targetting {} to be killed!```".format(ctx.author.display_name, self.target_list[ctx.guild.id]["names"][int(arg[0]) - 1]))
                            # FIX THIS SOON.Hah
                            await self.save_patients(ctx.guild.id, ctx.author.id, int(arg[0]) - 1)
                    # You should only be allowed to target 1 player, so anything that
                    # means you typed in more than 1 gets you disallowed.
                    elif len(arg) > 1:
                        await ctx.send('```You can only save one player!```')
                    # Again, if no player mentioned, tells you off.
                    else:
                        await ctx.send('```You have to identify a player to be saved!\nType /save [number] to pick!```')
                else:
                    await ctx.send("```You can't do that!```")
            else:
                await ctx.send("```You're not part of this game, {}!```".format(ctx.author.display_name))
        # This is if the guild.id cannot be found in the game_list dictionary.
        else:
            await ctx.send('```You do not have a game started!```')
            
                    
        
    @commands.command(help = "[/kill] let you nominate players to kill. Follow the instructions in the game dialogue to kill players.")
    async def kill(self, ctx, *arg):
        # Checking that the server that this is called in has a game running!
        if ctx.guild.id in self.bot.game_list:
            # Making sure we're not still in the setup phase of the game!
            if self.bot.game_list[ctx.guild.id]['turn'] > 0:
                # Check if author exists within the current game.
                if ctx.author.id in self.bot.game_list[ctx.guild.id]['active'].keys():
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
                                    await self.update_werewolf_victims(ctx.guild.id, ctx.author.id, int(arg[0]) - 1)
                            # You should only be allowed to target 1 player, so anything that
                            # means you typed in more than 1 gets you disallowed.
                            elif len(arg) > 1:
                                await ctx.send('```You can only target one player to be killed!```')
                            # Again, if no player mentioned, tells you off.
                            else:
                                await ctx.send('```You have to identify a player to be killed!\nType /kill [number]!```')
                        else:
                            await ctx.send("```You're not supposed to be in this channel, {}!```".format(ctx.author.display_name))
                    else:
                        # Makes sure lynching only happens during the daytime...
                        if self.bot.game_list[ctx.guild.id]["day"] == True:
                            # Checking if the author of the text is actually within the game.
                            # If not... Doesn't really help anyone. Also checks if
                            # this author is alive...
                            
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
                            await ctx.send("```It's not time to do that!```")
                else:
                    await ctx.send("```You're not part of this game, {}!```".format(ctx.author.display_name))
            else:
                await ctx.send("```It's not time to do that!```")
        # This is if the guild.id cannot be found in the game_list dictionary.
        else:
            await ctx.send('```You do not have a game started!```')
                           
def setup(bot):
    bot.add_cog(turns(bot))