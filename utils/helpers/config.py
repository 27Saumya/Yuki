import discord
from discord.ext import commands
from bot import Bot


def get_prefix(bot: Bot, message):
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