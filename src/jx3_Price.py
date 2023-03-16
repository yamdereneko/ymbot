# -*- coding: utf-8 -*-
import asyncio
import time
import nonebot
from src.internal.jx3api import API
from src.internal.wanbaolouAPI import WangBaoLouAPI

api = API()


class Price:
    def __init__(self, mono):
        self.mono = mono

    async def query_mono_price(self):
        response = await api.data_trade_record(name=self.mono)
        if response.code != 200:
            nonebot.logger.error("API接口next_price获取信息失败，请查看错误: ")
            nonebot.logger.error(f'报错代码: {response.code}, 报错信息:{response.msg}')
            return None
        return response

    async def create_price_figure(self):
        task = await self.query_mono_price()
        if task is None:
            nonebot.logger.error("获取物价信息失败，请查看报错信息")
            return None
        print(task.data)
        publication_type = 1
        on_sale_type = 2
        task_image = task.data.get('view')
        task_name = task.data.get('name')
        print(task_name)
        wangbaolou = WangBaoLouAPI()
        response = await wangbaolou.call_api(task_name, publication_type)
        for element in response.data.get('list'):
            print(element)
            single_unit_price = element.get('single_unit_price') // 100
            remaining_time = element.get('remaining_time')
            print(single_unit_price)
            hours = remaining_time // 3600
            minutes = (remaining_time // 60) % 60
            print(hours)
            print(minutes)
        # publication = []
        # on_sale = []
        # print(publication)
        # print(on_sale)


# price = Price("狗盒子")
# asyncio.run(price.create_price_figure())
