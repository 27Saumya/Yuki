import discord
from discord.ext import commands
from utils.buttons import TicketPanelView, TicketResetView, TicketCloseTop2

async def cleanup(guild: discord.Guild):
    for channel in guild.channels:
        if channel.name.lower().startswith('ticket'):
            await channel.delete()


class TicketCog(commands.Cog, name="Ticket"):
    """
Ticket related commands.

Use `panel` or `ticket` | `ticket setup` for more information!
    """
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.group(name="panel")
    async def panel_(self, ctx: commands.Context):
        """Ticket Panel related commands"""
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title="Panel", description="**--> `panel create`: Creates a panel\nUsage: `panel create <channel> [name]`\nExample: `panel create #ticket Get a ticket`\n\n--> `panel delete`: Deletes a panel\nUsage: `panel delete <channel> [panel_id]`\nExample: `panel delete #ticket 987654321123456789`\n\n--> `panel edit`: Edits the name of a panel\nUsage: `panel edit <channel> [panel_id] (name)`\nExample: `panel edit #ticket 987654321123456789 I just changed the name of the panel!`**", color=discord.Color.green()).set_footer(text="Note: All Ticket Realted Commands aren't avaliable in slash commands", icon_url=self.bot.user.avatar.url)
            await ctx.send(embed=embed)
    
    @commands.group(name="ticket")
    async def ticket_(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            """Ticket related commands"""
            embed = discord.Embed(title="Ticket", description="**--> `ticket role add` Adds a role to ticket channel. By doing this the role you add can view tickets! By default it is available for only admins\nUsage: `ticket role add <role>`\nExample: `ticket role add @MODS`\n\n--> `ticket role remove` Just the vice versa of the one stated above. Removes a role from viewing ticket\nUsage: `ticket role remove <role>`\nExample: `ticket role remove @MODS`\n\n--> `ticket reset` Resets the ticket count!\nUsage: `ticket reset`\n\n--> `ticket clean` Delete all tickets in the server\nUsage: `ticket clean`\n\n--> `ticket category` Get tickets inside a category. If you want to keep ticket view permissions, make sure to change the category permissions.\nUsage: `ticket category <category_id>`\nExample: `ticket category 98765432123456789`\n\n--> `ticket close` Closes the ticket. Use the command inside a ticket only\nUsage: `ticket close`\n\n--> `ticket add` Adds a user in the ticket. Use the command inside a ticket only\nUsage: `ticket add <user>`\nExample: `ticket add @27Saumya#0007`\n\n--> `ticket remove` Removes a user from the ticket. Use the command inside a ticket only\nUsage: `ticket remove <user>`\nExample: `ticket remove @27Saumya#0007`**", color=discord.Color.green()).set_footer(text="Note: All Ticket Realted Commands aren't avaliable in slash commands", icon_url=self.bot.user.avatar.url)
            await ctx.send(embed=embed)

    @panel_.command(name="create", aliases=['c', 'make', 'add'])
    async def create_(self, ctx: commands.Context, channel: discord.TextChannel, *, name = None):
        """Creates a panel in a channel through which users can interact and open tickets"""
        if not channel:
            embed = discord.Embed(
                description="**<:error:897382665781669908> Please enter a channel to make the panel in!**",
                color=discord.Color.red()
            )
            return await ctx.send(embed=embed)

        if not name:
            embed = discord.Embed(
                description="**<:error:897382665781669908> Please enter a name!**",
                color=discord.Color.red()
            )
            return await ctx.send(embed=embed)

        if not ctx.author.guild_permissions.manage_channels:
            embed = discord.Embed(
                description="**<:error:897382665781669908> You can't do that!**",
                color=discord.Color.red()
            )
            return await ctx.send(embed=embed)

        if channel == ctx.channel:
            panel = discord.Embed(
                title=name,
                description="To create a ticket react with 📩",
                color=discord.Color.green(),
            )
            panel.set_footer(text=f"{self.bot.user.name} - Ticket Panel", icon_url=self.bot.user.avatar.url)

            message = await channel.send(embed=panel, view=TicketPanelView(self.bot))
            try:
                await ctx.author.send(embed=discord.Embed(description=f"**Panel id** of the panel you just created in <#{channel.id}>: `{message.id}`", color=discord.Color.green()))
            except discord.Forbidden:
                print("Couldn't DM that user!")
        if channel != ctx.channel:
            panel1 = discord.Embed(
                title=name,
                description="To create a ticket react with 📩",
                color=discord.Color.green(),
            )
            panel1.set_footer(text=f"{self.bot.user.name} - Ticket Panel", icon_url=self.bot.user.avatar.url)

            message = await channel.send(embed=panel1, view=TicketPanelView(self.bot))
            embed2 = discord.Embed(description=f"**<:tick:897382645321850920> Successfully posted the panel in {channel.mention}\n\nPanel ID: `{message.id}`**", color=discord.Color.green())
            await ctx.send(embed=embed2)


    @panel_.command(name="delete", aliases=['del'])
    @commands.has_permissions(manage_channels=True)
    async def delete_(self, ctx: commands.Context, channel: discord.TextChannel, panel_id: int):
        """Deletes a previously built panel in the server. Requires the `panel_id` which is provided at the time of the creation of the panel"""
        message = await channel.fetch_message(panel_id)
        try:
            await message.delete()
            embed = discord.Embed(description="**<:tick:897382645321850920> Successfully deleted the panel!**", color=discord.Color.green())
            await ctx.send(embed=embed)
        except discord.Forbidden:
            embed = discord.Embed(description="**<:error:897382665781669908> I couldn't do that!**", color=discord.Color.green())
            await ctx.send(embed=embed)
        except discord.NotFound:
            embed = discord.Embed(description=f"**<:error:897382665781669908> I couldn't find a panel with id `{panel_id}`! Please try again after checking the id!**")
            await ctx.send(embed=embed)

    @panel_.command(name="edit", aliases=['e'])
    async def edit_(self, ctx: commands.Context, channel: discord.TextChannel, panel_id: int, *, name: str):
        """Edits a previously built panel in the server. Requires the `panel_id` which is provided at the time of the creation of the panel"""
        message = await channel.fetch_message(panel_id)
        try:
            embed1 = discord.Embed(title=name, description="To create a ticket react with 📩", color=discord.Color.green())
            await message.edit(embed=embed1)
            embed = discord.Embed(description="**<:tick:897382645321850920> Successfully edited the panel!**", color=discord.Color.green())
            await ctx.send(embed=embed)
        except discord.Forbidden:
            embed = discord.Embed(description="**<:error:897382665781669908> I couldn't do that!**", color=discord.Color.green())
            await ctx.send(embed=embed)
        except discord.NotFound:
            embed = discord.Embed(description=f"**<:error:897382665781669908> I couldn't find a panel with id `{panel_id}`! Please try again after checking the id!**")
            await ctx.send(embed=embed)


    @ticket_.command(name="reset")
    @commands.has_permissions(manage_channels=True)
    async def reset_(self, ctx: commands.Context):
        """Resets the ticket count set of the server"""
        embed = discord.Embed(description=f"Are you sure you want to reset the **Ticket Count**?\n------------------------------------------------\nRespond Within **15** seconds!", color=discord.Color.orange())
        message = await ctx.send(embed=embed)
        await message.edit(embed=embed, view=TicketResetView(ctx, message, self.bot))

    @ticket_.command(name="clean", hidden=True)
    @commands.is_owner()
    async def clean_(self, ctx: commands.Context):
        await cleanup(ctx.guild)
        await ctx.send("<:tick:897382645321850920> Cleaned up all tickets!")

    @ticket_.command(name="category")
    @commands.has_permissions(manage_channels=True)
    async def category_(self, ctx: commands.Context, categoryID: int=None):
        """Sets the category for tickets. Highly reccomended."""
        try:
            if categoryID is None:
                self.bot.dbcursor.execute(f'SELECT category FROM ticket WHERE guild_id=?', (ctx.guild.id,))
                dataCheck = self.bot.dbcursor.fetchone()
                if not dataCheck:
                    return await ctx.send(embed=discord.Embed(description="**<:error:897382665781669908> You have not assigned a category to tickets yet**", color=discord.Color.red()))
        
                self.bot.dbcursor.execute(f'SELECT * FROM ticket WHERE guild_id=?', (ctx.guild.id,))
                categoryFind = self.bot.dbcursor.fetchone()
                cat = categoryFind[2]
                return await ctx.send(embed=discord.Embed(description=f"**The category_id set for this server is {cat}**", color=discord.Color.green()))

            self.bot.dbcursor.execute(f'SELECT category FROM ticket WHERE guild_id=?', (ctx.guild.id,))
            data = self.bot.dbcursor.fetchone()
            if not data:
                self.bot.dbcursor.execute(f'SELECT * FROM ticket WHERE guild_id=?', (ctx.guild.id,))
                dataCheck2 = self.bot.dbcursor.fetchone()
                if not dataCheck2[0]:
                    self.bot.dbcursor.execute(f'INSERT INTO ticket (guild_id, category) VALUES(?,?)', (ctx.guild.id, categoryID))
                else:
                    self.bot.dbcursor.execute(f'INSERT INTO ticket (category) VALUES(?) WHERE guild_id=?', (categoryID, ctx.guild.id))
            if data:
                self.bot.dbcursor.execute(f'UPDATE ticket SET category = ? WHERE guild_id=?', (categoryID, ctx.guild.id))
            self.bot.db.commit()
            category = discord.utils.get(ctx.guild.categories, id=categoryID)
            embed = discord.Embed(description=f"**<:tick:897382645321850920> Successfully added `{category}` as the ticket category!\n\nIf you want to keep ticket view permissions, make sure to change the category permissions.**", color=discord.Color.green())
            await ctx.send(embed=embed)
        except Exception as e:
            print(e)
    
    @ticket_.command()
    @commands.has_permissions(manage_channels=True)
    async def close(self, ctx: commands.Context):
        """Closes the ticket"""
        self.bot.dbcursor.execute(f'SELECT * FROM tickets WHERE guild_id=? AND channel_id=?', (ctx.guild.id, ctx.channel.id))
        data = self.bot.dbcursor.fetchone()
        if data[3] == "close":
            return await ctx.send(embed=discord.Embed(description="**<:error:897382665781669908> The ticket is already closed**", color=discord.Color.red()))
        if ctx.channel.id != data[1]:
            await ctx.send(embed=discord.Embed(description="**<:error:897382665781669908> Looks like either this channel is not a ticket channel or you aren't in the same channel**", color=discord.Color.red()))
        embed = discord.Embed(description="**Are you sure you want to close the ticket?**", color=discord.Color.orange())
        message = await ctx.send(embed=embed)
        await message.edit(view=TicketCloseTop2(ctx.author, message, self.bot))

    @ticket_.command()
    async def add(self, ctx: commands.Context, user: discord.Member):
        """Adds a user in the ticket"""
        self.bot.dbcursor.execute(f'SELECT * FROM tickets WHERE guild_id=? AND channel_id=?', (ctx.guild.id, ctx.channel.id))
        data = self.bot.dbcursor.fetchone()
            
        if ctx.channel.id != data[1]:
            await ctx.send(embed=discord.Embed(description="**<:error:897382665781669908> Looks like either this channel is not a ticket channel or you aren't in the same channel**", color=discord.Color.red()))

        if user in ctx.channel.members:
            return await ctx.send(embed=discord.Embed(description="**<:error:897382665781669908> That user is already in the ticket**", color=discord.Color.red))
        
        channel: discord.TextChannel = ctx.channel
        perms = channel.overwrites_for(user)
        perms.view_channel = True
        perms.send_messages = True
        perms.read_message_history = True
        await channel.set_permissions(user, overwrite=perms)
        embed = discord.Embed(description=f"**<:tick:897382645321850920> Successfully added {user.mention} in the ticket!**", color=discord.Color.green())
        await ctx.send(embed=embed)

    @ticket_.command(aliases=['rm'])
    async def remove(self, ctx: commands.Context, user: discord.Member):
        """Removes a user from a ticket. Note: It can't be the user who created the ticket or a person with admin"""
        self.bot.dbcursor.execute(f'SELECT * FROM tickets WHERE guild_id=? AND channel_id=?', (ctx.guild.id, ctx.channel.id))
        data = self.bot.dbcursor.fetchone()
            
        if ctx.channel.id != data[1]:
            await ctx.send(embed=discord.Embed(description="**<:error:897382665781669908> Looks like either this channel is not a ticket channel or you aren't in the same channel**", color=discord.Color.red()))

        if user.id == data[2]:
            embed2 = discord.Embed(description=f"**<:error:897382665781669908> {user.mention} is the one who opened a ticket\nYou can't remove them from the ticket!**", color=discord.Color.red())
            await ctx.send(embed=embed2)
        
        if user.guild_permissions.administrator or user.guild_permissions.manage_channels:
            return await ctx.send(embed=discord.Embed(description="**<:error:897382665781669908> That user is a *MOD/ADMIN*.**", color=discord.Color.red()))

        if not user in ctx.channel.members:
            return await ctx.send(embed=discord.Embed(description="**<:error:897382665781669908> That user is already not in the ticket**", color=discord.Color.red))
        
        channel: discord.TextChannel = ctx.channel
        perms = channel.overwrites_for(user)
        perms.view_channel = False
        perms.send_messages = False
        perms.read_message_history = False
        await channel.set_permissions(user, overwrite=perms)
        embed = discord.Embed(description=f"**<:tick:897382645321850920> Successfully removed {user.mention} from the ticket!**", color=discord.Color.green())
        await ctx.send(embed=embed)

    @ticket_.command(hidden=True)
    @commands.is_owner()
    async def set(self, ctx: commands.Context, *, num: int):
        self.bot.dbcursor.execute('UPDATE ticket SET count=? WHERE guild_id=?', (num, ctx.guild.id))
        self.bot.db.commit()
        await ctx.send(embed=discord.Embed(description=f"**<:tick:897382645321850920> Set the Ticket Count to -> `{num}`**", color=discord.Color.green()))

    @ticket_.command(aliases=['how', 'guide'])
    @commands.has_permissions(manage_channels=True)
    async def setup(self, ctx: commands.Context):
        """Complete guide that shows us how to setup the perfect ticket system in the server"""
        embed = discord.Embed(title="__Ticket Setup__", description="**How to setup a ticket system :-**\n\n--> Create a panel buy using `+panel create <channel> [name]`\n--> Create a timepass ticket and close it\n--> Use command `+ticket category <category_id>` to setup a category (I highly reccomend using ticket categories. They are way better and you can personalize their permissions and stuff\n--> You are good to go. Use `+ticket` or `+panel` for more info!)", color=discord.Color.green()).set_footer(text=f"{self.bot.user.name} - Ticket System", icon_url=self.bot.user.avatar.url)
        await ctx.send(embed=embed)

    @ticket_.command()
    async def role(self, ctx: commands.Context, switch: str, *, role: discord.Role):
        """Adds a role or removes the role from a server.\nExample: `ticket role add @SOMEROLE` `ticket role remove remove @SOMEROLE`"""
        self.bot.dbcursor.execute(f'SELECT * FROM tickets WHERE guild_id=? AND channel_id=?', (ctx.guild.id, ctx.channel.id))
        data = self.bot.dbcursor.fetchone()
            
        if ctx.channel.id != data[1]:
            await ctx.send(embed=discord.Embed(description="**<:error:897382665781669908> Looks like either this channel is not a ticket channel or you aren't in the same channel**", color=discord.Color.red()))

        if switch.lower() == "add":
            channel: discord.Channel = ctx.channel
            perms = channel.overwrites_for(role)
            perms.view_channel = True
            perms.send_messages = True
            perms.read_message_history = True
            await channel.set_permissions(role, overwrite=perms)
            embed = discord.Embed(description=f"**<:tick:897382645321850920> Successfully added {role.mention} in the ticket!**", color=discord.Color.green())
            await ctx.send(embed=embed)
        
        if switch.lower() == "remove":
            channel: discord.Channel = ctx.channel
            perms = channel.overwrites_for(role)
            perms.view_channel = False
            perms.send_messages = False
            perms.read_message_history = False
            await channel.set_permissions(role, overwrite=perms)
            embed = discord.Embed(description=f"**<:tick:897382645321850920> Successfully added {role.mention} in the ticket!**", color=discord.Color.green())
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(TicketCog(bot))