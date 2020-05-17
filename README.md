# Werewolf Bot
## Written for Discord in discord.py

---
####Yet Another Werewolf Bot...
I decided that there weren't enough Werewolf Bots out there, so I've made my own Discord bot for werewolf. This was a bit of a handling-data challenge, and this bot will work across multiple Discord servers simultaneously once I deploy it for actual use. 

Current roles are (and I *am* planning to add more in the near future):

1. Villager
2. Werewolf

Ratios are:

- 8 or more players: 1/3 of the players will be werewolves.
- 5 - 7 players: 2 werewolves
- 4 or fewer: 1 werewolf

Fairly simple play, initialise by typing `[/werewolf]`, and follow the on-screen prompts.

Once you have all your players voted to join, type `[/ready]` to ready up. Roles will then be assigned, and if you're a werewolf, you'll be put into a `werewolves` channel that nobody else can see.

Due to Discord Permissions, the channel owner will always be able to see this, and the text inside of it, so if you want to have a good game, set up a channel with a dummy account and add the bot to that channel, then play on that channel!

Once everyone has their roles and you're ready to start playing, type `[/start]`. The first night will then start, so any discussion would have had to happen before that. The werewolves will then decide who to kill.

---
####Lynching:

If you're a werewolf, you'll have the option to kill live players. You can do this by typing `/kill 1` for a list of players that will be shown to you. As a werewolf, you only have 1 vote, and voting to kill multiple times will just overwrite your previous vote.

Majorities to kill are:

- 4 or more live werewolves: 3 or more votes to kill.
- 2 - 3 live werewolves: 2 or more votes to kill
- 1 werewolf... Fairly obvious.

During the day phase, you can type `[/kill @player]`, with a `mention` to nominate a lynch. Note that this can only be done **once** per day phase, so take your time about nominating players. You'll vote as you did with opting into the game, by clicking on reaction buttons.

Votes are made public once they're successful or unsuccessful, so werewolves can't just immediately nominate someone and try to lynch him.

---
####Planned Work:
- Introduce `Medic` class
- Tidy up this README
- Make nicer text for the bot.

---
####Links: 

- [Add to server](https://discord.com/api/oauth2/authorize?client_id=710860464183050361&permissions=8&scope=bot)
- [discord.py documentation](https://discordpy.readthedocs.io/en/latest/index.html)
- [Wikipedia page for Mafia](https://en.wikipedia.org/wiki/Mafia_(party_game))