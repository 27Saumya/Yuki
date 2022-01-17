import discord
from discord.ext import commands
from discord.commands import slash_command, user_command
from discord.commands import Option
import qrcode
import os
from pytube import YouTube
from speedtest import Speedtest
from typing import Union
import aiohttp
from io import BytesIO
from utils.buttons import *


class Misc(commands.Cog, name="Misc", description="Miscellaneous commands!"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    #Avatar
    @slash_command(description="Check your or someone else's PFP!")
    async def avatar(self, ctx, 
        member: Option(discord.Member, "Check someone else's PFP!", required=False, default=None)):
        member = member if member else ctx.author
        em = discord.Embed(color=member.color)
        em.set_image(url=member.avatar.url)
        em.set_author(name=f"{member.name}'s avatar!", icon_url=member.avatar.url)
        em.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar.url)
        await ctx.respond(embed=em)

    @commands.command(name="avatar", aliases=['av', 'pfp'])
    async def avatar_(self, ctx: commands.context, member: discord.Member=None):
        """View your's or someone's avatar"""
        member = member if member else ctx.author
        em = discord.Embed(color=member.color)
        em.set_image(url=member.avatar.url)
        em.set_author(name=f"{member.name}'s avatar!", icon_url=member.avatar.url)
        em.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar.url)
        await ctx.send(embed=em)

    #Qrcode
    @slash_command(description="Generate a Qrcode!")
    async def qrcode(self, ctx, url: Option(str, "The link you want the qrcode of", required=True, default=None), hidden: Option(str, "Do you want the qrcode to be visible only to you?", choices=["Yes", "No"], required=False, default=None)):
        img = qrcode.make(url)
        img.save("qrcode.png")
        if hidden == "Yes":
            await ctx.respond(content="**Here is your QRCode**", file=discord.File("qrcode.png"), ephemeral=True)
        else:
            await ctx.respond(content="**Here is your QRCode**", file=discord.File("qrcode.png"))
        os.remove("qrcode.png")

    @commands.command(name="qrcode", aliases=['qr'])
    async def qrcode_(self, ctx, *, url: str):
        """Create a qrcode.\nExample: `qrcode youtube.com`"""
        img = qrcode.make(url)
        img.save("qrcode.png")
        await ctx.send(content="**Here is your QRCode**", file=discord.File("qrcode.png"))
        os.remove("qrcode.png")

    #Youtube
    @commands.group(name="youtube")
    async def youtube_(self, ctx: commands.Context):
        """Youtube related commnands"""
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title="Youtube", description="**Youtube Commands:**\n    -->**download**\n**Usage** --> `youtube download <url>`", color=discord.Color.green())
            embed.set_footer(text="More Commands Coming Soon!")
            await ctx.send(embed=embed)

    @youtube_.command(name="download")
    async def download_(self, ctx: commands.Context, *, link: str):
        """Download a youtube video (currently closed)\nExample: `youtube download youtube.com/watch?v=dQw4w9WgXcQ`"""
        embed = discord.Embed(description="**Downloading the video <a:loading:911568431315292211>\n-------------------------\nThis may take some time.**", color=discord.Color.green())
        message = await ctx.send("Sorry this command is currently disabled :(")
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


    @commands.command(aliases=['st', 'speed'])
    async def speedtest(self, ctx: commands.Context):
        """Test the bot's speed"""
        message = await ctx.send(
            embed=discord.Embed(description="**<a:loading:911568431315292211> Starting Speed Test!**", color=discord.Color.embed_background(theme="dark"))
        )
        s = Speedtest()
        s.get_best_server()
        await message.edit(embed=discord.Embed(description="**<a:loading:911568431315292211> Found Best Server**", color=discord.Color.embed_background(theme="dark")))
        s.download()
        await message.edit(embed=discord.Embed(description="**<a:loading:911568431315292211> Download Complete**", color=discord.Color.embed_background(theme="dark")))
        s.upload()
        await message.edit(embed=discord.Embed(description="**<a:loading:911568431315292211> Uploading Complete\n-----------------------------\nSending results**", color=discord.Color.embed_background(theme="dark")))
        s = s.results.dict()

        await message.edit(
            embed=discord.Embed(title="Speed Test Results", description=f"Ping: `{s['ping']}` ms\nDownload: `{round(s['download']/10**6, 3)}` Mbit/s\nUpload: `{round(s['upload']/10**6, 3)}` Mbit/s\nServer: `{s['server']['sponsor']}`", color=discord.Color.embed_background(theme="dark"))
        )

    
    @commands.command(aliases=['eadd', 'ea'])
    @commands.has_permissions(manage_emojis_and_stickers=True)
    async def emojiadd(self, ctx: commands.Context, emoji: str, *, name: str):
        """Creates an emoji in the server using a url"""

        async with aiohttp.ClientSession() as session:
            async with session.get(emoji) as r:
                try:
                    imgOrGIF = BytesIO(await r.read())
                    bValue = imgOrGIF.getvalue()
                    if r.status in range(200, 299):
                        emojiCreate = await ctx.guild.create_custom_emoji(image=bValue, name=name)
                        await ctx.send(embed=discord.Embed(description=f"**<:tick:897382645321850920> Successfully created emoji - {emojiCreate} with name: `{name}`**", color=discord.Color.green()))
                    else:
                        await ctx.send(embed=discord.Embed(description=f"<:error:897382665781669908> An error occured while creating the emoji | {r.status}", color=discord.Color.red()))
                except discord.HTTPException:
                    await ctx.send(embed=discord.Embed(description=f"<:error:897382665781669908> The file size is too big!", color=discord.Color.red()))
                except Exception as e:
                    print(e)

    @commands.command(aliases=['emojisteal', 'copyemoji', 'steal'])
    @commands.has_permissions(manage_emojis_and_stickers=True)
    async def stealemoji(self, ctx: commands.Context, emoji: Union[discord.Emoji, discord.PartialEmoji], *, name: str):
        """Steal an emoji for another server.... The bot adds the emoji to this server"""
        try:
            emoji_bytes = await emoji.read()
            emoji_create = await ctx.guild.create_custom_emoji(image=emoji_bytes, name=name)
            await ctx.send(embed=discord.Embed(description=f"**<:tick:897382645321850920> Successfully created emoji - {emoji_create} with name: `{name}`**", color=discord.Color.green()))
            
        except Exception as e:
            error = str(e).capitalize()
            return await ctx.send(embed=discord.Embed(description=f"**<:error:897382665781669908> An error occurred while creating the emoji\n`{error}`**", color=discord.Color.red()))

    
    @commands.command(aliases=['userinfo'])
    async def whois(self, ctx: commands.Context, user: Union[discord.Member, discord.User]=None):
        """Get information about a user or yourself"""
        user = user or ctx.author

        accType = "Bot" if user.bot else "Human"

        badge_emojis = {
            "bug_hunter": str(self.bot.get_emoji(928298721916112916)),
            "bug_hunter_level_2": str(self.bot.get_emoji(928298721303736361)),
            "discord_certified_moderator": str(self.bot.get_emoji(928298721475698708)),
            "early_supporter": str(self.bot.get_emoji(928298721496686692)),
            "verified_bot_developer": str(self.bot.get_emoji(928299192428953660)),
            "hypesquad": str(self.bot.get_emoji(930418236678340668)),
            "hypesquad_balance": str(self.bot.get_emoji(928299452446412821)),
            "hypesquad_bravery": str(self.bot.get_emoji(928299808974843984)),
            "hypesquad_brilliance": str(self.bot.get_emoji(928299672840327208)),
            "partner": str(self.bot.get_emoji(928502472891330622)),
            "staff": str(self.bot.get_emoji(928502668224262195))
        }

        def get_badges(user: Union[discord.User, discord.Member]):
            badges = []
            for badge, value in iter(user.public_flags):
                if value and badge in badge_emojis.keys():
                    badges.append(badge_emojis[badge])
            return badges

        if not user in ctx.guild.members:
            em = discord.Embed(
                description=f"""**• Username: `{user}`
• UserID: `{user.id}`
• Account Type: `{accType}`
• Created at: {discord.utils.format_dt(user.created_at)}
• Badges: {"  ".join(get_badges(user)) if len(get_badges(user)) > 0 else "`-`"}**""",
                color=discord.Color.green()
            ).set_author(name=user.name, icon_url=user.avatar.url).set_thumbnail(url=user.avatar.url).set_footer(text="Note: This user is not from this server", icon_url=user.avatar.url)
            user_for_banner = await self.bot.fetch_user(user.id)
            if user_for_banner.banner:
                em.set_image(url=user_for_banner.banner.url)
            
            return await ctx.send(embed=em)

        member: discord.Member = ctx.guild.get_member(user.id)
        
        def timedOut(member: discord.Member):
            """Gets a string type of `member.timed_out` rather than a boolean type"""
            if member.timed_out:
                return "Yes"
            else:
                return "No"

        def getRoles(member: discord.Member):
            """Gets the user roles"""
            if len(list(member.roles)) == 0:
                return "-"
            else:
                sorted_roles = sorted(
                    [role for role in member.roles[1:]], key=lambda x: x.position, reverse=True
                )
                roles = " ".join(role.mention for role in sorted_roles)
                return roles

        nick = user.nick if user.nick else "-"

        embed = discord.Embed(
            description=f"""**• Username: `{user}`
• UserID: `{user.id}`
• Nickname: `{nick}`
• Account Type: `{accType}`
• Created at: {discord.utils.format_dt(user.created_at)}
• Joined at: {discord.utils.format_dt(member.joined_at)}
• Timed Out: `{timedOut(member)}`
• Roles: {getRoles(member)}
• Badges: {"  ".join(get_badges(user)) if len(get_badges(user)) > 0 else "`-`"}**""",
            color=user.color
        ).set_author(name=user.name, icon_url=user.avatar.url).set_thumbnail(url=user.avatar.url)
        userForBanner = await self.bot.fetch_user(user.id)
        if userForBanner.banner:
            embed.set_image(url=userForBanner.banner.url)

        return await ctx.send(embed=embed)

    @commands.command(aliases=['sourcecode'])
    async def source(self, ctx: commands.Context):
        await ctx.send("Here is my source code", view=SourceView())

    @commands.command(aliases=['support', 'botserver', 'supportguild', 'supportserverinvite'])
    async def supportserver(self, ctx: commands.Context):
        await ctx.send("Here is my support server invite", view=SupportView())

    @commands.command()
    async def vote(self, ctx: commands.Context):
        """Vote the bot on [top.gg](https://top.gg/bot/919314151535419463/vote)"""
        await ctx.send("Vote me now!", view=VoteView())

    @commands.command(aliases=['guildinfo'])
    @commands.guild_only()
    async def serverinfo(self, ctx: commands.Context):
        """Get information about the server"""
        guild = ctx.guild
        icon = guild.icon.url or "https://discord.com/assets/2d20a45d79110dc5bf947137e9d99b66.svg"
        embed = discord.Embed(
            description=f"""**• Owner: {guild.owner.mention}
• ServerID: `{guild.id}`**
• Members: `{len(guild.members)}`
• Created at: {discord.utils.format_dt(guild.created_at)}
• Roles: `{len(guild.roles)}`
• Text Channels: `{len(guild.text_channels)}`
• Voice Channels: `{len(guild.voice_channels)}`""",
            color=discord.Color.green()
        ).set_author(name=guild.name, icon_url=icon).set_thumbnail(url=icon)
        if guild.banner:
            embed.set_image(url=guild.banner.url)

        return await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Misc(bot))