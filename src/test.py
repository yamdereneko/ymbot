# -*- coding: utf-8 -*
"""
@Software : PyCharm
@File : 0.py
@Author : 喵
@Time : 2021/09/29 22:39:29
@Docs : 请求推栏战绩例子
"""

import websockets.exceptions

# import tkinter as Tkinter
# from tkinter import font as tkFont
#
# Tkinter.Frame().destroy()
# txt = tkFont.Font(family="Times New Roman", size=14)
# width = txt.measure("What the heck?")
# print(width)

# print(re.match(r'^2',data).group())
# print(re.match('\d*4',data).group())
# 请求头
#
# api = API()
#
# async def main():
#     config = jxData.config
#     pool = database(config)
#     # 获取所有的数据进行处理
#     # 判断连接池数据是否冲突
#     sql = "select * from JJC_rank_weekly"
#     await pool.connect()
#     weekly = await pool.fetchall(sql)
#     print(weekly)
#     s = pd.Series(weekly[0])
#     # df = s.loc['week', '蓬莱']
#     # print(df)
#     print(s)
#     # G = nx.from_pandas_edgelist(s, 'weekly', 'to', create_using=nx.DiGraph())
#     # G.from_nx(G)
#     # G.show('1_evidence.html')
#
#
# asyncio.run(main())
# import asyncio
#
# import nonebot
# from src.internal.tuilanapi import API
# from src.internal.tuilanapi import API
# from src.Data.database import DataBase as database
#
# # 请求头
# headers = jxData.headers
# tuilan_api = API()
# class GetPersonInfo:
#     def __init__(self, role: str, server: str):
#         config = jxData.config
#         self.role = role
#         self.server = jxData.mainServer(server)
#         self.zone = jxData.mainZone(self.server)
#         self.database = database(config)
#         self.role_id = None
#         self.person_id = None
#         self.ts = None
#         self.xsk = None
#         self.role_name = None
#
#     async def main(self):
#         try:
#             self.role_id = str(role_id_info.get("id"))
#
#             response = await api.role_indicator(role_id=self.role_id, server=self.server, zone=self.zone)
#             if response.code != 0:
#                 nonebot.logger.error("API接口Daily获取信息失败，请查看错误")
#                 return None
#             self.person_id = response.data['person_info']['person_id']
#
#             response = await api.mine_match_person9history(person_id=str(self.person_id), size=10, cursor=0)
#             if response.code != 0:
#                 nonebot.logger.error("API接口Daily获取信息失败，请查看错误")
#                 return None
#
#         except Exception as e:
#             nonebot.logger.error(e)
#             nonebot.logger.error("获取用户信息失败，请查看问题.")
#             traceback.print_exc()
#             return None
#
# personInfo = GetPersonInfo("时南星","姨妈")
# asyncio.run(personInfo.main())
#


# """
# @Software : PyCharm
# @File : 0.py
# @Author : 喵
# @Time : 2021/09/29 22:39:29
# @Docs : 请求推栏战绩例子
# """
# # import asyncio
# # 
# # import nonebot
# # from src.internal.tuilanapi import API
# # from src.Data.database import DataBase as database
# # 
# # -*- coding: utf-8 -*
# """
# @Software : PyCharm
# @File : 0.py
# @Author : 喵
# @Time : 2021/09/29 22:39:29
# @Docs : 请求推栏战绩例子
# """
# import asyncio
# import time
# import traceback
# from time import gmtime
# import dufte
# import nonebot
# import matplotlib.pyplot as plt
# import src.Data.jxDatas as jxData
# from src.Data.database import DataBase as database
# from src.internal.tuilanapi import API as tuilanAPI
# from src.internal.jx3api import API as jx3API
# # 请求头
# jx3api = jx3API()
# api = tuilanAPI()
# 
# 
# class GetPersonInfo:
#     def __init__(self, role: str, server: str):
#         config = jxData.config
#         self.role = role
#         self.server = jxData.mainServer(server)
#         self.zone = jxData.mainZone(self.server)
#         self.database = database(config)
#         self.role_id = None
#         self.person_id = None
#         self.ts = None
#         self.xsk = None
#         self.role_name = None
# 
#     async def get_person_info(self):
#         try:
#             response = await jx3api.data_role_roleInfo(server=self.server, name=self.role)
#             print(response)
#             if response.code != 200:
#                 nonebot.logger.error("API接口role_roleInfo获取信息失败，请查看错误")
#                 return None
#             self.role_id = response.data['roleId']
# 
# 
#             # response = await api.role_indicator(role_id=self.role_id, server=self.server, zone=self.zone)
#             # if response.code != 0:
#             #     nonebot.logger.error("API接口Daily获取信息失败，请查看错误")
#             #     return None
#             # self.person_id = response.data['person_info']['person_id']
#             self.person_id = response.data['personId']
#             response = await api.mine_match_person9history(person_id=str(self.person_id), size=10, cursor=0)
#             if response.code != 0:
#                 nonebot.logger.error("API接口Daily获取信息失败，请查看错误")
#                 return None
#             return response.data
# 
#         except Exception as e:
#             nonebot.logger.error(e)
#             nonebot.logger.error("获取用户信息失败，请查看问题.")
#             traceback.print_exc()
#             return None
# 
#     async def get_Fig(self, data):
#         try:
#             if data is None:
#                 nonebot.logger.error("获取用户信息失败，请查看问题.")
#                 return None
#             if not data:
#                 nonebot.logger.error("获取用户信息失败，请查看问题.")
#                 return None
#             server = None
#             fig, ax = plt.subplots(figsize=(8, 9), facecolor='white', edgecolor='white')
#             plt.style.use(dufte.style)
#             ax.axis([0, 10, 0, 10])
#             ax.axis('off')
#             for x, y in reversed(list(enumerate(data))):
#                 self.role_name = y.get("role_name")
#                 server = y.get("server")
#                 pvp_type = y.get("pvp_type")
#                 avg_grade = y.get("avg_grade")
#                 total_mmr = y.get("total_mmr")
#                 won = y.get("won") is True and "胜利" or "失败"
#                 consume_time = time.strftime("%M分%S秒", gmtime(y.get("end_time") - y.get("start_time")))
#                 if time.altzone == 0:
#                     start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(y.get("start_time") + 28800))
#                 else:
#                     start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(y.get("start_time")))
#                 ax.text(0, x, f'{pvp_type}V{pvp_type}', verticalalignment='bottom', horizontalalignment='left',
#                         color='#404040')
#                 ax.text(1, x, f'{avg_grade}段局 ', verticalalignment='bottom', horizontalalignment='left',
#                         color='#404040')
#                 ax.text(2, x, f'{total_mmr}', verticalalignment='bottom', horizontalalignment='left', color='#404040')
#                 fontColor = won == "胜利" and 'blue' or 'red'
#                 ax.text(3, x, f'{won}', verticalalignment='bottom', horizontalalignment='left', color=fontColor)
#                 ax.text(4, x, f'{consume_time}', verticalalignment='bottom', horizontalalignment='left',
#                         color='#404040')
#                 ax.text(6, x, f'{start_time}', verticalalignment='bottom', horizontalalignment='left', color='#404040')
#             ax.set_title(server + " " + self.role_name + '  近10场JJC战绩', fontsize=19, color='#303030',
#                          fontweight="heavy",
#                          verticalalignment='top')
#             datetime = int(time.time())
#             plt.savefig(f"/tmp/role{datetime}.png")
#             return datetime
#         except Exception as e:
#             nonebot.logger.error(e)
#             nonebot.logger.error("获取用户信息失败，请查看报错.")
#             traceback.print_exc()
#             return None
# 
# person = GetPersonInfo('冻冻','唯满侠')
# f = asyncio.run(person.get_person_info())
# print(f)

# def apply_ascyn(func, args, callback):
#     """
#     func 函数的是处理的函数
#     args 表示的参数
#     callback 表示的函数处理完成后的 该执行的动作
#     """
#     result = func(*args)
#     callback(result)
#
#
# def add(x, y):
#     return x + y
#
#
# def print_result(result):
#     print(result)
#
#
# apply_ascyn(add, (2, 3), callback=print_result)
# -*- coding: utf-8 -*
# -*- coding: utf-8 -*-
import asyncio
import json
from typing import Optional

import nonebot
import websockets
from nonebot import get_bots
from nonebot.message import handle_event
from websockets.exceptions import ConnectionClosedError, ConnectionClosedOK
from websockets.legacy.client import WebSocketClientProtocol
from plugins.websocket._jx3_event import EventRister, WsData, WsNotice


class Jx3WebSocket(object):
    """
    jx3_api的ws链接封装
    """

    _instance = None
    connect: Optional[WebSocketClientProtocol] = None
    """ws链接"""
    is_connecting: bool = False
    """是否正在连接"""

    def __new__(cls, *args, **kwargs):
        """单例"""
        if not hasattr(cls, "_instance"):
            orig = super(Jx3WebSocket, cls)
            cls._instance = orig.__new__(cls)
        return cls._instance

    async def _task(self):
        """
        说明:
            循环等待ws接受并分发任务
        """
        try:
            while True:
                msg = await self.connect.recv()
                asyncio.create_task(self._handle_msg(msg))

        except ConnectionClosedOK:
            nonebot.logger.debug("<g>jx3api > ws链接已主动关闭！</g>")
            self.connect = None
            await self._raise_notice("jx3api > ws已正常关闭！")

        except ConnectionClosedError as e:
            nonebot.logger.error(f"<r>jx3api > ws链接异常关闭：{e.reason}</r>")
            # 自启动
            self.connect = None
            await self.init()

    async def _raise_notice(self, message: str):
        """
        说明:
            抛出ws通知事件给机器人

        参数:
            * `message`：通知内容
        """
        event = WsNotice(message=message)
        bots = get_bots()
        for _, one_bot in bots.items():
            await handle_event(one_bot, event)

    async def _handle_msg(self, message: str):
        """
        说明:
            处理收到的ws数据，分发给机器人
        """
        try:
            ws_obj = json.loads(message)
            data = WsData.parse_obj(ws_obj)
            event = EventRister.get_event(data)
            if event:
                nonebot.logger.debug(event.log)
                bots = get_bots()
                for _, one_bot in bots.items():
                    await handle_event(one_bot, event)
            else:
                nonebot.logger.error(f"<r>未知的ws消息类型：{data}</r>")
        except Exception:
            nonebot.logger.error(f"未知ws消息：<g>{ws_obj}</g>")

    async def init(self) -> Optional[bool]:
        """
        说明:
            初始化实例并连接ws服务器
        """
        if self.connect or self.is_connecting:
            return None

        ws_path = 'wss://socket.nicemoe.cn'
        ws_token = "5f2143314ebbec94b7aa80f7fd295856b03e567358a4f966fcbe597949e985e8"
        if ws_token is None:
            ws_token = ""
        headers = {"token": ws_token}
        nonebot.logger.debug(f"<g>ws_server</g> | 正在链接jx3api的ws服务器：{ws_path}")
        print(f"<g>ws_server</g> | 正在链接jx3api的ws服务器：{ws_path}")
        self.is_connecting = True
        for i in range(1, 101):
            try:
                nonebot.logger.debug(f"<g>ws_server</g> | 正在开始第 {i} 次尝试")
                print(f"<g>ws_server</g> | 正在开始第 {i} 次尝试")
                self.connect = await websockets.connect(
                    uri=ws_path,
                    extra_headers=headers,
                    ping_interval=20,
                    ping_timeout=20,
                    close_timeout=10,
                )
                asyncio.create_task(self._task())
                nonebot.logger.debug("<g>ws_server</g> | ws连接成功！")
                print("<g>ws_server</g> | ws连接成功！")
                # await self._raise_notice("jx3api > ws已连接！")
                break
            except Exception as e:
                nonebot.logger.error(f"<r>链接到ws服务器时发生错误：{str(e)}</r>")
                await asyncio.sleep(1)

        self.is_connecting = False
        if not self.connect:
            # 未连接成功，发送消息给bot，如果有
            self.connect = None
            await self._raise_notice("jx3api > ws服务器连接失败，请查看日志或者重连。")
            return False
        return True

    async def close(self):
        """关闭ws链接"""
        if self.connect:
            await self.connect.close()
            self.connect = None

    @property
    def closed(self) -> bool:
        """ws是否关闭"""
        if self.connect:
            return self.connect.closed
        return True


ws_client = Jx3WebSocket()
x = asyncio.run(ws_client.init())  # 初始化
asyncio.run(ws_client.__new__(x,''))

# 关闭连接
"""
ws客户端，用于连接jx3api的ws服务器.

他在init连接到ws服务器后，在接受到的ws消息自动实例化为event事件并处理。
在ws服务器关闭后，会自动重连。

使用方式：
```
>>>await ws_client.init() # 初始化
>>>ws_client.closed # ws是否关闭
>>>await ws_client.close() # 关闭连接
```
"""
