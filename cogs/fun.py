import discord
from discord.ext import commands
from discord.commands import slash_command, Option
import random
from utils.buttons import NitroView, TicTacToe, BeerView, BeerPartyView
import asyncio
import akinator as ak


emojis_c = ['<:tick:897382645321850920>', '<:error:897382665781669908>', '<:idk:921509553953185832>', '👍', '👎', '⏮', '🔴']
emojis_w = ['<:tick:897382645321850920>', '<:error:897382665781669908>']

def w(name, desc, picture):
    embed_win = discord.Embed(description=f"**Is it {name}\n{desc}**", color=discord.Color.orange()).set_image(url=picture)
    return embed_win

class FunCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
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
                "send hazy, try again.":0xe67e22,
                "Ask again later.":0xe74c3c,
                "Better not tell you now.":0xe74c3c,
                "Cannot predict now.":0xe74c3c,
                "Concentrate and ask again.":0xe74c3c,
                "Don't count on it.":0xe74c3c,
                "My send is no.":0xe74c3c,
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
                "send hazy, try again.":0xe67e22,
                "Ask again later.":0xe74c3c,
                "Better not tell you now.":0xe74c3c,
                "Cannot predict now.":0xe74c3c,
                "Concentrate and ask again.":0xe74c3c,
                "Don't count on it.":0xe74c3c,
                "My send is no.":0xe74c3c,
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
        if user.self.bot:
            embed = discord.Embed(description=f"**Hey {ctx.author.mention},\nself.bots don't have beer!\n-------------\nTry having it with a human!**", color=discord.Color.red())
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
        if user.self.bot:
            embed = discord.Embed(description=f"**Hey {ctx.author.mention},\nself.bots don't have beer!\n--------------------------\nTry having it with a human!**", color=discord.Color.red())
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
    
    @commands.command(name="coinflip")
    async def coinflip_(self, ctx: commands.Context):
        coinsides = ['Heads', 'Tails']
        message = await ctx.send(embed=discord.Embed(description=f"**Flipping a coin! <a:loading:911568431315292211>**", color=discord.Color.orange()))
        await asyncio.sleep(1)
        await message.edit(embed=discord.Embed(description=f"**`{random.choice(coinsides)}` it is!**", color=discord.Color.green()))

    @commands.command(name="akinator", aliases=['aki', 'ak', 'akinat'])
    async def akinator_(self, ctx: commands.Context):
        await ctx.send(embed=discord.Embed(description="**Yukinator is here to guess!\n--------------------------------\nOptions: y: `yes\n`no: `n`\nidk: `Don't know`\np: `probably`\npn: `probably not`\nb: `previous question`**", color=discord.Color.green()).set_image(url="https://static.wikia.nocookie.net/video-game-character-database/images/9/9f/Akinator.png/revision/latest?cb=20200817020737"))
        def check(msg):
            return (
                msg.author == ctx.author
                and msg.channel == ctx.channel
                and msg.content.lower() in ["y", "n", "p", "pn", "b"]
            )

        try:
            aki = ak.Akinator()
            q = aki.start_game()
            while aki.progression <= 80:
                await ctx.send(embed=discord.Embed(description=f"**{q}\n\n[y | n | p | pn | b]**", color=discord.Color.embed_background(theme="dark")))
                msg = await self.bot.wait_for("message", check=check)
                if msg.content.lower() == "b":
                    try:
                        q = aki.back()
                    except ak.CantGoBackAnyFurther:
                        await ctx.send(embed=discord.Embed(description=f"**<:error:897382665781669908> {e}**"))
                        continue
                else:
                    try:
                        q = aki.answer(msg.content.lower())
                    except ak.InvalidAnswerError as e:
                        await ctx.send(embed=discord.Embed(description=f"**<:error:897382665781669908> {e}**"))
                        continue
            aki.win()
            await ctx.send(
                embed=discord.Embed(description=f"**Is it {aki.first_guess['name']}\n({aki.first_guess['description']})!\nWas I correct?(y/n)\n\t**", color=discord.Color.orange()).set_image(url=aki.first_guess['absolute_picture_path'])
            )
            correct = await self.bot.wait_for("message", check=check)
            if correct.content.lower() == "y":
                await ctx.send(embed=discord.Embed(description="**Yay!**", color=discord.Color.green()))
            else:
                await ctx.send(embed=discord.Embed(description="**Oof!**", color=discord.Color.red()))
        except Exception as e:
            await ctx.send(e)


def setup(bot):
    bot.add_cog(FunCog(bot))