import discord
from discord.ext import commands
from discord.commands import slash_command, Option
import json
from utils.buttons import NukeView
import datetime
import humanfriendly


class ModCog(commands.Cog, name="Moderation", description="Moderation commands"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="changeprefix", aliases=['setprefix', 'chpre', 'setpre', 'changepre', 'prefix', 'pre'])
    async def changeprefix_(self, ctx, *, new_prefix: str=None):
        """Changes Prefix for this server"""
        if new_prefix == None:
            return await ctx.send(embed=discord.Embed(description=f"My prefix for this server is `{ctx.clean_prefix}`", color=discord.Color.embed_background(theme="dark")))
        if not ctx.author.guild_permissions.manage_messages:
            embed = discord.Embed(description="**<:error:897382665781669908> You can't do that**", color=discord.Color.red())
            return await ctx.reply(embed=embed)
        if "_" in new_prefix:
            np = new_prefix.replace("_", " ")
            with open("utils/json/prefixes.json", "r") as f:
                prefixes = json.load(f)
            prefixes[str(ctx.guild.id)] = np
            with open("utils/json/prefixes.json", "w") as f:
                json.dump(prefixes, f, indent=4)
            embed = discord.Embed(description=f"**<:tick:897382645321850920> Prefix Updated to:  `{np}`**", color=discord.Color.green())
            return await ctx.send(embed=embed)
        with open("utils/json/prefixes.json", "r") as f:
            prefixes = json.load(f)
        prefixes[str(ctx.guild.id)] = new_prefix
        with open("utils/json/prefixes.json", "w") as f:
            json.dump(prefixes, f, indent=4)
        embed = discord.Embed(description=f"**<:tick:897382645321850920> Prefix Updated to:  `{new_prefix}`**", color=discord.Color.green())
        await ctx.send(embed=embed)
    

    @slash_command(description="Nuke a channel")
    async def nuke(self, ctx, channel: Option(discord.TextChannel, "The channel you want to nuke", required=False, default=None)):
        channel = channel if channel else ctx.channel
        interaction: discord.Interaction = ctx.interaction
        if not ctx.author.guild_permissions.manage_channels:
            em = discord.Embed(description="<:error:897382665781669908> You can't do that!", color=discord.Color.red())
            return await interaction.response.send_message(embed=em, ephemeral=True)
  
        embed1 = discord.Embed(description=f"Are you sure you want to **NUKE** {channel.mention}?\n------------------------------------------------\nRespond Within **15** seconds!", color=discord.Color.orange())
        await interaction.response.send_message(embed=embed1)
        message = await interaction.original_message()
        await message.edit(embed=embed1, view=NukeView(ctx, channel, message))

    @commands.command(name="nuke")
    async def nuke_(self, ctx, *, channel: discord.TextChannel=None):
        """Delete all messages in a channel\nExample: `nuke [channel]\nIf channel is None then it will nuke the channel the command is used in`"""
        channel = channel if channel else ctx.channel
        if not ctx.author.guild_permissions.manage_channels:
            em = discord.Embed(description="<:error:897382665781669908> You can't do that!", color=discord.Color.red())
            return await ctx.send(embed=em)

        embed1 = discord.Embed(description=f"Are you sure you want to **NUKE** {channel.mention}?\n------------------------------------------------\nRespond Within **15** seconds!", color=discord.Color.orange())
        message = await ctx.send(embed=embed1)
        await message.edit(embed=embed1, view=NukeView(ctx, channel, message))

    @commands.group(name="purge")
    async def purge_(self, ctx: commands.Context):
        """Sub commands for purge"""
        if ctx.invoked_subcommand is None:
            await ctx.send(embed=discord.Embed(title="Invalid Usage", description="**Usage: `{0}purge user <member> <amount>`**", color=discord.Color.red()))

    @purge_.command(aliases=['member', 'mem'])
    async def user(self, ctx: commands.Context, user: discord.Member, amount):
        """Delete message of a user in the channel"""
        def is_user(m):
            """Checks the user's messages in the channel"""
            return m.author == user

        channel: discord.TextChannel = ctx.channel
        deleted = await channel.purge(limit=amount, check=is_user)
        embed = discord.Embed(description=f"**<:tick:897382645321850920> Deleted {len(deleted)} messages of {user.mention}**", color=discord.Color.green())
        await ctx.send(embed=embed)

    @commands.command(aliases=['mute'])
    @commands.has_permissions(manage_channels=True)
    async def timeout(self, ctx: commands.Context, user: discord.Member, time, *, reason: str = "No reason provided"):
        """Timeout/Mute a user in the server"""
        if user == ctx.author:
            return await ctx.send(embed=discord.Embed(description="**<:error:897382665781669908> You can't timeout yourself!**", color=discord.Color.red()))

        if user.guild_permissions.administrator or user.guild_permissions.manage_channels:
            return await ctx.send(embed=discord.Embed(description="**<:error:897382665781669908> The user is a MOD/ADMIN!**", color=discord.Color.red()))
        
        timeConvert = humanfriendly.parse_timespan(time)
        await user.timeout(discord.utils.utcnow()+datetime.timedelta(seconds=timeConvert), reason=reason)
        embed = discord.Embed(description=f"**<:tick:897382645321850920> Successfully muted {user.mention} for {time} | Reason: {reason}**", color=discord.Color.green())
        await ctx.send(embed=embed)
        await user.send(embed=discord.Embed(description=f"**<:error:897382665781669908> You were muted in {ctx.guild.name} | Reason: {reason}**", color=discord.Color.red()))

    @commands.command(aliases=['um'])
    @commands.has_permissions(manage_channels=True)
    async def unmute(self, ctx: commands.Context, user: discord.Member, *, reason: str = "No reason provided"):
        """Unmutes a user from the server"""
        if user == ctx.author:
            return await ctx.send(embed=discord.Embed(description="**<:error:897382665781669908> You can't unmute yourself!**", color=discord.Color.red()))
        
        if not user.timed_out:
            return await ctx.send(embed=discord.Embed(description="**<:error:897382665781669908> That user isn't muted!**", color=discord.Color.red()))
        
        await user.timeout(None, reason=reason)
        embed = discord.Embed(description=f"**<:tick:897382645321850920> Successfully unmuted {user.mention} | Reason: {reason}**", color=discord.Color.green())
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(ModCog(bot))