import discord
from discord.ext import commands

POWERED_BY_GIPHY = "https://images-ext-1.discordapp.net/external/FW8Emlcxhqqi1YsZoXVHfC6c58tPptohhqNz0GNmdYQ/https/image.ibb.co/b0Gkwo/Poweredby_640px_Black_Vert_Text.png"

def get_prefix(bot, message):
    """Gets the prefix for the server"""
    try:
        bot.dbcursor.execute('SELECT prefix FROM guilds WHERE guild_id=?', (message.guild.id,))
        prefixes = bot.dbcursor.fetchone()
        if not prefixes:
            return "+"
        else:
            bot.dbcursor.execute('SELECT * FROM guilds WHERE guild_id=?', (message.guild.id,))
            prefix = bot.dbcursor.fetchone()
            return commands.when_mentioned_or(prefix[1])(bot, message)
    except:
        return "+"

def giphyUrl(id: str):
    return f"https://media.giphy.com/media/{id}/giphy.gif"