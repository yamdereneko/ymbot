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
import matplotlib.pyplot as plt
import nonebot
import src.Data.jxDatas as jxData
import dufte
from src.internal.tuilanapi import API
from time import gmtime
from src.Data.database import DataBase as database

# 请求头
api = API()


class GetPersonRecord:
    def __init__(self, role: str, server: str):
        config = jxData.config
        self.role = role
        self.server = jxData.mainServer(server)
        self.zone = jxData.mainZone(self.server)
        self.database = database(config)
        self.role_id = None
        self.global_role_id = None

    async def get_person_record(self):
        """
        说明：
            。丛Mysql数据库中获取角色的role_id

        参数：
            * `InfoCache`： 表名
            * `role`: 角色名
        """
        sql = "select id from InfoCache where name='%s'" % self.role
        await self.database.connect()
        role_id_dict = await self.database.fetchone(sql)
        if role_id_dict is None:
            nonebot.logger.error(self.role + "得role_id未得到，将返回None")
            return None
        self.role_id = str(role_id_dict.get("id"))

        response = await api.role_indicator(role_id=self.role_id, server=self.server, zone=self.zone)
        if response.code != 0:
            nonebot.logger.error("API接口Daily获取信息失败，请查看错误")
            return None
        self.global_role_id = response.data["role_info"]["global_role_id"]

        response = await api.cc_mine_match_history(global_role_id=self.global_role_id, size=10, cursor=0)
        if response.code != 0:
            nonebot.logger.error("API接口Daily获取信息失败，请查看错误")
            return None
        record = response.data
        return record

    async def get_person_record_figure(self, data):
        fig, ax = plt.subplots(figsize=(8, 9), facecolor='white', edgecolor='white')
        plt.style.use(dufte.style)
        ax.axis([0, 10, 0, 10])
        ax.set_title("斗转星移  " + self.role + '  近10场JJC战绩', fontsize=19, color='#303030', fontweight="heavy",
                     verticalalignment='top')
        ax.axis('off')
        for x, y in enumerate(data):
            floor = len(data) - x - 1
            pvp_type = y.get("pvp_type")
            avg_grade = y.get("avg_grade")
            total_mmr = y.get("total_mmr")
            won = y.get("won") is True and "胜利" or "失败"
            consume_time = time.strftime("%M分%S秒", gmtime(y.get("end_time") - y.get("start_time")))
            start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(y.get("start_time")))
            ax.text(0, floor, f'{pvp_type}V{pvp_type}', verticalalignment='bottom', horizontalalignment='left',
                    color='#404040')
            ax.text(1, floor, f'{avg_grade}段局 ', verticalalignment='bottom', horizontalalignment='left',
                    color='#404040')
            ax.text(2, floor, f'{total_mmr}', verticalalignment='bottom', horizontalalignment='left', color='#404040')
            font_color = won == "胜利" and 'blue' or 'red'
            ax.text(3, floor, f'{won}', verticalalignment='bottom', horizontalalignment='left', color=font_color)
            ax.text(4, floor, f'{consume_time}', verticalalignment='bottom', horizontalalignment='left',
                    color='#404040')
            ax.text(6, floor, f'{start_time}', verticalalignment='bottom', horizontalalignment='left', color='#404040')
        datetime = int(time.time())
        plt.savefig(f"/tmp/record{datetime}.png")
        return datetime
