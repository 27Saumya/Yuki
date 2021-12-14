import discord
from discord.ext import tasks, commands
from discord.commands import permissions, slash_command, Option
from utils.buttons import NukeView


class NukeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @slash_command(guild_ids=[824969244860088332, 847740349853073418, 865962392093851658, 896457384552202312, 918802666790993951], description="Nuke a channel")
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
        channel = channel if channel else ctx.channel
        if not ctx.author.guild_permissions.manage_channels:
            em = discord.Embed(description="<:error:897382665781669908> You can't do that!", color=discord.Color.red())
            return await ctx.send(embed=em)

        embed1 = discord.Embed(description=f"Are you sure you want to **NUKE** {channel.mention}?\n------------------------------------------------\nRespond Within **15** seconds!", color=discord.Color.orange())
        message = await ctx.send(embed=embed1)
        await message.edit(embed=embed1, view=NukeView(ctx, channel, message))


def setup(bot):
    bot.add_cog(NukeCog(bot))