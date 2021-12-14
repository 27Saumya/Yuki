import discord
from discord.ext import tasks, commands
from discord.commands import slash_command
from discord.commands import Option
import wikipedia


class WikpediaCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @slash_command(guild_ids=[824969244860088332, 847740349853073418, 865962392093851658, 896457384552202312, 918802666790993951], description="Search Wikipedia!")
    async def wikipedia(self, ctx: commands.Context, *, query: Option(str, "Type what you want to search!", required=True, default=None), 
        lines:Option(int, "The number of lines you want the result in. By default it is 5", required=False, default=5)):
        result = wikipedia.summary(query, sentences=lines)
        embed = discord.Embed(title=query, description=f"**{result}**", color=discord.Color.random())
        await ctx.respond(embed=embed)


    @commands.command(name="wikipedia", aliases=['wiki'])
    async def wikipedia_(self, ctx, *, query: str):
        try:
            result = wikipedia.summary(query, sentences=5)
            embed = discord.Embed(title=query, description=f"**{result}**", color=discord.Color.random())
            await ctx.send(embed=embed)
        except:
            embed = discord.Embed(description="**<:error:897382665781669908> An error occured while fetching the results**", color=discord.Color.red())
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(WikpediaCog(bot))