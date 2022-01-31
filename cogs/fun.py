import discord
from discord.ext import commands
from discord.commands import slash_command, Option
import random
from utils.buttons import NitroView, TicTacToe, BeerView, BeerPartyView
import asyncio
import akinator as ak
from discord.ext.commands import BucketType
from config import GIPHY_API_KEY
from bot import Bot
from giphy_client.rest import ApiException
from utils.helpers.configuration import *
import requests

def w(name, desc, picture):
    embed_win = discord.Embed(description=f"**Is it {name}\n{desc}**", color=discord.Color.orange()).set_image(url=picture)
    return embed_win

class FunCog(commands.Cog, name="Fun", description="Fun Stuff!"):
    """Fun commands that you would enjoy to use!"""
    def __init__(self, bot: Bot):
        self.bot = bot

    @slash_command(description="Generates a nitro link!")
    async def nitro(self, ctx):
        interaction: discord.Inteaction = ctx.interaction
        embed = discord.Embed(description=f"**{ctx.author.mention} generated a nitro link!**", color=discord.Color.nitro_pink())
        embed.set_image(url="https://media.discordapp.net/attachments/886639021772648469/903535585992523796/unknown.png")
        await interaction.response.send_message(embed=embed)
        message = await interaction.original_message()
        await message.edit(embed=embed, view=NitroView(message, ctx))

    
    @commands.command(name="nitro")
    async def nitro_(self, ctx):
        """Generates a Nitro"""
        embed = discord.Embed(description=f"**{ctx.author.mention} generated a nitro link!**", color=discord.Color.nitro_pink())
        embed.set_image(url="https://media.discordapp.net/attachments/886639021772648469/903535585992523796/unknown.png")
        message = await ctx.send(embed=embed)
        await message.edit(embed=embed, view=NitroView(message, ctx))


    @slash_command(description="Play a TicTacToe Game with Someone Online!")
    async def tictactoe(self, ctx: discord.ApplicationContext, user: Option(discord.Member, "The user you want to play tic-tac-toe with", default=None, required=True)):
        if user is None:
            return await ctx.respond(embed=discord.Embed(description="**<:error:897382665781669908? You can't play tic-tac-toe alone!**", color=discord.Color.red()), ephemeral=True)

        if user.bot:
            return await ctx.respond(embed=discord.Embed(description="**<:error:897382665781669908> You can't play with a bot!**", color=discord.Color.red()), ephemeral=True)

        players = {
            str(ctx.author.id): str(user.id),
            str(user.id): str(ctx.author.id)
        }

        player1 = random.choice(list(players.keys()))
        player2 = players[player1]

        await ctx.interaction.response.send_message(f"{ctx.guild.get_member(int(player1)).mention}\'s turn (X)")
        
        msg = await ctx.interaction.original_message()

        await msg.edit(view=TicTacToe(
            player1=ctx.guild.get_member(int(player1)),
            player2=ctx.guild.get_member(int(player2)),
            message=msg
        ))

    @commands.command(name="tictactoe", aliases=['ttt'])
    async def tictactoe_(self, ctx: commands.Context, user: discord.Member):
        """Play a tic-tac-toe Game with someone online"""
        if user is None:
            return await ctx.send(embed=discord.Embed(description="**<:error:897382665781669908? You can't play tic-tac-toe alone!**", color=discord.Color.red()))

        if user.bot:
            return await ctx.send(embed=discord.Embed(description="**<:error:897382665781669908> You can't play with a bot!**", color=discord.Color.red()))

        players = {
            str(ctx.author.id): str(user.id),
            str(user.id): str(ctx.author.id)
        }

        player1 = random.choice(list(players.keys()))
        player2 = players[player1]

        msg = await ctx.send(f"{ctx.guild.get_member(int(player1)).mention}\'s turn (X)")
        
        await msg.edit(view=TicTacToe(
            player1=ctx.guild.get_member(int(player1)),
            player2=ctx.guild.get_member(int(player2)),
            message=msg
        ))


    @slash_command(description="Ask Me Something!", name="8ball")
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
        """Ask me something\nExample: `8ball Am I cool?`"""
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
        await ctx.send(embed=embed)

    
    @slash_command(description="Have a drink with yourself or someone")
    async def beer(self, ctx: commands.Context, user: Option(discord.Member, "The user you want to drink with")):
        user = user if user else ctx.author
        interaction: discord.Interaction = ctx.interaction
        if user.bot:
            embed = discord.Embed(description=f"**Hey {ctx.author.mention},\nbots don't have beer!\n-------------\nTry having it with a human!**", color=discord.Color.red())
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
        """Have a beer with yourself or someone else\nExample: `beer` for having a drink and `beer [user]` to have a drink with someone"""
        user = user if user else ctx.author
        if user.bot:
            embed = discord.Embed(description=f"**Hey {ctx.author.mention},\nbots don't have beer!\n--------------------------\nTry having it with a human!**", color=discord.Color.red())
            await ctx.send(embed=embed)
            return
        if user == ctx.author:
            embed = discord.Embed(description=f"**{ctx.author.mention} is having a great time drinking lonely! :beer:**", color=discord.Color.green())
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description=f"**{ctx.author.mention} has invited {user.mention} for having a drink together :beers:!\n------------------------------------\nWould you like to join {user.mention}?**", color=discord.Color.orange())   
            message = await ctx.send(content=f"{user.mention}", embed=embed)
            await message.edit(embed=embed, view=BeerView(user, ctx, message))


    @slash_command(description="Have a beer party with some friends 🍻!")
    async def beerparty(self, ctx: commands.Context):
        interaction: discord.Interaction = ctx.interaction
        embed = discord.Embed(title="Beer Party 🍻", description=f"{ctx.author.mention} had invited everyone to join up this beer party :beers:!", color=discord.Color.green())
        await interaction.response.send_message(embed=embed)
        message = await interaction.original_message()
        await message.edit(embed=embed, view=BeerPartyView(message, ctx))

    @commands.command(name="beerparty")
    async def beerparty_(self, ctx: commands.Context):
        """Have a beerparty in the server. Invite your friends!"""
        embed = discord.Embed(title="Beer Party 🍻", description=f"{ctx.author.mention} had invited everyone to join up this beer party :beers:!", color=discord.Color.green())
        message = await ctx.send(embed=embed)
        await message.edit(embed=embed, view=BeerPartyView(message, ctx))
    
    @commands.command(name="coinflip")
    async def coinflip_(self, ctx: commands.Context):
        """Flip a coin!"""
        coinsides = ['Heads', 'Tails']
        message = await ctx.send(embed=discord.Embed(description=f"**Flipping a coin! <a:loading:911568431315292211>**", color=discord.Color.orange()))
        await asyncio.sleep(1)
        await message.edit(embed=discord.Embed(description=f"**`{random.choice(coinsides)}` it is!**", color=discord.Color.green()))

    @commands.command(name="akinator", aliases=['aki', 'ak', 'akinat'])
    async def akinator_(self, ctx: commands.Context):
        """Play a game of akinator\nHow to play: Think of a character it can either be a fictional or non-fictional character.\nThe bot will ask questions, just give them the right answer!"""
        await ctx.send(embed=discord.Embed(description="**Yukinator is here to guess!\n--------------------------------\nOptions: y: `yes\n`no: `n`\nidk: `Don't know`\np: `probably`\npn: `probably not`\nb: `previous question`\nq: `quit the game`**", color=discord.Color.green()).set_image(url="https://static.wikia.nocookie.net/video-game-character-database/images/9/9f/Akinator.png/revision/latest?cb=20200817020737"))
        def check(msg):
            return (
                msg.author == ctx.author
                and msg.channel == ctx.channel
                and msg.content.lower() in ["y", "n", "idk", "p", "pn", "b", "q"]
            )

        try:
            aki = ak.Akinator()
            q = aki.start_game()
            while aki.progression <= 80:
                await ctx.send(embed=discord.Embed(description=f"**{q}\n\n[`y` | `n` | `idk` | `p` | `pn` | `b` | `q`]**", color=discord.Color.embed_background(theme="dark")))
                try:
                    msg = await self.bot.wait_for("message", check=check, timeout=60)
                    if msg.content.lower() == "q":
                        await ctx.send(embed=discord.Embed(description="**You have quit the game!**", color=discord.Color.red()))
                        break
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
                except asyncio.TimeoutError:
                    return await ctx.send(embed=discord.Embed(description=f"**<:error:897382665781669908> The game timed-out.. try plsying a new one**"))

                except Exception as e:
                    await ctx.send(embed=discord.Embed(description=f"**<:error:897382665781669908> An error occured\n`{str(e).capitalize()}`**"))
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


    @commands.command(name="hug")
    @commands.cooldown(1, 10, BucketType.user)
    async def hug_(self, ctx: commands.Context, user: discord.Member):
        """Hug someone"""
        if user.bot:
            return await ctx.send(embed=discord.Embed(description="**<:error:897382665781669908> You can't hug a bot.**", color=discord.Color.red()))
        if user == ctx.author:
            return await ctx.send(embed=discord.Embed(description="**<:error:897382665781669908> You can't hug yourself!\n--------------------------\nTry hugging someone else.**", color=discord.Color.red()))

        if user.bot:
            return await ctx.send(embed=discord.Embed(description="**<:error:897382665781669908> You can't hug a bot!\n--------------------------\nTry hugging an human.**", color=discord.Color.red()))

        url = "https://some-random-api.ml/animu/hug"
        r = requests.get(url)
        data = r.json()
        embed = discord.Embed(description=f"**<:hug:922213806027968573> {ctx.author.mention} hugged {user.mention}**", color=discord.Color.embed_background(theme="dark"))
        embed.set_image(url=data['link'])
        await ctx.send(embed=embed)

    @commands.command(name="pat", aliases=['pats', 'headpat', 'headpats'])
    @commands.cooldown(1, 10, BucketType.user)
    async def pat_(self, ctx: commands.Context, user: discord.Member):
        """Pat someone"""
        if user.bot:
            return await ctx.send(embed=discord.Embed(description="**<:error:897382665781669908> You can't pat a bot.**"))
        if user == ctx.author:
            return await ctx.send(embed=discord.Embed(description="**<:error:897382665781669908> You can't pat yourself!\n--------------------------\nTry patting someone else.**", color=discord.Color.red()))

        url = "https://some-random-api.ml/animu/pat"
        r = requests.get(url)
        data = r.json()
        embed = discord.Embed(description=f"**{ctx.author.mention} patted {user.mention}**", color=discord.Color.embed_background(theme="dark"))
        embed.set_image(url=data['link'])
        await ctx.send(embed=embed)

    @commands.command(name="gif")
    @commands.cooldown(1, 10, BucketType.user)
    async def gif_(self, ctx: commands.Context, *, query: str):
        """Search Some GIF!"""
        lmt = 50
        
        try:
            r = self.bot.giphy.gifs_search_get(GIPHY_API_KEY, query, limit=lmt)
            gif = random.choice(list(r.data))
            url = giphyUrl(gif.id)
        except ApiException:
            return await ctx.send(embed=discord.Embed(description="**<:error:897382665781669908> Couldn't generate a gif. Please try again later.**", color=discord.Color.red()))
        
        await ctx.send(embed=discord.Embed(description=f"**Random result for {query}**", color=discord.Color.embed_background(theme="dark")).set_image(url=url).set_thumbnail(url=POWERED_BY_GIPHY))

    @commands.command(name="slap")
    @commands.cooldown(1, 10, BucketType.user)
    async def slap_(self, ctx: commands.Context, user: discord.Member):
        """Slap someone!"""
        if user.bot:
            return await ctx.send(embed=discord.Embed(description="**<:error:897382665781669908> You can't slap a bot.**", color=discord.Color.red()))
        if user == ctx.author:
            return await ctx.send(embed=discord.Embed(description="**<:error:897382665781669908> You can't slap yourself!\n--------------------------\nTry slapping someone else.**", color=discord.Color.red()))

        query = "anime slap"
        lmt = 50
    
        try:
            r = self.bot.giphy.gifs_search_get(GIPHY_API_KEY, query, limit=lmt)
            gif = random.choice(list(r.data))
            url = giphyUrl(gif.id)
        except ApiException:
            return await ctx.send(embed=discord.Embed(description="**<:error:897382665781669908> Couldn't generate a gif. Please try again later.**", color=discord.Color.red()))
        
        embed = discord.Embed(description=f"**{ctx.author.mention} slapped {user.mention}**", color=discord.Color.embed_background(theme="dark")).set_image(url=url)
        await ctx.send(embed=embed)

    @commands.command(name="kiss")
    @commands.cooldown(1, 10, BucketType.user)
    async def kiss(self, ctx: commands.Context, user: discord.Member):
        """Kiss someone!"""
        if user.bot:
            return await ctx.send(embed=discord.Embed(description="**<:error:897382665781669908> You can't kiss a bot.**", color=discord.Color.red()))
        if user == ctx.author:
            return await ctx.send(embed=discord.Embed(description="**<:error:897382665781669908> You can't kiss yourself!\n--------------------------\nTry kissing someone else.**", color=discord.Color.red()))

        query = "anime kiss"
        lmt = 50

        try:
            r = self.bot.giphy.gifs_search_get(GIPHY_API_KEY, query, limit=lmt)
            gif = random.choice(list(r.data))
            url = giphyUrl(gif.id)
        except ApiException:
            return await ctx.send(embed=discord.Embed(description="**<:error:897382665781669908> Couldn't generate a gif. Please try again later.**", color=discord.Color.red()))
        
        embed = discord.Embed(description=f"**{ctx.author.mention} kissed {user.mention}**", color=discord.Color.embed_background(theme="dark")).set_image(url=url)
        await ctx.send(embed=embed)

    @commands.command(name="marry")
    @commands.cooldown(1, 10, BucketType.user)
    async def marry(self, ctx: commands.Context, user: discord.Member):
        """Marry someone!"""
        if user.bot:
            return await ctx.send(embed=discord.Embed(description="**<:error:897382665781669908> You can't marry a bot.**", color=discord.Color.red()))
        if user == ctx.author:
            return await ctx.send(embed=discord.Embed(description="**<:error:897382665781669908> You can't marry yourself!\n--------------------------\nTry marrying someone else.**", color=discord.Color.red()))

        query = "anime marry"
        lmt = 50

        try:
            r = self.bot.giphy.gifs_search_get(GIPHY_API_KEY, query, limit=lmt)
            gif = random.choice(list(r.data))
            url = giphyUrl(gif.id)
        except ApiException:
            return await ctx.send(embed=discord.Embed(description="**<:error:897382665781669908> Couldn't generate a gif. Please try again later.**", color=discord.Color.red()))
        
        embed = discord.Embed(description=f"**{ctx.author.mention} married {user.mention}**", color=discord.Color.embed_background(theme="dark")).set_image(url=url)
        await ctx.send(embed=embed)

    @commands.command(aliases=['gayr8'])
    async def gayrate(self, ctx, user: discord.Member=None):
        """View your's or someone's gayrate"""
        user = user if user else ctx.author
        if user.bot:
            embed = discord.Embed(description="**<:error:897382665781669908> How lame of you! | This machine is for humans!\nNot for bots, You fool.**", color=discord.Color.red())
            return await ctx.send(embed=embed)
        gayrate = random.randint(1, 100)
        
        if gayrate >= 90:
            embed = discord.Embed(title="Yuki's Gayr8 Machine!", description=f"**The MACHINE Broke :slot_machine:!\n\n{user.mention}**'s gayr8: **{gayrate}**%", color=discord.Color.embed_background(theme="dark"))
            embed.set_image(url="https://media.giphy.com/media/j2es27Xohj5EMK6G8c/giphy.gif")
            return await ctx.send(embed=embed)

        else:
            embed = discord.Embed(title="Yuki's Gayr8 Machine!", description=f"**{user.mention}**'s gayr8: **{gayrate}**%", color=discord.Color.dark_purple())
            return await ctx.send(embed=embed)

    @commands.command(aliases=['02'])
    async def zerotwo(self, ctx: commands.Context):
        """Gives a random zerotwo gif <:zerolove:920425612613660753>!"""
        query = "zerotwo anime"
        lmt = 50

        try:
            r = self.bot.giphy.gifs_search_get(GIPHY_API_KEY, query, limit=lmt)
            gif = random.choice(list(r.data))
            url = giphyUrl(gif.id)        
        except ApiException:
            return await ctx.send(embed=discord.Embed(description="**<:error:897382665781669908> Couldn't generate a gif. Please try again later.**"))

        embed = discord.Embed(description="**<:zerolove:920425612613660753> Zerotwo is just so cute!**", color=discord.Color.embed_background(theme="dark")).set_image(url=url)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(FunCog(bot))