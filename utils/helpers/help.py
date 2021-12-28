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
        `tictactoe` - Play a game of tic-tac-toe with yourself, Multiplayer soon!""",
    "Config": """
        Configure the Bot for the server!

        `changeprefix` - Change the bot's prefix for the server
        `ticket setup` - Setup ticket system for the server
        `settings` - View the bot's setting for the server""",
    "Misc": """
        Miscellaneous bot commands!
        
        `botinfo` - Bot Stats
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
        `nuke` - Deletes all messages of a channel""",
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
        `ticket role remove` - Removes a role from the ticket"""
}

def Help_Embed():
    em = discord.Embed(
        title="**__Yuki ✨ Help!__**",
        description=f"""
        > Hey, I am Yuki ✨ a multipurpose discord bot.
        The bot includes many features in various topics such as:
        **Fun, Misc, Utility and *MUCH MORE IN PROGRESS!***
        
        Now I am open source on [github](https://github.com/27Saumya/Yuki), you may contribute in making me 
        and submitting a pull request. If you don't know how to code please give a star to the [repository](https://github.com/27Saumya/Yuki)!
        
        > To view more about me use `+botinfo`
        > Invite me using the `invite` command or clicking on the button below!
        
        > What's New:
        - Added `_` option in `changeprefix`. You can use `_` that means the `_` will be considered as a space.\nSo that means now your prefix can have spaces too!

        **HOPE YOU HAVE GREAT TIME USING ME!**""",
        color=discord.Color.embed_background(theme="dark")
    ).set_footer(text="Use help [command] or help [category] for more information | <>: required | []: optional")
    return em