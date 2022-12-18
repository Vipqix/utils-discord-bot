from discord import app_commands
import discord
import random
import requests
import time

class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents = discord.Intents.default())
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync() 
            self.synced = True
        print(f"We have logged in as {self.user}.")

client = aclient()
tree = app_commands.CommandTree(client)

@tree.command(name ="ping", description="Pong!")
async def ping(interaction: discord.Interaction):
    em = discord.Embed(title="Pong!", description=f"Latency: {round(client.latency * 1000)}ms")
    em.set_footer(text=f"Requested by {interaction.user}")
    await interaction.response.send_message(embed=em, ephemeral=True)

@tree.command(name="roll", description="Rolls a dice")
async def roll(interaction: discord.Interaction):
    await interaction.response.send_message(f"You rolled a {random.randint(1,6)}!")

@tree.command(name="joke", description="Tells a joke")
async def joke(interaction: discord.Interaction):
    joke = requests.get("https://official-joke-api.appspot.com/random_joke").json()
    em = discord.Embed(title=joke["setup"], description=joke["punchline"])
    em.set_footer(text=f"Requested by {interaction.user}")
    await interaction.response.send_message(embed=em)

@tree.command(name='kick', description='Kicks a member')
async def kick(interaction: discord.Interaction, user: discord.Member, reason: str = None):
    await user.kick()
    if reason == None:
        try:
            em = discord.Embed(title=f"kicked!", description=f"Kicked : {user}\nReason: {reason}")
            await interaction.response.send_message(embed=em)
            user.send(f"You have been kicked from {interaction.guild} from {interaction.user} for {reason}!")
        except Exception as e:
            await interaction.response.send_message(f"error : ```{e}```", ephemeral=True)
    else:
        try:
            em = discord.Embed(title=f"kicked!", description=f"Kicked : {user}\nReason: {reason}")
            await interaction.response.send_message(embed=em)
            user.send(f"You have been kicked from {interaction.guild} from {interaction.user} for {reason}!")
        except Exception as e:
            await interaction.response.send_message(f"error : ```{e}```", ephemeral=True)

@tree.command(name='ban', description='Bans a member')
async def ban(interaction: discord.Interaction, user: discord.Member, reason:str = None):
    await user.ban()
    if reason == None:
        try:
            em = discord.Embed(title=f"banned!", description=f"Banned : {user}")
            await interaction.response.send_message(embed=em)
            user.send(f"You have been banned from {interaction.guild} from {interaction.user} for {reason}!")
        except Exception as e:
            await interaction.response.send_message(f"error : ```{e}```", ephemeral=True)
    else:
        try:
            em = discord.Embed(title=f"banned!", description=f"Banned :{user}\nReason: {reason}")
            await interaction.response.send_message(embed=em)
            user.send(f"You have been banned from {interaction.guild} from {interaction.user} for {reason}!")
        except Exception as e:
            await interaction.response.send_message(f"error : ```{e}```", ephemeral=True)

@tree.command(name='unban', description='Unbans a member')
async def unban(interaction: discord.Interaction, user: discord.User):
    await interaction.guild.unban(user)
    try:
        em = discord.Embed(title=f"unbanned!", description=f"Unbanned : {user}")
        await interaction.response.send_message(embed=em, ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"error : ```{e}```", ephemeral=True)

@tree.command(name='mute', description='Mutes a member')
async def mute(interaction: discord.Interaction, user: discord.Member, reason: str = None):
    await user.edit(mute=True)
    if reason == None:
        try:
            em = discord.Embed(title=f"muted!", description=f"Muted : {user}")
            await interaction.response.send_message(embed=em, ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"error : ```{e}```")
    else:
        try:
            em = discord.Embed(title=f"muted!", description=f"Muted : {user}\nReason: {reason}")
            await interaction.response.send_message(embed=em, ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"error : ```{e}```")

@tree.command(name='unmute', description='Unmutes a member')
async def unmute(interaction: discord.Interaction, user: discord.Member):
    await user.edit(mute=False)
    try:
        em = discord.Embed(title=f"unmuted!", description=f"Unmuted : {user}")
        await interaction.response.send_message(embed=em, ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"error : ```{e}```")

@tree.command(name='dm', description='DMs a member')
async def dm(interaction: discord.Interaction, user: discord.Member,  message: str):
    try:
        em = discord.Embed(title=f"DM sent!", description=f"Sent to : {user}\nMessage: ```{message}```")
        await user.send(message)
    except Exception as e:
        await interaction.response.send_message(f"error : ```{e}```")

@tree.command(name='clear', description='Clears messages')
async def clear(interaction: discord.Interaction, amount: int):
    try:
        em = discord.Embed(title=f"cleared!", description=f"Cleared {amount} messages!")
        await interaction.response.send_message(embed=em, ephemeral=True)
        await interaction.channel.purge(limit=amount)
    except Exception as e:
        await interaction.response.send_message(f"error : ```{e}```")

@tree.command(name='slowmode', description='Sets slowmode')
async def slowmode(interaction: discord.Interaction, seconds: int):
    try:
        em = discord.Embed(title=f"slowmode set!", description=f"Set slowmode to {seconds} seconds!")
        await interaction.response.send_message(embed=em, ephemeral=False)
        await interaction.channel.slowmode_delay(seconds)
    except Exception as e:
        await interaction.response.send_message(f"error : ```{e}```", ephemeral=True)

@tree.command(name='remove_slowmode', description='Removes slowmode')
async def remove_slowmode(interaction: discord.Interaction):
    try:
        em = discord.Embed(title=f"slowmode removed!", description=f"Removed slowmode!")
        await interaction.response.send_message(embed=em, ephemeral=False)
        await interaction.channel.slowmode_delay(0)
    except Exception as e:
        await interaction.response.send_message(f"error : ```{e}```")

@tree.command(name='lock', description='Locks a channel')
async def lock(interaction: discord.Interaction):
    try:
        em = discord.Embed(title=f"locked!", description=f"Locked {interaction.channel}!")
        await interaction.response.send_message(embed=em, ephemeral=False)
        await interaction.channel.set_permissions(interaction.guild.default_role, send_messages=False)
    except Exception as e:
        await interaction.response.send_message(f"error : ```{e}```")

@tree.command(name='unlock', description='Unlocks a channel')
async def unlock(interaction: discord.Interaction):
    try:
        em = discord.Embed(title=f"unlocked!", description=f"Unlocked {interaction.channel}!")
        await interaction.response.send_message(embed=em, ephemeral=False)
        await interaction.channel.set_permissions(interaction.guild.default_role, send_messages=True)
    except Exception as e:
        await interaction.response.send_message(f"error : ```{e}```")

@tree.command(name='support', description='makes a support ticket')
async def support(interaction: discord.Interaction):
    category = discord.utils.get(interaction.guild.categories, name="Tickets")
    overwrites = {
        interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
        interaction.author: discord.PermissionOverwrite(read_messages=True, send_messages=True)
    }
    channel = await interaction.guild.create_text_channel(f"ticket-{interaction.author.name}", category=category, overwrites=overwrites)
    em = discord.Embed(title=f"Ticket created!", description=f"Ticket created in {channel.mention}\nTo close the ticket, use /close")
    await channel.send(embed=em)
    try:
        em = discord.Embed(title=f"Ticket created!", description=f"Ticket created in {channel.mention}\nTo close the ticket, use /close")
        await channel.send(embed=em)
    except Exception as e:
        await interaction.response.send_message(f"error : ```{e}```")

@tree.command(name='close', description='closes a support ticket')
async def close(interaction: discord.Interaction):
    if interaction.check(interaction.channel.name.startswith("ticket-")):
        try:
            em = discord.Embed(title=f"Ticket closed!", description=f"closing : {interaction.channel.mention}\nDeleting in 5 seconds...")
            await interaction.response.send_message(embed=em, ephemeral=False)
            time.sleep(5)
            await interaction.channel.delete()
        except Exception as e:
            await interaction.response.send_message(f"error : ```{e}```")
    else:
        await interaction.response.send_message("This is not a ticket channel!", ephemeral=True)

@tree.command(name='help', description='Shows all commands')
async def help(interaction: discord.Interaction):
    embed = discord.Embed(title="Help", description="All commands", color=0x00ff00)
    embed.add_field(name="/ping", value="Shows the bot's latency", inline=True)
    embed.add_field(name='/roll', value='Rolls a dice', inline=True)
    embed.add_field(name='/joke', value='Tells a joke', inline=True)
    embed.add_field(name="/ban", value="Bans a member", inline=True)
    embed.add_field(name="/unban", value="Unbans a member", inline=True)
    embed.add_field(name="/mute", value="Mutes a member", inline=True)
    embed.add_field(name="/unmute", value="Unmutes a member", inline=True)
    embed.add_field(name="/dm", value="DMs a member", inline=True)
    embed.add_field(name="/clear", value="Clears messages", inline=True)
    embed.add_field(name="/slowmode", value="Sets slowmode", inline=True)
    embed.add_field(name="/remove_slowmode", value="Removes slowmode", inline=True)
    embed.add_field(name="/lock", value="Locks a channel", inline=True)
    embed.add_field(name="/unlock", value="Unlocks a channel", inline=True)
    embed.add_field(name="/support", value="Makes a support ticket", inline=True)
    embed.add_field(name="/close", value="Closes a support ticket", inline=True)
    embed.add_field(name="/help", value="Shows all commands", inline=True)
    embed.set_author(name=f'reqested by {interaction.user}')
    await interaction.response.send_message(embed=embed)

    
# create a text file called bottoken.txt and paste your bot token in it
f = open('bottoken.txt', 'r')
client.run(f.read())
