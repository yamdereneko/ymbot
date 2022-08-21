# -*- coding: utf-8 -*

"""
@Software : PyCharm
@File : 0.py
@Author : 喵
@Time : 2021/09/29 22:39:29
@Docs : 请求推栏战绩例子
"""
import datetime
import os
import matplotlib
import matplotlib.pyplot as plt
import nonebot
import requests
import json
from src.Data.database import DataBase as database
import src.Data.jxDatas as jxData
import dufte

# 请求头
headers = jxData.headers
matplotlib.rc("font", family='PingFang HK')


class GetDaily:
    def __init__(self, server: str = "姨妈", daily_next: int = 0):
        config = jxData.config
        self.server = jxData.mainServer(server)
        self.zone = jxData.mainZone(self.server)
        self.daily_next = daily_next
        self.Pool = "jx3_Daily"
        self.database = database(config)
        if self.daily_next is None:
            self.daily_next = 0
        self.day = (datetime.datetime.now() + datetime.timedelta(days=+self.daily_next)).strftime("%Y-%m-%d")

    async def Get_Daily(self):
        param = {'server': self.server, 'next': self.daily_next}
        daily_info = requests.get(url="https://www.jx3api.com/app/daily", data=json.dumps(param)).json()
        if daily_info.get("code") != 200:
            nonebot.logger.error("API接口Daily获取信息失败，请查看错误")
            return None
        return daily_info

    async def SyncDateConnectPool(self):
        try:
            daily_info = await self.Get_Daily()
            await self.database.connect()
            if daily_info is None:
                nonebot.logger.error("同步数据至连接池异常:" + self.Pool)
                return None
            date = daily_info.get("data").get("date")
            week = daily_info.get("data").get("week")
            war = daily_info.get("data").get("war")
            battle = daily_info.get("data").get("battle")
            camp = daily_info.get("data").get("camp")
            prestige = ":".join(daily_info.get("data").get("prestige"))
            relief = daily_info.get("data").get("relief")
            team = ":".join(daily_info.get("data").get("team"))
            draw = daily_info.get("data").get("draw")
            sql = "insert into jx3_Daily values ('%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                date, week, war, battle, camp, prestige, relief, team, draw)
            res = await self.database.execute(sql)
            return True if res else None
        except Exception as e:
            nonebot.logger.error(e)
            return None

    async def QueryTodayDaily(self):
        sql = "select * from jx3_Daily where date='%s'" % self.day
        await self.database.connect()
        res = await self.database.fetchone(sql)
        if res is None:
            nonebot.logger.warning("连接池中不存在该数据，将进行数据同步...")
            syncResult = await self.SyncDateConnectPool()
            if syncResult is None:
                nonebot.logger.error("连接池同步失败...")
                return None
            res = await self.database.fetchone(sql)
        return res
        # 获取门派每周个数趋势图，返回DICT结果，并打印趋势图至相关目录

    async def QueryDailyFigure(self):
        if os.path.exists(f"/tmp/daily{self.server}{self.day}.png"):
            nonebot.logger.info(self.day + "日常图已经存在")
            return True
        else:
            data = await self.QueryTodayDaily()
            if data is None:
                nonebot.logger.error(self.day + self.server + "日常未得到，将返回None")
                return None
            fig, ax = plt.subplots(figsize=(8, 9), facecolor='white', edgecolor='white')
            plt.style.use(dufte.style)
            ax.axis([0, 2, 0, 4])
            ax.set_title(f'今天是{self.day},星期{data.get("week")}', fontsize=19, color='#303030', fontweight="heavy",
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
            ax.text(0.1, 1.5, f'「公共日常周常」:{data.get("team").split(":")[0]}', verticalalignment='bottom',
                    horizontalalignment='left', color='#404040')
            ax.text(0.1, 1, f'「5人周常副本」:{data.get("team").split(":")[1]}', verticalalignment='bottom',
                    horizontalalignment='left', color='#404040')
            ax.text(0.1, 0.5, f'「10人周常副本」:{data.get("team").split(":")[2]}', verticalalignment='bottom',
                    horizontalalignment='left', color='#404040')
            beautifulWoman = data.get("draw") is None and '无' or data.get("draw")
            ax.text(0.1, 0, f'「美人图」:{beautifulWoman}', verticalalignment='bottom', horizontalalignment='left',
                    color='#404040')
            plt.savefig(f"/tmp/daily{self.server}{self.daily_next}.png")
            return True

    async def QueryWeeklyDaily(self):
        param = {"count": 7}
        daily_info = requests.get(url="https://www.jx3api.com/app/calculate", data=json.dumps(param)).json()
        if daily_info.get("code") != 200:
            nonebot.logger.error("API接口Daily获取信息失败，请查看错误")
            return None
        return daily_info