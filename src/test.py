# -*- coding: utf-8 -*
"""
@Software : PyCharm
@File : 0.py
@Author : 喵
@Time : 2021/09/29 22:39:29
@Docs : 请求推栏战绩例子
"""
import asyncio
import datetime
import time
import traceback
import random
import urllib
from time import gmtime
import dufte
import nonebot
import matplotlib
import matplotlib.pyplot as plt
import pytz
import src.Data.jxDatas as jxData
from src.Data.database import DataBase as database
from src.internal.tuilanapi import API
from matplotlib import font_manager
import numpy as np
import pandas as pd
import networkx as nx

import asyncio
import websockets
import websockets.exceptions
from src.Data.jxDatas import jx3api_ticket

import re

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



#
#
aa = {'霸刀': 7, '少林': 7, '补天': 4, '蓬莱': 8, '紫霞': 15, '藏剑': 9, '明教': 6, '云裳': 18, '花间': 11, '丐帮': 5, '凌雪': 0, '田螺': 3, '惊羽': 6, '相知': 13, '胎虚': 7, '苍云': 7, '天策': 8, '无方': 17, '灵素': 16, '冰心': 2, '毒经': 3, '衍天': 0, '莫问': 4, '离经': 9, '凌雪阁': 7, '衍天宗': 8}
bb = {'霸刀': 3, '少林': 2, '补天': 0, '蓬莱': 3, '紫霞': 3, '藏剑': 3, '明教': 3, '云裳': 3, '花间': 3, '丐帮': 1, '凌雪': 0, '田螺': 0,
       '惊羽': 1, '相知': 3, '胎虚': 2, '苍云': 2, '天策': 1, '无方': 5, '灵素': 6, '冰心': 0, '毒经': 2, '衍天': 0, '莫问': 0, '离经': 1,
       '凌雪阁': 2, '衍天宗': 1}
cc = {'霸刀': 3, '少林': 5, '补天': 3, '蓬莱': 4, '紫霞': 8, '藏剑': 3, '明教': 3, '云裳': 7, '花间': 6, '丐帮': 3, '凌雪': 0, '田螺': 0,
       '惊羽': 3, '相知': 4, '胎虚': 6, '苍云': 3, '天策': 5, '无方': 10, '灵素': 11, '冰心': 1, '毒经': 2, '衍天': 0, '莫问': 1, '离经': 2,
       '凌雪阁': 4, '衍天宗': 3}
print(sum(cc.values()))
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