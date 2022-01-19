import discord
from discord.ext import commands
from bot import Bot
import giphy_client
import config


class TestCog(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command()
    async def test(self, ctx: commands.Context, q: str):
        """Just for some tests"""
        await ctx.send(
            embed=discord.Embed(
                title="Test Completed UwU"
            ).set_image(url="https://giphy.com/gifs/uwu-cafeilustrando-May0SdjFNSrckK7LO9")
        )

def setup(bot: Bot):
    bot.add_cog(TestCog(bot))