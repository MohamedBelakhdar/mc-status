import os
import discord
from discord.ext import commands, tasks
from mcstatus import JavaServer

TOKEN = os.getenv("TOKEN")
SERVER_IP = "your.server.ip"  # Replace with your Minecraft server IP

intents = discord.Intents.default()
client = commands.Bot(command_prefix="!", intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    update_status.start()  # Start the status update loop

@tasks.loop(minutes=1)  # Update every minute
async def update_status():
    try:
        server = JavaServer.lookup(SERVER_IP)
        status = server.status()
        player_count = status.players.online
        activity = discord.Game(f"🟢 {player_count} players online")
    except:
        activity = discord.Game("🔴 Server offline")
    
    await client.change_presence(activity=activity)

client.run(TOKEN)
