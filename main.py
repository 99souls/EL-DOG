import discord
from discord.ext import commands
import cassiopeia as cass
from cassiopeia import Summoner
import json
import random
import time


from keystore import API_KEY
from tokenstore import token

cass.set_riot_api_key(API_KEY) # setting riot api key to key from keystore file
client = discord.Client() # creating discord client
client = commands.Bot(command_prefix='.') # setting command prefix

# setting status to stream + rick roll 

@client.event
async def on_ready():
    print('bot is logged in')
    activity = discord.Streaming(name="BARK BARK", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ", type = "3")
    await client.change_presence(status=discord.Status.idle, activity=activity)


@client.command()
async def link(ctx, *, args):
    args = args.split()
    username = args[0]
    region = args[1]
    userID = ctx.author.id

    with open('iconIDs.json', 'r') as f:
        icons = json.load(f)

    randomIconID = random.randint(0,28)
    message1 = await ctx.send(f'change league icon to ``{icons[str(randomIconID)]}``')
    await message1.add_reaction('💜')
    time.sleep(2)
    @client.event
    async def on_raw_reaction_add(message1):
        user = Summoner(name = username, region = region)
        iconID = user.profile_icon.id

        if randomIconID == iconID:
            await ctx.send('ur fucking in cunt')
        else:
            await ctx.send('ur out')
    
client.run(token)
