import discord
from discord.ext import tasks, commands
from discord.commands import slash_command, user_command
from discord.commands import Option
from discord.commands import permissions
import qrcode
import os
from pytube import YouTube
from speedtest import Speedtest
from utils.buttons import NukeView
import aiohttp
from io import BytesIO


class Misc(commands.Cog, name="Misc", description="Miscellaneous commands!"):
    def __init__(self, bot):
        self.bot = bot


    #Avatar
    @slash_command(guild_ids=[824969244860088332, 847740349853073418, 865962392093851658, 896457384552202312, 918802666790993951], description="Check your or someone else's PFP!")
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
    @slash_command(guild_ids=[824969244860088332, 847740349853073418, 865962392093851658, 896457384552202312, 918802666790993951], description="Generate a Qrcode!")
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

    
    @commands.command(aliases=['eadd', 'ea', 'steal', 'emojisteal', 'stealemoji'])
    async def emojiadd(self, ctx: commands.Context, emoji: str, name: str):
        """Creates an emoji in the server"""
        guild: discord.Guild = ctx.guild
        async with aiohttp.ClientSession() as session:
            async with session.get(emoji) as r:
                try:
                    imgOrGIF = BytesIO(await r.read())
                    bValue = imgOrGIF.getvalue()
                    if r.status in range(200, 299):
                        emojiCreate = await guild.create_custom_emoji(image=bValue, name=name)
                        await ctx.send(embed=discord.Embed(description=f"**<:tick:897382645321850920> Successfully created emoji - {emojiCreate} with name: `{name}`**", color=discord.Color.red()))
                    else:
                        await ctx.send(embed=discord.Embed(description=f"<:error:897382665781669908> An error occured while creating the emoji | {r.status}", color=discord.Color.red()))
                except discord.HTTPException:
                    await ctx.send(embed=discord.Embed(description=f"<:error:897382665781669908> The file size is too big!", color=discord.Color.red()))
                except Exception as e:
                    print(e)


def setup(bot):
    bot.add_cog(Misc(bot))