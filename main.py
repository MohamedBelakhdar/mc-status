import os
import discord
from discord.ext import commands, tasks
from mcstatus import JavaServer

TOKEN = os.getenv("TOKEN")
SERVER_IP = "windows-chrysler.gl.joinmc.link"  # Replace with your Minecraft server IP
CHANNEL_ID = 1352335748770168852  # Replace with your actual channel ID

intents = discord.Intents.default()
client = commands.Bot(command_prefix="!", intents=intents)

message_id = None  # Store the message ID to update

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    update_status.start()  # Start the status update loop

@tasks.loop(minutes=1)
async def update_status():
    global message_id
    channel = client.get_channel(CHANNEL_ID)

    if channel is None:
        print("Channel not found!")
        return

    try:
        server = JavaServer.lookup(SERVER_IP)
        status = server.status()
        player_count = status.players.online
        embed = discord.Embed(
            title="ApelapaToo KINGS Server!",
            description=f"🟢 **Online**\n👥 **Players**: {player_count}/20",
            color=discord.Color.green()
        )
    except:
        embed = discord.Embed(
            title="ApelapaToo KINGS Server!",
            description="🔴 **Offline**",
            color=discord.Color.red()
        )

    if message_id is None:
        # First-time message send
        msg = await channel.send(embed=embed)
        message_id = msg.id
    else:
        # Edit existing message
        try:
            msg = await channel.fetch_message(message_id)
            await msg.edit(embed=embed)
        except:
            print("Message not found, sending new one...")
            msg = await channel.send(embed=embed)
            message_id = msg.id

client.run(TOKEN)
