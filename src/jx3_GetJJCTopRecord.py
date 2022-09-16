import os
import time

import matplotlib
import matplotlib.pyplot as plt
import nonebot
import src.Data.jxDatas as jxData
from src.Data.database import DataBase as database
import dufte
from matplotlib.ticker import MultipleLocator


class GetJJCTopInfo:
    def __init__(self, table: str, weekly: int, school: str):
        self.table = table
        self.weekly = weekly
        self.school = jxData.school(school)
        config = jxData.config
        self.database = database(config)

    # 获取每周每个门派趋势图，返回DICT结果，并打印趋势图至相关目录
    async def get_JJCWeeklyRecord(self):
        sql = "select * from %s where week='%s'" % (self.table, self.weekly)
        await self.database.connect()
        res = await self.database.fetchone(sql)
        if res is None:
            return None
        tuples = sorted(res.items(), key=lambda x: x[1], reverse=True)
        res_total = dict(tuples)
        del res_total["week"]
        return res_total

    async def get_JJCWeeklyRecord_figure(self, data: dict):
        plt.style.use(dufte.style)
        fig, ax = plt.subplots(figsize=(22, 10), facecolor='white', edgecolor='white')
        ax.set_title("推栏" + str(self.weekly) + "周JJC排名", fontsize=18)
        ax.yaxis.set_major_locator(MultipleLocator(5))
        for x, y in data.items():
            plt.text(x, y, '%.0f' % y, ha="center", va="bottom")
        bar_width = 0.3
        ax.bar(data.keys(), data.values(), width=bar_width)
        datetime = int(time.time())
        plt.savefig(f"/tmp/top{datetime}.png")
        return datetime

    # 获取门派每周个数趋势图，返回DICT结果，并打印趋势图至相关目录
    async def get_JJCWeeklySchoolRecord(self):
        sql = "select week,%s from %s " % (self.school, self.table)
        await self.database.connect()
        res = await self.database.fetchall(sql)
        return res

    async def get_JJCWeeklySchoolRecord_figure(self, data):
        plt.style.use(dufte.style)
        fig, ax = plt.subplots(figsize=(22, 10), facecolor='white', edgecolor='white')
        x = []
        y = []
        ax.set_xlabel('周', fontsize=16)
        ax.set_ylabel('数量', fontsize=16)
        ax.set_title(f"推栏" + str(self.school) + f"JJC趋势图", fontsize=18)
        for data in data:
            x.append(data["week"])
            y.append(data[self.school])
            plt.text(data["week"], data[self.school], '%.0f' % data[self.school], ha="center", va="bottom")
        ax.plot(x, y, "o-", color='#607d8b')
        datetime = int(time.time())
        plt.savefig(f"/tmp/SchoolTop{datetime}.png")
        nonebot.logger.info(self.school + "JJC趋势图重新创建")
        return datetime
