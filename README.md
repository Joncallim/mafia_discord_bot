# Jacob 
## A Werewolf Bot Written for Discord in discord.py
### Version 0.9

---
#### Yet Another Werewolf Bot...
I decided that there weren't enough Werewolf Bots out there, so I've made my own Discord bot for werewolf. If you just want to jump in, you can add it to a server [here](https://discord.com/api/oauth2/authorize?client_id=710860464183050361&permissions=8&scope=bot).

At the behest of a good friend, I've had to name my bot - apparently "werewolf-discord-bot-0.845b" didn't cut it. So, here's Jacob, a brilliant narrator who will help you and your friends play a game of werewolf!

I've meant for this game to be played by a group of friends on video/voice chat, so you should really think about adding your own stories to the ones that have been crafted here! Thanks to the very talented Beth Davis ([Click here to follow her on Instagram!!!](https://www.instagram.com/beth.wtf15/?hl=en)), there are now some new bits of narration included for the Werewolf kill/no-kill/save sequences!

Currently deployed on Google Cloud Compute, if you run into any issues please leave a comment on the github server or drop me a DM, my Discord ID is #6991. 

This is very much a personal project, and I've poured *quite* a lot of time into just for the heck of it, so I'd really appreciate any comments! (Especially if there's a way to improve it, bugs or whatever - I've heard that a big github profile is good for finding jobs).

---

#### Play

Play is started by the command `/werewolf`, and the bot will prompt you to opt into a game by clicking on emoji reaction. Once everyone who's playing has opted in, you can start the game with `/ready`, and follow the on-screen prompts.

You'll be put into an appropriate secret group, based on where you've been assigned to. These are only text, so you should stay in your main voice channel and keep chatting.

Play is divided into two phases: Day and Night. In the day phase, you vote as a group to lynch a player. You can do this by typing `/vote @player`, with a `mention` to nominate a lynch. Note that this can only be done **once** per day phase, so take your time about nominating players. You'll vote as you did with opting into the game, by clicking on reaction buttons.

Votes are made public once they're successful or unsuccessful, so werewolves can't just immediately nominate someone and try to lynch him.

---
#### Player Roles:

Players are divided into 2 general alignments:

1. Humans, which have the collective goal of eliminating the werewolves via the daily lynch mob.
2. Werewolves, which have the goal of killing off all humans by thinning their ranks at night.

Current roles (and I *am* planning to add more in the near future):

1. **Villager**
	- Run-of-the-mill human, doesn't really do much, but will add some features in the future to make your night phases a bit more interesting. Everyone who doesn't have a special role will be assigned to "villager".
2. **Werewolf**
	- Werewolves get to vote for who they want to kill during the night. They appear in the ratio: : 1/3 of players, rounded off.
	- During the night phase, werewolves get to vote on who to kill. This works like so for *live* werewolves:
		- **> 3 werewolves**: At least 3 votes to kill (this was not made a majority vote so that the game moves along).
		- **2 - 3 werewolves**: 2 votes to kill.
		- **1 werewolf**: You know how this one goes...
3. **Medic**
	- Medics save players (you have no idea who's going to be attacked, so it's about trying to save players you think are close to being killed by a werewolf -- like if someone reveals he's the detective!)
	- All medic saves count, so if there are 2 medics, both people saved by the medics will not die.
	- There will be the following player ratio: 1/5 of players, rounded down.
4. **Detective**
	- Detectives can investigate their fellow players during the night phase. Detectives currently can know who their fellow detectives are, but will get the results of an investigation in a private chat.
	- There will be the following player ratio: 1/5 of players, rounded down.

Once you have all your players voted to join, type `[/ready]` to ready up. Roles will then be assigned, and if you're a werewolf, you'll be put into a `werewolves` channel that nobody else can see.

Due to Discord Permissions, the channel owner will always be able to see this, and the text inside of it, so if you want to have a good game, set up a channel with a dummy account and add the bot to that channel, then play on that channel!

Once everyone has their roles and you're ready to start playing, type `[/start]`. The first night will then start, so any discussion would have had to happen before that. The werewolves will then decide who to kill.

---
#### Most Recent Update (30 May 2020):
- Converted all the text from `code` format to Embedded text, making for much prettier text.
- Added a huge wall of text all over the bot, fairly visible when you get it open.
- Re-worked much of the classes so that text and role functions are now distributed to different classes - will make for easier upgrades and reworks.
- Moved checks out into a seperate `PlayerChecks` class, which allows the code to be much more readable in the main function since it's all been moved into a single column. 
- Bug fix to do with `/save` -> `kill` not working but `kill` > `save` working.
- Added administrator check so only I can reload Cogs.
- Lots of bug fixes all around, particularly with low-player-count startups.


---
#### Futures List:
- Add option to let detectives not know who each other other.
- Balance fixes after trail runs.
- Speed optimisations.

---
#### Links: 

- [Add to server](https://discord.com/api/oauth2/authorize?client_id=710860464183050361&permissions=8&scope=bot)
- [discord.py documentation](https://discordpy.readthedocs.io/en/latest/index.html)
- [Wikipedia page for Mafia](https://en.wikipedia.org/wiki/Mafia_(party_game))