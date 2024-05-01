from connect import db
from hashlib import md5
import json

data = db()

def changePassword(uid,password):
    _uid = str(uid)
    _password = str(password)
    hash = md5()
    key = "IxMMveJRWsxStJgX"
    hash.update((_password + key).encode())
    data.execute(f"update arknights.account set password=\"{hash.hexdigest()}\" where uid={_uid};")

def getData(uid) -> json:
    _uid = str(uid)
    return(json.loads(data.execute(f"select user from arknights.account where uid = {_uid}")[0][0]))

def saveData(uid, userData): #此处data应为json
    _uid = str(uid)
    _data = json.dumps(userData)
    data.execute(f"update arknights.account set user=\'{_data}\' where uid = {_uid}")

def delUser(uid): 
    _uid = str(uid)
    data.execute(f"delete from arknights.account where uid ={_uid}")

def dropDatabase(): #删库跑路，防止误删，这里注释掉了
    twice = input("你真的确定要删库 y/N?")
    if twice == 'y':
        #data.execute("drop databases arknights")  
        pass

def getBan(uid):
    _uid = str(uid)
    return(data.execute(f"select ban from arknights.account where uid = {_uid}")[0][0])

def changeBan(uid,status):
    _uid = str(uid)
    data.execute(f"update arknights.account set ban={status} where uid = {_uid}")

def getAlluid():
    return(data.execute("select uid from arknights.account"))

if __name__ == '__main__':
    print(getAlluid().__len__())