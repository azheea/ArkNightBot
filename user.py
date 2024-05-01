from utils import getBan,getData,saveData,delUser,changePassword,changeBan,getAlluid
import json

class user:
    uid = None
    isBan = None
    Status_list = ["ap","gold","level","nickName","resume","diamondShard","androidDiamond","iosDiamond"] #目前感觉有用的就这些，懒得弄了

    data = None                 #存档


    def __init__(self,uid) -> None:
        self.uid = uid
        self.isBan = getBan(uid)
        self.data = getData(self.uid)
    
    def __del__(self) -> None:
        saveData(uid=self.uid,userData=self.data)
        changeBan(uid=self.uid,status=self.isBan)
    
    def getStatus(self,parameter): # ap gold level resume nickNumber diamondShard
        try:
            if parameter in self.Status_list:
                res = self.data["status"][parameter]
            else:
                return None
        except Exception as E:
            #print("[Error --]",E)
            return None
        return(res)

    def setStatus(self,parameter,num): # ap gold level resume nickNumber diamondShard
        try:
            if parameter == "androidDiamond" or parameter == "iosDiamond":
                self.data["status"]["androidDiamond"] = num
                self.data["status"]["iosDiamond"] = num
                return None
            else:
                self.data["status"][parameter] = num
                return None
        except Exception as E:
            print("[Error --]",E)
            return 1
        
    def savetStatus(self):
        _data = json.dumps(self.data)
        saveData(self.uid,_data)

    def show(self):
        data = []
        for i in self.Status_list:
            data.append(f"{i}:{self.getStatus(i)}")
        data.append(f"isBan:{self.isBan}")
        print(data)

    def changePasswd(self,password):
        changePassword(self.uid,password)

    def ban(self):
        self.isBan = 1
        changeBan(uid=self.uid,status=1)

    def unban(self):
        self.isBan = 0
        changeBan(uid=self.uid,status=0)
    

    


    
    
    
    


if __name__ == '__main__':
    # u = user(10000001)
    # u.show()
    # u.setStatus(parameter="androidDiamond",num=114514)
    # u.setStatus(parameter="")
    # u.show()
    uid = getAlluid()
    for i in uid:
        #print(i[0])
        u = user(i[0])
        u.show()
       
