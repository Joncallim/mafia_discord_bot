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
    
    # This creates a nice little random sequence of text for werewolf kills.
    async def werewolf_kill(self, guild_id, kill_list, kill_fails):
        # First check for more than 1 victim:
        embed = discord.Embed(title="The werewolves were on the hunt last night...",
                              description="Night descends, and all the villagers return home, but not all those who sleep stay sleeping.",
                              color=0x154360)
        if len(kill_fails) > 0:
            for VictimID in kill_fails:
                VictimName = self.bot.game_list[guild_id]["active"][VictimID]['name']
                embed.add_field(name="{} was attacked, but survived.".format(VictimName),
                                value=self.bot.Narrator.GetNothingText(),
                                inline=False)
        # Sets the status of stop_game so that the game won't just kill itself
        # if no victory conditions are met in this function.
        stop_game = False
        formal_kills = []
        # As long as at least one person was killed, creates a random sequence
        # of strings that should make sense. It'll append each victim's name to
        # the kill.
        if len(kill_list) > 0:
            for victim_id in kill_list:
                VictimName = self.bot.game_list[guild_id]["active"][victim_id]['name']
                # The two checks here make sure that the saves is not an empty
                # list, and the victim has not been saved. If either condition
                # is true, the victim is saved.
                if (self.target_list[guild_id]['saves'] != []):
                    # Here, the victim has been saved by the medic!
                    if (victim_id in self.target_list[guild_id]['saves'].values()):
                        embed.add_field(name="{} was attacked, but survived.".format(VictimName),
                                        value=self.bot.Narrator.GetSaveText(VictimName),
                                        inline=False)
                    else:
                        embed.add_field(name="{} was attacked and killed!".format(VictimName),
                                        value=self.bot.Narrator.GetKillText(VictimName),
                                        inline=False)
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
                        formal_kills.append(VictimName)
                else:
                    embed.add_field(name="{} was attacked and killed!".format(VictimName),
                                    value=self.bot.Narrator.GetKillText(VictimName),
                                    inline=False)
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
                    formal_kills.append(VictimName)
        # Nobody killed - brings up some normal-ish text
        if (len(kill_list) == 0) & (len(kill_fails) == 0):
            embed.add_field(name="Nothing much happened that night...",
                                value="Crickets... And the sounds of the wind.",
                                inline=False)
        if len(formal_kills) > 0:
            KillNames="\n - ".join(formal_kills)
            embed.add_field(name="The following players have been killed:",
                            value=" - {}".format(KillNames),
                            inline=False)
        else:
            embed.add_field(name="The werewolves need to step up their game...",
                            value="Nobody was killed last night.",
                            inline=False)
        await self.send_message_general(guild_id, embed)
        # Finally, removes the target list from the game's memory.
        self.target_list.pop(guild_id)
        # If the game is to stop, enters the game-end phase, otherwise sets the
        # day to... daytime, and sends a nice daytime message.
        if stop_game:
            await self.game_end(guild_id, ww_vic)
        else:
            LivePlayers = self.set_day(guild_id)
            embed = discord.Embed(title="It's a new day in Village-ville.",
                              description="Turn Number: {}".format(self.bot.game_list[guild_id]["turn"]),
                              color=0xF7DC6F)
            embed.add_field(name="Players Remaining: {}".format(self.bot.game_list[guild_id]["player_numbers"]["alive"]),
                            value=LivePlayers,
                            inline=False)
            embed.add_field(name="What to do now:",
                            value="You can nominate a player to be killed by entering `/vote @player`, using the 'mention' feature to nominate him. You can only do this once per day-phase, so make sure some good discussion happens before you do this!",
                            inline=False)
            await self.send_message_general(guild_id, embed)
            
    
    def check_turns_complete(self, guild_id):
        return (self.bot.game_list[guild_id]['turn_complete']['werewolves'] & self.bot.game_list[guild_id]['turn_complete']['medics']) & (self.bot.game_list[guild_id]['turn_complete']['detectives'])
    
    # Small function to send a message on the general channel, from just the 
    # guild id.
    async def send_message_general(self, guild_id, Embed):
        guild = self.bot.get_guild(guild_id)
        general_channel = guild.get_channel(self.bot.game_list[guild_id]["channel_ids"]["general"])
        await general_channel.send(embed = Embed)
        pass
    
    # Game ending. Prints all the important EOG info, and clears memory of the
    # game.    
    async def game_end(self, guild_id, werewolf_victory = True):
        guild = self.bot.get_guild(guild_id)
        general_channel = guild.get_channel(self.bot.game_list[guild_id]["channel_ids"]["admin"])
        await general_channel.send(embed = self.bot.AdminText.Victory(self.bot.game_list[guild_id], werewolf_victory))
        # Now purging the game from memory.
        for key, channelID in self.bot.game_list[guild_id]['channel_ids'].items():
            channel = guild.get_channel(channelID)
            # Simple check to ensure that the channel exists.
            if channel:
                # Deletes all channels except for the general channel.
                if key != 'admin':
                    try:
                        await channel.delete()
                    except discord.Forbidden:
                        print('Could not delete {} channel from server: {}'.format(key, guild_id))
            else:
                print("{} channel did not exist in server: {}".format(key, guild_id))
        # As the last thing done, clears the memory of this game.
        self.bot.game_list.pop(guild_id)
        if self.bot.DetectiveClass.Investigations[guild_id]:
                self.bot.DetectiveClass.Investigations.pop(guild_id)
        print('Game completed in server: {}, id: {}'.format(guild.name, guild.id))
    
    # Return True for game ending, False for game continuing. Second condition
    # is the werewolf victory. True means the werewolves win.
    async def kill_player(self, guild_id, player_id):
        # Updates the player's status to dead, and changes the counters
        # that store the number of live and dead players.
        await self.bot.WWChannels.Kill(guild_id, player_id)
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
        self.bot.DetectiveClass.Investigations.update({guild.id: []})
        self.bot.game_list[guild.id]["day"] = False
        self.bot.game_list[guild.id]["turn"] = self.bot.game_list[guild.id]["turn"] + 1
        self.bot.game_list[guild.id]["turn_complete"] = {"werewolves": False,
                                                         "medics": False,
                                                         "detectives": False }
        if self.bot.game_list[guild.id]["player_numbers"]["detectives_live"] == 0:
            self.bot.game_list[guild.id]["turn_complete"]["detectives"] = True
        if self.bot.game_list[guild.id]["player_numbers"]["medics_live"] == 0:
            self.bot.game_list[guild.id]["turn_complete"]["medics"] = True
        guild = self.bot.get_guild(guild.id)
        # Getting the various channels that private messages need to be sent to.
        GeneralChannel = guild.get_channel(self.bot.game_list[guild.id]["channel_ids"]["general"])
        WerewolfChannel = guild.get_channel(self.bot.game_list[guild.id]["channel_ids"]["werewolf"])
        MedicChannel = guild.get_channel(self.bot.game_list[guild.id]["channel_ids"]["medic"])
        DetectiveChannel = guild.get_channel(self.bot.game_list[guild.id]["channel_ids"]["detective"])
        # Prep to send prompts to each night-time channel. Actual prompt for
        # the general channel also handled here.
        live_target_list = []
        live_target_id_list = []
        # Getting the status of each player, and if they're alive, moving them
        # into this list of live players.
        for key, player in self.bot.game_list[guild.id]['active'].items():
            if (player['status'] == 'alive'):
                live_target_list.append(player['name'])
                live_target_id_list.append(key)
        self.target_list.update({guild.id: {"names": live_target_list,
                                                "target_ids": live_target_id_list,
                                                "saves": [],
                                                "investigations": 0}})
        # Getting the actual embedded text for each channel. The channels
        # are retrieved earlier to prevent some weird ASYNCIO bug...
        GeneralEmbed, WerewolfEmbed, MedicEmbed, DetectiveEmbed = self.bot.VoteText.NightPrompts(live_target_list, False)
        try:
            await GeneralChannel.send( embed = GeneralEmbed )
            await WerewolfChannel.send( embed = WerewolfEmbed )
            await MedicChannel.send( embed = MedicEmbed )
            await DetectiveChannel.send( embed = DetectiveEmbed )
        except discord.Forbidden as Error:
            print("Failed to send message in {} due to {}".format(guild.name, Error))
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
        return live_string
    
    async def end_night_phase(self, guild_id):
        werewolf_votes = list(self.target_list[guild_id]['votes'].values())
        # Creates and empty werewolf kill list. This will be populated with
        # successful kills, and passed to another function to create a nice
        # string for printing. This uses player_ids, so no confusion and
        # quick indexing.
        werewolf_kill_list = []
        werewolf_kill_failures = []
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
            else:
                werewolf_kill_failures.append(victim)
        await self.werewolf_kill(guild_id, werewolf_kill_list, werewolf_kill_failures)
    
    # This function is called when a werewolf picks someone to kill. Werewolf
    # kills are fairly nuanced, so it might help to have a 2-input NN with a
    # few layers and a sigmoid activation function to train it against what you'd
    # decide to be "kills," but this needs lots of data, and will probably slow
    # down the overall speed of the program.
    def update_werewolf_victims(self, guild_id, werewolf_id, target_number):
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
            return True
            
    
    # Similar to killing victims, but medics and patients, not werewolves and
    # victims.
    def save_patients(self, guild_id, medic_id, target_number):
        patient_id = self.target_list[guild_id]["target_ids"][target_number]
        # Pushing the new vote into the array. It should update everytime, so
        # will only keep your last vote.
        self.target_list[guild_id].update({"saves": {medic_id: patient_id}})
        # Checks if the total number of votes match the number of live medics
        if len(self.target_list[guild_id]['saves']) == self.bot.game_list[guild_id]["player_numbers"]["medics_live"]:
            # Setting a boolean so that we can really easily check if all the 
            # roles have finished their night-time turn.
            return True
    
    async def end_voting(self, guild_id):
        kill_details = self.kill_message.pop(guild_id, None)
        # Just checking that the kill dictionary exists. Prevents a whole host
        # of errors flooding the log if this isn't here - also helps me more
        # easily identify the server causing the issue.
        if kill_details == None:
            print('Error occured in server {}: No kill dictionary found to remove.'.format(guild_id))
        else:
            # Quick pull of player details, makes it easier to read.
            PlayerID = kill_details["player_to_kill_id"]
            PlayerName = kill_details["player_to_kill_name"]
            # Gets the embed and if a kill has occurred.
            embed, Death = self.bot.VoteText.Lynch(PlayerName, kill_details)
            # Sending the embed asynchronously while deciding if the game is 
            # going to end. Having this here speeds the initial kill string up
            # so it doesn't interfere with the other bits of text.
            guild = self.bot.get_guild(guild_id)
            general_channel = guild.get_channel(self.bot.game_list[guild_id]["channel_ids"]["general"])
            await general_channel.send( embed = embed )
            if Death:
                # Kills player - Can end game here if needed!
                game_end, werewolf_victory = await self.kill_player(guild_id, PlayerID)
                # Only one iteration of this will happen, so no need to save the
                # value of game_end earlier.
                if game_end:
                    await self.game_end(guild_id, werewolf_victory)
                    
    
    @commands.command(help = "This command starts the game properly - once all players have joined, and `/ready` has been invoked, this command can be called to begin the night phase.")
    async def start(self, ctx):
        # Checks that this game is valid to start, and presents some error text
        # if it's found to not be the case.
        if await self.bot.PlayerChecks.ReadyToStartGame(ctx):
            # Retrieving channels early to see if this fixes a bug.
            guild = self.bot.get_guild(ctx.guild.id)
            # Getting the various channels that private messages need to be sent to.
            GeneralChannel = guild.get_channel(self.bot.game_list[ctx.guild.id]["channel_ids"]["general"])
            WerewolfChannel = guild.get_channel(self.bot.game_list[ctx.guild.id]["channel_ids"]["werewolf"])
            MedicChannel = guild.get_channel(self.bot.game_list[ctx.guild.id]["channel_ids"]["medic"])
            DetectiveChannel = guild.get_channel(self.bot.game_list[ctx.guild.id]["channel_ids"]["detective"])
            # Sets the markers for detectives and medics if not present in
            # this particular game.
            if self.bot.game_list[ctx.guild.id]["player_numbers"]["detectives_live"] == 0:
                self.bot.game_list[ctx.guild.id]["turn_complete"]["detectives"] = True
            if self.bot.game_list[ctx.guild.id]["player_numbers"]["medics_live"] == 0:
                self.bot.game_list[ctx.guild.id]["turn_complete"]["medics"] = True
            if self.bot.game_list[ctx.guild.id]["player_numbers"]["werewolves_live"] == 0:
                self.bot.game_list[ctx.guild.id]["turn_complete"]["werewolves"] = True
            # Day turns to night, turn one starts, etc.
            self.bot.DetectiveClass.Investigations.update({ctx.guild.id: []})
            self.bot.game_list[ctx.guild.id]['day'] = False
            self.bot.game_list[ctx.guild.id]['turn'] = 1
            # Prep to send prompts to each night-time channel. Actual prompt for
            # the general channel also handled here.
            live_target_list = []
            live_target_id_list = []
            # Getting the status of each player, and if they're alive, moving them
            # into this list of live players.
            for key, player in self.bot.game_list[ctx.guild.id]['active'].items():
                if (player['status'] == 'alive'):
                    live_target_list.append(player['name'])
                    live_target_id_list.append(key)
            self.target_list.update({ctx.guild.id: {"names": live_target_list,
                                                    "target_ids": live_target_id_list,
                                                    "saves": {},
                                                    "investigations": 0,
                                                    "votes": {}}})
            # Getting the actual embedded text for each channel. The channels
            # are retrieved earlier to prevent some weird ASYNCIO bug...
            GeneralEmbed, WerewolfEmbed, MedicEmbed, DetectiveEmbed = self.bot.VoteText.NightPrompts(live_target_list, True)
            try:
                await GeneralChannel.send( embed = GeneralEmbed )
                await WerewolfChannel.send( embed = WerewolfEmbed )
                await MedicChannel.send( embed = MedicEmbed )
                await DetectiveChannel.send( embed = DetectiveEmbed )
            except discord.Forbidden as Error:
                print("Could not send message in {} due to {}".format(ctx.guild.name, Error))
        
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
                                    if person.display_name in kill_list:
                                        kill_list.remove(person.display_name)
                                    # Append player to appropriate vote list.
                                    if person.display_name not in no_kill_list:
                                        no_kill_list.append(person.display_name)
                        await react.remove(person)
                        # Updates the screen to show how many votes have been
                        # cast, and how many should be cast in total.
                        total_votes = len(kill_list) + len(no_kill_list)
                        await react.message.edit( embed = self.bot.VoteText.EditNomination(guildID, total_votes) )
                self.kill_message[guildID].update({"vote_kill": kill_list})
                self.kill_message[guildID].update({"vote_no_kill": no_kill_list})
                # Check if the total number of votes now matches the total
                # number of live players in the game.
                if self.bot.game_list[guildID]['player_numbers']['alive'] == (len(self.kill_message[guildID]['vote_no_kill']) + len(self.kill_message[guildID]['vote_kill'])):
                    # Gets the channel ID using the rection, and sends it
                    # on through to the end_voting parameter.
                    self.bot.VoteText.RemoveNomination(guildID)
                    await self.end_voting(guildID)
                    if react.message.guild.id in self.bot.game_list:
                        if self.bot.game_list[react.message.guild.id]["playing"] == True:
                            await self.set_night(react.message.guild)
                pass
            
    @commands.command(help = '`/investigate` lets the detectives check if a player is of a particular alignment, but not their specific roles.')
    async def investigate(self, ctx, *arg):
        # First, catches any invalid player who's somehow entering commands in
        # the game/server. This is repeated across most command-modules, but is
        # not built-into the seperate checks just to keep things a bit more 
        # visible here.
        if await self.bot.PlayerChecks.IsValidPlayer(ctx):
            # Now ensures that the player mentioned is making a valid werewolf
            # action.
            if await self.bot.PlayerChecks.IsValidDetective(ctx):
                if await self.bot.DetectiveClass.CheckSelection(ctx, arg, self.target_list[ctx.guild.id]["names"]):
                    # First pulls the player ID, and the name of the player that
                    # has been chosen.
                    TargetID = self.target_list[ctx.guild.id]["target_ids"][int(arg[0]) - 1]
                    # Uses the Boolean return from the SendInvestigationResults
                    # function to set the check for the detectives having completed
                    # their night phase.
                    self.bot.game_list[ctx.guild.id]["turn_complete"]["detectives"] = await self.bot.DetectiveClass.SendInvestigationResults(ctx, TargetID)
                    # This function returns True when all the markers have been 
                    # set to true. Then ends the night phase by calculating kills 
                    # and generating some text.
                    if self.check_turns_complete(ctx.guild.id):
                        await self.end_night_phase(ctx.guild.id)
                        pass
            
    @commands.command(name = "save", help = '`/save` allows a medic to save a player from inevitable death at the hands of the brutal werewolves.')
    async def save(self, ctx, *arg):
        # First, catches any invalid player who's somehow entering commands in
        # the game/server. This is repeated across most command-modules, but is
        # not built-into the seperate checks just to keep things a bit more 
        # visible here.
        if await self.bot.PlayerChecks.IsValidPlayer(ctx):
            # Now ensures that the player mentioned is making a valid werewolf
            # action.
            if await self.bot.PlayerChecks.IsValidMedic(ctx):
                if await self.bot.MedicClass.CheckSelection(ctx, arg, self.target_list[ctx.guild.id]["names"]):
                    # FIX THIS SOON.Hah
                    self.bot.game_list[ctx.guild.id]["turn_complete"]["medics"] = self.save_patients(ctx.guild.id, ctx.author.id, int(arg[0]) - 1)
                    # This function returns True when all the markers have been set to
                    # true. Then ends the night phase by calculating kills and generating
                    # some text.
                    if self.check_turns_complete(ctx.guild.id):
                        await self.end_night_phase(ctx.guild.id)
                            
    @commands.command(name = "vote", help = "`/vote` allows you to nominate a player to be killed during the day phase. Enter `/vote` and then mention a target player using `@`.")
    async def vote(self, ctx, *arg):
        # First, catches any invalid player who's somehow entering commands in
        # the game/server. This is repeated across most command-modules, but is
        # not built-into the seperate checks just to keep things a bit more 
        # visible here.
        if await self.bot.PlayerChecks.IsValidPlayer(ctx):
            # Second check makes sure that the vote is being performed correctly.
            # For more info see the PlayerChecks class.
            Nomination = ctx.message.mentions
            if await self.bot.PlayerChecks.IsValidVote(ctx, Nomination):
                message = await ctx.send(embed = self.bot.VoteText.Nomination(ctx.guild.id, Nomination[0].mention, Nomination[0].display_name, ctx.author.mention, self.bot.game_list[ctx.guild.id]["player_numbers"]["alive"], 0))
                await message.add_reaction('\u2705')
                await message.add_reaction('\u274e')
                # Populates an interim storage solution - stores the message
                # id within the guild, and keeps details about the player to 
                # be killed, and who has voted to kill or not kill.
                message_info = {message.guild.id: {"message": message.id,
                                                   "player_to_kill_id": Nomination[0].id,
                                                   "player_to_kill_name": Nomination[0].display_name,
                                                   "vote_kill": [],
                                                   "vote_no_kill": []}}
                self.kill_message.update(message_info)
            
        
    @commands.command(help = "`/kill` let you nominate players to kill. Follow the instructions in the game dialogue to kill players.")
    async def kill(self, ctx, *arg):
        # First, catches any invalid player who's somehow entering commands in
        # the game/server. This is repeated across most command-modules, but is
        # not built-into the seperate checks just to keep things a bit more 
        # visible here.
        if await self.bot.PlayerChecks.IsValidPlayer(ctx):
            # Now ensures that the player mentioned is making a valid werewolf
            # action.
            if await self.bot.PlayerChecks.IsValidWerewolf(ctx):
                # Legacy code from here, modify as needed.
                if await self.bot.WerewolfClass.CheckSelection(ctx, arg, self.target_list[ctx.guild.id]['names']):
                    self.bot.game_list[ctx.guild.id]["turn_complete"]["werewolves"] = self.update_werewolf_victims(ctx.guild.id, ctx.author.id, int(arg[0]) - 1)
                    # This function returns True when all the markers have been set to
                    # true. Then ends the night phase by calculating kills and generating
                    # some text.
                    if self.check_turns_complete(ctx.guild.id):
                        await self.end_night_phase(ctx.guild.id)
                            
                           
def setup(bot):
    bot.add_cog(turns(bot))