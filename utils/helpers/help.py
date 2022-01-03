import discord

cog_help = {
    "Fun": """
        Fun Commands!

        `8ball` - Ask me something
        `akinator` - Play an akinator game
        `beer` - Have a beer with yourself or someone
        `coinflip` - Flip a coin
        `nitro` - Get nitro
        `gif` - Search some GIFs
        `gayrate` - Check yours or someone's gayrate
        `hug` - Hug someone
        `kiss` - Kiss someone
        `marry` - Marry someone
        `slap` - Slap someone
        `pat` - Pat someone
        `tictactoe` - Play a game of tic-tac-toe with yourself, Multiplayer soon!
        `zerotwo` - Get a random zerotwo gif! <:zerolove:920425612613660753>""",
    "Config": """
        Configure the Bot for the server!

        `changeprefix` - Change the bot's prefix for the server
        `ticket setup` - Setup ticket system for the server
        `settings` - View the bot's setting for the server""",
    "Misc": """
        Miscellaneous bot commands!
        
        `botinfo` - Check the bot stats
        `help` - Stuck? Check it out
        `invite` - Invite the bot to your server!""",
    "Info": """
        Information related commands!
        
        `covid global` - View global covid-19 stats
        `covid country` - View a specific country's covid-19 stats
        `google` - Search Google <:google:917143687870414878>
        `wikipedia` - Search Wikipedia""",
    "Moderation": """
        Mod related commands
        `nuke` - Deletes all messages of a channel
        `purge user` - Purges messages of a user from the channel
        `mute` - Timeout/Mute a user in the server
        `unmute` - Unmute a user in the server""",
    "Utility": """
        Basic Miscellaneous and Utility commands!
        
        `avatar` - View someone's avatar
        `speedtest` - Check the bot's connection speed
        `youtube download`- Download a youtube video (Currently Closed)""",
    "Tickets": """
        Ticket related commands!
        
        `ticket` - View the command group info
        `panel` - View the command group info
        `ticket reset` - Reset the ticket count of the server
        `ticket close` - Closes the ticket
        `ticket add` - Adds a user to the ticket
        `ticket remove` - Removes a user from the ticket
        `ticket role add` - Adds a role to the ticket
        `ticket role remove` - Removes a role from the ticket""",
    "Music": """
        Music related commands!
        
        `play` - Play a song
        `disconnect` - Disconnects the bot from the voice chat and delete the current queue
        `pause` - Pause the current song
        `resume` - Resume the current song
        `seek` Go to a specific number of seconds in the song
        `skip` Skip the current song and play the next song
        `now` - Shows the currently playing song
        `save` - DMs you the currently playing song
        `queue` - View the queue of songs in the current session
        `volume` - Adjust the volume
        `shuffle` - Shuffle the queue
        `repeat` - Repeat the current song
        `remove` - Remove a song from the queue
        `equalizer` - Equalize the player: bass and much more"""
}

def Help_Embed():
    em = discord.Embed(
        title="**__Yuki ✨ Help!__**",
        description=f"""
        **Hey, I am Yuki ✨ a multipurpose discord bot.**
        The bot includes many features in various topics such as:
        **Fun, Misc, Utility and *MUCH MORE IN PROGRESS!***
        
        Now I am open source on [github](https://github.com/27Saumya/Yuki), you may contribute in making me 
        and submitting a pull request. If you don't know how to code please give a star to the [repository](https://github.com/27Saumya/Yuki)!
        
        To view more about me use `+botinfo`
        Invite me using the `invite` command or clicking on the button below!
        
        **What's New:**
        - Added `_` option in `changeprefix`. You can use `_` that means the `_` will be considered as a space.
        So that means now your prefix can have spaces too!

        - Music commands are now available! Use the `play` command to play a song more command details are avaialble by either doing `help [command] or by clicking in the **Music** option from the seclect menu given below!

        **HOPE YOU HAVE GREAT TIME USING ME!**""",
        color=discord.Color.embed_background(theme="dark")
    ).set_footer(text="Use help [command] for more info | <>: required | []: optional")
    return em