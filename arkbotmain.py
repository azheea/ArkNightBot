
#版本1.0
import os
import re
import requests
import json
import pickle
#from user import user
import time

import botpy
from botpy import logging

from botpy.message import DirectMessage
from botpy.types.message import Reference
from botpy.message import Message
from botpy.ext.cog_yaml import read

#---------配置---------

server_ip = ""

gmkey = ""

console_token_mode = 4 #使用控制台执行命令的身份组权限 1-全体成员 2-管理员 4-频道创建者 5-子频道管理员

console_token_use = True #允许频道主等身份组使用控制台执行命令，默认开启

customcommand = {" 解锁地图":"prop um 1"," 治疗":"h"}#自定义命令

white_channal = []

#----------------------

useruid = {"null":"null"}

all_character = {'Lancet-2': 'char_285_medic2', 'Castle-3': 'char_286_cast3'}#自己补全捏

all_item_type = {'5001': 'EXP_PLAYER', 'SOCIAL_PT': 'SOCIAL_PT'}#自己补全捏

test_config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))

_log = logging.get_logger()


class MyClient(botpy.Client):
    async def on_ready(self):
        _log.info(f"robot 「{self.robot.name}」 on_ready!")


    async def on_at_message_create(self, message: Message):


        message.content = message.content[23:]

        if(message.channel_id in white_channal or "/子频道" in message.content):
            #/帮助命令
            if("/帮助" in message.content):
                backw = "本机器人由啊这.制作\n使用#命令以执行命令,目前支持的修改的有:\n龙门币、(博士)等级、源石、理智、玩家昵称 目前以上功能已暂时停用\n 远程获取角色 物品\n输入/帮助 <命令> 显示帮助"
                if("昵称" in message.content):
                    backw = "使用格式#昵称 <昵称> 暂时停用"
                if("龙门币" in message.content):
                    backw = "使用格式#龙门币 <数量> 暂时停用"
                if("角色" in message.content):
                    backw = "使用格式#角色 <角色id>"
                if("物品" in message.content):
                    backw = "使用格式#物品 <物品id> <数量>"
                if("等级" in message.content):
                    backw = "使用格式#等级 <等级> 暂时停用"
                if("理智" in message.content):
                    backw = "使用格式#理智 <数量> 暂时停用"
                if("全角色" in message.content):
                    backw = "使用格式#全角色"
                if("源石" in message.content):
                    backw = "使用格式#源石 <数量> 暂时停用"

            #/状态命令
            elif("/状态" in message.content ):
                if((json.loads((requests.post(server_ip+"/online/v1/ping", json={"value":"/v1/ping"},verify=False)).text))["message"] == "OK"):
                    backw = "服务器在线!"
                else:
                    backw = "服务器离线!"

            #/状态命令
            elif("/子频道" in message.content ):
                backw = "子频道id为:"+message.channel_id


            #执行命令
            elif(message.content[1] == "#"):
                #提取命令
                player_command = message.content
                if(player_command == ""):
                    player_command ="null"
                if(str(useruid.get(message.author.id, "null")) == "null"):
                    backw = "请先使用/绑定命令"
                else:
                    player_uid = str(useruid.get(message.author.id, "null"))
                    if("#角色" in player_command):
                        player_command = message.content.replace('#角色','')
                        player_command = player_command.replace(' ','')
                        for key, value in all_character.items():
                            if key in player_command:
                                player_command = player_command.replace(key, value)
                        headers = {'GMKey': str(gmkey)}
                        params = {
                        'uid': useruid.get(message.author.id, "null"),
                        'charId': player_command
                        }
                        yuanchengip = server_ip+"/admin/send"#自己补全捏
                        response = requests.get(yuanchengip, headers=headers, params=params)
                        backw = "成功给予" + str(str(useruid.get(message.author.id, "null")))+"玩家角色"+str(player_command)+"\n重新登录后生效"

                    elif("#全角色" in player_command):
                        _message = await message.reply(content="[Arkbot]收到! 已经开始发送! 请其他玩家稍等!",message_reference=Reference(message_id=message.id))
                        cishu = 0
                        for value in all_character.values():
                            headers = {'GMKey': str(gmkey)}
                            params = {
                            'uid': useruid.get(message.author.id, "null"),
                            'charId': value
                            }
                            yuanchengip = server_ip+"/admin/send"#自己补全捏
                            response = requests.get(yuanchengip, headers=headers, params=params)
                        backw = "已为玩家<@"+str(message.author.id)+">发送全角色 \n重新登录后生效 \n其他玩家可以执行指令了!"

                    elif("物品" in player_command):
                        user_command = player_command.split(' ')
                        if("#物品" in user_command):
                            if (len(user_command)-1 == user_command.index("#物品") or len(user_command)-2  == user_command.index("#物品")):
                                backw = "格式错误 正确格式为#物品 <物品id> <数量>"
                            
                            else:
                                if(user_command[len(user_command)-2] in all_item_type):
                                    headers = {'GMKey': str(gmkey)}
                                    params = {
                                    'uid': useruid.get(message.author.id, "null"),
                                    'itemId': user_command[len(user_command)-2],
                                    'count' : user_command[len(user_command)-1],
                                    'itemType': all_item_type[user_command[len(user_command)-2]]
                                    }
                                    yuanchengip = server_ip+"/admin/send"#自己补全捏
                                    response = requests.get(yuanchengip, headers=headers, params=params)
                                    backw = "成功给予" + str(str(useruid.get(message.author.id, "null")))+"玩家"+str(user_command[len(user_command)-2])+"\n重新登录后生效"
                                else:
                                    backw = "物品不存在"
                        else:
                            backw = "格式错误 正确格式为#物品 <物品id> <数量>"
                    else:
                        backw = "未知命令"

            #绑定uid
            elif("/绑定" in message.content):
                #提取uid
                player_uid = message.content.replace('/绑定','')
                player_uid = player_uid.replace(' ','')
                if(player_uid == ""):
                    player_uid ="null"
                if(player_uid.isdecimal() == True and len(player_uid) == 8):
                    useruid[message.author.id] = player_uid
                    backw = "绑定uid为"+player_uid
                else:
                    backw = "错误，uid：" + player_uid + "中含有非数字内容或不是标准的8位uid"
                


            #其它的情况？
            else:
                backw = "未知命令，请使用/帮助 获取帮助"

        else:
            backw = "请前往对应子频道执行指令"
        #反馈
        _message = await message.reply(content="[Arkbot]" + str(backw),message_reference=Reference(message_id=message.id))
















if __name__ == "__main__":
    # 通过预设置的类型，设置需要监听的事件通道 
    # intents = botpy.Intents.none()
    # intents.public_guild_messages=True

    # 通过kwargs，设置需要监听的事件通道
    intents = botpy.Intents(public_guild_messages=True)
    client = MyClient(intents=intents)
    client.run(appid=test_config["appid"], token=test_config["token"])
