import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import discord
from _keystore import FB_KEY
from _keystore import URL


cred = credentials.Certificate(FB_KEY)
firebase_admin.initialize_app(cred, {
    'databaseURL': URL

})
ref = db.reference("/")

def postData(username, region, dID):
    name = region + ":" + username
    print(name)
    print(region)
    print(dID)
    ref.child(name).push({
        'username': username,
        'region': region,
        'discordid': dID,
    })

async def reqData(ctx, username, region, field):
    try:
        key = region + ":" + username
        print(key)
        x = ref.child(key).get()
        print('a')
        for i in x.values():
            print('b')
            if field == "nil":
                print('c')
                embed=discord.Embed(title="requested data", color=0x1fffd2)
                embed.add_field(name="username", value=i["username"], inline=False)
                embed.add_field(name="region", value=i["region"], inline=False)
                embed.add_field(name="discord user", value=f"<@{i['discordid']}>", inline=False)
                embed.add_field(name="discord id", value=i['discordid'], inline=False)
                print('d')
                await ctx.send(embed=embed)
                return
                
            else:
                await ctx.send(i[field])
                return
    except: await ctx.send('user is not linked')
    
def checkUserExists(username, region):
    try:
        key = region + ":" + username
        print('a2')
        ref.child(key).get()
    except:
        return 'account is already linked'
            
# def generateUID():
#     x = ref.order_by_key().limit_to_last(1).get()
    
#     for i in x:
#         uid = int(i) + 1
#         return str(uid)
            

# def userCheck(username, region):
#     users = ref.get()
    
#     for user in users:
#         for x in user:
#             if x["username"] == username & x["region"] == region:
#                 print('true')

        

