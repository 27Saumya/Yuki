import discord
from discord.ext import commands
from discord.commands import slash_command, Option
from utils.buttons import InviteView
from utils.helpers.help import Help_Embed, cog_help
import asyncio
import time
import datetime
import os


def members(bot: commands.Bot):
    memc = 0
    for guild in bot.guilds:
        memc += guild._member_count
    return memc


class HelpEmbed(discord.Embed):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.timestamp = datetime.datetime.utcnow()
        text = "Use help [command] or help [category] for more information | <>: required | []: optional"
        self.set_footer(text=text)
        self.color = discord.Color.embed_background(theme="dark")


class HelpOptions(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(discord.ui.Button(label="Invite Me!", url="https://discord.com/api/oauth2/authorize?client_id=919314151535419463&permissions=8&scope=bot%20applications.commands", row=1))

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
                label="Utility",
                description="View all Utility commands!",
                emoji=":gear:"
            ),
            discord.SelectOption(
                label="Info",
                description="View all Info commands!",
                emoji=":information_source:"
            ),
            discord.SelectOption(
                label="Moderation",
                description="View all MOD commands",
                emoji="<:mod:923117346984435722>"
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
                    colour=discord.Color.random(),
                ).set_footer(
                    text="Use `help <command>` to get additional help on a specific command."
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
                """Hey! it looks like i am missing some permissions. Please give me the following permissions:\n
                            - Send messages and embeds\n-Join and speak in voice channels\n-Ban, Kick and Delete messages\n thats it for the normal stuff... but remember... if i dont respond, its probably because i dont have the perms to do so."""
            )

    async def send_command_help(self, command):
        """triggers when a `<prefix>help <command>` is called"""
        ctx = self.context
        signature = self.get_command_signature(
            command
        )  # get_command_signature gets the signature of a command in <required> [optional]
        embed = HelpEmbed(
            title=signature, description=command.help or "No help found..."
        )

        if cog := command.cog:
            embed.add_field(name="Category", value=cog.qualified_name)

        # use of internals to get the cooldown of the command
        if command._buckets and (cooldown := command._buckets._cooldown):
            embed.add_field(
                name="Cooldown",
                value=f"{cooldown.rate} per {cooldown.per:.0f} seconds",
            )

        await ctx.send(embed=embed)


class HelpCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.bot.help_command = MyHelpCommand()

    @commands.Cog.listener()
    async def on_ready(self):
        global startTime
        startTime = time.time()


    @slash_command(guild_ids=[824969244860088332, 847740349853073418, 865962392093851658, 896457384552202312], description="Invite me to your server")
    async def invite(self, ctx):
        await ctx.respond("Invite Here!", view=InviteView())
        
    @commands.command(name="invite")
    async def invite_(self, ctx):
        """Invite the bot to your server!"""
        await ctx.send("Invite Here!", view=InviteView())


    @slash_command(guild_ids=[824969244860088332, 847740349853073418, 865962392093851658, 896457384552202312], description="View the bot's info")
    async def botinfo(self, ctx: commands.Context):
        uptime = str(datetime.timedelta(seconds=int(round(time.time()-startTime))))
        embed = discord.Embed(title="Bot Info!", description=f"**Guilds**\n{len(list(self.bot.guilds))}\n\n**Users**\n{members(self.bot)}\n\n**System**\n{os.name}\n\n**Memory**\n67.97\n\n**Python Version**\n3.9.9\n\n**Uptime**\n{uptime}\n\n**Owner/Creator**\n27Saumya", color=discord.Color.green())
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        await ctx.respond(embed=embed)

    @commands.command(name="botinfo", aliases=['bot', 'stats', 'info'])
    async def botinfo_(self, ctx: commands.Context):
        """View the bot's info"""
        uptime = str(datetime.timedelta(seconds=int(round(time.time()-startTime))))
        embed = discord.Embed(title="Bot Info!", description=f"**Guilds**\n{len(list(self.bot.guilds))}\n\n**Users**\n{members(self.bot)}\n\n**System**\n{os.name}\n\n**Memory**\n67.97\n\n**Python Version**\n3.9.9\n\n**Uptime**\n{uptime}\n\n**Owner/Creator**\n27Saumya", color=discord.Color.green())
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
        """View the bot's latency (Edit Latency)"""
        before = time.monotonic()
        embed = discord.Embed(description="**:ping_pong: Bot Latency: **", color=discord.Color.green())
        message = await ctx.send(embed=embed)
        ping = (time.monotonic() - before) * 1000
        embed2 = discord.Embed(description=f"**:ping_pong: Bot Latency: `{int(ping)}` ms**", color=discord.Color.green())
        await message.edit(embed=embed2)


def setup(bot):
    bot.add_cog(HelpCog(bot))