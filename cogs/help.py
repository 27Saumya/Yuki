import discord
from discord.ext import commands
from discord.commands import slash_command, Option
from utils.buttons import InviteView2
from utils.helpers.help import Help_Embed, cog_help
import asyncio
import time
import datetime
import psutil
import platform
import sys


def members(bot: commands.Bot):
    memc = 0
    for guild in bot.guilds:
        memc += guild._member_count
    return memc


class HelpEmbed(discord.Embed):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        text = "Use help [command] | <>: required | []: optional"
        self.set_footer(text=text)
        self.color = discord.Color.embed_background(theme="dark")


class HelpOptions(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(discord.ui.Button(label="Invite Me!", url="https://discord.com/api/oauth2/authorize?client_id=919314151535419463&permissions=8&scope=bot%20applications.commands", row=1))
        self.add_item(discord.ui.Button(label="Support Server", url="https://discord.gg/RqKvY5MQgb", row=1))

    @discord.ui.button(label="Delete", style=discord.ButtonStyle.red, emoji="⛔", row=2)
    async def delete_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.message.delete()

    @discord.ui.select(
        placeholder="Select a Category!",
        min_values=1,
        max_values=1,
        options=[
            discord.SelectOption(
                label="Config", 
                description="Configure the bot", 
                emoji="🔧"
            ),
            discord.SelectOption(
                label="Fun",
                description="View all Fun commands!",
                emoji="🪄"
            ),
            discord.SelectOption(
                label="Misc",
                description="View all normal and mod commands!",
                emoji="🤖"
            ),
            discord.SelectOption(
                label="Info",
                description="View all Info commands!",
                emoji="ℹ️"
            ),
            discord.SelectOption(
                label="Moderation",
                description="View all MOD commands",
                emoji="<:modlogo:923117346984435722>"
            ),
            discord.SelectOption(
                label="Tickets",
                description="View all ticket system commands!",
                emoji="📩"
            )
        ])
    async def select_callback(self, select, interaction: discord.Interaction):
        if select.values[0]:
            await interaction.response.edit_message(
                embed=discord.Embed(
                    title=f"{select.values[0]} Help!",
                    description=cog_help[select.values[0]],
                    color=discord.Color.embed_background(theme="dark"),
                ).set_footer(
                    text="Use help <command> to get additional help on a specific command."
                )
            )


class MyHelpCommand(commands.MinimalHelpCommand):
    def __init__(self):
        super().__init__()

    async def send_pages(self):
        ctx = self.context

        try:

            m = await ctx.send(embed=Help_Embed(), view=HelpOptions())
            await asyncio.sleep(120)
            try:
                await m.edit("This help session expired!", embed=Help_Embed(), view=None)
            except:
                pass
        except discord.Forbidden:
            await ctx.send(
                """Hey! it looks like i am missing some permissions."""
            )
        except Exception as e:
            print(e)

    async def send_command_help(self, command):
        """triggers when a `<prefix>help <command>` is called"""
        try:
            ctx = self.context
            signature = self.get_command_signature(
                command
            )
            embed = HelpEmbed(
                title=signature, description=command.help or "No help found..."
            )

            if cog := command.cog:
                embed.add_field(name="Category", value=cog.qualified_name)

            if command._buckets and (cooldown := command._buckets._cooldown):
                embed.add_field(
                    name="Cooldown",
                    value=f"{cooldown.rate} per {cooldown.per:.0f} seconds",
                )

            await ctx.send(embed=embed)
        except Exception as e:
            print(e)


class HelpCog(commands.Cog, name="Help"):
    """Help command and bot related commands"""
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.bot.help_command = MyHelpCommand()

    @commands.Cog.listener()
    async def on_ready(self):
        global startTime
        startTime = time.time()


    @slash_command(description="Invite me to your server")
    async def invite(self, ctx):
        await ctx.respond("Invite Here!", view=InviteView2())
        
    @commands.command(name="invite", aliases=['inv', 'botinv', 'botbotinvite'])
    async def invite_(self, ctx):
        """Invite the bot to your server!"""
        await ctx.send("Invite Here!", view=InviteView2())


    @slash_command(description="View the bot's info")
    async def botinfo(self, ctx: commands.Context):
        memory = "{:.4} MB".format(psutil.Process().memory_info().rss / 1024 ** 2)
        py_ver = ".".join([str(v) for v in sys.version_info[:3]])
        uptime = str(datetime.timedelta(seconds=int(round(time.time()-startTime))))
        embed = discord.Embed(title="Bot Info!", description=f"**Servers**\n{len(list(self.bot.guilds))}\n\n**Users**\n{members(self.bot)}\n\n**System**\n{platform.release()}\n\n**Memory**\n{memory}\n\n**Python Version**\n{py_ver}\n\n**Uptime**\n{uptime}\n\n**Owner/Creator**\n27Saumya", color=discord.Color.green())
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        await ctx.respond(embed=embed)

    @commands.command(name="botinfo", aliases=['bot', 'stats', 'info'])
    async def botinfo_(self, ctx: commands.Context):
        """View the bot's info"""
        memory = "{:.4} MB".format(psutil.Process().memory_info().rss / 1024 ** 2)
        py_ver = ".".join([str(v) for v in sys.version_info[:3]])
        uptime = str(datetime.timedelta(seconds=int(round(time.time()-startTime))))
        embed = discord.Embed(title="Bot Info!", description=f"**Servers**\n{len(list(self.bot.guilds))}\n\n**Users**\n{members(self.bot)}\n\n**System**\n{platform.release()}\n\n**Memory**\n{memory}\n\n**Python Version**\n{py_ver}\n\n**Uptime**\n{uptime}\n\n**Owner/Creator**\n27Saumya", color=discord.Color.green())
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        await ctx.send(embed=embed)
        
    @slash_command(description="🏓 Check the bot's latency")
    async def ping(self, ctx: commands.Context):
        interaction: discord.Interaction = ctx.interaction
        before = time.monotonic()
        embed = discord.Embed(title=":ping_pong:", color=discord.Color.green())
        await interaction.response.send_message(embed=embed)
        message = await interaction.original_message()
        ping = (time.monotonic() - before) * 1000
        embed2 = discord.Embed(title=":ping_pong: Pong!", description=f"**Bot latency: `{round(self.bot.latency * 1000)}` ms\n------------------------------\nDiscord Latency: `{int(ping)}` ms**", color=discord.Color.green())
        await message.edit(embed=embed2)

    @commands.command(name="ping")
    async def ping_(self, ctx: commands.Context):
        """View the bot's latency (Edit Latency)"""
        before = time.monotonic()
        embed = discord.Embed(title=":ping_pong:", color=discord.Color.green())
        message = await ctx.send(embed=embed)
        ping = (time.monotonic() - before) * 1000
        embed2 = discord.Embed(title=":ping_pong: Pong!", description=f"**Bot latency: `{round(self.bot.latency * 1000)}` ms\n------------------------------\nDiscord Latency: `{int(ping)}` ms**", color=discord.Color.green())
        await message.edit(embed=embed2)


def setup(bot):
    bot.add_cog(HelpCog(bot))