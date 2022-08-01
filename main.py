import discord
from discord.ext import commands
import cassiopeia as cass
from cassiopeia import Summoner
import json
import random
import time
from database import postData
from database import reqData
from database import generateUID

from _keystore import API_KEY
from _keystore import TOKEN

cass.set_riot_api_key(API_KEY) # setting riot api key to key from keystore file


intents = discord.Intents.default()
client = commands.Bot(command_prefix='.', intents = intents) # setting command prefix

# setting status to stream + rick roll 

@client.event
async def on_ready():
    print('bot is logged in')
    activity = discord.Streaming(name="BARK BARK | .help", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ", type = "3")
    await client.change_presence(status=discord.Status.idle, activity=activity)

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        ctx.send('you are missing permissions')
    else:
        await ctx.send(error)

@client.command()
async def link(ctx, username, region):
    userID = ctx.author.id
    dm = ctx.author
    try:
        with open('__iconIDs.json', 'r') as f:
            icons = json.load(f)

        randomIconID = random.randint(0,28)
        message1 = await dm.send(f'change league icon to ``{icons[str(randomIconID)]}``')
        print(1)
        await message1.add_reaction('💜')
        print(2)
        @client.event
        async def on_raw_reaction_add(payload):
                print(3)
                user = Summoner(name = username, region = region)
                iconID = user.profile_icon.id
                
                if randomIconID == iconID:
                    uid = generateUID()
                    postData(username, region, userID, uid)
        
                    dataMsg = discord.Embed(title="verification successful", color=0x1fffd2)
                    dataMsg.add_field(name="username", value=username, inline=False)
                    dataMsg.add_field(name="region", value=region, inline=False)
                    dataMsg.add_field(name="discord id", value=f"<@{userID}>", inline=False)
                    dataMsg.add_field(name="uid", value=uid, inline=False)
                    await dm.send(embed=dataMsg)
                    return
                else:
                    await dm.send('verification failed')
                    return
    except: await ctx.send('unable to send dm, check your privacy settings')

@client.command()
async def icon(ctx, id):
    with open('__iconIDs.json', 'r') as f:
        icons = json.load(f)
        await ctx.send(json.dumps(icons[id]))
        
@client.command()
@commands.has_permissions(administrator = True)
async def submit(ctx, username, region):
    user = ctx.author.id
    uid = generateUID()
    
    postData(username, region, user, uid)
    
    dataMsg = discord.Embed(title="user data", color=0x1fffd2)
    dataMsg.add_field(name="username", value=username, inline=False)
    dataMsg.add_field(name="region", value=region, inline=False)
    dataMsg.add_field(name="discord id", value=f"<@{user}>", inline=False)
    dataMsg.add_field(name="uid", value=uid, inline=False)
    await ctx.send(embed=dataMsg)
                
                
        
@client.command()
async def get(ctx, id, field="nil"):
    await reqData(ctx, id, field)

client.run(TOKEN)
