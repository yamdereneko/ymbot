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
        """
        说明：
            。丛Mysql数据库中获取角色的role_id

        参数：
            * `InfoCache`： 表名
            * `role`: 角色名
        """
        response = await jx3api.data_role_roleInfo(server=self.server, name=self.role)
        print(response)
        if response.code != 200:
            nonebot.logger.error("API接口role_roleInfo获取信息失败，请查看错误")
            return None
        self.global_role_id = response.data['globalRoleId']

        response = await api.cc_mine_match_history(global_role_id=self.global_role_id, size=10, cursor=0)
        print(response)
        if response.data is []:
            nonebot.logger.error("API接口cc_mine_match_history获取信息失败，请查看错误")
            return None

        for element in response.data:
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
        return response.data

    async def get_person_record_figure(self, data):
        fig, ax = plt.subplots(figsize=(8, 9), facecolor='white', edgecolor='white')
        plt.style.use(dufte.style)
        ax.axis([0, 10, 0, 10])

        ax.set_title(f"{data[0]['server']}  " + self.role + '  近10场JJC战绩', fontsize=19, color='#303030',
                     fontweight="heavy",
                     verticalalignment='top')
        ax.axis('off')
        for x, y in enumerate(data):
            floor = len(data) - x - 1
            pvp_type = y.get("pvp_type")
            avg_grade = y.get("avg_grade")
            total_mmr = y.get("total_mmr")
            kungfu = jxData.school(y.get("kungfu"))
            won = y.get("won") is True and "胜利" or "失败"
            consume_time = time.strftime("%M分%S秒", gmtime(y.get("end_time") - y.get("start_time")))
            if time.altzone == 0:
                start_time = time.strftime("%m-%d %H:%M", time.localtime(y.get("start_time") + 28800))
            else:
                start_time = time.strftime("%m-%d %H:%M", time.localtime(y.get("start_time")))

            ax.text(0.5, floor, f'{pvp_type}V{pvp_type}', verticalalignment='bottom', horizontalalignment='left',
                    color='#404040')
            ax.text(1.5, floor, f'{avg_grade}段局 ', verticalalignment='bottom', horizontalalignment='left',
                    color='#404040')
            ax.text(2.5, floor, f'{total_mmr}', verticalalignment='bottom', horizontalalignment='left', color='#404040')
            font_color = won == "胜利" and 'blue' or 'red'
            ax.text(3.5, floor, f'{won}', verticalalignment='bottom', horizontalalignment='left', color=font_color)
            ax.text(4.5, floor, f'{consume_time}', verticalalignment='bottom', horizontalalignment='left',
                    color='#404040')
            ax.text(6, floor, f'{kungfu}', verticalalignment='bottom', horizontalalignment='left',
                    color='#404040')
            ax.text(7, floor, f'{start_time}', verticalalignment='bottom', horizontalalignment='left', color='#404040')
        datetime = int(time.time())
        plt.savefig(f"/tmp/record{datetime}.png")
        return datetime


record = GetPersonRecord("小疏竹", "姨妈")
total = asyncio.run(record.get_person_record())
