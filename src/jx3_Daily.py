# -*- coding: utf-8 -*-

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
from src.internal.jx3api import API

# 请求头
api = API()


class GetDaily:
    def __init__(self, server: str = "姨妈", daily_next: int = 0):
        self.server = jxData.mainServer(server)
        self.zone = jxData.mainZone(self.server)
        self.daily_next = daily_next
        if self.daily_next is None:
            self.daily_next = 0

    async def get_daily(self):
        response = await api.data_active_current(server=self.server, next=self.daily_next)
        if response.code != 200:
            nonebot.logger.error("API接口Daily获取信息失败，请查看错误")
            return None
        return response.data

    async def query_daily_figure(self, data):
        if data is None:
            nonebot.logger.error(self.server + "日常未得到，将返回None")
            return None
        team = ":".join(data.get("team"))
        fig, ax = plt.subplots(figsize=(8, 9), facecolor='white', edgecolor='white')
        plt.style.use(dufte.style)
        ax.axis([0, 2, 0, 4])
        ax.set_title(f'今天是{data.get("date")},星期{data.get("week")}', fontsize=19, color='#303030', fontweight="heavy",
                     verticalalignment='top')
        ax.axis('off')
        ax.text(0.1, 3.5, f'「大战」:{data.get("war")}', verticalalignment='bottom', horizontalalignment='left',
                color='#404040')
        ax.text(0.1, 3, f'「战场」:{data.get("battle")}', verticalalignment='bottom', horizontalalignment='left',
                color='#404040')
        ax.text(0.1, 2.5, f'「阵营日常」:{data.get("camp")}', verticalalignment='bottom', horizontalalignment='left',
                color='#404040')
        ax.text(0.1, 2, f'「驰援」:{data.get("relief")}', verticalalignment='bottom', horizontalalignment='left',
                color='#404040')
        ax.text(0.1, 1.5, f'「公共日常周常」:{team.split(":")[0]}', verticalalignment='bottom',
                horizontalalignment='left', color='#404040')
        ax.text(0.1, 1, f'「5人周常副本」:{team.split(":")[1]}', verticalalignment='bottom',
                horizontalalignment='left', color='#404040')
        ax.text(0.1, 0.5, f'「10人周常副本」:{team.split(":")[2]}', verticalalignment='bottom',
                horizontalalignment='left', color='#404040')
        beautifulWoman = data.get("draw") is None and '无' or data.get("draw")
        ax.text(0.1, 0, f'「美人图」:{beautifulWoman}', verticalalignment='bottom', horizontalalignment='left',
                color='#404040')
        datetime = int(time.time())
        plt.savefig(f"/tmp/daily{datetime}.png")
        return datetime

    async def query_weekly_daily(self):
        response = await api.app_calculate(count=7)
        if response.code != 200:
            nonebot.logger.error("API接口Daily获取信息失败，请查看错误")
            return None
        return response.data

