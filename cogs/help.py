import discord
from discord.ext import commands
from discord.commands import slash_command, Option
from utils.buttons import InviteView
import time
import datetime
import os


def members(bot: commands.Bot):
    memc = 0
    for guild in bot.guilds:
        memc += guild._member_count
    return memc


class HelpCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        global startTime
        startTime = time.time()

    @slash_command(guild_ids=[824969244860088332, 847740349853073418, 865962392093851658, 896457384552202312], description="View all of my commands")
    async def help(self, ctx: commands.Context, command: Option(str, "The command you want the help with", required=False, default="default")):
        if command == "default":
            embed = discord.Embed(title="Help", color=discord.Color.green())
            embed.add_field(name="__Moderation__", value="`nuke` `changeprefix` `invite`", inline=False)
            embed.add_field(name="__Misc__", value="`avatar` `qrcode` `invite` `youtube download`", inline=True)
            embed.add_field(name="__Info__", value="`covid country` `covid global` `google` `wikipedia` `botinfo`", inline=False)
            embed.add_field(name="__Fun__", value="`8ball`, `nitro`, `tictactoe` `beer`", inline=True)
            embed.add_field(name="__Utility__", value="`settings`", inline=False)
            embed.set_footer(text=f"To view detailed information use | +help <command>")
            await ctx.respond(embed=embed, view=InviteView())
        if command.lower().startswith('cov'):
            embed = discord.Embed(title="Covid Info", description="**__Commands__:** \n-->`global`:\nGets Global covid info\naliases: `world` `all`\n\n-->`country` \nDirectly type the country you want.\nExample: \n`+covid country India`\n`+covid country USA`", color=discord.Color.green())
            await ctx.respond(embed=embed)
        if command.lower() == "nitro":
            embed = discord.Embed(title="Nitro", description="Generates a nitro link for you!", color=discord.Color.green())
            await ctx.respond(embed=embed)
        if command.lower() == "beer":
            embed = discord.Embed(title="Beer", description="Have a beer with yourself or a friend\n------------------------------\n**--> Usage:\n\n `+beer` -> To have a drink with yourself!\n`+beer <user>` -> Have a beer with a friend!**", color=discord.Color.green())
            await ctx.respond(embed=embed)
        if command.lower().startswith('tic') or command.lower() == "ttt":
            embed = discord.Embed(title="TicTacToe", description="Play a tictactoe with yourself\n\nMultiplayer will be added soon!", color=discord.Color.green())
            await ctx.respond(embed=embed)
        if command.lower().startswith('8') or command.lower().startswith('eight'):
            embed = discord.Embed(title="8ball", description="Ask the bot something. It returns a random answer\n----------------------------\n**--> Usage:\n\n `+8ball <question>`**\n----------------------------\n**--> Example: `+8ball Am I cool?`**", color=discord.Color.green())
            await ctx.respond(embed=embed)
        if command.lower() == "google":
            embed = discord.Embed(title="Google", description="Search <:google:917143687870414878>!\n\n**--> Usage:\n\n `+google <query>`\nExample: `+google The Slash Bot`**", color=discord.Color.green())
            await ctx.respond(embed=embed)
        if command.lower().startswith('av'):
            embed = discord.Embed(title="Avatar", description="View someone's or your's avatar!\n\n**--> Usage:\n\n `+avatar <member>`**", color=discord.Color.green())
            await ctx.respond(embed=embed)
        if command.lower().startswith('qr'):
            embed = discord.Embed(title="Qrocde", description="Generate a qrcode!\n\n**--> Usage:\n\n `+qrcode <url>`\n--> Example: `+qrcode https://www.youtube.com/watch?v=dQw4w9WgXcQ`**", color=discord.Color.green())
            await ctx.respond(embed=embed)
        if command.lower() == "nuke":
            embed = discord.Embed(title="Nuke", description="Nuke a channel!\n\n**--> Usage:\n\n `+nuke <channel>` -> for some other channel\n`+nuke` -> for the current channel**", color=discord.Color.green())
            await ctx.respond(embed=embed)
        if command.lower().startswith('wiki'):
            embed = discord.Embed(title="Wikipedia", description="Search Wikipedia!\n\n**--> Usage:\n\n `=nuke <query>`\n--> Example: `+wikipedia The Slash Bot`**", color=discord.Color.green())
            await ctx.respond(embed=embed)    


    @commands.group(name="help")
    async def help_(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title="Help", color=discord.Color.green())
            embed.add_field(name="__Moderation__", value="`nuke` `changeprefix` `invite`", inline=False)
            embed.add_field(name="__Misc__", value="`avatar` `qrcode` `invite` `youtube download`", inline=True)
            embed.add_field(name="__Info__", value="`covid country` `covid global` `google` `wikipedia` `botinfo`", inline=False)
            embed.add_field(name="__Fun__", value="`8ball`, `nitro`, `tictactoe` `beer`", inline=True)
            embed.add_field(name="__Utility__", value="`settings`", inline=False)
            embed.set_footer(text=f"To view detailed information use | +help <command>")
            await ctx.send(embed=embed, view=InviteView())
        
    @help_.command(aliases=['cov', 'covidinfo'])
    async def covid(self, ctx: commands.Context):
        embed = discord.Embed(title="Covid Info", description="**__Commands__:** \n-->`global`:\nGets Global covid info\naliases: `world` `all`\n\n-->`country` \nDirectly type the country you want.\nExample: \n`+covid country India`\n`+covid country USA`", color=discord.Color.green())
        await ctx.send(embed=embed)
    
    @help_.command()
    async def nitro(self, ctx: commands.Context):
        embed = discord.Embed(title="Nitro", description="Generates a nitro link for you!", color=discord.Color.green())
        await ctx.send(embed=embed)

    @help_.command(aliases=['ttt', 'tic', 'tictac'])
    async def tictactoe(self, ctx: commands.Context):
        embed = discord.Embed(title="TicTacToe", description="Play a tictactoe with yourself\n\nMultiplayer will be added soon!", color=discord.Color.green())
        await ctx.send(embed=embed)

    @help_.command(aliases=['8ball', '8b'])
    async def eightball(self, ctx: commands.Context):
        embed = discord.Embed(title="8ball", description="Ask the bot something. It returns a random answer\n----------------------------\n**--> Usage:\n\n `+8ball <question>`**\n----------------------------\n**--> Example: `+8ball Am I cool?`**", color=discord.Color.green())
        await ctx.send(embed=embed)

    @help_.command()
    async def beer(self, ctx: commands.Context):
        embed = discord.Embed(title="Beer", description="Have a beer with yourself or a friend\n------------------------------\n**--> Usage:\n\n `+beer` -> To have a drink with yourself!\n`+beer <user>` -> Have a beer with a friend!**", color=discord.Color.green())
        await ctx.send(embed=embed)

    @help_.command()
    async def google(self, ctx: commands.Context):
        embed = discord.Embed(title="Google", description="Search <:google:917143687870414878>!\n\n**--> Usage:\n\n `+google <query>`\nExample: `+google The Slash Bot`**", color=discord.Color.green())
        await ctx.send(embed=embed)

    @help_.command(aliases=['av', 'pfp'])
    async def avatar(self, ctx: commands.Context):
        embed = discord.Embed(title="Avatar", description="View someone's or your's avatar!\n\n**--> Usage:\n\n `+avatar <member>`**", color=discord.Color.green())
        await ctx.send(embed=embed)

    @help_.command(aliases=['qr'])
    async def qrcode(self, ctx: commands.Context):
        embed = discord.Embed(title="Qrocde", description="Generate a qrcode!\n\n**--> Usage:\n\n `+qrcode <url>`\n--> Example: `+qrcode https://www.youtube.com/watch?v=dQw4w9WgXcQ`**", color=discord.Color.green())
        await ctx.send(embed=embed)

    @help_.command()
    async def nuke(self, ctx: commands.Context):
        embed = discord.Embed(title="Nuke", description="Nuke a channel!\n\n**--> Usage:\n\n `+nuke <channel>` -> for some other channel\n`+nuke` -> for the current channel**", color=discord.Color.green())
        await ctx.send(embed=embed)

    @help_.command(aliases=['wiki'])
    async def wikipedia(self, ctx: commands.Context):
        embed = discord.Embed(title="Wikipedia", description="Search Wikipedia!\n\n**--> Usage:\n\n `=nuke <query>`\n--> Example: `+wikipedia The Slash Bot`**", color=discord.Color.green())
        await ctx.send(embed=embed)



    @slash_command(guild_ids=[824969244860088332, 847740349853073418, 865962392093851658, 896457384552202312], description="Invite me to your server")
    async def invite(self, ctx):
        await ctx.respond("Invite Here!", view=InviteView())
        
    @commands.command(name="invite")
    async def invite_(self, ctx):
        await ctx.send("Invite Here!", view=InviteView())


    @slash_command(guild_ids=[824969244860088332, 847740349853073418, 865962392093851658, 896457384552202312], description="View the bot's info")
    async def botinfo(self, ctx: commands.Context):
        uptime = str(datetime.timedelta(seconds=int(round(time.time()-startTime))))
        embed = discord.Embed(title="Bot Info!", description=f"**Guilds**\n{len(list(self.bot.guilds))}\n\n**Users**\n{members(self.bot)}\n\n**System**\n{os.name}\n\n**Memory**\n59.97\n\n**Python Version**\n3.9.9\n\n**Uptime**\n{uptime}", color=discord.Color.green())
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        await ctx.respond(embed=embed)

    @commands.command(name="botinfo", aliases=['bot', 'stats', 'info'])
    async def botinfo_(self, ctx: commands.Context):
        uptime = str(datetime.timedelta(seconds=int(round(time.time()-startTime))))
        embed = discord.Embed(title="Bot Info!", description=f"**Guilds**\n{len(list(self.bot.guilds))}\n\n**Users**\n{members(self.bot)}\n\n**System**\n{os.name}\n\n**Memory**\n59.97\n\n**Python Version**\n3.9.9\n\n**Uptime**\n{uptime}", color=discord.Color.green())
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        await ctx.send(embed=embed)
        
    @slash_command(guild_ids=[824969244860088332, 847740349853073418, 865962392093851658, 896457384552202312], description="🏓 Check the bot's latency")
    async def ping(self, ctx: commands.Context):
        interaction: discord.Interaction = ctx.interaction
        before = time.monotonic()
        embed = discord.Embed(description="**:ping_pong: Bot Latency: **", color=discord.Color.green())
        await interaction.response.send_message(embed=embed)
        message = await interaction.original_message()
        ping = (time.monotonic() - before) * 1000
        embed2 = discord.Embed(description=f"**:ping_pong: Bot Latency: `{int(ping)}` ms**", color=discord.Color.green())
        await message.edit(embed=embed2)

    @commands.command(name="ping")
    async def ping_(self, ctx: commands.Context):
        before = time.monotonic()
        embed = discord.Embed(description="**:ping_pong: Bot Latency: **", color=discord.Color.green())
        message = await ctx.send(embed=embed)
        ping = (time.monotonic() - before) * 1000
        embed2 = discord.Embed(description=f"**:ping_pong: Bot Latency: `{int(ping)}` ms**", color=discord.Color.green())
        await message.edit(embed=embed2)


def setup(bot):
    bot.add_cog(HelpCog(bot))