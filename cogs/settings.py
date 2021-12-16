import discord
from discord.ext import commands
from discord.commands import slash_command, Option
import aiosqlite

class SettingsCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.group(name="settings", aliases=['setting'])
    async def settings_(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            async with aiosqlite.connect("utils/databases/main.db") as db:
                async with db.cursor() as cursor:
                    await cursor.execute(f'SELECT bump FROM settings WHERE guild_id = {ctx.guild.id}')
                    data = await cursor.fetchone()
                    if not data:
                        await cursor.execute('INSERT INTO settings(guild_id, bump) VALUES(?,?)', (ctx.guild.id, "off"))
                await db.commit()
                await cursor.close()
            async with aiosqlite.connect("utils/databases/main.db") as db:
                async with db.cursor() as cursor:
                    await cursor.execute(f'SELECT * FROM settings WHERE guild_id = {ctx.guild.id}')
                    setting = await cursor.fetchone()
            embed = discord.Embed(title="Settings", description=f"**Bump Reminder**: `{setting[1]}`", color=discord.Color.green())
            embed.set_footer(text="Use +settings <id> [on/off] to toggle the settings | Use +settings id to view all IDs!", icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)

    @settings_.command(name="id")
    async def id_(self, ctx: commands.Context):
        embed = discord.Embed(title="Setting IDs", description="**Bump Reminder**: `bump`", color=discord.Color.green())
        await ctx.send(embed=embed)

    @settings_.command(name="bump")
    async def bump_(self, ctx: commands.Context, switch: str):
        async with aiosqlite.connect("utils/databases/main.db") as db:
            async with db.cursor() as cursor:
                await cursor.execute(f'SELECT bump FROM settings WHERE guild_id = {ctx.guild.id}')
                data = await cursor.fetchone()
                if not data:
                    await cursor.execute('INSERT INTO settings (guild_id, bump) VALUES(?,?)', (ctx.guild.id, "off"))
            await db.commit()
            await cursor.close()
        async with aiosqlite.connect("utils/databases/main.db") as db:
            async with db.cursor() as cursor:
                if switch.lower() == "on" or switch.lower() == "enable" or switch.lower() == "yes":
                    await cursor.execute(f'UPDATE settings SET bump = "on" WHERE guild_id = {ctx.guild.id}')
                if switch.lower() == "off" or switch.lower() == "disable" or switch.lower() == "no":
                    await cursor.execute(f'UPDATE settings SET bump = "off" WHERE guild_id = {ctx.guild.id}')
            await db.commit()
            await cursor.close()
        if switch.lower() == "on" or switch.lower() == "enable" or switch.lower() == "yes":
            embed = discord.Embed(description="**<:tick:897382645321850920> Enabled `bump reminding` service!**", color=discord.Color.green())
            await ctx.send(embed=embed)
        if switch.lower() == "off" or switch.lower() == "disable" or switch.lower() == "no":
            embed = discord.Embed(description="**<:tick:897382645321850920> Disabled `bump reminding` service!**", color=discord.Color.green())
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(SettingsCog(bot))