# -*- coding: utf-8 -*

"""
@Software : PyCharm
@File : 0.py
@Author : 喵
@Time : 2021/09/29 22:39:29
@Docs : 请求推栏战绩例子
"""
import time
from time import gmtime
import matplotlib
import matplotlib.pyplot as plt
import nonebot
import src.Data.jxDatas as jxData
from src.Data.database import DataBase as database
import requests
import json
import dufte

# 请求头
headers = jxData.headers
matplotlib.rc("font", family='PingFang HK')


class GetPersonRecord:
    def __init__(self, role: str, server: str):
        config = jxData.config
        self.role = role
        self.server = jxData.mainServer(server)
        self.zone = jxData.mainZone(self.server)
        self.database = database(config)
        self.role_id = None
        self.ts = None
        self.xsk = None
        self.global_role_id = None

    async def get_xsk(self, data=None):
        data = json.dumps(data)
        res = requests.post(url="https://www.jx3api.com/token/calculate", data=data).json()
        return res['data']['ts'], res['data']['sk']

    async def get_global_role_id(self):
        # 准备请求参数
        param = {'role_id': self.role_id, 'server': self.server, "zone": self.zone}
        self.ts, self.xsk = await self.get_xsk(param)
        param['ts'] = self.ts
        param = json.dumps(param).replace(" ", "")  # 记得格式化，参数需要提交原始json，非已格式化的json
        headers['X-Sk'] = self.xsk  # 修改请求中的xsk
        data = requests.post(url="https://m.pvp.xoyo.com/role/indicator", data=param, headers=headers).json()
        if data.get("code") != 0:
            nonebot.logger.error("获取全局role_id失败，请重试")
            return None
        if data.get('data').get('role_info') is None:
            nonebot.logger.error("获取角色失败，请重试")
            return None
        self.global_role_id = data.get("data").get("role_info").get("global_role_id")

    async def get_jjc_record(self):
        # 准备请求参数
        param = {'global_role_id': self.global_role_id, "size": 10, "cursor": 0}
        self.ts, self.xsk = await self.get_xsk(param)
        param['ts'] = self.ts
        param = json.dumps(param).replace(" ", "")  # 记得格式化，参数需要提交原始json，非已格式化的json
        headers['X-Sk'] = self.xsk  # 修改请求中的xsk
        data = requests.post(url="https://m.pvp.xoyo.com/3c/mine/match/history", data=param, headers=headers).json()
        if data.get("code") != 0:
            nonebot.logger.error("获取JJC战绩失败，请重试")
            return None
        if not data.get('data'):
            nonebot.logger.error("没有JJC战绩，请重试")
            return None
        return data

    async def get_person_record(self):
        sql = "select id from InfoCache where name='%s'" % self.role
        await self.database.connect()
        role_id_dict = await self.database.fetchone(sql)
        if role_id_dict is None:
            nonebot.logger.error(self.role + "得role_id未得到，将返回None")
            return None
        self.role_id = str(role_id_dict.get("id"))
        await self.get_global_role_id()
        dataSet = await self.get_jjc_record()
        if dataSet is None:
            nonebot.logger.info(f"没有拿到{self.role}数据")
            return None
        if dataSet.get("code") != 0:
            nonebot.logger.info(f"没有拿到{self.role}数据")
            return None
        data = dataSet.get("data")
        fig, ax = plt.subplots(figsize=(8, 9), facecolor='white', edgecolor='white')
        plt.style.use(dufte.style)
        ax.axis([0, 10, 0, 10])
        ax.set_title("斗转星移  " + self.role + '  近10场JJC战绩', fontsize=19, color='#303030', fontweight="heavy",
                     verticalalignment='top')
        ax.axis('off')
        for x, y in reversed(list(enumerate(data))):
            pvp_type = y.get("pvp_type")
            avg_grade = y.get("avg_grade")
            total_mmr = y.get("total_mmr")
            won = y.get("won") is True and "胜利" or "失败"
            consume_time = time.strftime("%M分%S秒", gmtime(y.get("end_time") - y.get("start_time")))
            start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(y.get("start_time")))
            ax.text(0, x, f'{pvp_type}V{pvp_type}', verticalalignment='bottom', horizontalalignment='left',
                    color='#404040')
            ax.text(1, x, f'{avg_grade}段局 ', verticalalignment='bottom', horizontalalignment='left', color='#404040')
            ax.text(2, x, f'{total_mmr}', verticalalignment='bottom', horizontalalignment='left', color='#404040')
            fontColor = won == "胜利" and 'blue' or 'red'
            ax.text(3, x, f'{won}', verticalalignment='bottom', horizontalalignment='left', color=fontColor)
            ax.text(4, x, f'{consume_time}', verticalalignment='bottom', horizontalalignment='left', color='#404040')
            ax.text(6, x, f'{start_time}', verticalalignment='bottom', horizontalalignment='left', color='#404040')
        plt.savefig(f"/tmp/role{self.role}.png")
        return data

    # async def get_plot(role: str):
    #     TotalData = await main(role)
    #     plt.figure()
    #     plt.title(role+'近10场JJC战绩')
    #     jjc_time = []
    #     mmr = []
    #     # plt.xlabel('周', fontsize=16)
    #     # plt.ylabel('数量', fontsize=16)
    #     for y in reversed(TotalData):
    #         start_time = time.strftime("%H:%M:%S", time.localtime(y.get("start_time")))
    #         jjc_time.append(str(start_time))
    #         mmr.append(y.get("total_mmr"))
    #         plt.text(jjc_time, mmr, '%.0f' % y.get("total_mmr"), ha="center", va="bottom")
    #     containsMmr = mmr[0] // 100 * 100
    #     plt.axis([0, 10, containsMmr, containsMmr+100])
    #     plt.grid(True)
    #     plt.plot(jjc_time, mmr, "o-")
    #     plt.show()