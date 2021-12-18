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
        await ctx.send(embed=discord.Embed(description="**Akinator is here to guess!\n--------------------------------\nOptions: <:tick:897382645321850920>: `yes`<:error:897382665781669908>: `no`, <:idk:921509553953185832>: `Don't know`\n👍: `probably`👎: `probably not`\n⏮: `previous question`, 🔴: `end the game`**", color=discord.Color.green()).set_image(url="https://static.wikia.nocookie.net/video-game-character-database/images/9/9f/Akinator.png/revision/latest?cb=20200817020737"))
        desc_loss = ''
        d_loss = ''

        def check_c(reaction, user):
            return user == ctx.author and str(
                reaction.emoji) in emojis_c and reaction.message.content == q

        def check_w(reaction, user):
            return user == ctx.author and str(reaction.emoji) in emojis_w

        try:
            aki = ak.Akinator()    
            q = await aki.start_game()

            while aki.progression <= 85:
                embedSend = discord.Embed(description=f"**{q}**", color=discord.Color.orange())
                message = await ctx.send(embed=embedSend)

                for m in emojis_c:
                    await message.add_reaction(m)

                try:
                    symbol, username = await self.bot.wait_for('reaction_add',
                                                        timeout=45.0,
                                                        check=check_c)
                except asyncio.TimeoutError:
                    embed_game_ended = discord.Embed(
                        description='**<:error:897382665781669908> You took too long,the game has ended!**',
                        color=discord.Color.red())
                    await ctx.send(embed=embed_game_ended)
                    return

                if str(symbol) == emojis_c[0]:
                    a = 'y'
                elif str(symbol) == emojis_c[1]:
                    a = 'n'
                elif str(symbol) == emojis_c[2]:
                    a = 'idk'
                elif str(symbol) == emojis_c[3]:
                    a = 'p'
                elif str(symbol) == emojis_c[4]:
                    a = 'pn'
                elif str(symbol) == emojis_c[5]:
                    a = 'b'
                elif str(symbol) == emojis_c[6]:
                    embed_game_end = discord.Embed(
                        title='I ended the game because you asked me to do it',
                        color=discord.Color.red())
                    await ctx.send(embed=embed_game_end)
                    return

                if a == "b":
                    try:
                        q = await aki.back()
                    except ak.CantGoBackAnyFurther:
                        pass
                else:
                    q = await aki.answer(a)

            await aki.win()

            wm = await ctx.send(
                embed=w(aki.first_guess['name'], aki.first_guess['description'],
                        aki.first_guess['absolute_picture_path']))

            for e in emojis_w:
                await wm.add_reaction(e)

            try:
                s, u = await self.bot.wait_for('reaction_add',
                                        timeout=30.0,
                                        check=check_w)
            except asyncio.TimeoutError:
                for times in aki.guesses:
                    d_loss = d_loss + times['name'] + '\n'
                t_loss = 'Here is a list of all the people I had in mind :'
                embed_loss = discord.Embed(title=t_loss,
                                        description=d_loss,
                                        color=discord.Color.red())
                await ctx.send(embed=embed_loss)
                return

            if str(s) == emojis_w[0]:
                embed_win = discord.Embed(
                    title='Great, guessed right one more time!', color=0x00FF00)
                await ctx.send(embed=embed_win)
            elif str(s) == emojis_w[1]:
                for times in aki.guesses:
                    desc_loss = desc_loss + times['name'] + '\n'
                title_loss = 'No problem, I will win next time! But here is a list of all the people I had in mind :'
                embed_loss = discord.Embed(title=title_loss,
                                        description=desc_loss,
                                        color=discord.Color.red())
                await ctx.send(embed=embed_loss)
        except Exception as error:
            print(error)


def setup(bot):
    bot.add_cog(FunCog(bot))