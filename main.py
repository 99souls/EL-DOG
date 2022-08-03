import discord
from discord.ext import commands
import cassiopeia as cass
from cassiopeia import Summoner
import json
import random
from discord_components import DiscordComponents, Button
from database import postData, reqData, checkUserExists


from _keystore import API_KEY
from _keystore import TOKEN

cass.set_riot_api_key(API_KEY)


intents = discord.Intents.default()
client = commands.Bot(command_prefix='.', intents = intents) # setting command prefix
DiscordComponents(client)

def createSuccessEmbed(username, region, userID):
    dataMsg = discord.Embed(title='verification successful', color=0x1fffd2)
    dataMsg.add_field(name='username', value=username, inline=False)
    dataMsg.add_field(name='region', value=region, inline=False)
    dataMsg.add_field(name='discord id', value=f'<@{userID}>', inline=False)
    return dataMsg

async def checkIcon(interaction, username, region, userID, user, randomIcon):
    iconID = user.profile_icon.id
    print(iconID)
    print(randomIcon)
    if randomIcon == iconID:
        print('verify success')
        postData(username, region, userID)
        print('posted data to firebase')
        await interaction.send(embed = createSuccessEmbed(username, region, userID))
        print('sent embed message')
        return
    else:
        print('failed to verify')
        await interaction.send('verification failed')
        return


@client.event
async def on_ready():
    print('bot is logged in')
    activity = discord.Streaming(name='BARK BARK | .help', url='https://www.youtube.com/watch?v=dQw4w9WgXcQ', type = '3')
    await client.change_presence(status=discord.Status.idle, activity=activity)


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        ctx.send('you are missing permissions')
    else:
        await ctx.send(error)


@client.command()
async def link(ctx, username, region):
    region = region.upper()
    userID = ctx.author.id
    dm = ctx.author
    try: 
        # print('a')
        # await ctx.send(checkUserExists(username, region))
        # print('b')
        print(checkUserExists(username, region))
        print('c')
    except:
        try:
            with open('__iconIDs.json', 'r') as f:
                icons = json.load(f)
            print('opened icon ids file')

            randomIconID = random.randint(0,28)
            print('random id generated')
            
            await dm.send(
                f'change league icon to ``{icons[str(randomIconID)]}``',
                components = [
                    Button(label = '🐬', custom_id = 'button1', style = 1)
                ],
            )

            print('dm sent + waiting for button click')
            interaction = await client.wait_for('button_click', check = lambda i: i.custom_id == 'button1')
            print('button clicked')
            user = Summoner(name = username, region = region)
            print('fetched user details')
            await checkIcon(interaction, username, region, userID, user, randomIconID)

        except: 
            await ctx.send('something went wrong... make sure to check your privacy settings')


@client.command()
async def icon(ctx, id):
    with open('__iconIDs.json', 'r') as f:
        icons = json.load(f)
        await ctx.send(json.dumps(icons[id]))

        
@client.command()
@commands.has_permissions(administrator = True)
async def submit(ctx, username, region):
    user = ctx.author.id
    postData(username, region, user)
    
    dataMsg = discord.Embed(title='user data', color=0x1fffd2)
    dataMsg.add_field(name='username', value=username, inline=False)
    dataMsg.add_field(name='region', value=region, inline=False)
    dataMsg.add_field(name='discord id', value=f'<@{user}>', inline=False)
    await ctx.send(embed=dataMsg)


@client.command()
async def get(ctx, username, region, field='nil'):
    await reqData(ctx, username, region.upper(), field)

client.run(TOKEN)

