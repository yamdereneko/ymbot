# -*- coding: utf-8 -*

"""
@Software : PyCharm
@File : 0.py
@Author : 喵
@Time : 2021/09/29 22:39:29
@Docs : 请求推栏战绩例子
"""
import asyncio
from functools import partial
import time
import matplotlib.pyplot as plt
import nonebot
import src.Data.jxDatas as jxData
import dufte
from src.internal.tuilanapi import API as tuilanAPI
from src.internal.jx3api import API as jx3API
from time import gmtime
from src.Data.database import DataBase as database

# 请求头
api = tuilanAPI()
jx3api = jx3API()


class GetPersonRecord:
    def __init__(self, role: str, server: str):
        config = jxData.config
        self.role = role
        self.server = jxData.mainServer(server)
        self.zone = jxData.mainZone(self.server)
        self.database = database(config)
        self.global_role_id = None

    async def get_person_record(self):
        response = await jx3api.data_role_roleInfo(server=self.server, name=self.role)
        if response.code != 200:
            nonebot.logger.error("API接口role_roleInfo获取信息失败，请查看错误")
            return None
        self.global_role_id = response.data['globalRoleId']

        response = await api.cc_mine_match_history(global_role_id=self.global_role_id, size=10, cursor=0)
        if response.data is []:
            nonebot.logger.error("API接口cc_mine_match_history获取信息失败，请查看错误")
            return None
        [print(_) for _ in response.data]
        return response.data

    async def get_person_record_figure(self):
        data = await self.get_person_record()
        for element in data:
            team1 = {}
            team2 = {}
            match_id = element.get("match_id")
            response = await api.cc_mine_match_detail(match_id=match_id)
            for team_info in response.data.get("team1").get("players_info"):
                team1[team_info.get("role_name")] = team_info.get("kungfu")
            for team_info in response.data.get("team2").get("players_info"):
                team2[team_info.get("role_name")] = team_info.get("kungfu")
            print(team1)
            print(team2)
            for _ in team1.values():
                print(_)
            print("**" * 20)


record = GetPersonRecord("小疏竹", "姨妈")
total = asyncio.run(record.get_person_record_figure())
