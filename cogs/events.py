import discord
from discord.ext import tasks, commands
from .help import members


class EventsCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            embed = discord.Embed(description="**<:error:897382665781669908> You are missing required arguments!**", color=discord.Color.red())
            await ctx.send(embed=embed, delete_after=10)
        elif isinstance(error, commands.errors.CommandNotFound):
            if ctx.message.content.startswith("{0}jsk".format(ctx.clean_prefix)) or ctx.message.content.lower().startswith("{0}rep".format(ctx.clean_prefix)):
                return
            embed = discord.Embed(description=f"**<:error:897382665781669908> Couldn't find that command!**", color=discord.Color.red())
            await ctx.send(embed=embed, delete_after=10)
        elif isinstance(error, commands.errors.BadArgument):
            embed = discord.Embed(description=f"**<:error:897382665781669908> Invalid datatype passed in.\nError: `{str(error)}`**", color=discord.Color.red())
            await ctx.send(embed=embed)
        elif isinstance(error, commands.errors.BotMissingPermissions):
            embed = discord.Embed(description=f"**<:error:897382665781669908> I am missing required permissions!**", color=discord.Color.red())
            await ctx.send(embed=embed)
        elif isinstance(error, commands.errors.MemberNotFound):
            embed = discord.Embed(description=f"**<:error:897382665781669908> I can't find that user!**", color=discord.Color.red())
            await ctx.send(embed=embed, delete_after=10)
        elif isinstance(error, commands.errors.NotOwner):
            embed = discord.Embed(description=f"**<:error:897382665781669908> This command is a `owner` only command.**", color=discord.Color.red())
            await ctx.send(embed=embed, delete_after=10)
        elif isinstance(error, commands.errors.TooManyArguments):
            embed = discord.Embed(description=f"**<:error:897382665781669908> Too many arguments {ctx.author.mention}!**", color=discord.Color.red())
            await ctx.send(embed=embed, delete_after=10)
        elif isinstance(error, commands.errors.MissingPermissions):
            embed = discord.Embed(description=f"**<:error:897382665781669908> You are missing reqired permission(s)!**", color=discord.Color.red())
            await ctx.send(embed=embed, delete_after=10)
        elif isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(description=f"**<:error:897382665781669908> Keep cool!\nThe **{ctx.command.name}** command is on a cooldown. Wait for `{error.retry_after:.1f}`s**", color=discord.Color.red())
            await ctx.send(embed=embed)
        elif isinstance(error, commands.DisabledCommand):
            embed = discord.Embed(description="<:error:897382665781669908> This command is disabled :(", color=discord.Color.red())
            await ctx.send(embed=embed)
        else:
            raise error

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx: discord.ApplicationContext, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            embed = discord.Embed(description="**<:error:897382665781669908> You are missing required arguments!**", color=discord.Color.red())
            await ctx.respond(embed=embed)
        elif isinstance(error, commands.errors.CommandNotFound):
            embed = discord.Embed(description=f"**<:error:897382665781669908> Couldn't find a command named {ctx.command}!**", color=discord.Color.red())
            await ctx.respond(embed=embed)
        elif isinstance(error, commands.errors.BadArgument):
            embed = discord.Embed(description=f"**<:error:897382665781669908> Invalid datatype passed in.\nError: `{str(error)}`**", color=discord.Color.red())
            await ctx.respond(embed=embed)
        elif isinstance(error, commands.errors.BotMissingPermissions):
            embed = discord.Embed(description=f"**<:error:897382665781669908> I am missing required permissions!**", color=discord.Color.red())
            await ctx.respond(embed=embed)
        elif isinstance(error, commands.errors.MemberNotFound):
            embed = discord.Embed(description=f"**<:error:897382665781669908> I can't find that user!**", color=discord.Color.red())
            await ctx.respond(embed=embed)
        elif isinstance(error, commands.errors.NotOwner):
            embed = discord.Embed(description=f"**<:error:897382665781669908> This command is a `owner` only command.**", color=discord.Color.red())
            await ctx.respond(embed=embed)
        elif isinstance(error, commands.errors.TooManyArguments):
            embed = discord.Embed(description=f"**<:error:897382665781669908> Too many arguments {ctx.author.mention}!**", color=discord.Color.red())
            await ctx.respond(embed=embed)
        elif isinstance(error, commands.errors.MissingPermissions):
            embed = discord.Embed(description=f"**<:error:897382665781669908> You are missing reqired permission(s)!**", color=discord.Color.red())
            await ctx.respond(embed=embed)
        else:
            raise error

    @tasks.loop(seconds=10)
    async def updatestats(self):
        """Updates the bot activity"""
        await self.bot.wait_until_ready()
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"+help in {len(self.guilds)} servers for {members(self)} members."))

    @updatestats.before_loop
    async def set_activity(self):
        """Sets the bot activity"""
        await self.bot.wait_until_ready()
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"+help in {len(list(self.guilds))} servers for {members(self)} members"))


def setup(bot):
    bot.add_cog(EventsCog(bot))