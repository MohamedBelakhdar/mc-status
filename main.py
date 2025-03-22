import os
import discord
from discord.ext import commands, tasks
import mcstatus
import datetime

TOKEN = os.getenv("TOKEN")
SERVER_IP = "windows-chrysler.gl.joinmc.link"  # Replace with your actual server IP

intents = discord.Intents.default()
client = commands.Bot(command_prefix="!", intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    
    # Set bot status
    await client.change_presence(activity=discord.Game("Made with ChatGPT 🤖 × ApelapaToo 🔥"))

    # Start the status update loop
    update_status.start()

channel_id = 1352335748770168852  # Replace with your #server-status channel ID
message_id = None  # To store the ID of the status message

@tasks.loop(seconds=10)  # Update every 10 seconds
async def update_status():
    global message_id

    # Fetch server status
    server = mcstatus.JavaServer.lookup(SERVER_IP)
    try:
        status = server.status()
        online = True
        player_count = status.players.online
        version = status.version.name
    except:
        online = False
        player_count = 0
        version = "N/A"

    # Get the channel
    channel = client.get_channel(channel_id)
    if channel is None:
        print("Channel not found!")
        return

    # Format the status message
    current_time = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    embed = discord.Embed(title="ApelapaToo KINGS Server!", color=0x00FF00 if online else 0xFF0000)
    embed.add_field(name="Status", value="🟢 Online" if online else "🔴 Offline", inline=True)
    embed.add_field(name="Players", value=f"{player_count}/20", inline=True)
    embed.add_field(name="Version", value=version, inline=True)
    embed.set_footer(text=f"Last update: {current_time}")

    # Send or edit the message
    if message_id:
        try:
            msg = await channel.fetch_message(message_id)
            await msg.edit(embed=embed)
        except:
            message_id = None  # Reset if message is deleted
    if not message_id:
        msg = await channel.send(embed=embed)
        message_id = msg.id

client.run(TOKEN)
