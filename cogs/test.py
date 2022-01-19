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
        giphy = giphy_client.DefaultApi()
        result = giphy.gifs_search_get(config.GIPHY_API_KEY, q, limit=50)
        await ctx.send(f"```{str(result).strip()}```")

def setup(bot: Bot):
    bot.add_cog(TestCog(bot))