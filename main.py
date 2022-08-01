import discord
from discord.ext import commands
import cassiopeia as cass
from cassiopeia import Summoner
import json
import random
import time
import uuid

from _keystore import API_KEY
from _keystore import token

cass.set_riot_api_key(API_KEY) # setting riot api key to key from keystore file


intents = discord.Intents.default()
intents.message_content = True
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
    print(username)
    print(region)
    userID = ctx.author.id
    dm = ctx.author
    try: await dm.send('fuck')
    except: await ctx.send('unable to send dm, check your privacy settings')
    with open('__iconIDs.json', 'r') as f:
        icons = json.load(f)

    randomIconID = random.randint(0,28)
    message1 = await ctx.send(f'change league icon to ``{icons[str(randomIconID)]}``')
    await message1.add_reaction('💜')
    time.sleep(5)
    @client.event
    async def on_raw_reaction_add(message1):
        user = Summoner(name = username, region = region)
        iconID = user.profile_icon.id

        if randomIconID == iconID:
            await ctx.send('ur fucking in cunt')
            return
        else:
            await ctx.send('ur out')
            return

@client.command()
async def icon(ctx, id):
    with open('__iconIDs.json', 'r') as f:
        icons = json.load(f)
        await ctx.send(json.dumps(icons[id]))
        
@client.command()
async def submit(ctx, username, region):
    with open('__userdataStore.json', 'a+', newline = '\r\n') as userdataFile:
        user = ctx.author.id
        uid = uuid.uuid4()
        uid = str(uid)
        userinfo = { username : {
            "region" : region,
            "discordID" : user,
            "uid" : uid
        }
        }
        json.dump(userinfo, userdataFile, ensure_ascii=False, indent=4, sort_keys=True)
        await ctx.send(userinfo)
        
        
@client.command()
async def find(ctx, username):
    with open('__userdataStore.json', 'r') as userdataFile:
    #    csv_reader = csv.reader(userdataFile, delimiter = ',')
        for line in userdataFile:
            line = line.split(',')
            if line[1] == username:
                userid = line[0]
                # userid = userid[:-2]
                await ctx.send(f'{username} is linked to <@{userid}>')
                return
            else:
                await ctx.send('that account has not been linked')
                return

client.run(token)
