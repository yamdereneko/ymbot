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

# 请求头

api = API()
matplotlib.rc("font", family='PingFang HK')


class GetPersonInfo:
    def __init__(self, role: str, server: str):
        config = jxData.config
        self.role = role
        self.server = jxData.mainServer(server)
        self.zone = jxData.mainZone(self.server)
        self.database = database(config)
        self.role_id = None
        self.person_id = None
        self.ts = None
        self.xsk = None
        self.role_name = None

    async def main(self):
        try:
            sql = "select id from InfoCache where name='%s'" % self.role
            await self.database.connect()
            role_id_info = await self.database.fetchone(sql)

            if role_id_info is None:
                nonebot.logger.error("获取用户id失败")
                return None
            self.role_id = str(role_id_info.get("id"))

            response = await api.role_indicator(role_id=self.role_id, server=self.server, zone=self.zone)
            if response.code != 0:
                nonebot.logger.error("API接口Daily获取信息失败，请查看错误")
                return None
            self.person_id = response.data['person_info']['person_id']

            response = await api.mine_match_person9history(person_id=str(self.person_id), size=10, cursor=0)
            if response.code != 0:
                nonebot.logger.error("API接口Daily获取信息失败，请查看错误")
                return None

            for _ in response.data:
                res = await api.cc_mine_match_detail(match_id=_['match_id'])
                if res.code == 0:
                    # for info in res.data["team1"]["players_info"]:
                    #     print(info["role_name"])
                    # print('***' * 30)
                    print(res.data)
        except Exception as e:
            nonebot.logger.error(e)
            nonebot.logger.error("获取用户信息失败，请查看问题.")
            traceback.print_exc()
            return None
personInfo = GetPersonInfo("时南星","姨妈")
asyncio.run(personInfo.main())