import discord
from discord.ext import commands
import os
from discord.commands import Option, SlashCommandGroup
import json
from pytube import YouTube
import requests
import asyncio
import config
from utils.buttons import TicketControlsView
import sqlite3


def get_prefix(bot, message):
    with open("utils/json/prefixes.json", "r") as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]



class Bot(commands.Bot):
    def __init__(self):
        self.db = sqlite3.connect("utils/databases/main.db")
        self.dbcursor = self.db.cursor()

        super().__init__(command_prefix=get_prefix, help_command=None, intents=discord.Intents().all(), case_insensitiv1e=True)

        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                self.load_extension(f"cogs.{filename[:-3]}")


    async def on_ready(self):
        print(f"{self.user.name} is online!")
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="+help | Slash Commands (selected guild only :())"))
        self.dbcursor.execute('CREATE TABLE IF NOT EXISTS ticket (guild_id INTEGER , count INTEGER, category INTEGER)')
        self.dbcursor.execute('CREATE TABLE IF NOT EXISTS settings (guild_id INTEGER, "bump")')
        self.dbcursor.execute('CREATE TABLE IF NOT EXISTS tickets (guild_id INTEGER, channel_id INTEGER, opener INTEGER, switch TEXT)')
        self.db.commit()
    
    async def on_guild_join(self, guild):
        with open("utils/json/prefixes.json", "r") as f:
            prefixes = json.load(f)

        prefixes[str(guild.id)] = "+"

        with open("utils/json/prefixes.json", "w") as f:
            json.dump(prefixes, f, indent=4)

    async def on_message(self, message: discord.Message):
        try:
            if message.author.id == bot.user.id and len(message.embeds) > 0 and message.embeds[0].description.startswith('**Ticket closed by'):
                bot.dbcursor.execute(f'SELECT * FROM tickets WHERE guild_id=? AND channel_id=?', (message.guild.id, message.channel.id))
                data = bot.dbcursor.fetchone()
                member = await bot.fetch_user(data[2])
                embed = discord.Embed(description="```py\n[Support team ticket controls]```", color=discord.Color.embed_background(theme="dark"))
                message2 = await message.channel.send(embed=embed)
                await message2.edit(view=TicketControlsView(member, message2, bot))
        except AttributeError:
            print("That wasn't a ticket close message.")

        if message.author == bot.user:
            return

        try:
            if message.author.id == 302050872383242240 and len(message.embeds) > 0 and "Bump done! :thumbsup:" in message.embeds[0].description:
                bot.dbcursor.execute(f'SELECT bump FROM settings WHERE guild_id = {message.guild.id}')
                data = bot.dbcursor.fetchone()
                if not data:
                    return
                if data:
                    await bot.dbcursor.execute(f'SELECT * FROM settings WHERE guild_id = {message.guild.id}')
                    switch = bot.dbcursor.fetchone()
                if switch[1] == "off":
                    return

                embed = discord.Embed(description="**<:zerolove:920425612613660753> Thanks to bump the server <3**", color=discord.Color.green())
                await message.channel.send(embed=embed)
                await asyncio.sleep(3600*2) # Bump delay == 2 hours | 1 hour == 3600 seconds so, 2 hours == 3600*2
                embed = discord.Embed(title="It's time to bump!", description="Use `!d bump` to bump the server!", color=discord.Color.green())
                await message.channel.send(embed=embed)
        except AttributeError:
            print("Not a bump message.")
        with open("utils/json/prefixes.json", "r") as f:
            prefixes = json.load(f)
        if str(message.guild.id) not in prefixes:
            with open("utils/json/prefixes.json", "w") as f:
                prefixes[str(message.guild.id)] = "+"
                json.dump(prefixes, f, indent=4)
        
        await bot.process_commands(message)
            

bot = Bot()            

@bot.slash_command(guild_ids=[824969244860088332, 847740349853073418, 865962392093851658, 896457384552202312, 918802666790993951], description="Change the prefix")
async def changeprefix(ctx, *, new_prefix: Option(str, "The prefix to set | Keep empty to reset the prefix", required=False, default='+')):
    if not ctx.author.guild_permissions.manage_messages:
        embed = discord.Embed(description="**<:error:897382665781669908> You can't do that**", color=discord.Color.red())
        return await ctx.respond(embed=embed, ephemeral=True)
    with open("utils/json/prefixes.json", "r") as f:
        prefixes = json.load(f)
    prefixes[str(ctx.guild.id)] = new_prefix
    with open("utils/json/prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)
    embed = discord.Embed(description=f"**<:tick:897382645321850920> Prefix Updated to:  `{new_prefix}`**", color=discord.Color.green())
    await ctx.respond(embed=embed)


@bot.command(name="changeprefix", aliases=['setprefix', 'chpre', 'setpre', 'changepre', 'prefix', 'pre'])
async def changeprefix_(ctx, *, new_prefix='+'):
    if not ctx.author.guild_permissions.manage_messages:
        embed = discord.Embed(description="**<:error:897382665781669908> You can't do that**", color=discord.Color.red())
        return await ctx.reply(embed=embed)
    with open("utils/json/prefixes.json", "r") as f:
        prefixes = json.load(f)
    prefixes[str(ctx.guild.id)] = new_prefix
    with open("utils/json/prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)
    embed = discord.Embed(description=f"**<:tick:897382645321850920> Prefix Updated to:  `{new_prefix}`**", color=discord.Color.green())
    await ctx.send(embed=embed)

youtube = SlashCommandGroup("youtube", "Commands realted to youtube")

@youtube.command(guild_ids=[824969244860088332, 847740349853073418, 865962392093851658, 896457384552202312, 918802666790993951], description="Download a youtube video!")
async def download(ctx: commands.Context, link: Option(str, "The video you want to download!", required=True, defaul=None)):
    interaction: discord.Interaction = ctx.interaction
    return await interaction.response.send_message("This command is currently closed ):")
    embed = discord.Embed(description="**Downloading the video <a:loading:911568431315292211>\n-------------------------\nThis may take some time.**", color=discord.Color.green())
    await interaction.response.send_message(embed=embed)
    message = await interaction.original_message()
    url = YouTube(link)
    video = url.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    video.download(output_path='./yt_vids')
    def find_vid():
        for vid in os.listdir('./yt_vids'):
            if vid == video.default_filename:
                print(vid)
        return vid
    await message.edit(content="**Here is your video!**", embed=None, file=discord.File(f'yt_vids/{find_vid()}'))

    for mp4file in os.listdir('./yt_vids'):
        os.remove(f"yt_vids/{mp4file}")

covid = SlashCommandGroup("covid", "commands related to covid info")


@covid.command(guild_ids=[824969244860088332, 847740349853073418, 865962392093851658, 896457384552202312, 918802666790993951], description="Covid Information!")
async def country(ctx, *, country: Option(str, "Name of the Country you want the Covid info of!", required=True, default=None)):
    interaction: discord.Interaction = ctx.interaction
    em = discord.Embed(description="**Fetching information <a:loading:911568431315292211>**", color=discord.Color.green())
    await interaction.response.send_message(embed=em)
    message = await interaction.original_message()
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


@covid.command(name="global", guild_ids=[824969244860088332, 847740349853073418, 865962392093851658, 896457384552202312, 918802666790993951], description="View Global Covid Info!")
async def global_(ctx):
    interaction: discord.Interaction = ctx.interaction
    em = discord.Embed(description="**Fetching information <a:loading:911568431315292211>**", color=discord.Color.green())
    await interaction.response.send_message(embed=em)
    message = await interaction.original_message()
    url = f"https://coronavirus-19-api.herokuapp.com/countries/world"
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

    embed = discord.Embed(title=f"**Global Covid 19 Info**!", description="This Information Isn't Live Always, Hence It May Not Be Accurate!",colour=discord.Color.random())
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


@bot.command()
@commands.is_owner()
async def load(ctx: commands.Context, ext: str):
    bot.load_extension(f"cogs.{ext}")
    await ctx.send(f"Loaded extension `{ext}`", delete_after=7)

@bot.command()
@commands.is_owner()
async def unload(ctx: commands.Context, ext: str):
    bot.unload_extension(f"cogs.{ext}")
    await ctx.send(f"Unloaded extension `{ext}`", delete_after=7)


@bot.command(aliases=['al','reload'])
@commands.is_owner()
async def autoload(ctx: commands.Context, ext: str):
    if ext == "all":
        for filename in os.listdir('./cogs'):
            bot.unload_extension(f"cogs.{filename[:-3]}")
            await asyncio.sleep(0.3)
        await ctx.send("Unloaded all extensions. Now loading them!")
        await asyncio.sleep(0.5)
        for filename in os.listdir('./cogs'):
            bot.load_extension(f"cogs.{filename[:-3]}")
        await ctx.send("Succesfully reloaded all extensions")
    else:
        bot.unload_extension(f"cogs.{ext}")
        await asyncio.sleep(0.5)
        bot.load_extension(f"cogs.{ext}")
        await ctx.send(f"Succesfully reloaded `{ext}`")

bot.add_application_command(youtube)
bot.add_application_command(covid)


bot.run(config.TOKEN)