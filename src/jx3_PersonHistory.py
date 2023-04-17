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
import matplotlib.pyplot as plt
import src.Data.jxDatas as jxData
from src.Data.database import DataBase as database
from src.internal.tuilanapi import API as tuilanAPI
from src.internal.jx3api import API as jx3API

# 请求头
jx3api = jx3API()
api = tuilanAPI()


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

    async def get_person_info(self):
        try:
            response = await jx3api.data_role_roleInfo(server=self.server, name=self.role)
            print(response)
            if response.code != 200:
                nonebot.logger.error("API接口role_roleInfo获取信息失败，请查看错误")
                return None
            self.role_id = response.data['roleId']
            self.person_id = response.data['personId']
            response = await api.role_indicator(role_id=self.role_id, server=self.server, zone=self.zone)
            if response.code != 0:
                nonebot.logger.error("API接口Daily获取信息失败，请查看错误")
                return None

            self.person_id = response.data['person_info']['person_id']
            response = await api.mine_match_person9history(person_id=str(self.person_id), size=10, cursor=0)
            print(response)
            if response.code != 0:
                nonebot.logger.error("API接口Daily获取信息失败，请查看错误")
                return None
            return response.data

        except Exception as e:
            nonebot.logger.error(e)
            nonebot.logger.error("获取用户信息失败，请查看问题.")
            traceback.print_exc()
            return None

    async def get_Fig(self, data):
        try:
            if data is None:
                nonebot.logger.error("获取用户信息失败，请查看问题.")
                return None
            if not data:
                nonebot.logger.error("获取用户信息失败，请查看问题.")
                return None
            server = None
            fig, ax = plt.subplots(figsize=(8, 9), facecolor='white', edgecolor='white')
            plt.style.use(dufte.style)
            ax.axis([0, 10, 0, 10])
            ax.axis('off')
            for x, y in reversed(list(enumerate(data))):
                self.role_name = y.get("role_name")
                server = y.get("server")
                pvp_type = y.get("pvp_type")
                avg_grade = y.get("avg_grade")
                total_mmr = y.get("total_mmr")
                won = y.get("won") is True and "胜利" or "失败"
                consume_time = time.strftime("%M分%S秒", gmtime(y.get("end_time") - y.get("start_time")))
                if time.altzone == 0:
                    start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(y.get("start_time") + 28800))
                else:
                    start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(y.get("start_time")))
                ax.text(0, x, f'{pvp_type}V{pvp_type}', verticalalignment='bottom', horizontalalignment='left',
                        color='#404040')
                ax.text(1, x, f'{avg_grade}段局 ', verticalalignment='bottom', horizontalalignment='left',
                        color='#404040')
                ax.text(2, x, f'{total_mmr}', verticalalignment='bottom', horizontalalignment='left', color='#404040')
                fontColor = won == "胜利" and 'blue' or 'red'
                ax.text(3, x, f'{won}', verticalalignment='bottom', horizontalalignment='left', color=fontColor)
                ax.text(4, x, f'{consume_time}', verticalalignment='bottom', horizontalalignment='left',
                        color='#404040')
                ax.text(6, x, f'{start_time}', verticalalignment='bottom', horizontalalignment='left', color='#404040')
            ax.set_title(server + " " + self.role_name + '  近10场JJC战绩', fontsize=19, color='#303030',
                         fontweight="heavy",
                         verticalalignment='top')
            datetime = int(time.time())
            plt.savefig(f"/tmp/role{datetime}.png")
            return datetime
        except Exception as e:
            nonebot.logger.error(e)
            nonebot.logger.error("获取用户信息失败，请查看报错.")
            traceback.print_exc()
            return None

# person_infomation = GetPersonInfo('潇潇凌千烨','双梦')
# asyncio.run(person_infomation.get_person_info())
