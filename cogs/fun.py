import discord
from discord.ext import commands
from discord.commands import slash_command, Option
import random
from utils.buttons import NitroView, TicTacToe, BeerView, BeerPartyView



class FunCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(guild_ids=[824969244860088332, 847740349853073418, 865962392093851658, 896457384552202312, 918802666790993951], description="Generates a nitro link!")
    async def nitro(self, ctx):
        interaction: discord.Inteaction = ctx.interaction
        embed = discord.Embed(description=f"**{ctx.author.mention} generated a nitro link!**", color=discord.Color.nitro_pink())
        embed.set_image(url="https://media.discordapp.net/attachments/886639021772648469/903535585992523796/unknown.png")
        await interaction.response.send_message(embed=embed)
        message = await interaction.original_message()
        await message.edit(embed=embed, view=NitroView(message, ctx))

    
    @commands.command(name="nitro")
    async def nitro_(self, ctx):
        embed = discord.Embed(description=f"**{ctx.author.mention} generated a nitro link!**", color=discord.Color.nitro_pink())
        embed.set_image(url="https://media.discordapp.net/attachments/886639021772648469/903535585992523796/unknown.png")
        message = await ctx.send(embed=embed)
        await message.edit(embed=embed, view=NitroView(message, ctx))


    @slash_command(guild_ids=[824969244860088332, 847740349853073418, 865962392093851658, 896457384552202312, 918802666790993951], description="Play a TicTacToe Game with Yourself!")
    async def tictactoe(self, ctx: commands.Context):
        await ctx.respond("**TicTacToe**\n`X` goes first!", view=TicTacToe())

    @commands.command(name="tictactoe", aliases=['ttt'])
    async def tictactoe_(self, ctx):
        await ctx.send("**TicTacToe**\n`X` goes first!", view=TicTacToe())


    @slash_command(guild_ids=[824969244860088332, 847740349853073418, 865962392093851658, 896457384552202312, 918802666790993951], description="Ask Me Something!", name="8ball")
    async def eightball(self, ctx, *, question: Option(str, "The question you want to ask!", required=True, default=None)):
        responses = {"It is certain.":0x2ecc71,
                "It is decidedly so.":0x2ecc71,
                "Without a doubt.":0x2ecc71,
                "Yes - definitely.":0x2ecc71,
                "You may rely on it.":0x2ecc71,
                "As I see it, yes.":0x2ecc71,
                "Most likely.":0x2ecc71,
                "Outlook good.":0x2ecc71,
                "Yes.":0x2ecc71,
                "Signs point to yes.":0x2ecc71,
                "Reply hazy, try again.":0xe67e22,
                "Ask again later.":0xe74c3c,
                "Better not tell you now.":0xe74c3c,
                "Cannot predict now.":0xe74c3c,
                "Concentrate and ask again.":0xe74c3c,
                "Don't count on it.":0xe74c3c,
                "My reply is no.":0xe74c3c,
                "My sources say no.":0xe74c3c,
                "Outlook not so good.":0xe74c3c,
                "Very doubtful.":0xe67e22,
                "Maybe.":0xe67e22}

        answer = random.choice(list(responses.keys()))
        color = responses[answer]

        embed = discord.Embed(title=f"8ball", description=f"**:8ball: Question: {question}\n:8ball: Answer: {answer}**", color=color)
        embed.set_footer(text=f"Asked by {ctx.author.name}", icon_url=ctx.author.avatar.url)
        await ctx.respond(embed=embed)

    @commands.command(name="eightball", aliases=['8ball', '8b'])
    async def eightball_(self, ctx: commands.Context, *, question: str):
        responses = {"It is certain.":0x2ecc71,
                "It is decidedly so.":0x2ecc71,
                "Without a doubt.":0x2ecc71,
                "Yes - definitely.":0x2ecc71,
                "You may rely on it.":0x2ecc71,
                "As I see it, yes.":0x2ecc71,
                "Most likely.":0x2ecc71,
                "Outlook good.":0x2ecc71,
                "Yes.":0x2ecc71,
                "Signs point to yes.":0x2ecc71,
                "Reply hazy, try again.":0xe67e22,
                "Ask again later.":0xe74c3c,
                "Better not tell you now.":0xe74c3c,
                "Cannot predict now.":0xe74c3c,
                "Concentrate and ask again.":0xe74c3c,
                "Don't count on it.":0xe74c3c,
                "My reply is no.":0xe74c3c,
                "My sources say no.":0xe74c3c,
                "Outlook not so good.":0xe74c3c,
                "Very doubtful.":0xe67e22,
                "Maybe.":0xe67e22}

        answer = random.choice(list(responses.keys()))
        color = responses[answer]

        embed = discord.Embed(title=f"8ball", description=f"**:8ball: Question: {question}\n:8ball: Answer: {answer}**", color=color)
        embed.set_footer(text=f"Asked by {ctx.author.name}", icon_url=ctx.author.avatar)
        await ctx.send(embed=embed)

    
    @slash_command(guild_ids=[824969244860088332, 847740349853073418, 865962392093851658, 896457384552202312, 918802666790993951], description="Have a drink with yourself or someone")
    async def beer(self, ctx: commands.Context, user: Option(discord.Member, "The user you want to drink with")):
        user = user if user else ctx.author
        interaction: discord.Interaction = ctx.interaction
        if user.bot:
            embed = discord.Embed(description=f"**Hey {ctx.author.mention},\nBots don't have beer!\n-------------\nTry having it with a human!**", color=discord.Color.red())
            await interaction.response.send_message(embed=embed)
            return
        if user == ctx.author:
            embed = discord.Embed(description=f"**{ctx.author.mention} is having a great time drinking lonely! :beer:**", color=discord.Color.green())
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(description=f"**{ctx.author.mention} has invited {user.mention} for having a drink together :beers:!\n------------------------------------\nWould you like to join {user.mention}?**", color=discord.Color.orange())   
            await interaction.response.send_message(content=f"{user.mention}", embed=embed)
            message = await interaction.original_message()
            await message.edit(embed=embed, view=BeerView(user, ctx, message))

    @commands.command(name="beer")
    async def beer_(self, ctx: commands.Context, user: discord.Member=None):
        user = user if user else ctx.author
        if user.bot:
            embed = discord.Embed(description=f"**Hey {ctx.author.mention},\nBots don't have beer!\n--------------------------\nTry having it with a human!**", color=discord.Color.red())
            await ctx.send(embed=embed)
            return
        if user == ctx.author:
            embed = discord.Embed(description=f"**{ctx.author.mention} is having a great time drinking lonely! :beer:**", color=discord.Color.green())
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description=f"**{ctx.author.mention} has invited {user.mention} for having a drink together :beers:!\n------------------------------------\nWould you like to join {user.mention}?**", color=discord.Color.orange())   
            message = await ctx.send(content=f"{user.mention}", embed=embed)
            await message.edit(embed=embed, view=BeerView(user, ctx, message))


    @slash_command(guild_ids=[824969244860088332, 847740349853073418, 865962392093851658, 896457384552202312, 918802666790993951], description="Have a beer party with some friends 🍻!")
    async def beerparty(self, ctx: commands.Context):
        interaction: discord.Interaction = ctx.interaction
        embed = discord.Embed(title="Beer Party 🍻", description=f"{ctx.author.mention} had invited everyone to join up this beer party :beers:!", color=discord.Color.green())
        await interaction.response.send_message(embed=embed)
        message = await interaction.original_message()
        await message.edit(embed=embed, view=BeerPartyView(message, ctx))

    @commands.command(name="beerparty")
    async def beerparty_(self, ctx: commands.Context):
        embed = discord.Embed(title="Beer Party 🍻", description=f"{ctx.author.mention} had invited everyone to join up this beer party :beers:!", color=discord.Color.green())
        message = await ctx.send(embed=embed)
        await message.edit(embed=embed, view=BeerPartyView(message, ctx))
    


def setup(bot):
    bot.add_cog(FunCog(bot))