# Werewolf Bot Changelog
## Written for Discord in discord.py
---
### 2 June 2020:

- Added:
	- `/echo` command to echo admin messages across all "general" channels that the bot has been added to. Useful to push updates and all.
	- Jacob will now create a general Village-ville voice and text channel, and invite all players to it. These are set to read-only by default.
	- New auto-mute incorporated. Jacob will mute all non-active players and dead players. Non-active players will not get to see the specialised chats, but dead players will have the other specialised chats revealed on death (Possible fix for next push).

- Removed:
	- Test command that I left in the code by accident.

- Changes:
	- Changed some message sends to `try/except` to catch any exceptions that might show up. Should not happen, but it's in there just in case.
	- Now sends a message on death so you know that you've been muted.

---
### 30 May 2020:

This update was mostly changing the text format to embedded, and fixing the 3 million bugs that appeared because of that.

- Converted all the text from `code` format to Embedded text, making for much prettier text.
- Added a huge wall of text all over the bot, fairly visible when you get it open.
- Re-worked much of the classes so that text and role functions are now distributed to different classes - will make for easier upgrades and reworks.
	- Moved checks out into a seperate `PlayerChecks` class, which allows the code to be much more readable in the main function since it's all been moved into a single column. 
	- Added a file containing all the various `TextGenerator` classes, which hold the various bits of information. This includes a pretty cool randomised text returner for long sections of formatted text without having to piece them together bit by bit.
	- `RoleClasses` file for a seperate file for each Role - will allow much simpler extension of features by class 
- Bug fix to do with `/save` -> `kill` not working but `kill` -> `save` working.
- Added administrator check so only I can reload Cogs.
- Lots of bug fixes all around, particularly with low-player-count startups.

---
### 21 May 2020:

- **Medic** and **Detective** classes added to the game (See README)!
- Added a daily loop to clean any idle server data from the bot's memory.
- Reworked the kill process so it takes medics into account.
- Removed various bugs and generalised the code a little more so that future classes can be added more easily.

---