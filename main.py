import os
import discord
from discord.ext import commands, tasks
import mcstatus

# Load token from environment variable
TOKEN = os.getenv("TOKEN")

# Bot setup
intents = discord.Intents.default()
client = commands.Bot(command_prefix="!", intents=intents)

# Minecraft server details
SERVER_IP = "windows-chrysler.gl.joinmc.link"
CHANNEL_ID = 1352335748770168852  # Replace with your server-status channel ID

@client.event
async def on_ready():
    activity = discord.Game(name="Made with ChatGPT 🤖 x ApelapaToo 👑")
    await client.change_presence(status=discord.Status.online, activity=activity)
    print(f"Logged in as {client.user}")
    update_status.start()  # Start updating the server status

@tasks.loop(minutes=1)  # Update every 5 minutes
async def update_status():
    channel = client.get_channel(CHANNEL_ID)
    if channel is None:
        print("Channel not found!")
        return

    try:
        server = mcstatus.JavaServer.lookup(SERVER_IP)
        status = server.status()
        embed = discord.Embed(title="MC SERVER INFO", color=discord.Color.green())
        embed.add_field(name="Status", value="🟢 Online", inline=True)
        embed.add_field(name="Players", value=f"{status.players.online}/{status.players.max}", inline=True)
        embed.add_field(name="Version", value=status.version.name, inline=False)
    except:
        embed = discord.Embed(title="MC SERVER INFO", color=discord.Color.red())
        embed.add_field(name="Status", value="🔴 Offline", inline=True)

    # Send or edit the status message
    async for message in channel.history(limit=10):
        if message.author == client.user:
            await message.edit(embed=embed)
            return

    await channel.send(embed=embed)  # If no previous message, send a new one

client.run(TOKEN)
