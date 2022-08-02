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

def postData(username, region, dID, uid):
    ref.child(uid).push({
        'username': username,
        'region': region,
        'discordid': dID,
        'uid': uid
    })
 
async def reqData(ctx, id, field):
    try:
        x = ref.child(id).get()
        for i in x.values():
            if field == "nil":
                embed=discord.Embed(title="requested data", color=0x1fffd2)
                embed.add_field(name="username", value=i["username"], inline=False)
                embed.add_field(name="region", value=i["region"], inline=False)
                embed.add_field(name="discord user", value=f"<@{i['discordid']}>", inline=False)
                embed.add_field(name="discord id", value=i['discordid'], inline=False)
                embed.add_field(name="uid", value=i["uid"], inline=False)
                await ctx.send(embed=embed)
                
            else:
                await ctx.send(i[field])
    except: await ctx.send('user is not linked')
            
def generateUID():
    x = ref.order_by_key().limit_to_last(1).get()
    
    for i in x:
        uid = int(i) + 1
        return str(uid)
            



