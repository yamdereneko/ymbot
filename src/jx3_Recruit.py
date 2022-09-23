# -*- coding: utf-8 -*-
import asyncio
import time
import traceback
import dufte
import nonebot
import src.Data.jxDatas as jxData
from src.internal.jx3api import API
from matplotlib import pyplot as plt

api = API()


class Recruit:
    def __init__(self, server, keyword):
        self.server = jxData.mainServer(server)
        self.zone = jxData.mainZone(self.server)
        self.keyword = keyword

    async def query_server_recruit(self):
        response = await api.next_recruit(server=self.server, keyword=self.keyword)
        if response.code != 200:
            nonebot.logger.error("API接口next_recruit获取信息失败，请查看错误")
            return None
        return response.data

    async def get_Fig(self):
        try:
            task = await self.query_server_recruit()
            if task is None:
                nonebot.logger.error("获取用户信息失败，请查看问题.")
                return None
            data = task['data']
            fig, ax = plt.subplots(figsize=(16, 5 + len(task) / 2), facecolor='#FAF2E2', edgecolor='white')
            plt.style.use(dufte.style)
            data.insert(0, {'activity': '活动', "leader": "团长", "number": "人数", "maxNumber": "", "content": "内容",
                            "createTime": "时间"})
            ax.axis([0, 14, 0, len(task) + 2])
            ax.axis('off')

            for floor, element in enumerate(data):
                activity = element.get("activity")
                leader = element.get("leader")
                number = element.get("number")
                max_number = element.get("maxNumber")
                content = element.get("content")
                create_time = element.get("createTime")
                if create_time == 0:
                    start_time = '时间未详'
                elif create_time == "时间":
                    start_time = "时间"
                elif create_time == '':
                    start_time = ''
                else:
                    if time.altzone == 0:
                        start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(create_time + 28800))
                    else:
                        start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(create_time))
                if floor == 0:
                    plt.rcParams['text.color'] = 'black'
                    plt.rcParams['font.weight'] = 'heavy'
                    plt.rcParams['font.size'] = 16
                else:
                    plt.rcParams['font.size'] = 14
                    plt.rcParams['text.color'] = '#404040'
                floor = len(task) - floor + 1
                ax.text(0, floor, f'{activity}', horizontalalignment='left',
                        verticalalignment='top')
                ax.text(2, floor, f'{leader}', horizontalalignment='left',
                        verticalalignment='top')
                ax.text(3.5, floor, f'{number}/{max_number}', horizontalalignment='left',
                        verticalalignment='top')
                ax.text(5, floor, f'{content}', horizontalalignment='left',
                        verticalalignment='top')
                ax.text(12, floor, f'{start_time}', horizontalalignment='left',
                        verticalalignment='top')
            ax.set_title(f'{self.server}    招募', fontsize=24, color='black',
                         fontweight="heavy", verticalalignment='top', horizontalalignment='center')
            datetime = int(time.time())
            plt.savefig(f"/tmp/recruit{datetime}.png")
            return datetime
        except Exception as e:
            nonebot.logger.error(e)
            nonebot.logger.error("获取用户信息失败，请查看报错.")
            traceback.print_exc()
            return None
