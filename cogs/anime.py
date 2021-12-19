import discord
from discord.ext import commands
from discord.ext.commands import BucketType
from config import tenor_api_key
import random
import requests
import json


class CuteCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="hug")
    @commands.cooldown(1, 10, BucketType.user)
    async def hug_(self, ctx: commands.Context, user: discord.Member):
        if user == ctx.author:
            return await ctx.send(embed=discord.Embed(description="**<:error:897382665781669908> You can't hug yourself!\n--------------------------\nTry hugging someone else.**", color=discord.Color.red()))

        if user.bot:
            return await ctx.send(embed=discord.Embed(description="**<:error:897382665781669908> You can't pat a bot!\n--------------------------\nTry hugging an human.**", color=discord.Color.red()))

        query = "anime hug"
        lmt = 50
        r = requests.get(
            "https://api.tenor.com/v1/search?q=%s&key=%s&limit=%s" % (query, tenor_api_key, lmt)
        )

        if r.status_code == 200:
            top_gifs = json.loads(r.content)
            url = random.choice(random.choice(top_gifs["results"])["media"])["gif"]["url"]
        else:
            return await ctx.send(embed=discord.Embed(description="**<:error:897382665781669908> Couldn't generate a gif. Please try again later.**", color=discord.Color.red()))
        
        embed = discord.Embed(description=f"**<:hug:922213806027968573> {ctx.author.mention} hugged {user.mention}!**", color=discord.Color.embed_background(theme="dark")).set_image(url=url)
        await ctx.send(embed=embed)

    @commands.command(name="pat", aliases=['pats', 'headpat', 'headpats'])
    @commands.cooldown(1, 10, BucketType.user)
    async def pat_(self, ctx: commands.Context, user: discord.Member):
        if user == ctx.author:
            return await ctx.send(embed=discord.Embed(description="**<:error:897382665781669908> You can't pat yourself!\n--------------------------\nTry hugging someone else.**", color=discord.Color.red()))

        if user.bot:
            return await ctx.send(embed=discord.Embed(description="**<:error:897382665781669908> You can't pat a bot!\n--------------------------\nTry patting an human.**", color=discord.Color.red()))
        
        query = "anime head pat"
        lmt = 50
        r = requests.get(
            "https://api.tenor.com/v1/search?q=%s&key=%s&limit=%s" % (query, tenor_api_key, lmt)
        )

        if r.status_code == 200:
            top_gifs = json.loads(r.content)
            url = random.choice(random.choice(top_gifs["results"])["media"])["gif"]["url"]
        else:
            return await ctx.send(embed=discord.Embed(description="**<:error:897382665781669908> Couldn't generate a gif. Please try again later.**", color=discord.Color.red()))

        embed = discord.Embed(description=f"**{ctx.author.mention} patted {user.mention}**", color=discord.Color.embed_background(theme="dark")).set_image(url=url)
        await ctx.send(embed=embed)

    @commands.command(name="gif")
    @commands.cooldown(1, 10, BucketType.user)
    async def gif_(self, ctx: commands.Context, *, query: str):
        lmt = 50
        r = requests.get(
            "https://api.tenor.com/v1/search?q=%s&key=%s&limit=%s" % (query, tenor_api_key, lmt)
        )
        
        if r.status_code == 200:
            top_gifs = json.loads(r.content)
            url = random.choice(random.choice(top_gifs["results"])["media"])["gif"]["url"]
        else:
            return await ctx.send(embed=discord.Embed(description="**<:error:897382665781669908> Couldn't generate a gif. Please try again later.**", color=discord.Color.red()))
        
        await ctx.send(embed=discord.Embed(description=f"**Random result for {query}**", color=discord.Color.embed_background(theme="dark")).set_image(url=url))

def setup(bot):
    bot.add_cog(CuteCog(bot))