import discord
from discord.ext import tasks, commands
from discord.commands import slash_command, Option
from utils.buttons import Google
import requests
import json
import wikipedia


class Info(commands.Cog, name="Info", description="Information related commands"):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(guild_ids=[824969244860088332, 847740349853073418, 865962392093851658, 896457384552202312, 918802666790993951], description="Google Search")
    async def google(self, ctx: commands.Context, *, 
        query: Option(str, "Type what you want to search!", required=True, default=None)):
        await ctx.respond(f"Google Result for `{query}`", view=Google(query))

    @commands.command(name="google")
    async def google_(self, ctx: commands.Context, *, query: str):
        await ctx.send(f"Google result for `{query}`", view=Google(query))

    @commands.group(name="covid", description="Info about COVID-19")
    async def covid_(self, ctx: commands.Context):
        """Command group to get covid stats use `covid` for more info"""
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title="Covid Info", description="**__Commands__:** \n-->`global`:\nGets Global covid info\naliases: `world` `all`\n\n-->`country` \nDirectly type the country you want.\nExample: \n`+covid country India`\n`+covid country USA`", color=discord.Color.green())
            await ctx.send(embed=embed)

    @covid_.command(name="country", aliases=['c', 'cou', 'coun'])
    async def country_(self, ctx, *, country: str):
        """Get covid stats of a country\nExample: `covid country India` and `covid country USA`"""
        em = discord.Embed(description="**Fetching information <a:loading:911568431315292211>**", color=discord.Color.green())
        message = await ctx.send(embed=em)
        url = f"https://coronavirus-19-api.herokuapp.com/countries/{country}"
        stats = requests.get(url)
        json_stats = stats.json()
        country = json_stats["country"]
        totalCases = json_stats["cases"]
        todayCases = json_stats["todayCases"]
        totalDeaths = json_stats["deaths"]
        todayDeaths = json_stats["todayDeaths"]
        recovered = json_stats["recovered"]
        active = json_stats["active"]
        critical = json_stats["critical"]
        casesPerOneMillion = json_stats["casesPerOneMillion"]
        deathsPerOneMillion = json_stats["deathsPerOneMillion"]
        totalTests = json_stats["totalTests"]
        testsPerOneMillion = json_stats["testsPerOneMillion"]

        embed = discord.Embed(title=f"**COVID-19 Status Of {country}**!", description="This Information Isn't Live Always, Hence It May Not Be Accurate!", colour=discord.Color.random())
        embed.add_field(name="**Total Cases**", value=totalCases, inline=True)
        embed.add_field(name="**Today Cases**", value=todayCases, inline=True)
        embed.add_field(name="**Total Deaths**", value=totalDeaths, inline=True)
        embed.add_field(name="**Today Deaths**", value=todayDeaths, inline=True)
        embed.add_field(name="**Recovered**", value=recovered, inline=True)
        embed.add_field(name="**Active**", value=active, inline=True)
        embed.add_field(name="**Critical**", value=critical, inline=True)
        embed.add_field(name="**Cases Per One Million**", value=casesPerOneMillion, inline=True)
        embed.add_field(name="**Deaths Per One Million**", value=deathsPerOneMillion, inline=True)
        embed.add_field(name="**Total Tests**", value=totalTests, inline=True)
        embed.add_field(name="**Tests Per One Million**", value=testsPerOneMillion, inline=True)

        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/564520348821749766/701422183217365052/2Q.png")
        embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar.url)
        await message.edit(embed=embed)


    @covid_.command(name="global", aliases=['world', 'all'])
    async def global_(self, ctx):
        """Gets the global Covid-19 INFO"""
        em = discord.Embed(description="**Fetching information <a:loading:911568431315292211>**", color=discord.Color.green())
        message = await ctx.send(embed=em)
        url = f"https://coronavirus-19-api.herokuapp.com/countries/world"
        stats = requests.get(url)
        json_stats = stats.json()
        totalCases = json_stats["cases"]
        todayCases = json_stats["todayCases"]
        totalDeaths = json_stats["deaths"]
        todayDeaths = json_stats["todayDeaths"]
        recovered = json_stats["recovered"]
        active = json_stats["active"]
        critical = json_stats["critical"]
        casesPerOneMillion = json_stats["casesPerOneMillion"]
        deathsPerOneMillion = json_stats["deathsPerOneMillion"]
        totalTests = json_stats["totalTests"]
        testsPerOneMillion = json_stats["testsPerOneMillion"]

        embed = discord.Embed(title=f"**Global Covid 19 Info**!", description="This Information Isn't Live Always, Hence It May Not Be Accurate!", colour=discord.Color.random())
        embed.add_field(name="**Total Cases**", value=totalCases, inline=True)
        embed.add_field(name="**Today Cases**", value=todayCases, inline=True)
        embed.add_field(name="**Total Deaths**", value=totalDeaths, inline=True)
        embed.add_field(name="**Today Deaths**", value=todayDeaths, inline=True)
        embed.add_field(name="**Recovered**", value=recovered, inline=True)
        embed.add_field(name="**Active**", value=active, inline=True)
        embed.add_field(name="**Critical**", value=critical, inline=True)
        embed.add_field(name="**Cases Per One Million**", value=casesPerOneMillion, inline=True)
        embed.add_field(name="**Deaths Per One Million**", value=deathsPerOneMillion, inline=True)
        embed.add_field(name="**Total Tests**", value=totalTests, inline=True)
        embed.add_field(name="**Tests Per One Million**", value=testsPerOneMillion, inline=True)

        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/564520348821749766/701422183217365052/2Q.png")
        embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar.url)
        await message.edit(embed=embed)

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
    bot.add_cog(Info(bot))