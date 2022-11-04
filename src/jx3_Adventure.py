# -*- coding: utf-8 -*-
import asyncio
import json
import time
import traceback
import dufte
import nonebot
import random
import src.Data.jxDatas as jxData
from src.internal.jx3api import API
from matplotlib import pyplot as plt
from functools import partial

api = API()


class Adventure:
    def __init__(self, server, user):
        self.server = jxData.mainServer(server)
        self.zone = jxData.mainZone(self.server)
        self.user = user

    async def query_user_info(self):
        response = await api.data_lucky_serendipity(server=self.server, name=self.user,
                                                    ticket=random.choice(jxData.ticket))
        if response.code != 200:
            nonebot.logger.error("API接口next_serendipity获取信息失败，请查看错误")
            return None
        adventure_info = []
        for _ in response.data:
            if _['level'] < 3:
                adventure_info.append(_)
        return adventure_info

    async def get_Fig(self, task):
        try:
            if task is None:
                nonebot.logger.error("获取用户信息失败，请查看问题.")
                return None

            fig, ax = plt.subplots(figsize=(5, len(task) / 2), facecolor='#FAF2E2', edgecolor='white')
            plt.style.use(dufte.style)

            ax.axis([0, 4, 0, len(task) + 2])
            ax.axis('off')

            for floor, element in enumerate(task, start=1):
                adventure = element.get("serendipity")
                date = element.get("time")
                if date == 0:
                    start_time = '时间未详'
                else:
                    if time.altzone == 0:
                        start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(date + 28800))
                    else:
                        start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(date))

                floor = len(task) - floor + 1
                ax.text(0.5, floor, f'{adventure}', horizontalalignment='left',
                        color='#404040', verticalalignment='top')
                ax.text(1.5, floor, f'{start_time}', horizontalalignment='left',
                        color='#404040', verticalalignment='top')
            ax.text(2, len(task) + 2.2, f'{self.server}   {self.user}', fontsize=20, color='#4F443C',
                    fontweight="heavy", verticalalignment='top', horizontalalignment='center')
            datetime = int(time.time())
            plt.savefig(f"/tmp/adventure{datetime}.png")
            return datetime
        except Exception as e:
            nonebot.logger.error(e)
            nonebot.logger.error("获取用户信息失败，请查看报错.")
            traceback.print_exc()
            return None