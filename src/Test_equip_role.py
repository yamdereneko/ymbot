# -*- coding: utf-8 -*
"""
@Software : PyCharm
@File : 0.py
@Author : 喵
@Time : 2021/09/29 22:39:29
@Docs : 请求推栏战绩例子
"""
import asyncio
import time
import traceback
from time import gmtime
import dufte
import nonebot
import matplotlib
import matplotlib.pyplot as plt
import src.Data.jxDatas as jxData
from src.Data.database import DataBase as database
from src.internal.tuilanapi import API
from src.internal.jx3api import API as jx3API
from rich import print
from rich.columns import Columns

# 请求头

api = API()
jx3api = jx3API()


class GetRoleEquip:
    def __init__(self, role: str, server: str):
        config = jxData.config
        self.role = role
        self.server = jxData.mainServer(server)
        self.zone = jxData.mainZone(self.server)
        self.database = database(config)
        self.role_id = None
        self.person_id = None
        self.role_name = None
        self.globalRoleId = None

    async def equips(self):
        try:
            response = await jx3api.data_role_roleInfo(server=self.server, name=self.role)
            if response.code != 200:
                nonebot.logger.error("API接口role_roleInfo获取信息失败，请查看错误")
                return None
            print(response)
            self.globalRoleId = response.data["globalRoleId"]
            self.role_id = response.data["roleId"]
            response = await api.role_indicator(role_id=self.role_id, server=self.server, zone=self.zone)
            if response.code != 0:
                nonebot.logger.error("API接口role_indicator获取信息失败，请查看错误")
                return None
            print(response)

            self.person_id = response.data['person_info']['person_id']

            # response = await api.mine_match_person9history(person_id=str(self.person_id), size=10, cursor=0)
            # if response.code != 0:
            #     nonebot.logger.error("API接口Daily获取信息失败，请查看错误")
            #     return None
            # print(response.data)
            # # self.role_id = response.data[0]["role_id"]
            # self.server = response.data[0]["server"]
            # self.zone = response.data[0]["zone"]
            # print(response)

            print('==' * 50)
            response = await api.mine_equip_get9role9equip(game_role_id=self.role_id, server=self.server,
                                                           zone=self.zone)
            if response.code != 0:
                nonebot.logger.error("API接口mine_equip_get9role9equip获取信息失败，请查看错误")
                return None
            return response.data

        except Exception as e:
            nonebot.logger.error(e)
            nonebot.logger.error("获取用户信息失败，请查看问题.")
            traceback.print_exc()
            return None

    async def get_Fig(self):
        try:
            data = await self.equips()
            print(data)
            print('==' * 30)
            print(data)
            equip = data['Equips']
            for _ in equip:
                print(_['Name'])
                print(_['Quality'])

            kungfu = data['Kungfu']
            print(kungfu)

            PersonalPanel = data['PersonalPanel']
            print(PersonalPanel)

            TotalEquipsScore = data['TotalEquipsScore']
            print(TotalEquipsScore)
        except Exception as e:
            nonebot.logger.error(e)
            nonebot.logger.error("获取用户信息失败，请查看报错.")
            traceback.print_exc()
            return None


role_equip = GetRoleEquip("时今朝", "龙虎")
asyncio.run(role_equip.get_Fig())
