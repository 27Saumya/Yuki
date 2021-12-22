import discord
from discord.ext import tasks, commands
from discord.commands import permissions, Option, slash_command
import requests


class CovidCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    



def setup(bot):
    bot.add_cog(CovidCog(bot))