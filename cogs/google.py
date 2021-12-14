import discord
from discord.ext import tasks, commands
from discord.commands import slash_command, Option
from utils.buttons import Google


class GoogleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(guild_ids=[824969244860088332, 847740349853073418, 865962392093851658, 896457384552202312, 918802666790993951], description="Google Search")
    async def google(self, ctx: commands.Context, *, 
        query: Option(str, "Type what you want to search!", required=True, default=None)):
        await ctx.respond(f"Google Result for `{query}`", view=Google(query))

    @commands.command(name="google")
    async def google_(self, ctx: commands.Context, *, query: str):
        await ctx.send(f"Google result for `{query}`", view=Google(query))


def setup(bot):
    bot.add_cog(GoogleCog(bot))