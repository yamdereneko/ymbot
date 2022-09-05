import os
import matplotlib
import matplotlib.pyplot as plt
import nonebot
import src.Data.jxDatas as jxData
from src.Data.database import DataBase as database
import dufte
from matplotlib.ticker import MultipleLocator

matplotlib.rc("font", family='PingFang HK')


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

        plt.style.use(dufte.style)

        fig, ax = plt.subplots(figsize=(22, 10), facecolor='white', edgecolor='white')
        ax.set_title("推栏" + str(self.weekly) + "周JJC前200排名", fontsize=18)
        ax.yaxis.set_major_locator(MultipleLocator(5))
        for x, y in res_total.items():
            plt.text(x, y, '%.0f' % y, ha="center", va="bottom")
        bar_width = 0.3
        ax.bar(res_total.keys(), res_total.values(), width=bar_width)
        plt.savefig(f"/tmp/top{self.table}.png")
        return res_total


    # 获取门派每周个数趋势图，返回DICT结果，并打印趋势图至相关目录
    async def get_JJCWeeklySchoolRecord(self):
        sql = "select week,%s from %s " % (self.school, self.table)
        await self.database.connect()
        res = await self.database.fetchall(sql)
        if os.path.exists(f"/tmp/top{self.school}.png"):
            nonebot.logger.info(self.school + "JJC趋势图已经存在")
            return None
        else:
            plt.style.use(dufte.style)
            fig, ax = plt.subplots(figsize=(22, 10), facecolor='white', edgecolor='white')
            x = []
            y = []
            ax.set_xlabel('周', fontsize=16)
            ax.set_ylabel('数量', fontsize=16)
            ax.set_title(f"推栏" + str(self.school) + f"JJC{self.table}趋势图", fontsize=18)
            for data in res:
                x.append(data["week"])
                y.append(data[self.school])
                plt.text(data["week"], data[self.school], '%.0f' % data[self.school], ha="center", va="bottom")
            ax.plot(x, y, "o-", color='#607d8b')
            plt.savefig(f"/tmp/schoolTop{self.school}.png")
            nonebot.logger.info(self.school + "JJC趋势图重新创建")
        return res
