import discord
from discord.ext import commands
from typing import List
from urllib.parse import quote_plus
import asyncio

def joins(list: list):
    return "\n".join([f"<@{i}>" for i in list])

async def set_perms(channel: discord.TextChannel):
    for member in channel.guild.members:
        if member.guild_permissions.manage_channels:
            await channel.set_permissions(member, view_channel=True)
            await channel.set_permissions(member, send_messages=True)
            await channel.set_permissions(member, read_message_history=True)
            await channel.set_permissions(member, manage_channel=True)


class NitroView(discord.ui.View):
    def __init__(self, msg: discord.Message, ctx: commands.Context):
        super().__init__(timeout=30)
        self.msg = msg
        self.ctx = ctx

    @discord.ui.button(label="Claim", style=discord.ButtonStyle.success, emoji="<:nitro:914110236707680286>")
    async def button_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user != self.ctx.author:
            embed = discord.Embed(description=f"<:error:897382665781669908> You can't do that {interaction.user.mention}!", color=discord.Color.red())
            return await self.ctx.send(embed=embed, delete_after=5)
        button.label = "Claimed"
        button.style = discord.ButtonStyle.danger
        button.emoji = "<:nitro:914110236707680286>"
        button.disabled = True
        await interaction.response.send_message(content="https://imgur.com/NQinKJB", ephemeral=True)
        embed = discord.Embed(description=f"***<:nitro:914110236707680286> {self.ctx.author.mention} claimed the nitro!***", color=discord.Color.nitro_pink())
        embed.set_image(url="https://media.discordapp.net/attachments/886639021772648469/903535585992523796/unknown.png")
        await self.msg.edit(embed=embed, view=self)

    async def on_timeout(self):
        for child in self.children:
            if child.disabled:
                return
        for child in self.children:
            child.disabled = True
        embed = discord.Embed(description=f"**<:error:897382665781669908> Looks like either {self.ctx.author.mention} didn't wanna have it or {self.ctx.author.mention} went AFK**", color=discord.Color.red())
        embed.set_image(url="https://media.discordapp.net/attachments/886639021772648469/903535585992523796/unknown.png")
        await self.msg.edit(embed=embed, view=self)



class TicTacToeButton(discord.ui.Button["TicTacToe"]):
    def __init__(self, x: int, y: int):
        super().__init__(style=discord.ButtonStyle.secondary, label="\u200b", row=y)
        self.x = x
        self.y = y

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: TicTacToe = self.view
        state = view.board[self.y][self.x]
        if state in (view.X, view.O):
            return

        if view.current_player == view.X:
            self.style = discord.ButtonStyle.danger
            self.label = "X"
            self.disabled = True
            view.board[self.y][self.x] = view.X
            view.current_player = view.O
            content = "It is now O's turn"
        else:
            self.style = discord.ButtonStyle.success
            self.label = "O"
            self.disabled = True
            view.board[self.y][self.x] = view.O
            view.current_player = view.X
            content = "It is now X's turn"

        winner = view.check_board_winner()
        if winner is not None:
            if winner == view.X:
                content = "X won!"
            elif winner == view.O:
                content = "O won!"
            else:
                content = "It's a tie!"

            for child in view.children:
                child.disabled = True

            view.stop()

        await interaction.response.edit_message(content=content, view=view)



class TicTacToe(discord.ui.View):
    children: List[TicTacToeButton]
    X = -1
    O = 1
    Tie = 2

    def __init__(self):
        super().__init__()
        self.current_player = self.X
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

        for x in range(3):
            for y in range(3):
                self.add_item(TicTacToeButton(x, y))

    def check_board_winner(self):
        for across in self.board:
            value = sum(across)
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        for line in range(3):
            value = self.board[0][line] + self.board[1][line] + self.board[2][line]
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        diag = self.board[0][2] + self.board[1][1] + self.board[2][0]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        diag = self.board[0][0] + self.board[1][1] + self.board[2][2]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        if all(i != 0 for row in self.board for i in row):
            return self.Tie

        return None

    
class Google(discord.ui.View):
    def __init__(self, query: str):
        super().__init__()
        query = quote_plus(query)
        url = f"https://www.google.com/search?q={query}"

        self.add_item(discord.ui.Button(label="Click Here", url=url))


class NukeView(discord.ui.View):
    def __init__(self, ctx: commands.Context, channel: discord.TextChannel, msg: discord.Message):
        super().__init__(timeout=15)
        self.ctx = ctx
        self.channel = channel
        self.msg = msg

        
    @discord.ui.button(label="Yes", style=discord.ButtonStyle.success, custom_id="Yes")
    async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user != self.ctx.author:
            em = discord.Embed(description=f"<:error:897382665781669908> You can't do that {interaction.user.mention}!", color=discord.Color.red())
            return await self.ctx.send(embed=em)
        for child in self.children:
            child.disabled = True
        channel = self.channel
        channel_position = channel.position
                
        new_channel = await channel.clone()
        await channel.delete()
        await new_channel.edit(position=channel_position, sync_permissions=True)
        await new_channel.send(f"**Successfully nuked {new_channel.mention}**")
        embed = discord.Embed(description=f"**<:tick:897382645321850920> Successfuly Nuked {new_channel.mention}!**", color=discord.Color.green())
        await interaction.response.edit_message(embed=embed, view=self)
        await new_channel.send(f"https://media.giphy.com/media/hvGKQL8lasDvIlWRBC/giphy.gif")


    @discord.ui.button(label="No", style=discord.ButtonStyle.red, custom_id="No")
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user != self.ctx.author:
            em = discord.Embed(description=f"<:error:897382665781669908> You can't do that {interaction.user.mention}!", color=discord.Color.red())
            return await self.ctx.send(embed=em)
        for child in self.children:
            child.disabled = True
        embed = discord.Embed(description=f"**<:tick:897382645321850920> Canceled Nuking {self.channel.mention}**", color=discord.Color.green())
        await interaction.response.edit_message(embed=embed, view=self)

    async def on_timeout(self):
        for child in self.children:
            if child.disabled:
                return
        for child in self.children:
            child.disabled = True
        embed = discord.Embed(description=f"**<:error:897382665781669908> You didn't respond within time! So, Canceled Nuking {self.channel.mention}**", color=discord.Color.red())
        await self.msg.edit(embed=embed, view=self)


class InviteView(discord.ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(discord.ui.Button(label="Invite Me!", url="https://discord.com/api/oauth2/authorize?client_id=919314151535419463&permissions=8&scope=bot%20applications.commands"))


class BeerView(discord.ui.View):
    def __init__(self, user: discord.Member, ctx: commands.Context, msg: discord.Message):
        super().__init__(timeout=30)
        self.user = user
        self.ctx = ctx
        self.msg = msg

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.success, emoji="🍻")
    async def confirm_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user != self.user:
            if interaction.user == self.ctx.author:
                embed = discord.Embed(description=f"**<:error:897382665781669908> {self.ctx.author.mention} You can't do that!\n---------------------------------------\nYou are the one who invited {self.user.mention}.**", color=discord.Color.red())
            embed = discord.Embed(description=f"**<:error:897382665781669908> {self.ctx.author.mention} hasn't invited you to have a drink {interaction.user.mention}!**", color=discord.Color.red())
            return await interaction.channel.send(embed=embed, delete_after=5)
        for child in self.children:
            child.disabled = True
        embed = discord.Embed(description=f"**{self.ctx.author.mention} and {self.user.mention} are having great time drinking together :beers:!**", color=discord.Color.green())
        await interaction.response.edit_message(content=None, embed=embed, view=self)

    @discord.ui.button(label="No", style=discord.ButtonStyle.danger)
    async def cancel_callback(self, button: discord.Button, interaction: discord.Interaction):
        if interaction.user != self.user:
            embed = discord.Embed(description=f"<:error:897382665781669908> {self.ctx.author.mention} hasn't invited you to have a drink {interaction.user.mention}!", color=discord.Color.red())
            return await interaction.channel.send(embed=embed, delete_after=5)
        for child in self.children:
            child.disabled = True
        embed = discord.Embed(description=f"**<:error:897382665781669908> Oops!\nLooks like either {self.user.mention} doesn't wanna have a drink :beers: with {self.ctx.author.mention} or {self.user.mention} is busy!**", color=discord.Color.red())
        await interaction.response.edit_message(content=None, embed=embed, view=self)

    async def on_timeout(self):
        for child in self.children:
            if child.disabled:
                return
        for child in self.children:
            child.disabled = True
        embed = discord.Embed(description=f"**<:error:897382665781669908> Looks like either {self.user.mention} didn't wanna drink :beers: with {self.ctx.author} or {self.user.mention} went AFK**", color=discord.Color.red())
        await self.msg.edit(content=None, embed=embed, view=self)



class BeerPartyView(discord.ui.View):
    def __init__(self, msg: discord.Message, ctx: commands.Context):
        super().__init__(timeout=5)
        self.msg = msg
        self.clicked = [ctx.author.id]
        self.ctx = ctx

    @discord.ui.button(label="Join the Party", style=discord.ButtonStyle.green, emoji="🍻")
    async def callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user == self.ctx.author:
            embed = discord.Embed(description="**<:error:897382665781669908> You are already chilling in the party cuz the party is your's lol :beers:**", color=discord.Color.red())
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        if interaction.user.id in self.clicked:
            embed = discord.Embed(description="**<:error:897382665781669908> You are already chilling in the party :beers:**", color=discord.Color.red())
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        self.clicked.append(interaction.user.id)
        embed = discord.Embed(description=f"**{interaction.user.mention} has just joined the party 🍻!**", color=discord.Color.green())
        await interaction.response.send_message(embed=embed)


    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        embed = discord.Embed(title="The Party Ended", description=f"**The party :beers: was joined by:\n\n{joins(self.clicked)}**", color=discord.Color.green())
        await self.msg.channel.send(embed=embed)
        embed2 = discord.Embed(title="The Beer Party Ended, if you didn't join wait for the next one :beers:!", color=discord.Color.orange())
        await self.msg.edit(embed=embed2, view=self)


class TicketPanelView(discord.ui.View):
    def __init__(self, bot: commands.Bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label="Create Ticket", style=discord.ButtonStyle.grey, emoji="📩", custom_id="panel")
    async def callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        embed = discord.Embed(description="**<a:loading:911568431315292211> Creating ticket**", color=0x2F3136)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        message = await interaction.original_message()
        self.bot.dbcursor.execute(f'SELECT count FROM ticket WHERE guild_id=?', (interaction.guild_id,))
        data = self.bot.dbcursor.fetchone()
        if not data:
            self.bot.dbcursor.execute(f'INSERT INTO ticket(guild_id, count) VALUES(?,?)', (interaction.guild_id, 1))
        if data:
            self.bot.dbcursor.execute(f'UPDATE ticket SET count = count + 1 WHERE guild_id=?', (interaction.guild_id,))
           
        self.bot.dbcursor.execute(f'SELECT category FROM ticket WHERE guild_id=?', (interaction.guild_id,))
        categoryCheck = self.bot.dbcursor.fetchone()

        if not categoryCheck:
            self.bot.dbcursor.execute(f'SELECT * FROM ticket WHERE guild_id=?', (interaction.guild_id,))
            ticket_num = self.bot.dbcursor.fetchone()
            ticket_channel = await interaction.guild.create_text_channel(name=f"ticket-{ticket_num[1]}")
            await ticket_channel.set_permissions(interaction.guild.default_role, view_channel=False)
            embed = discord.Embed(description=f"**<:tick:897382645321850920> Successfully created a ticket at {ticket_channel.mention}**", color=discord.Color.green())
            await message.edit(embed=embed)
            embed1 = discord.Embed(description=f"**Support will be with you shortly.\nTo close this ticket react with 🔒**", color=discord.Color.green()).set_footer(text=f"{self.bot.user.name} - Ticket System", icon_url=self.bot.user.avatar.url)
            await ticket_channel.send(content=interaction.user.mention, embed=embed1, view=TicketCloseTop(interaction.user, self.bot))
            await set_perms(ticket_channel)
            self.bot.dbcursor.execute(f'INSERT INTO tickets (guild_id, channel_id, opener, switch) VALUES(?,?,?,?)', (interaction.guild_id, ticket_channel.id, interaction.user.id, "open"))
            self.bot.db.commit()

        if categoryCheck:
            self.bot.dbcursor.execute(f'SELECT * FROM ticket WHERE guild_id=?', (interaction.guild_id,))
            data = self.bot.dbcursor.fetchone()
            category = discord.utils.get(interaction.guild.categories, id=data[2])
            ticketChannel = await interaction.guild.create_text_channel(name=f"ticket-{data[1]}", category=category)
            await ticketChannel.edit(sync_permissions=True)
            embed = discord.Embed(description=f"**<:tick:897382645321850920> Successfully created a ticket at {ticketChannel.mention}**", color=discord.Color.green())
            await message.edit(embed=embed)
            await ticketChannel.set_permissions(interaction.user, view_channel=True)
            await ticketChannel.set_permissions(interaction.user, send_messages=True)
            await ticketChannel.set_permissions(interaction.user, read_message_history=True)
            embed1 = discord.Embed(description=f"**Support will be with you shortly.\nTo close this ticket react with 🔒**", color=discord.Color.green()).set_footer(text=f"{self.bot.user.name} - Ticket System", icon_url=self.bot.user.avatar.url)
            await ticketChannel.send(content=interaction.user.mention, embed=embed1, view=TicketCloseTop(interaction.user, self.bot))
            self.bot.dbcursor.execute(f'INSERT INTO tickets (guild_id, channel_id, opener, switch) VALUES(?,?,?,?)', (interaction.guild_id, ticketChannel.id, interaction.user.id, "open"))
            self.bot.db.commit()


class TicketCloseTop(discord.ui.View):
    def __init__(self, ticketOpener: discord.Member, bot: commands.Bot):
        super().__init__(timeout=None)
        self.member = ticketOpener
        self.bot = bot

    @discord.ui.button(label="Close", style=discord.ButtonStyle.gray, emoji="🔒", custom_id="top:close")
    async def close_callback(self, button: discord.Button, interaction: discord.Interaction):
        self.bot.dbcursor.execute(f'SELECT * FROM tickets WHERE guild_id=? AND channel_id=?', (interaction.guild_id, interaction.channel_id))
        data = self.bot.dbcursor.fetchone()
        if data[3] == "closed":
            return await interaction.response.send_message(embed=discord.Embed(description=f"**<:error:897382665781669908> The ticket is already closed!**", color=discord.Color.red()), ephemeral=True)
        await interaction.response.send_message(embed=discord.Embed(description="**Are you sure you want to close the ticket?**", color=discord.Color.orange()))
        message = await interaction.original_message()
        await message.edit(view=TicketCloseTop2(interaction.user, self.member, message, self.bot))

class TicketCloseTop2(discord.ui.View):
    def __init__(self, buttonUser: discord.Member, ticketOpener: discord.Member, msg: discord.Message, bot: commands.Bot):
        super().__init__(timeout=15)
        self.user = buttonUser
        self.member = ticketOpener
        self.msg = msg
        self.bot = bot

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.danger)
    async def yes_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user != self.user:
            return await interaction.channel.send(embed=discord.Embed(description=f"**<:error:897382665781669908> You can't do that {interaction.user.mention}**", color=discord.Color.red()))
        for child in self.children:
            child.disabled = True
        if self.member.guild_permissions.administrator or self.member.guild_permissions.manage_channels:
            pass
        else:
            perms = interaction.channel.overwrites_for(self.member)
            perms.view_channel = False
            perms.send_messages = False
            perms.read_message_history = False
            await interaction.channel.set_permissions(self.member, overwrite=perms)
        self.bot.dbcursor.execute(f'UPDATE tickets SET switch = "closed" WHERE guild_id=? AND channel_id=?', (interaction.guild_id, interaction.channel_id))
        self.bot.db.commit()
        await self.msg.delete()
        await interaction.channel.send(embed=discord.Embed(description=f"**Ticket closed by {interaction.user.mention}**", color=discord.Color.orange()))

    @discord.ui.button(label="No", style=discord.ButtonStyle.gray)
    async def no_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user != self.user:
            return await interaction.channel.send(embed=discord.Embed(description=f"**<:error:897382665781669908> You can't do that {interaction.user.mention}**", color=discord.Color.red()))
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(embed=discord.Embed(description=f"**<:tick:897382645321850920> Canceled closing {interaction.channel.mention}**", color=discord.Color.green()), view=self)

    async def on_timeout(self):
        try:
            for child in self.children:
                if child.disabled:
                    return
            for child in self.children:
                child.disabled = True
            embed = discord.Embed(description=f"**<:error:897382665781669908> Oops you didn't respond within time! So, Canceled closing the ticket!**", color=discord.Color.red())
            await self.msg.edit(embed=embed, view=self)
        except discord.NotFound:
            pass
    
class TicketControlsView(discord.ui.View):
    def __init__(self, ticketOpener: discord.Member, message: discord.Message, bot: commands.Bot):
        super().__init__(timeout=None)
        self.member = ticketOpener
        self.msg = message
        self.bot = bot

    @discord.ui.button(label="Open", style=discord.ButtonStyle.gray, emoji="🔓", custom_id="controls:open")
    async def open_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        if not interaction.user.guild_permissions.manage_channels:
            return await interaction.response.send_message(embed=discord.Embed(description=f"<:error:897382665781669908> You can't do that {interaction.user.mention}!", color=discord.Color.red()))
        perms = interaction.channel.overwrites_for(self.member)
        perms.view_channel = True
        perms.send_messages = True
        perms.read_message_history = True
        await interaction.channel.set_permissions(self.member, overwrite=perms)
        self.bot.dbcursor.execute(f'UPDATE tickets SET switch = "open" WHERE guild_id=? AND channel_id=?', (interaction.guild_id, interaction.channel_id))
        self.bot.db.commit()
        await self.msg.delete()
        await interaction.channel.send(embed=discord.Embed(description=f"**Ticket opened by {interaction.user.mention}**", color=discord.Color.green()))

    @discord.ui.button(label="Delete", style=discord.ButtonStyle.gray, emoji="⛔", custom_id="controls:close")
    async def delete_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        if not interaction.user.guild_permissions.manage_channels:
            return await interaction.response.send_message(embed=discord.Embed(description=f"<:error:897382665781669908> You can't do that!", color=discord.Color.red()), ephemeral=True)
        try:
            await self.msg.delete()
            await interaction.channel.send(embed=discord.Embed(description=f"**<:tick:897382645321850920> The ticket will be deleted soon**", color=discord.Color.orange()))
            await asyncio.sleep(3)
            await interaction.channel.delete()
            self.bot.dbcursor.execute('DELETE FROM tickets WHERE guild_id=? AND channel_id=?', (interaction.guild_id, interaction.channel_id))
            self.bot.db.commit()
        except discord.NotFound:
            print("The ticket was deleted")


class TicketResetView(discord.ui.View):
    def __init__(self, ctx: commands.Context, message: discord.Message, bot: commands.Bot):
        super().__init__(timeout=15)
        self.ctx = ctx
        self.msg = message
        self.bot = bot

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.green, emoji="<:tick:897382645321850920>")
    async def confirm_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user != self.ctx.author:
            embed = discord.Embed(description=f"<:error:897382665781669908> You can't do that {interaction.user.mention}!", color=discord.Color.red())
            return await self.ctx.send(embed=embed, delete_after=5)
        for child in self.children:
            child.disabled = True
        self.bot.dbcursor.execute(f'UPDATE ticket SET count = 0 WHERE guild_id=?', (interaction.guild_id,))
        self.bot.db.commit()
        embed = discord.Embed(description="**<:tick:897382645321850920> Succesfully resetted the ticket count!**", color=discord.Color.green())
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="No", style=discord.ButtonStyle.red, emoji="<:error:897382665781669908>")
    async def decline_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user != self.ctx.author:
            embed = discord.Embed(description=f"<:error:897382665781669908> You can't do that {interaction.user.mention}!", color=discord.Color.red())
            return await self.ctx.send(embed=embed, delete_after=5)
        for child in self.children:
            child.disabled = True
        embed = discord.Embed(description="**<:tick:897382645321850920> Canceled resetting ticket count!**", color=discord.Color.green())
        await interaction.response.edit_message(embed=embed, view=self)

    async def on_timeout(self):
        try:
            for child in self.children:
                if child.disabled:
                    return
            for child in self.children:
                child.disabled = True
            embed = discord.Embed(description=f"**<:error:897382665781669908> Oops you didn't respond within time! So, Canceled resetting ticket count!**", color=discord.Color.red())
            await self.msg.edit(embed=embed, view=self)
        except discord.NotFound:
            print("Ticket count reset complete")