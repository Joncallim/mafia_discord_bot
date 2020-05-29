#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 29 10:57:36 2020

@author: Jonathan

These are the basic text chunks that will be used to print errors and admin bits
in the bot. Colours are defined by class (ErrorTextGenerator, etc.), and they 
are not really commented since you can basically read what each message is for
from the name and the string.

The advantage of this file is that all the text is fairly streamlined, so any
edits can be done in this single file instead of having to scroll through lots
of harder-to-read code. (I like to think my code is readable though).

The text inside "Narration" was written by the very talented Beth Davis! (Credit
where credit is due!) More links up in the README.
"""
# "day": 0xF7DC6F,
# "night": 0x154360,
# "werewolf": 0xE74C3C,
# "villager": 0x7DCEA0,
# "detective": 0xA569BD,
# "medic": 0xDC7633}

import discord
import random
        

class Narration():
    def __init__(self, *args, **kwargs):
        pass
    
    def kill_1(self, Name):
        return f"{Name} leaves their home in search of their love who promised them to a night of pleasures. But they never reached their lovers door, for with one fell swoop, {Name} was gathered up into the ferocious maw of the werewolf crouching on the rooftop awaiting its meal. All that was left was {Name}’s right hand, known well by their fair love."
    def kill_2(self, Name):
        return f"{Name} eagerly leaves their home in search of the outhouse. Their lantern clangs by their side as they waddle through the door, but they are soon interrupted by a looming shadows from above, their entrails splattered across the walls of the fateful outhouse."
    def kill_3(self, Name):
        return f"{Name} finds their way onto their roof for a look into the stars. Tracing the constellations with their fingers, they don’t notice the light from the moon being blocked out by the monster that lurks nearby. With nary a sound, {Name}’s life is ended as the stars blink down from the heavens."
    def kill_4(self, Name):
        return f"{Name} is sleeping soundly at their desk, an unfinished work of genius smudged against their cheek. A hairy arm reaches in through the open window, talons glinting in the moonlight, and snatches the body into the night. Shame, they only had another paragraph to go."
    def kill_5(self, Name):
        return f"{Name} cannot sleep, the ceiling taunting them with the promise of slumber. {Name} turns onto their right side and is greeted by two glinting yellow eyes. Needless to say, they got to sleep eventually."
    
    def GetKillText(self, Name):
        Choices = {1: self.kill_1(Name), 2: self.kill_2(Name), 3:self.kill_3(Name), 4:self.kill_4(Name), 5:self.kill_5(Name)}
        RandomPick = random.randint(1,5)
        return Choices.get(RandomPick, lambda: "Error - Contact me on discord at #6991 if you encounter this error!")
    
    def nothing_1(self, Name):
        return f"{Name} leaves their home in search of their love who promised them to a night of pleasures. Arriving at the house, with a werewolf lurking nearby, {Name} dons an abhorrent perfume alleged to be his lovers favourite. But neither their lover, nor the werewolf, could bear the stench. {Name} leaves dejected; not aware the cursed perfume saved their life that night."
    def nothing_2(self, Name):
        return f"{Name} eagerly leaves their home in search of the outhouse. Their lantern clangs by their side as they waddle through the door, but they are soon interrupted by a looming shadows from above. With a cry, {Name} throws yesterday’s bad meat up at the monster. The werewolf cries out as {Name} waddles away, screaming bloody murder."
    def nothing_3(self, Name):
        return f"{Name} finds their way onto their roof for a look into the stars. Tracing the constellations with their fingers, they only notice the monster prowling towards them when the beast disappears through the roof and into {Name}’s front room. As the werewolf attempts to scramble back up to its prey, {Name} gets away."
    def nothing_4(self, Name):
        return f"{Name} is sleeping soundly at their desk, an unfinished work of genius smudged against their cheek. A hairy arm reaches in through the open window, talons glinting in the moonlight, when {Name} snaps awake with a triumphant “aha”! This turns into an “aah!” and {Name} buries their silver quill into the monster’s arm. The werewolf flees, whimpering as it’s flesh burns. {Name}, however, tries to find something to finish their masterpiece with."
    def nothing_5(self, Name):
        return f"{Name} cannot sleep, the ceiling taunting them with the promise of slumber. {Name} turns onto their right side and is greeted by two glinting yellow eyes. Unfortunately for the werewolf, {Name} had been waiting for this moment. Pulling the shotgun from under the covers, {Name} hits the monster square between the eyes. As the beast lumbers away, their wound already healing, {Name} reloads the shotgun…like a badass."
    
    def GetNothingText(self, Name):
        Choices = {1: self.nothing_1(Name), 2: self.nothing_2(Name), 3:self.nothing_3(Name), 4:self.nothing_4(Name), 5:self.nothing_5(Name)}
        RandomPick = random.randint(1,5)
        return Choices.get(RandomPick, lambda: "Error - Contact me on discord at #6991 if you encounter this error!")
    
    def save_1(self, Name):
        return f"{Name} leaves their home in search of their love who promised them to a night of pleasures. Their journey is interrupted by a lumbering beast. Taking a swipe at {Name}, the werewolf tears at their chest. But the allure of their sweet love pushes {Name} on. Barely able to outrun the monster, {Name} stumbles into the arms of a stranger. {Name} wakes up wounded but bound…unfortunately for {Name}, not in the sexy way."
    def save_2(self, Name):
        return f"{Name} eagerly leaves their home in search of the outhouse. Their lantern clangs by their side as they waddle through the door, but they are soon interrupted by a looming shadows from above. {Name} ducks just in time but their back is ripped to shreds on the werewolf’s claws. The werewolf tumbles into the outhouse and flees covered in {Name}’s leavings. {Name} wakes up with their trousers down outside the outhouse, their back patched up and aching."
    def save_3(self, Name):
        return f"{Name} finds their way onto their roof for a look into the stars. Tracing the constellations with their fingers, they only notice the monster prowling towards them when the beast disappears through the roof and into {Name}’s front room. But the beast catches {Name}’s leg on the way down, pulling a good deal of flesh from the bone. {Name} hears gun shots as they’re pulled to one side. Awaking the next morning, {Name}’s leg is bandaged, and a handful of painkillers left on their bedside table."
    def save_4(self, Name):
        return f"{Name} is sleeping soundly at their desk, an unfinished work of genius smudged against their cheek. A hairy arm reaches in through the open window, talons glinting in the moonlight, when {Name} snaps awake with a triumphant “aha”! This turns into an “aah!” and {Name} and goes to gather up the papers and run. This delay allows the werewolf to slash at {Name}’s shoulder and blood spills onto the masterpiece. As name mourns the work, a gunshot rings out. As {Name} sobs into their papers, a stranger pulls their bloody shoulder back together and leaves without a sound."
    def save_5(self, Name):
        return f"{Name} cannot sleep, the ceiling taunting them with the promise of slumber. {Name} turns onto their right side and is greeted by two glinting yellow eyes. With a flash of white, {Name} sees red as pain sears through their body. Their door opens wide and bullets fly. {Name} drops to the floor and wakes up in bed the next afternoon. Best nights sleep {Name} has had in a while."
    
    def GetSaveText(self, Name):
        Choices = {1: self.save_1(Name), 2: self.save_2(Name), 3:self.save_3(Name), 4:self.save_4(Name), 5:self.save_5(Name)}
        RandomPick = random.randint(1,5)
        return Choices.get(RandomPick, lambda: "Error - Contact me on discord at #6991 if you encounter this error!")
    
''' Text generator for the voting section. Given it's own class just beause.
Also includes the night-and-day-time text generators.'''
class VoteTextGenerator():
    def __init__(self, *args, **kwargs):
        self.colour = 0x7DCEA0
        self.NightColour = 0x154360
        self.NightScenes = ["The villagers of Village-ville go to bed and shut their doors as the night closes in, and the beasts begin to prowl outside...",
                            "Candles are lit, and the occupants of Village-ville hunker down, hoping that the creatures roaming the night will not choose their homes to attack...",
                            "As the darkness looms, the villagers disappear into their homes. Outside, creatures begin to roam the streets...",
                            "The moon rises outside, as the occupants of Village-ville huddle in their homes, praying that the beasts will not attack tonight..."]
        self.TextStorage = {}
        pass
    
    # This "nomination" is for the day-phase lynch-mob nominations. You can put
    # up a vote that will then be voted on. Text is a bit longer, thus all the 
    # add_fields you see here.
    def Nomination(self, GuildID, NominationMention, NominationName, PlayerMention, PlayersTotal, Voted):
        embed = discord.Embed(title = "You have nominated a player to be killed!",
                              description = "{} has been nominated to be lynched by {}!".format(NominationMention, PlayerMention),
                              color = self.colour)
        embed.add_field(name="What to do:",
                        value="Click on \u2705 if you'd like to vote to kill {}, or \u274e if you want to spare {}.\n\nThe game will automatically move ahead once all active players have voted.".format(NominationName, NominationName),
                        inline=False)
        embed.add_field(name="If you're {}".format(NominationName),
                        value="It's not too late! You can still desperately tell the others why you're a human and should not be put to death!",
                        inline=False)
        embed.add_field(name="Votes:",
                        value="{} players have voted out of {}".format(Voted, PlayersTotal))
        # Quick storage solution so that the embed can be reused without having
        # to pass ugly lengths of information to and fro every time. Won't really
        # affect readability.
        self.TextStorage.update({GuildID: {"NominationMention": NominationMention,
                                           "NominationName": NominationName,
                                           "PlayerMention": PlayerMention,
                                           "PlayersTotal": PlayersTotal }})
        return embed
    
    def EditNomination(self, GuildID, Votes):
        # reuses the Nomination function with the updated value, and the stored
        # names.
        return self.Nomination(GuildID,
                               self.TextStorage[GuildID]["NominationMention"],
                               self.TextStorage[GuildID]["NominationName"],
                               self.TextStorage[GuildID]["PlayerMention"],
                               self.TextStorage[GuildID]["PlayersTotal"],
                               Votes)
    
    def RemoveNomination(self, GuildID):
        self.TextStorage.pop(GuildID)
        return
    
    def Lynch(self, PlayerName, Votes):
        # Pulls the lengths of each array - just makes for slightly easier
        # reading here, in case some changes need to be made along the way.
        VotesFor = len(Votes['vote_kill'])
        VotesAgainst = len(Votes['vote_no_kill'])
        TotalVotes = VotesFor + VotesAgainst
        if VotesFor > VotesAgainst:
            embed = discord.Embed(title = "The mob has executed {}!".format(PlayerName),
                                  description = "Total Votes: {}".format(TotalVotes),
                                  color = self.colour)
            Death = True
        else:
            embed = discord.Embed(title = "The villages decided to spare {}!".format(PlayerName),
                                  description = "Total Votes: {}".format(TotalVotes),
                                  color = self.colour)
            Death = False
        if (VotesFor > 0) & (VotesAgainst > 0):
            VoteForList = "\n - ".join(Votes['vote_kill'])
            VoteForText = "\n - {}".format(VoteForList)
            embed.add_field(name="{} people voted to execute {}:".format(VotesFor,PlayerName),
                            value=VoteForText,
                            inline=False)
            VoteAgainstList = "\n - ".join(Votes['vote_no_kill'])
            VoteAgainstText = "\n - {}".format(VoteAgainstList)
            embed.add_field(name="{} people voted to spare {}:".format(VotesAgainst,PlayerName),
                            value=VoteAgainstText,
                            inline=False)
        elif VotesAgainst == 0:
            VoteForList = "\n - ".join(Votes['vote_kill'])
            VoteForText = "\n - {}".format(VoteForList)
            embed.add_field(name="Everyone voted to execute {}:".format(PlayerName),
                            value=VoteForText,
                            inline=False)
        elif VotesFor == 0:
            VoteAgainstList = "\n - ".join(Votes['vote_no_kill'])
            VoteAgainstText = "\n - {}".format(VoteAgainstList)
            embed.add_field(name="Everyone voted to spare {}:".format(PlayerName),
                            value=VoteAgainstText,
                            inline=False)
        return embed, Death
    
    def NightText(self, FirstNight):
        if FirstNight:
            GeneralEmbed = discord.Embed(title="The first night falls!",
                                  description="Everyone goes to bed, slightly afraid of what the night will bring, now that the threat of werewolves has been brought to light. Somewhere outside, a large beast begins to move...",
                                  color=self.NightColour)
            return GeneralEmbed
        else:
            
            GeneralEmbed = discord.Embed(title="Nightfall!",
                                  description=random.choice(self.NightScenes),
                                  color=self.NightColour)
            return GeneralEmbed
    
    def NightPrompts(self, TargetList, FirstNight = False):
        # Begins by sending the night prompt out, so that everyone else knows
        # that it's happening - this is placed here so that the main document
        # can be streamlined a little.
        GeneralEmbed = self.NightText(FirstNight)
        # Generates a fairly simple numbered list of players now - including all
        # live players (even yourself).
        TargetString = ""
        for i, Target in enumerate(TargetList):
            TargetString = "{} {}. {}\n".format(TargetString, i+1, Target)
        # Now generating the text for each channel, getting ready to print them
        # to each channel.
        WerewolfEmbed = discord.Embed(title="Time to hunt!",
                                      description="It is nighttime, and the werewolves have been let loose on the village!",
                                      color = self.NightColour)
        WerewolfEmbed.add_field(name="What to do:",
                                value="You can type `/kill x` to kill someone on the list of live players, where `x` is the number next to the player's name. You can also choose not to kill anyone by selecting `/kill 0`. You can re-cast your vote, but only the latest vote will be kept, and when all night-time tasks have been completed the game will automatically continue.",
                                inline=False)
        WerewolfEmbed.add_field(name="How to kill:",
                                value="Each werewolf can vote to kill different players, but you need a majority of votes (or a minimum of 3) to successfully kill a villager! You can also vote to kill werewolves, if you are so inclined.",
                                inline=False)
        WerewolfEmbed.add_field(name="Live Players:",
                                value=TargetString,
                                inline=False)
        # Embed for Medic Channel
        MedicEmbed = discord.Embed(title="Your fellow villagers are in danger!",
                                   description="It is nighttime, and the werewolves are on the hunt! Only you can save someone from certain death!",
                                   color = self.NightColour)
        MedicEmbed.add_field(name="What to do:",
                             value="You can type `/save x` to save someone on the list of live player, where `x` is the number next to the player's name. Every medic can save a seperate player. You can re-send your save, but only the latest save will be kept, and when all night-time tasks have been completed the game will automatically continue.",
                             inline=False)
        MedicEmbed.add_field(name="Live Players:",
                             value=TargetString,
                             inline=False)
        # Embed for Detective Channel
        DetectiveEmbed = discord.Embed(title="The village is asleep!",
                                       description="It is night-time, and now that everyone is asleep, you can safely investigate your fellow villagers!",
                                       color = self.NightColour)
        DetectiveEmbed.add_field(name="What to do:",
                                 value="You can type `/investigate x` to investigate someone on the list of live players, where `x` is the number next to the player's name. You will then get a DM from me (the bot) telling you that player's alignment. What you do with this information is entirely up to you. You can only do this once, so use your investigation carefully!",
                                 inline=False)
        DetectiveEmbed.add_field(name="Live Players:",
                                 value=TargetString,
                                 inline=False)
        # Sending each embed to the various private channels.
        return GeneralEmbed, WerewolfEmbed, MedicEmbed, DetectiveEmbed

''' Error Text Generator. This helps to present errors that are common throughout
the game, so they can be called multiple times. Also helps to keep all the text
in one place so that any edits can be streamlined without having to go into the
code. '''
class ErrorTextGenerator():
    def __init__(self, *args, **kwargs):
        self.colour = 0x943126
        pass
        
    def PlayerDead(self, Player):
        embed = discord.Embed(title="You're dead!",
                              description="You're dead, {}. You can't actively participate in this game now!".format(Player.mention),
                              color=self.colour)
        return embed
    
    def GenericError(self):
        embed = discord.Embed(title="It's not time to do that!",
                              description="Wait for the prompts to perform any actions!",
                              color=self.colour)
        return embed
    
    def NoGame(self, GuildName):
        embed = discord.Embed(title="No game found in {}".format(GuildName),
                              description="You haven't started the Werewolf Bot! Type `/werewolf` to get started!",
                              color=self.colour)
        return embed
    
    def GameNotStarted(self, GuildName):
        embed = discord.Embed(title="Game not found!",
                              description="A game for {} could not be found. You can start a new game by entering `/werewolf`, or end the preparation phase by entering `/ready`.",
                              color=self.colour)
        return embed
    
    def NotJoined(self, Player):
        embed = discord.Embed(title="You are not part of this game!",
                              description="You did not join the game, {}! Wait for the next game, or ask the players to restart to include you.".format(Player.mention),
                              color=self.colour)
        return embed
    
    def WrongChannel(self):
        embed = discord.Embed(title="Wrong channel!",
                              description="You cannot use that command in this channel, wait for the prompts to tell you what to do!",
                              color = self.colour)
        return embed
    
    def PlayerInWrongChannel(self, Player):
        embed = discord.Embed(title="You're not supposed to be in this channel!",
                              description="You do not have the correct role to be in this channel, {}!\n\nIf this should not have happened, please report the bug by sending an email to me at Joncallim@gmail.com or send a DM to me at #6991".format(Player.mention),
                              color = self.colour)
        return embed
    
    def TooManyNominations(self):
        embed = discord.Embed(title="Too many nominations!",
                              description="You can only nominate 1 player to be lynched. Use the `@` command to nominate a player to lynch!",
                              color = self.colour)
        return embed
    
    def NoNominations(self):
        embed = discord.Embed(title="No nomination found!",
                              description="You need to nominate a player to be lynched. Use the `@` command to nominate a player to lynch!",
                              color = self.colour)
        return embed

''' Text for various administrative tasks - starting the bot, checking if it is
active, etc. '''
class AdminTextGenerator():
    def __init__(self, *args, **kwargs):
        self.colour = 0xCCD1D1
        pass
    
    def StartUp(self, GuildName, NumberOfPlayers):
        embed = discord.Embed(title="Game starting in {}!".format(GuildName),
                              description="Click \u2705 to join the game, or \u274e to cancel.\n\nOnce all players have joined, type `/ready` to get sorted into various classes!",
                              color=self.colour)
        embed.add_field(name="About the game:",
                        value="Werewolf (also known as Mafia) is a social deduction game, first devised by Dimitry Davidoff in 1986, and modified in 1997 by Andrew Plotkin, who gave it the name 'Werewolf.' You'll probably have played this game in one form or another before, so just go along with the bot narrator and have fun as a group!",
                        inline=False)
        embed.add_field(name="The story so far:",
                        value="Werewolves! Suspicions have been raised about werewolves in the village of village-ville. But since nobody has come or gone from the village in a long long time, it has to be someone in the village...",
                        inline=False)
        embed.add_field(name="Implementation:",
                        value="The Werewolf bot will create several private rooms that you'll be sorted into (so if you're a server owner, this won't work well since you can **always** see every channel in the server!)\n\nOnce you've started the game by typing `/ready`, I strongly encourage a bit of discussion or just light-hearted banter before you begin the first night by typing `/start`.",
                        inline=False)
        embed.add_field(name="Roles and Alignments:",
                        value=" 1. Werewolves - Your goal is, quite simply, to kill everyone else and survive till the end\n 2. Villagers/Humans - Your goal is to survive, weeding out the werewolves by discussion in the day phase and lynching them (or executing them, if you prefer).\n 3. Medics (also Human) - You can **each** save 1 person from being mauled to death every night phase!\n 4. Detectives (also Human) - You can **each** make an investigation on a player during the night phase to discover their alignment.",
                        inline=False)
        embed.add_field(name="Number of Players:",
                        value=NumberOfPlayers,
                        inline=False)
        return embed
    
    def NoPermission(self, AuthorName):
        embed = discord.Embed(title="You do not have permission to execute that command.",
                              description="{} attempted to execute an administrator command!".format(AuthorName),
                              color=self.colour)
        return embed
    
    def StatusCheck(self, GuildName):
        embed = discord.Embed(title="The Werewolf Bot is active.",
                              description="Server: {}".format(GuildName),
                              color=self.colour)
        return embed
        
    def PlayerPersonalInfo(self, GuildName, Role, Alignment):
        embed = discord.Embed(title="Game Starting!",
                              description="You have joined a game in {}!".format(GuildName),
                              color=self.colour)
        embed.add_field(name="Alignment:",
                        value=Alignment,
                        inline=False)
        embed.add_field(name="Role:",
                        value=Role,
                        inline=False)
        if Role == "Villager":
            embed.add_field(name="Your job:",
                            value="Werewolves know who all other werewolves are, but they don't know if you have a special role or not! Try to find out who the werewolves are, and make your case during the day phase to lynch them!",
                            inline=False)
            return embed
        elif Role == "Werewolf":
            embed.add_field(name="Your job:",
                            value="Every night phase, you get to pick someone to kill! You need to work together as a pack, so make sure you target the same players as each other, otherwise you'll land up not killing anybody!\n\nDuring the day phase, protect each other from being lynched, and try to stay alive!",
                            inline=False)
            return embed
        elif Role == "Medic":
            embed.add_field(name="Your job:",
                            value="You get to pick someone to save from certain death during the night phase! Make sure to save anyone you think is in danger from the werewolves!",
                            inline=False)
            return embed
        elif Role == "Detective":
            embed.add_field(name="Your job:",
                            value="An **investigation** will allow you to reveal the identity of any player in the night phase! You can choose what you do with this information, and with any information about your role.",
                            inline=False)
            return embed
        else:
            print("Error found in guild: ", GuildName)
            pass
            
    def GameStarting(self, GuildName, Roles, Players):
        embed = discord.Embed(title="Game Starting in {}!".format(GuildName),
                              description="Check your DMs for your individual roles!",
                              color=self.colour)
        embed.add_field(name="Players:",
                        value = Players,
                        inline = False)
        embed.add_field(name="Villagers:",
                        value = Roles.count('Villager'),
                        inline = False)
        embed.add_field(name="Werewolves:",
                        value = Roles.count('Werewolf'),
                        inline = False)
        embed.add_field(name="Medics:",
                        value = Roles.count('Medic'),
                        inline = False)
        embed.add_field(name="Detectives:",
                        value = Roles.count('Detective'),
                        inline = False)
        embed.add_field(name="What to do now:",
                        value = "Have a bit of a discussion - talk about who's likely to be a werewolf and show off your social deductive skills! Then, when everyone is ready, type `/start` to begin the first night!",
                        inline = False)
        return embed

    def GameDeleted(self, GuildName):
        embed = discord.Embed(title = "Game Terminated",
                              description = "Memory and channels deleted from {}".format(GuildName),
                              color = self.colour)
        return embed
    
    def Victory(self, GameInfo, WerewolfVictory = True):
        if WerewolfVictory:
            embed = discord.Embed(title="Werewolf Victory!",
                                  description="Game over! Some game statistics:",
                                  color=self.colour)
        else:
            embed = discord.Embed(title="Human Victory!",
                                  description="Game over! Some game statistics:",
                                  color=self.colour)
        embed.add_field(name="Statistics:",
                        value = "Number of Turns: {}\n\nPlayers Remaining: {}\n - Werewolves: {}\n - Humans: {}\n\nTotal Players: {}\n - Werewolves: {}\n - Humans: {}".format(GameInfo["turn"],GameInfo["player_numbers"]["alive"],GameInfo["player_numbers"]["werewolves_live"],GameInfo["player_numbers"]["villagers_live"],GameInfo["player_numbers"]["total"],GameInfo["player_numbers"]["werewolves_total"],GameInfo["player_numbers"]["villagers_total"]),
                        inline = False)
        liveString = ""
        deadString = ""
        for player in GameInfo['active'].values():
            if player['status'] == "alive":
                liveString = "{} - {} ({})\n".format(liveString,
                                                     player['name'],
                                                     player['role'])
            else:
                deadString = "{} - {} ({}), Turns: {}\n".format(deadString,
                                                                player['name'],
                                                                player['role'],
                                                                player['turns'])
        # Catching an exception -- "value" in an embed field cannot be an empty
        # string, so changes this to "None" so something is shown, and the game 
        # can actually end.
        if liveString == "":
            liveString = "None"
        if deadString == "":
            deadString = "None"
        embed.add_field(name = "Live Players:",
                        value = liveString,
                        inline = False)
        embed.add_field(name = "Dead Players:",
                        value = deadString,
                        inline = False)
        embed.add_field(name = "Game deleted from memory, and channels cleared!",
                        value = "Thanks for playing! This is a personal project and is far from perfect! If you have any ideas for improvement or bugs to report, you can e-mail me at joncallim@gmail.com, or on Discord - my ID is #6991.",
                        inline = False)
        return embed
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            