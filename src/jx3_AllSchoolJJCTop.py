# -*- coding: utf-8 -*-
import asyncio
import os
import matplotlib
import matplotlib.pyplot as plt
import nonebot
import src.Data.jxDatas as jxData
from src.Data.database import DataBase as database
import dufte
from matplotlib.ticker import MultipleLocator


class GetAllSchool:
    def __init__(self, table: str):
        config = jxData.config
        self.table = table
        self.database = database(config)

    # 获取门派每周个数趋势图，返回DICT结果，并打印趋势图至相关目录
    async def get_JJCWeeklyAllSchoolRecord(self):
        plt.style.use(dufte.style)
        plt.figure(figsize=(28, 18), dpi=80)
        school_list = ['蓬莱', '苍云', '冰心','莫问','田螺']
        for school in school_list:
            school = jxData.school(school)
            sql = "select week,%s from %s " % (school, self.table)
            await self.database.connect()
            res = await self.database.fetchall(sql)
            x = []
            y = []
            for data in res:
                x.append(data["week"])
                y.append(data[school])
                plt.text(data["week"], data[school], '%.0f' % data[school], ha="center", va="bottom")
            plt.plot(x, y, marker='o', label=school)
            plt.xlabel(u'周数')
        plt.legend(fontsize=12)
        plt.show()
        # plt.savefig(f"/tmp/schoolTop{self.school}.png")


allSchool = GetAllSchool('JJC_rank_weekly')
asyncio.run(allSchool.get_JJCWeeklyAllSchoolRecord())
