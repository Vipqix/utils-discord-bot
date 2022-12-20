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

# this is an server invite dont get confused and please change it to your server invite
invite = "https://discord.gg/invite"

client = aclient()
tree = app_commands.CommandTree(client)

# commands = 19

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
    await interaction.response.send_message(embed=em, ephemeral=True)

@tree.command(name='kick', description='Kicks a member')
async def kick(interaction: discord.Interaction, user: discord.Member, reason: str = None):
    if interaction.user.guild_permissions.administrator == True:
        if reason == None:
            try:
                em = discord.Embed(title=f"kicked!", description=f"Kicked : {user}\nReason: {reason}")
                await interaction.response.send_message(embed=em)
                emb = discord.Embed(title=f"Kicked!", description=f"You have been kicked from `{interaction.guild}`\nfrom `{interaction.user}!`\nNo reason was given.")
                await user.send(embed=emb)
                await user.kick()
            except Exception as e:
                await interaction.response.send_message(f"error : ```{e}```", ephemeral=True)
        else:
            try:
                em = discord.Embed(title=f"kicked!", description=f"Kicked : {user}\nReason: {reason}")
                await interaction.response.send_message(embed=em)
                emb = discord.Embed(title=f"Kicked!", description=f"You have been kicked from `{interaction.guild}`\nfrom `{interaction.user}!`\nReason: {reason}")
                await user.send(embed=emb)
                await user.kick()
            except Exception as e:
                await interaction.response.send_message(f"error : ```{e}```", ephemeral=True)
    else:
        await interaction.response.send_message("You do not have permission to use this command!", ephemeral=True)

@tree.command(name='ban', description='Bans a member')
async def ban(interaction: discord.Interaction, user: discord.Member, reason:str = None):
    if interaction.user.guild_permissions.administrator == True:
        if reason == None:
            try:
                em = discord.Embed(title=f"banned!", description=f"Banned : {user}")
                await interaction.response.send_message(embed=em)
                await user.ban()
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
    else:
        await interaction.response.send_message("You do not have permission to use this command!", ephemeral=True)

@tree.command(name='unban', description='Unbans a member')
async def unban(interaction: discord.Interaction, user: discord.User):
    if interaction.user.guild_permissions.administrator == True:
        try:
            em = discord.Embed(title=f"unbanned!", description=f"Unbanned : {user}")
            await interaction.response.send_message(embed=em, ephemeral=True)
            await interaction.guild.unban(user)
            await user.send(f"You have been unbanned from (server) {interaction.guild} from (user) {interaction.user}, here is an invite to the server {invite}")
        except Exception as e:
            await interaction.response.send_message(f"error : ```{e}```", ephemeral=True)
    else:
        await interaction.response.send_message("You do not have permission to use this command!", ephemeral=True)

@tree.command(name='voice_mute', description='Mutes a member')
async def mute(interaction: discord.Interaction, user: discord.Member, reason: str = None):
    if interaction.user.guild_permissions.administrator == True:
        if reason == None:
            try:
                await user.edit(mute=True)
                em = discord.Embed(title=f"muted!", description=f"Muted : {user}")
                await interaction.response.send_message(embed=em, ephemeral=True)
            except Exception as e:
                await interaction.response.send_message(f"error : ```{e}```")
        else:
            try:
                em = discord.Embed(title=f"unmuted!", description=f"Unmuted : {user}\nReason: {reason}")
                await interaction.response.send_message(embed=em, ephemeral=True)
                await user.edit(mute=False)
            except Exception as e:
                await interaction.response.send_message(f"error : ```{e}```")
    else:
        await interaction.response.send_message("You do not have permission to use this command!", ephemeral=True)

@tree.command(name='voice_unmute', description='Unmutes a member')
async def unmute(interaction: discord.Interaction, user: discord.Member):
    if interaction.user.guild_permissions.administrator == True:
        try:
            em = discord.Embed(title=f"unmuted!", description=f"Unmuted : {user}")
            await interaction.response.send_message(embed=em, ephemeral=True)
            await user.edit(mute=False)
        except Exception as e:
            await interaction.response.send_message(f"error : ```{e}```")
    else:
        await interaction.response.send_message("You do not have permission to use this command!", ephemeral=True)

@tree.command(name='dm', description='DMs a member')
async def dm(interaction: discord.Interaction, user: discord.Member,  message: str):
    if interaction.user.guild_permissions.administrator == True:
        try:
            em = discord.Embed(title=f"DM sent!", description=f"Sent to : {user}\nMessage: ```{message}```")
            await interaction.response.send_message(embed=em, ephemeral=True)
            await user.send(message)
        except Exception as e:
            await interaction.response.send_message(f"error : ```{e}```")
    else:
        await interaction.response.send_message("You do not have permission to use this command!", ephemeral=True)

@tree.command(name='clear', description='Clears messages')
async def clear(interaction: discord.Interaction, amount: int):
    if interaction.user.guild_permissions.administrator == True:
        try:
            em = discord.Embed(title=f"cleared!", description=f"Cleared {amount} messages!")
            await interaction.response.send_message(embed=em, ephemeral=True)
            await interaction.channel.purge(limit=amount)
        except Exception as e:
            await interaction.response.send_message(f"error : ```{e}```")
    else:
        await interaction.response.send_message("You do not have permission to use this command!", ephemeral=True)

@tree.command(name='slowmode', description='Sets slowmode')
async def slowmode(interaction: discord.Interaction, seconds: int):
    if interaction.user.guild_permissions.administrator == True:
        try:
            em = discord.Embed(title=f"slowmode set!", description=f"Set slowmode to {seconds} seconds!")
            await interaction.response.send_message(embed=em, ephemeral=False)
            await interaction.channel.edit(slowmode_delay=seconds)
        except Exception as e:
            await interaction.response.send_message(f"error : ```{e}```", ephemeral=True)
    else:
        await interaction.response.send_message("You do not have permission to use this command!", ephemeral=True)

@tree.command(name='remove_slowmode', description='Removes slowmode')
async def remove_slowmode(interaction: discord.Interaction):
    if interaction.user.guild_permissions.administrator == True:
        try:
            em = discord.Embed(title=f"slowmode removed!", description=f"Removed slowmode!")
            await interaction.response.send_message(embed=em, ephemeral=False)
            await interaction.channel.edit(slowmode_delay=0)
        except Exception as e:
            await interaction.response.send_message(f"error : ```{e}```")
    else:
        await interaction.response.send_message("You do not have permission to use this command!", ephemeral=True)

@tree.command(name='lock', description='Locks a channel')
async def lock(interaction: discord.Interaction):
    if interaction.user.guild_permissions.administrator == True:
        try:
            em = discord.Embed(title=f"locked!", description=f"Locked {interaction.channel}!")
            await interaction.response.send_message(embed=em, ephemeral=False)
            await interaction.channel.set_permissions(interaction.guild.default_role, send_messages=False)
        except Exception as e:
            await interaction.response.send_message(f"error : ```{e}```")
    else:
        await interaction.response.send_message("You do not have permission to use this command!", ephemeral=True)

@tree.command(name='unlock', description='Unlocks a channel')
async def unlock(interaction: discord.Interaction):
    if interaction.user.guild_permissions.administrator == True:
        try:
            em = discord.Embed(title=f"unlocked!", description=f"Unlocked {interaction.channel}!")
            await interaction.response.send_message(embed=em, ephemeral=False)
            await interaction.channel.set_permissions(interaction.guild.default_role, send_messages=True)
        except Exception as e:
            await interaction.response.send_message(f"error : ```{e}```")
    else:
        await interaction.response.send_message("You do not have permission to use this command!", ephemeral=True)

@tree.command(name='support', description='makes a support ticket')
async def support(interaction: discord.Interaction):
    category = discord.utils.get(interaction.guild.categories, name="Tickets")
    overwrites = {
        interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
        interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True)
    }
    try:
        channel = interaction.guild.create_text_channel(f"ticket-{interaction.user.name}", category=category, overwrites=overwrites)
        await channel
        em = discord.Embed(title=f"Ticket created!", description=f"Ticket created in {channel.mention}\nTo close the ticket, use /close")
        await channel.send(embed=em)
    except Exception as e:
        await interaction.response.send_message(f"error : ```{e}```")

@tree.command(name='close', description='closes a support ticket')
async def close(interaction: discord.Interaction, reason: str):
    if interaction.channel.name.startswith("ticket-"):
        try:
            em = discord.Embed(title=f"Ticket closed!", description=f"closing : {interaction.channel.mention}\nDeleting in 5 seconds...")
            await interaction.response.send_message(embed=em, ephemeral=False)
            time.sleep(5)
            await discord.Member.send(interaction.user, f"Your ticket has been closed for the reason: {reason}")
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

@tree.command(name='dmspam', description='DM spams a member')
async def dmspam(interaction: discord.Interaction, member: discord.Member, message: str, amount: int, delay: str):
    if interaction.user.guild_permissions.administrator == True:
        try:
            em = discord.Embed(title=f"DM spam sent!", description=f"Sent `{amount}` messages to `{member.mention}`")
            await interaction.response.send_message(embed=em, ephemeral=False)
            for x in range(amount):
                await member.send(message)
                time.sleep(delay)
        except Exception as e:
            await interaction.response.send_message(f"error : ```{e}```")
    else:
        await interaction.response.send_message("You do not have permission to use this command!", ephemeral=True)
    
@tree.command(name='test', description='test')
async def test(interaction: discord.Interaction, member : discord.Member):
    await interaction.response.send_message(f"test : {member.mention}")
    

# create a text file called bottoken.txt and paste your bot token in it
f = open('bottoken.txt', 'r')
client.run(f.read())
