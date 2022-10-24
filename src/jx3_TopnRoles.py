# -*- coding: utf-8 -*
"""
@Software : PyCharm
@File : 0.py
@Author : 喵
@Time : 2021/09/29 22:39:29
@Docs : 请求推栏战绩例子
"""
import asyncio
import nonebot
import src.Data.jxDatas as jxData
from src.internal.tuilanapi import API as tuilanAPI
from src.internal.jx3api import API as jx3API


# 请求头
api = tuilanAPI()
jx3api = jx3API()


class GetTopnRoles:
    def __init__(self, server: str):
        self.server = jxData.mainServer(server)
        self.zone = jxData.mainZone(self.server)

    async def get_topn_data(self):
        """
        说明：
            。丛Mysql数据库中获取角色的role_id

        参数：
            * `InfoCache`： 表名
            * `role`: 角色名
        """
        response = await api.user_list9jx39topn9roles9info(cursor=0, size=1000, gameVersion=0, zoneName=self.zone,
                                                           serverName=self.server, forceId=24)
        if response.data is []:
            nonebot.logger.error("API接口user_list9jx39topn9roles9info获取信息失败，请查看错误")
            return None
        print(response)
        print(response.data)


topn = GetTopnRoles('姨妈')
asyncio.run(topn.get_topn_data())
