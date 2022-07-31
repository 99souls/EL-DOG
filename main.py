import discord
from tokenstore import token

client = discord.Client()

@client.event
async def on_ready():
    print('bot is logged in')
    activity = discord.Streaming(name="BARK BARK", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ", type = "3")
    await client.change_presence(status=discord.Status.idle, activity=activity)
    
client.run(token)
