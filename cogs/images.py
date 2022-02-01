import discord
from discord.ext import commands
from bot import Bot
from typing import *


class Images(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.group(aliases=['img'], invoke_without_command=True)
    async def image(self, ctx: commands.Context):
        """Command group to get images use `help` and then checkout the MISC category for sub commands. These commands work on an avatar. Basic Usage: `image <command> [user]`. If user is not specified, the command will use the author's avatar."""
        await ctx.send_help(ctx.command)

    @image.command(aliases=['lgbt', 'lbtq'])
    async def gay(self, ctx: commands.Context, user: Optional[discord.Member]):
        """Get the avatar formatted in the `gay` touch"""
        user = user or ctx.author
        try:
            avatar = user.avatar.with_format("png").url
        except AttributeError:
            return await ctx.send(embed=discord.Embed(description="**<:error:89738266578166908> That user doesn't have any avatar!**", color=discord.Color.red()))
        except Exception as e:
            return await ctx.send(embed=discord.Embed(description=f"**<:error:89738266578166908> An error occured\n{str(e).capitalize()}**", color=discord.Color.red()))
        url = f"https://some-random-api.ml/canvas/gay?avatar={avatar}"
        r = await self.bot.session.get(url)
        if 300 > r.status >= 200:
            data = await r.content
        else:
            return await ctx.send(embed=discord.Embed(description="**<:error:897382665781669908> An error occured!**", color=discord.Color.red()))
        
        await ctx.send(
            embed=discord.Embed(color=discord.Color.embed_background(theme="dark")).set_image(url=data)
        )

    @image.command()
    async def glass(self, ctx: commands.Context, user: Optional[discord.Member]):
        """Get the avatar formatted in the `glass` touch"""
        user = user or ctx.author
        try:
            avatar = user.avatar.with_format("png").url
        except AttributeError:
            return await ctx.send(embed=discord.Embed(description="**<:error:89738266578166908> That user doesn't have any avatar!**", color=discord.Color.red()))
        except Exception as e:
            return await ctx.send(embed=discord.Embed(description=f"**<:error:89738266578166908> An error occured\n{str(e).capitalize()}**", color=discord.Color.red()))
        url = f"https://some-random-api.ml/canvas/gay?avatar={avatar}"
        r = await self.bot.session.get(url)
        if 300 > r.status >= 200:
            data = await r.content
        else:
            return await ctx.send(embed=discord.Embed(description="**<:error:897382665781669908> An error occured!**", color=discord.Color.red()))
        
        await ctx.send(
            embed=discord.Embed(color=discord.Color.embed_background(theme="dark")).set_image(url=data)
        )

    @image.command()
    async def wasted(self, ctx: commands.Context, user: Optional[discord.Member]):
        """Get the avatar formatted in the `wasted` touch"""
        user = user or ctx.author
        try:
            avatar = user.avatar.with_format("png").url
        except AttributeError:
            return await ctx.send(embed=discord.Embed(description="**<:error:89738266578166908> That user doesn't have any avatar!**", color=discord.Color.red()))
        except Exception as e:
            return await ctx.send(embed=discord.Embed(description=f"**<:error:89738266578166908> An error occured\n{str(e).capitalize()}**", color=discord.Color.red()))
        url = f"https://some-random-api.ml/canvas/wasted?avatar={avatar}"
        r = await self.bot.session.get(url)
        if 300 > r.status >= 200:
            data = await r.content
        else:
            return await ctx.send(embed=discord.Embed(description="**<:error:897382665781669908> An error occured!**", color=discord.Color.red()))
        
        await ctx.send(
            embed=discord.Embed(color=discord.Color.embed_background(theme="dark")).set_image(url=data)
        )
    
    @image.command(aliases=['mp'])
    async def missionpassed(self, ctx: commands.Context, user: Optional[discord.Member]):
        """Get the avatar formatted in the `mission passed` touch"""
        user = user or ctx.author
        try:
            avatar = user.avatar.with_format("png").url
        except AttributeError:
            return await ctx.send(embed=discord.Embed(description="**<:error:89738266578166908> That user doesn't have any avatar!**", color=discord.Color.red()))
        except Exception as e:
            return await ctx.send(embed=discord.Embed(description=f"**<:error:89738266578166908> An error occured\n{str(e).capitalize()}**", color=discord.Color.red()))
        url = f"https://some-random-api.ml/canvas/missionpassed?avatar={avatar}"
        r = await self.bot.session.get(url)
        if 300 > r.status >= 200:
            data = await r.content
        else:
            return await ctx.send(embed=discord.Embed(description="**<:error:897382665781669908> An error occured!**", color=discord.Color.red()))
        
        await ctx.send(
            embed=discord.Embed(color=discord.Color.embed_background(theme="dark")).set_image(url=data)
        )

    @image.command()
    async def jail(self, ctx: commands.Context, user: Optional[discord.Member]):
        """Get the avatar formatted in the `jail` touch"""
        user = user or ctx.author
        try:
            avatar = user.avatar.with_format("png").url
        except AttributeError:
            return await ctx.send(embed=discord.Embed(description="**<:error:89738266578166908> That user doesn't have any avatar!**", color=discord.Color.red()))
        except Exception as e:
            return await ctx.send(embed=discord.Embed(description=f"**<:error:89738266578166908> An error occured\n{str(e).capitalize()}**", color=discord.Color.red()))
        url = f"https://some-random-api.ml/canvas/jail?avatar={avatar}"
        r = await self.bot.session.get(url)
        if 300 > r.status >= 200:
            data = await r.content
        else:
            return await ctx.send(embed=discord.Embed(description="**<:error:897382665781669908> An error occured!**", color=discord.Color.red()))
        
        await ctx.send(
            embed=discord.Embed(color=discord.Color.embed_background(theme="dark")).set_image(url=data)
        )
    
    @image.command()
    async def comrade(self, ctx: commands.Context, user: Optional[discord.Member]):
        """Get the avatar formatted in the `comrade` touch"""
        user = user or ctx.author
        try:
            avatar = user.avatar.with_format("png").url
        except AttributeError:
            return await ctx.send(embed=discord.Embed(description="**<:error:89738266578166908> That user doesn't have any avatar!**", color=discord.Color.red()))
        except Exception as e:
            return await ctx.send(embed=discord.Embed(description=f"**<:error:89738266578166908> An error occured\n{str(e).capitalize()}**", color=discord.Color.red()))
        url = f"https://some-random-api.ml/canvas/comrade?avatar={avatar}"
        r = await self.bot.session.get(url)
        if 300 > r.status >= 200:
            data = await r.content
        else:
            return await ctx.send(embed=discord.Embed(description="**<:error:897382665781669908> An error occured!**", color=discord.Color.red()))
        
        await ctx.send(
            embed=discord.Embed(color=discord.Color.embed_background(theme="dark")).set_image(url=data)
        )
    
    @image.command()
    async def triggered(self, ctx: commands.Context, user: Optional[discord.Member]):
        """Get the avatar formatted in the `triggered` touch"""
        user = user or ctx.author
        try:
            avatar = user.avatar.with_format("png").url
        except AttributeError:
            return await ctx.send(embed=discord.Embed(description="**<:error:89738266578166908> That user doesn't have any avatar!**", color=discord.Color.red()))
        except Exception as e:
            return await ctx.send(embed=discord.Embed(description=f"**<:error:89738266578166908> An error occured\n{str(e).capitalize()}**", color=discord.Color.red()))
        url = f"https://some-random-api.ml/canvas/triggered?avatar={avatar}"
        r = await self.bot.session.get(url)
        if 300 > r.status >= 200:
            data = await r.content
        else:
            return await ctx.send(embed=discord.Embed(description="**<:error:897382665781669908> An error occured!**", color=discord.Color.red()))
        
        await ctx.send(
            embed=discord.Embed(color=discord.Color.embed_background(theme="dark")).set_image(url=data)
        )
    
    @image.group(invoke_without_command=True)
    async def filter(self, ctx: commands.Context):
        """Image filters. Has the same syntax as the image command. `image filter <name_of_filter> [user]`"""
        await ctx.send_help(ctx.command)

    @filter.command()
    async def greyscale(self, ctx: commands.Context, user: Optional[discord.Member]):
        """Get the avatar formatted in the `greyscale` filter"""
        user = user or ctx.author
        try:
            avatar = user.avatar.with_format("png").url
        except AttributeError:
            return await ctx.send(embed=discord.Embed(description="**<:error:89738266578166908> That user doesn't have any avatar!**", color=discord.Color.red()))
        except Exception as e:
            return await ctx.send(embed=discord.Embed(description=f"**<:error:89738266578166908> An error occured\n{str(e).capitalize()}**", color=discord.Color.red()))
        url = f"https://some-random-api.ml/canvas/greyscale?avatar={avatar}"
        r = await self.bot.session.get(url)
        if 300 > r.status >= 200:
            data = await r.content
        else:
            return await ctx.send(embed=discord.Embed(description="**<:error:897382665781669908> An error occured!**", color=discord.Color.red()))
        
        await ctx.send(
            embed=discord.Embed(color=discord.Color.embed_background(theme="dark")).set_image(url=data)
        )
    
    @filter.command()
    async def invert(self, ctx: commands.Context, user: Optional[discord.Member]):
        """Get the avatar formatted in the `invert` filter"""
        user = user or ctx.author
        try:
            avatar = user.avatar.with_format("png").url
        except AttributeError:
            return await ctx.send(embed=discord.Embed(description="**<:error:89738266578166908> That user doesn't have any avatar!**", color=discord.Color.red()))
        except Exception as e:
            return await ctx.send(embed=discord.Embed(description=f"**<:error:89738266578166908> An error occured\n{str(e).capitalize()}**", color=discord.Color.red()))
        url = f"https://some-random-api.ml/canvas/invert?avatar={avatar}"
        r = await self.bot.session.get(url)
        if 300 > r.status >= 200:
            data = await r.content
        else:
            return await ctx.send(embed=discord.Embed(description="**<:error:897382665781669908> An error occured!**", color=discord.Color.red()))
        
        await ctx.send(
            embed=discord.Embed(color=discord.Color.embed_background(theme="dark")).set_image(url=data)
        )
    
    @filter.command(aliases=['igs'])
    async def invertgreyscale(self, ctx: commands.Context, user: Optional[discord.Member]):
        """Get the avatar formatted in the `invertgreyscale` filter"""
        user = user or ctx.author
        try:
            avatar = user.avatar.with_format("png").url
        except AttributeError:
            return await ctx.send(embed=discord.Embed(description="**<:error:89738266578166908> That user doesn't have any avatar!**", color=discord.Color.red()))
        except Exception as e:
            return await ctx.send(embed=discord.Embed(description=f"**<:error:89738266578166908> An error occured\n{str(e).capitalize()}**", color=discord.Color.red()))
        url = f"https://some-random-api.ml/canvas/invertgreyscale?avatar={avatar}"
        r = await self.bot.session.get(url)
        if 300 > r.status >= 200:
            data = await r.content
        else:
            return await ctx.send(embed=discord.Embed(description="**<:error:897382665781669908> An error occured!**", color=discord.Color.red()))
        
        await ctx.send(
            embed=discord.Embed(color=discord.Color.embed_background(theme="dark")).set_image(url=data)
        )

    @filter.command()
    async def brightness(self, ctx: commands.Context, brightness, user: discord.Member=None):
        """Get the avatar formatted in the `brightness` filter.. according to the brightness value"""
        user = user or ctx.author
        try:
            avatar = user.avatar.with_format("png").url
        except AttributeError:
            return await ctx.send(embed=discord.Embed(description="**<:error:89738266578166908> That user doesn't have any avatar!**", color=discord.Color.red()))
        except Exception as e:
            return await ctx.send(embed=discord.Embed(description=f"**<:error:89738266578166908> An error occured\n{str(e).capitalize()}**", color=discord.Color.red()))
        url = f"https://some-random-api.ml/canvas/brightness?avatar={avatar}&brightness={brightness}"
        r = await self.bot.session.get(url)
        if 300 > r.status >= 200:
            data = await r.content
        else:
            return await ctx.send(embed=discord.Embed(description="**<:error:897382665781669908> An error occured!**", color=discord.Color.red()))
        
        await ctx.send(
            embed=discord.Embed(color=discord.Color.embed_background(theme="dark")).set_image(url=data)
        )

    @filter.command()
    async def threshold(self, ctx: commands.Context, threshold, user: discord.Member=None):
        """Get the avatar formatted in the `threshold` filter... according to the threshold value"""
        user = user or ctx.author
        try:
            avatar = user.avatar.with_format("png").url
        except AttributeError:
            return await ctx.send(embed=discord.Embed(description="**<:error:89738266578166908> That user doesn't have any avatar!**", color=discord.Color.red()))
        except Exception as e:
            return await ctx.send(embed=discord.Embed(description=f"**<:error:89738266578166908> An error occured\n{str(e).capitalize()}**", color=discord.Color.red()))
        url = f"https://some-random-api.ml/canvas/threshold?avatar={avatar}&threshold={threshold}"
        r = await self.bot.session.get(url)
        if 300 > r.status >= 200:
            data = await r.content
        else:
            return await ctx.send(embed=discord.Embed(description="**<:error:897382665781669908> An error occured!**", color=discord.Color.red()))
        
        await ctx.send(
            embed=discord.Embed(color=discord.Color.embed_background(theme="dark")).set_image(url=data)
        )

    @filter.command()
    async def sepia(self, ctx: commands.Context, user: discord.Member=None):
        """Get the avatar formatted in the `sepia` filter"""
        user = user or ctx.author
        try:
            avatar = user.avatar.with_format("png").url
        except AttributeError:
            return await ctx.send(embed=discord.Embed(description="**<:error:89738266578166908> That user doesn't have any avatar!**", color=discord.Color.red()))
        except Exception as e:
            return await ctx.send(embed=discord.Embed(description=f"**<:error:89738266578166908> An error occured\n{str(e).capitalize()}**", color=discord.Color.red()))
        url = f"https://some-random-api.ml/canvas/sepia?avatar={avatar}"
        r = await self.bot.session.get(url)
        if 300 > r.status >= 200:
            data = await r.content
        else:
            return await ctx.send(embed=discord.Embed(description="**<:error:897382665781669908> An error occured!**", color=discord.Color.red()))
        
        await ctx.send(
            embed=discord.Embed(color=discord.Color.embed_background(theme="dark")).set_image(url=data)
        )
    
    @filter.command()
    async def red(self, ctx: commands.Context, user: discord.Member=None):
        """Get the avatar formatted in the `red` filter"""
        user = user or ctx.author
        try:
            avatar = user.avatar.with_format("png").url
        except AttributeError:
            return await ctx.send(embed=discord.Embed(description="**<:error:89738266578166908> That user doesn't have any avatar!**", color=discord.Color.red()))
        except Exception as e:
            return await ctx.send(embed=discord.Embed(description=f"**<:error:89738266578166908> An error occured\n{str(e).capitalize()}**", color=discord.Color.red()))
        url = f"https://some-random-api.ml/canvas/red?avatar={avatar}"
        r = await self.bot.session.get(url)
        if 300 > r.status >= 200:
            data = await r.content
        else:
            return await ctx.send(embed=discord.Embed(description="**<:error:897382665781669908> An error occured!**", color=discord.Color.red()))
        
        await ctx.send(
            embed=discord.Embed(color=discord.Color.embed_background(theme="dark")).set_image(url=data)
        )

    @filter.command()
    async def green(self, ctx: commands.Context, user: discord.Member=None):
        """Get the avatar formatted in the `green` filter"""
        user = user or ctx.author
        try:
            avatar = user.avatar.with_format("png").url
        except AttributeError:
            return await ctx.send(embed=discord.Embed(description="**<:error:89738266578166908> That user doesn't have any avatar!**", color=discord.Color.red()))
        except Exception as e:
            return await ctx.send(embed=discord.Embed(description=f"**<:error:89738266578166908> An error occured\n{str(e).capitalize()}**", color=discord.Color.red()))
        url = f"https://some-random-api.ml/canvas/green?avatar={avatar}"
        r = await self.bot.session.get(url)
        if 300 > r.status >= 200:
            data = await r.content
        else:
            return await ctx.send(embed=discord.Embed(description="**<:error:897382665781669908> An error occured!**", color=discord.Color.red()))
        
        await ctx.send(
            embed=discord.Embed(color=discord.Color.embed_background(theme="dark")).set_image(url=data)
        )

    @filter.command()
    async def blue(self, ctx: commands.Context, user: discord.Member=None):
        """Get the avatar formatted in the `blue` filter"""
        user = user or ctx.author
        try:
            avatar = user.avatar.with_format("png").url
        except AttributeError:
            return await ctx.send(embed=discord.Embed(description="**<:error:89738266578166908> That user doesn't have any avatar!**", color=discord.Color.red()))
        except Exception as e:
            return await ctx.send(embed=discord.Embed(description=f"**<:error:89738266578166908> An error occured\n{str(e).capitalize()}**", color=discord.Color.red()))
        url = f"https://some-random-api.ml/canvas/blue?avatar={avatar}"
        r = await self.bot.session.get(url)
        if 300 > r.status >= 200:
            data = await r.content
        else:
            return await ctx.send(embed=discord.Embed(description="**<:error:897382665781669908> An error occured!**", color=discord.Color.red()))
        
        await ctx.send(
            embed=discord.Embed(color=discord.Color.embed_background(theme="dark")).set_image(url=data)
        )

    @filter.command()
    async def blurple(self, ctx: commands.Context, user: discord.Member=None):
        """Get the avatar formatted in the `blurple` filter"""
        user = user or ctx.author
        try:
            avatar = user.avatar.with_format("png").url
        except AttributeError:
            return await ctx.send(embed=discord.Embed(description="**<:error:89738266578166908> That user doesn't have any avatar!**", color=discord.Color.red()))
        except Exception as e:
            return await ctx.send(embed=discord.Embed(description=f"**<:error:89738266578166908> An error occured\n{str(e).capitalize()}**", color=discord.Color.red()))
        url = f"https://some-random-api.ml/canvas/blurple?avatar={avatar}"
        r = await self.bot.session.get(url)
        if 300 > r.status >= 200:
            data = await r.content
        else:
            return await ctx.send(embed=discord.Embed(description="**<:error:897382665781669908> An error occured!**", color=discord.Color.red()))
        
        await ctx.send(
            embed=discord.Embed(color=discord.Color.embed_background(theme="dark")).set_image(url=data)
        )
    
    @filter.command(name="blurple2")
    async def blurpletwo(self, ctx: commands.Context, user: discord.Member=None):
        """Get the avatar formatted in the `blurple2` filter"""
        user = user or ctx.author
        try:
            avatar = user.avatar.with_format("png").url
        except AttributeError:
            return await ctx.send(embed=discord.Embed(description="**<:error:89738266578166908> That user doesn't have any avatar!**", color=discord.Color.red()))
        except Exception as e:
            return await ctx.send(embed=discord.Embed(description=f"**<:error:89738266578166908> An error occured\n{str(e).capitalize()}**", color=discord.Color.red()))
        url = f"https://some-random-api.ml/canvas/blurple2?avatar={avatar}"
        r = await self.bot.session.get(url)
        if 300 > r.status >= 200:
            data = await r.content
        else:
            return await ctx.send(embed=discord.Embed(description="**<:error:897382665781669908> An error occured!**", color=discord.Color.red()))
        
        await ctx.send(
            embed=discord.Embed(color=discord.Color.embed_background(theme="dark")).set_image(url=data)
        )
    
    @commands.command()
    async def pixelate(self, ctx: commands.Context, user: discord.Member=None):
        """`Pixelate` the avatar of the user"""
        user = user or ctx.author
        try:
            avatar = user.avatar.with_format("png").url
        except AttributeError:
            return await ctx.send(embed=discord.Embed(description="**<:error:89738266578166908> That user doesn't have any avatar!**", color=discord.Color.red()))
        except Exception as e:
            return await ctx.send(embed=discord.Embed(description=f"**<:error:89738266578166908> An error occured\n{str(e).capitalize()}**", color=discord.Color.red()))
        url = f"https://some-random-api.ml/canvas/pixelate?avatar={avatar}"
        r = await self.bot.session.get(url)
        if 300 > r.status >= 200:
            data = await r.content
        else:
            return await ctx.send(embed=discord.Embed(description="**<:error:897382665781669908> An error occured!**", color=discord.Color.red()))
        
        await ctx.send(
            embed=discord.Embed(color=discord.Color.embed_background(theme="dark")).set_image(url=data)
        )
    
    @commands.command()
    async def blur(self, ctx: commands.Context, user: discord.Member=None):
        """`Blur` the avatar of the user"""
        user = user or ctx.author
        try:
            avatar = user.avatar.with_format("png").url
        except AttributeError:
            return await ctx.send(embed=discord.Embed(description="**<:error:89738266578166908> That user doesn't have any avatar!**", color=discord.Color.red()))
        except Exception as e:
            return await ctx.send(embed=discord.Embed(description=f"**<:error:89738266578166908> An error occured\n{str(e).capitalize()}**", color=discord.Color.red()))
        url = f"https://some-random-api.ml/canvas/blur?avatar={avatar}"
        r = await self.bot.session.get(url)
        if 300 > r.status >= 200:
            data = await r.content
        else:
            return await ctx.send(embed=discord.Embed(description="**<:error:897382665781669908> An error occured!**", color=discord.Color.red()))
        
        await ctx.send(
            embed=discord.Embed(color=discord.Color.embed_background(theme="dark")).set_image(url=data)
        )
    
    @commands.command(name="comment", aliases=['ytcomment'])
    async def youtubecomment(self, ctx: commands.Context, comment: str):
        """Comment Something"""
        avatar = ctx.author.avatar_url_as(format="png").url if ctx.author.avatar else "https://pnggrid.com/wp-content/uploads/2021/05/Discord-Logo-Circle-1024x1024.png"
        url = f"https://some-random-api.ml/canvas/youtube-comment?avatar={avatar}&username={ctx.author.name}&comment={comment}"
        r = await self.bot.session.get(url)
        if 300 > r.status >= 200:
            data = await r.content
        else:
            return await ctx.send(embed=discord.Embed(description="**<:error:897382665781669908> An error occured!**", color=discord.Color.red()))
        
        await ctx.send(
            embed=discord.Embed(color=discord.Color.embed_background(theme="dark")).set_image(url=data)
        )

    @commands.command()
    async def tweet(self, ctx: commands.Context, tweet: str):
        """Tweet Something"""
        avatar = ctx.author.avatar_url_as(format="png").url if ctx.author.avatar else "https://pnggrid.com/wp-content/uploads/2021/05/Discord-Logo-Circle-1024x1024.png"
        url = f"https://some-random-api.ml/canvas/tweet?avatar={avatar}&username={ctx.author.name}&tweet={tweet}"
        r = await self.bot.session.get(url)
        if 300 > r.status >= 200:
            data = await r.content
        else:
            return await ctx.send(embed=discord.Embed(description="**<:error:897382665781669908> An error occured!**", color=discord.Color.red()))
        
        await ctx.send(
            embed=discord.Embed(color=discord.Color.embed_background(theme="dark")).set_image(url=data)
        )

    @commands.command()
    async def simpcard(self, ctx: commands.Context, user: discord.Member=None):
        """Get an offically verified Simp Card... which provides license to simp"""
        user = user or ctx.author
        try:
            avatar = user.avatar.with_format("png").url
        except AttributeError:
            return await ctx.send(embed=discord.Embed(description="**<:error:89738266578166908> That user doesn't have any avatar!**", color=discord.Color.red()))
        except Exception as e:
            return await ctx.send(embed=discord.Embed(description=f"**<:error:89738266578166908> An error occured\n{str(e).capitalize()}**", color=discord.Color.red()))
        url = f"https://some-random-api.ml/canvas/simpcard?avatar={avatar}"
        r = await self.bot.session.get(url)
        if 300 > r.status >= 200:
            data = await r.content
        else:
            return await ctx.send(embed=discord.Embed(description="**<:error:897382665781669908> An error occured!**", color=discord.Color.red()))
        
        await ctx.send(
            embed=discord.Embed(color=discord.Color.embed_background(theme="dark")).set_image(url=data)
        )

    @commands.command(aliases=['horny'])
    async def hornycard(self, ctx: commands.Context, user: discord.Member=None):
        """Get an offically verified Horny Card... which provides license to be horny"""
        user = user or ctx.author
        try:
            avatar = user.avatar.with_format("png").url
        except AttributeError:
            return await ctx.send(embed=discord.Embed(description="**<:error:89738266578166908> That user doesn't have any avatar!**", color=discord.Color.red()))
        except Exception as e:
            return await ctx.send(embed=discord.Embed(description=f"**<:error:89738266578166908> An error occured\n{str(e).capitalize()}**", color=discord.Color.red()))
        url = f"https://some-random-api.ml/canvas/horny?avatar={avatar}"
        r = await self.bot.session.get(url)
        if 300 > r.status >= 200:
            data = await r.content
        else:
            return await ctx.send(embed=discord.Embed(description="**<:error:897382665781669908> An error occured!**", color=discord.Color.red()))
        
        await ctx.send(
            embed=discord.Embed(color=discord.Color.embed_background(theme="dark")).set_image(url=data)
        )

    @commands.command(aliases=['lolipolice'])
    async def lolice(self, ctx: commands.Context, user: discord.Member=None):
        """LOLICE (LOLI POLICE)"""
        user = user or ctx.author
        try:
            avatar = user.avatar.with_format("png").url
        except AttributeError:
            return await ctx.send(embed=discord.Embed(description="**<:error:89738266578166908> That user doesn't have any avatar!**", color=discord.Color.red()))
        except Exception as e:
            return await ctx.send(embed=discord.Embed(description=f"**<:error:89738266578166908> An error occured\n{str(e).capitalize()}**", color=discord.Color.red()))
        url = f"https://some-random-api.ml/canvas/lolice?avatar={avatar}"
        r = await self.bot.session.get(url)
        if 300 > r.status >= 200:
            data = await r.content
        else:
            return await ctx.send(embed=discord.Embed(description="**<:error:897382665781669908> An error occured!**", color=discord.Color.red()))
        
        await ctx.send(
            embed=discord.Embed(color=discord.Color.embed_background(theme="dark")).set_image(url=data)
        )

def setup(bot: Bot):
    bot.add_cog(Images(bot))