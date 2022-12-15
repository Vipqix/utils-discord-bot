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
    await interaction.response.send_message(embed=em)

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
            await interaction.response.send_message(f"{user} has been kicked!")
        except Exception as e:
            await interaction.response.send_message(f"error : ```{e}```")
    else:
        try:
            await interaction.response.send_message(f"{user} has been kicked for {reason}!")
        except Exception as e:
            await interaction.response.send_message(f"error : ```{e}```")

@tree.command(name='ban', description='Bans a member')
async def ban(interaction: discord.Interaction, user: discord.Member, reason:str = None):
    await user.ban()
    if reason == None:
        try:
            await interaction.response.send_message(f"{user} has been banned!")
        except Exception as e:
            await interaction.response.send_message(f"error : ```{e}```")
    else:
        try:
            await interaction.response.send_message(f"{user} has been banned for {reason}!")
        except Exception as e:
            await interaction.response.send_message(f"error : ```{e}```")

@tree.command(name='unban', description='Unbans a member')
async def unban(interaction: discord.Interaction, user: discord.User):
    await interaction.guild.unban(user)
    try:
        await interaction.response.send_message(f"{user} has been unbanned!")
    except Exception as e:
        await interaction.response.send_message(f"error : ```{e}```")

@tree.command(name='mute', description='Mutes a member')
async def mute(interaction: discord.Interaction, user: discord.Member, reason: str = None):
    await user.edit(mute=True)
    if reason == None:
        try:
            await interaction.response.send_message(f"{user} has been muted!")
        except Exception as e:
            await interaction.response.send_message(f"error : ```{e}```")
    else:
        try:
            await interaction.response.send_message(f"{user} has been muted for {reason}!")
        except Exception as e:
            await interaction.response.send_message(f"error : ```{e}```")

@tree.command(name='unmute', description='Unmutes a member')
async def unmute(interaction: discord.Interaction, user: discord.Member):
    await user.edit(mute=False)
    try:
        await interaction.response.send_message(f"{user} has been unmuted!")
    except Exception as e:
        await interaction.response.send_message(f"error : ```{e}```")

@tree.command(name='dm', description='DMs a member')
async def dm(interaction: discord.Interaction, user: discord.Member,  message: str):
    try:
        await user.send(message)
        await interaction.response.send_message(f"Message sent to {user}")
    except Exception as e:
        await interaction.response.send_message(f"error : ```{e}```")

@tree.command(name='clear', description='Clears messages')
async def clear(interaction: discord.Interaction, amount: int):
    try:
        await interaction.response.send_message(f"{amount} messages have been cleared!")
        await interaction.channel.purge(limit=amount)
    except Exception as e:
        await interaction.response.send_message(f"error : ```{e}```")

@tree.command(name='slowmode', description='Sets slowmode')
async def slowmode(interaction: discord.Interaction, seconds: int):
    await interaction.channel.edit(slowmode_delay=seconds)
    try:
        await interaction.response.send_message(f"Slowmode has been set to {seconds} seconds!")
    except Exception as e:
        await interaction.response.send_message(f"error : ```{e}```")

@tree.command(name='remove_slowmode', description='Removes slowmode')
async def remove_slowmode(interaction: discord.Interaction):
    await interaction.channel.edit(slowmode_delay=0)
    try:
        await interaction.response.send_message(f"Slowmode has been removed!")
    except Exception as e:
        await interaction.response.send_message(f"error : ```{e}```")

@tree.command(name='lock', description='Locks a channel')
async def lock(interaction: discord.Interaction):
    await interaction.channel.set_permissions(interaction.guild.default_role, send_messages=False)
    try:
        await interaction.response.send_message(f"{interaction.channel} has been locked!")
    except Exception as e:
        await interaction.response.send_message(f"error : ```{e}```")

@tree.command(name='unlock', description='Unlocks a channel')
async def unlock(interaction: discord.Interaction):
    await interaction.channel.set_permissions(interaction.guild.default_role, send_messages=True)
    try:
        await interaction.response.send_message(f"{interaction.channel} has been unlocked!")
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
    await channel.send(f"{interaction.author.mention} has created a ticket!")
    try:
        await interaction.response.send_message(f"Ticket created in {channel.mention}")
    except Exception as e:
        await interaction.response.send_message(f"error : ```{e}```")

@tree.command(name='close', description='closes a support ticket')
async def close(interaction: discord.Interaction):
    try:
        await interaction.response.send_message(f"Ticket closes in 5 seconds!")
        time.sleep(5)
        await interaction.channel.delete()
    except Exception as e:
        await interaction.response.send_message(f"error : ```{e}```")

@tree.command(name='help', description='Shows all commands')
async def help(interaction: discord.Interaction):
    embed = discord.Embed(title="Help", description="All commands", color=0x00ff00)
    embed.add_field(name="/ping", value="Shows the bot's latency", inline=False)
    embed.add_field(name='/roll', value='Rolls a dice', inline=False)
    embed.add_field(name='/joke', value='Tells a joke', inline=False)
    embed.add_field(name="/ban", value="Bans a member", inline=False)
    embed.add_field(name="/unban", value="Unbans a member", inline=False)
    embed.add_field(name="/mute", value="Mutes a member", inline=False)
    embed.add_field(name="/unmute", value="Unmutes a member", inline=False)
    embed.add_field(name="/dm", value="DMs a member", inline=False)
    embed.add_field(name="/clear", value="Clears messages", inline=False)
    embed.add_field(name="/slowmode", value="Sets slowmode", inline=False)
    embed.add_field(name="/remove_slowmode", value="Removes slowmode", inline=False)
    embed.add_field(name="/lock", value="Locks a channel", inline=False)
    embed.add_field(name="/unlock", value="Unlocks a channel", inline=False)
    embed.add_field(name="/support", value="Makes a support ticket", inline=False)
    embed.add_field(name="/close", value="Closes a support ticket", inline=False)
    embed.add_field(name="/help", value="Shows all commands", inline=False)
    embed.set_author(name=f'reqested by {interaction.user}')
    await interaction.response.send_message(embed=embed)

    

f = open('FPbottoken.txt', 'r')
client.run(f.read())
