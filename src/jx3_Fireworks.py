# -*- coding: utf-8 -*-
import asyncio
import re
import time
import traceback
import dufte
import nonebot
import src.Data.jxDatas as jxData
from src.internal.jx3api import API
from matplotlib import pyplot as plt

api = API()


class Fireworks:
    def __init__(self, server, user):
        self.server = jxData.mainServer(server)
        self.zone = jxData.mainZone(self.server)
        self.user = user

    async def query_user_firework_info(self):
        response = await api.role_firework(server=self.server, name=self.user)
        if response.code != 200:
            nonebot.logger.error("API接口role_fireworky获取信息失败，请查看错误")
            return None
        return response.data

    async def get_Fig(self):
        try:
            task = await self.query_user_firework_info()
            if task is None:
                nonebot.logger.error("获取用户信息失败，请查看问题.")
                return None
            elif not task:
                nonebot.logger.error("获取用户信息失败，请查看问题.")
                return None

            fig, ax = plt.subplots(figsize=(14, len(task) / 2), facecolor='#FAF2E2', edgecolor='white')
            plt.style.use(dufte.style)
            task.insert(0, {'name': '烟花', "sender": "赠方", "recipient": "收方", "map": "地图", "time": "时间"})
            ax.axis([0, 12, 0, len(task) + 2])
            ax.axis('off')
            for floor, element in enumerate(task):
                fire = element.get("name")
                fire_map_send = element.get("sender")
                fire_map_get = element.get("recipient")
                fire_map = element.get("map")
                fire_date = element.get("time")
                if fire_date == 0:
                    start_time = '时间未详'
                elif fire_date == "时间":
                    start_time = "时间"
                else:
                    if time.altzone == 0:
                        start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(fire_date + 28800))
                    else:
                        start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(fire_date))

                floor = len(task) - floor + 1
                ax.text(0, floor, f'{fire}', horizontalalignment='left',
                        color='#404040', verticalalignment='top')
                ax.text(1.5, floor, f'{fire_map_send}', horizontalalignment='left',
                        color='#404040', verticalalignment='top')
                ax.text(4, floor, f'{fire_map_get}', horizontalalignment='left',
                        color='#404040', verticalalignment='top')
                ax.text(6.5, floor, f'{fire_map}', horizontalalignment='left',
                        color='#404040', verticalalignment='top')
                ax.text(8, floor, f'{start_time}', horizontalalignment='left',
                        color='#404040', verticalalignment='top')
            ax.set_title(f'{self.server}    {self.user}', fontsize=25, color='#4F443C',
                         fontweight="heavy", verticalalignment='top', horizontalalignment='center')
            datetime = int(time.time())
            plt.savefig(f"/tmp/fireworks{datetime}.png")
            return datetime
        except Exception as e:
            nonebot.logger.error(e)
            nonebot.logger.error("获取用户信息失败，请查看报错.")
            traceback.print_exc()
            return None
