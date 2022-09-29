# -*- coding: utf-8 -*-
import asyncio
import time
import traceback
import dufte
import nonebot
from src.internal.jx3api import API
from matplotlib import pyplot as plt

api = API()


class Price:
    def __init__(self, mono):
        self.mono = mono

    async def query_mono_price(self):
        response = await api.data_trade_search(name=self.mono)
        if response.code != 200:
            nonebot.logger.error("API接口next_price获取信息失败，请查看错误: ")
            nonebot.logger.error(f'报错代码: {response.code}, 报错信息:{response.msg}')
            return None
        print(response)
        return response

    async def create_price_figure(self):
        try:
            task = await self.query_mono_price()
            if task is None:
                nonebot.logger.error("获取物价信息失败，请查看报错信息")
                return None
            data = task.data['data']

            fig, ax = plt.subplots(figsize=(22, 8), facecolor='#FAF2E2', edgecolor='white')
            plt.style.use(dufte.style)

            ax.set_title(f'物价   {self.mono}', fontsize=24, color='black',
                         fontweight="heavy", verticalalignment='top', horizontalalignment='center')

            ax.axis([0, 20, 0, 6])
            ax.axis('off')
            server_class = ['电信点卡', '双线点卡', '电信月卡', '双线月卡', '双线四区']
            for x, element in enumerate(data):
                x_size = x * 4
                ax.text(x_size + 0.8, 5, f'{server_class[x]}',
                        color='#404040', fontsize=16, verticalalignment='top')
                if element:
                    floor = 5
                    for floors, content in enumerate(element[:5]):
                        floor = floor - 1
                        source = content["source"]
                        sales = content["sales"]
                        value = content["value"].split('.')[0]
                        date = content["date"]
                        match source:
                            case "百度贴吧":
                                source_end = '贴吧'
                            case "废牛助手":
                                source_end = '废牛'
                            case "物价小黑":
                                source_end = '小黑'
                            case _:
                                source_end = source
                        middle = time.strptime(date, '%Y-%m-%d')
                        end_date = time.strftime("%y/%m/%d", middle)
                        ax.text(x_size, floor, f'{source_end}',
                                color='#404040', fontsize=14, verticalalignment='top')
                        ax.text(x_size + 0.6, floor, f'{value}',
                                color='#404040', fontsize=14, verticalalignment='top')
                        ax.text(x_size + 1.4, floor, f'{sales}',
                                color='#404040', fontsize=14, verticalalignment='top')
                        ax.text(x_size + 1.7, floor, f'{end_date}',
                                color='#404040', fontsize=14, verticalalignment='top')

            datetime = int(time.time())
            plt.savefig(f"/tmp/price{datetime}.png")
            return datetime
        except Exception as e:
            nonebot.logger.error(e)
            nonebot.logger.error("获取用户信息失败，请查看报错.")
            traceback.print_exc()
            return None

# price = Price('龙女金')
# asyncio.run(price.create_price_figure())
