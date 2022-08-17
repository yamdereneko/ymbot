# -*- coding: utf-8 -*
"""
@Software : PyCharm
@File : 0.py
@Author : 喵
@Time : 2021/09/29 22:39:29
@Docs : 请求推栏战绩例子
"""
import time
import traceback
from time import gmtime
import dufte
import nonebot
import matplotlib
import matplotlib.pyplot as plt
from .jxDatas import jx3Data as jxData
from .database import DataBase as database
import requests
import json

# 请求头

headers = jxData.headers
matplotlib.rc("font", family='PingFang HK')


class GetPersonInfo:
    def __init__(self, role: str, server: str):
        jx3Data = jxData()
        config = jxData.config
        self.role = role
        self.server = jx3Data.mainServer(server)
        self.zone = jx3Data.mainZone(self.server)
        self.database = database(config)
        self.role_id = None
        self.person_id = None
        self.ts = None
        self.xsk = None
        self.role_name = None

    async def get_xsk(self, data=None):
        try:
            data = json.dumps(data)
            res = requests.post(url="https://www.jx3api.com/token/calculate", data=data).json()
            return res['data']['ts'], res['data']['sk']
        except Exception as e:
            nonebot.logger.error(e)
            nonebot.logger.error("get_xsk失败，请查看问题.")
            traceback.print_exc()

    async def get_person_id(self):
        # 准备请求参数
        try:
            param = {'role_id': self.role_id, 'server': self.server, "zone": self.zone}
            self.ts, self.xsk = await self.get_xsk(param)  # 获取ts和xsk， data 字典可以传ts,不传自动生成
            param['ts'] = self.ts  # 给参数字典赋值ts参数
            param = json.dumps(param).replace(" ", "")  # 记得格式化，参数需要提交原始json，非已格式化的json
            headers['X-Sk'] = self.xsk  # 修改请求中的xsk
            data = requests.post(url="https://m.pvp.xoyo.com/role/indicator", data=param, headers=headers).json()
            if data.get("data").get("person_info") is not None:
                self.person_id = str(data.get("data").get("person_info").get("person_id"))
            else:
                self.person_id = None

        except Exception as e:
            nonebot.logger.error(e)
            nonebot.logger.error("获取Perosn_ID失败，请查看问题.")
            traceback.print_exc()

    async def get_person_history(self):
        # 准备请求参数
        try:
            if self.person_id is None:
                nonebot.logger.error("person_id 未获取到，返回空")
                return None
            param = {'person_id': str(self.person_id), "size": 10, "cursor": 0}
            ts, xsk = await self.get_xsk(param)  # 获取ts和xsk， data 字典可以传ts,不传自动生成
            param['ts'] = ts  # 给参数字典赋值ts参数
            param = json.dumps(param).replace(" ", "")  # 记得格式化，参数需要提交原始json，非已格式化的json
            headers['X-Sk'] = xsk  # 修改请求中的xsk
            data = requests.post(url="https://m.pvp.xoyo.com/mine/match/person-history", data=param,
                                 headers=headers).json()
            return data
        except Exception as e:
            nonebot.logger.error(e)
            nonebot.logger.error("获取用户信息失败，请查看问题.")
            traceback.print_exc()
            return None

    async def main(self):
        try:
            sql = "select id from InfoCache where name='%s'" % self.role
            await self.database.connect()
            role_id_info = await self.database.fetchone(sql)
            if role_id_info is None:
                nonebot.logger.error("获取用户id失败")
                return None
            self.role_id = str(role_id_info.get("id"))
            await self.get_person_id()
            role_info = await self.get_person_history()
            if role_info is not None:
                data = role_info.get("data")
                return data
            else:
                return None
        except Exception as e:
            nonebot.logger.error(e)
            nonebot.logger.error("获取用户信息失败，请查看问题.")
            traceback.print_exc()
            return None

    async def get_Fig(self):
        try:
            data = await self.main()
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
            plt.savefig(f"/tmp/role{self.role_name}.png")
            return self.role_name
        except Exception as e:
            nonebot.logger.error(e)
            nonebot.logger.error("获取用户信息失败，请查看报错.")
            traceback.print_exc()
            return None
