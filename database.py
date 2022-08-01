import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


cred = credentials.Certificate("D:/el-dog-689900cf7f9c.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://el-dog-default-rtdb.europe-west1.firebasedatabase.app/'

})
ref = db.reference("/")

def postData(username, region, dID, uid):
    ref.child(username).push({
        'username': username,
        'region': region,
        'discordid': dID,
        'uid': uid
    })

def reqData(username):
    x = ref.child(username).get()
    print(x["region"])

