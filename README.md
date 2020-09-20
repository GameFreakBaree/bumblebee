# Bumblebee
Bumblebee is a bot designed for moderation and leveling. We also made the bot 100% free for everyone to use. Once we reach 500 guilds we will make a premium bot.

## Commands
### Commands for Everyone
* **b!help** - Displays this Embed.
* **b!ping** - Get the ping in milliseconds of the bot.
* **b!info** - Get all the information about the bot.
* **b!invite** - Get an invite to add the bot.
* **b!leaderboard** - Get a leaderboard with the most active users'.
* **b!rank \<name>** - Returns which level you are and the messages count.

### Commands for users' with MANAGE_SERVER permission
* **b!kick \<name> [reason]** - Kick a user from the server.
* **b!silentkick \<name> [reason]** - Kick a user without sending a DM.
* **b!ban \<name> [reason]** - Ban a user permanently.
* **b!silentban \<name> [reason]** - Ban a user permanently without sending a DM.
* **b!unban \<name>** - Unban a user from the server.
* **b!tempban \<name> [reason]** - Ban a user temporarily from the server..
* **b!mute \<name> [reason]** - Mute a user (must have a valid `Muted` role).
* **b!unmute \<name>** - Unmute a user if they have the Muted role.
* **b!tempmute \<name> [reason]** - Temporarily mute a user.
* **b!clear \<name>** - Clear up to 125 messages at a time.
* **b!warn \<name> [reason]** - Warn a user with a reason.
* **b!config \<setting> [value]** - Configurate the bot however you like.

### Commands for the Owner of the guild
* **c!resetall** - Remove all data from the bot in the guild.
* **b!resetlevels** - Remove all level data from the bot in the guild.

## Config (c!config)
* **c!config** - See all possible commands in config.
* **b!config command <command> <enable/disable>** - Enable/Disable any command you want. [Default: enable]
* **b!config maxlevel <1-999>** - Sets the maximum level a user can be. [Default: 99]
* **b!config setxp <min/max> <0-99>** - Change the maximum and minimum XP a user can get for each message. [Default: min=1, max=5]
* **b!config setcooldown <30-120>** - Set the cooldown between counting the XP in 2 messages. [Default: 60]

***Possible Commands:*** ban, tempban, unban, mute, tempmute, unmute, kick, clear, warn, automoderator, levels
