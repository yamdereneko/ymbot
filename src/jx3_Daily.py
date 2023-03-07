# -*- coding: utf-8 -*-

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
from src.internal.jx3api import API
from PIL import ImageFont
from PIL import Image, ImageDraw

# 请求头
api = API()


async def image_prospect(image):
    im2 = Image.new('RGBA', image.size, (255, 255, 255, 255))
    im2.paste(image, (0, 0), image)
    return im2


class GetDaily:
    def __init__(self, server: str = "姨妈", daily_next: int = 0):
        self.server = jxData.mainServer(server)
        self.zone = jxData.mainZone(self.server)
        self.daily_next = daily_next
        if self.daily_next is None:
            self.daily_next = 0

    async def get_daily(self):
        response = await api.data_active_current(server=self.server, next=self.daily_next)
        if response.code != 200:
            nonebot.logger.error("API接口Daily获取信息失败，请查看错误")
            return None
        return response.data

    async def query_daily_figure(self):
        data = await self.get_daily()
        if data is None:
            nonebot.logger.error(self.server + "日常未得到，将返回None")
            return None
        images = await image_prospect(Image.open("src/images/daily.png").convert("RGBA"))
        draw = ImageDraw.Draw(images)
        today = data.get("date") + " 星期" + data.get("week")
        war = data.get("war")
        battle = data.get("battle")
        five_persons_instance = "\n".join(str(data.get("team")[1]).split(';'))
        ten_persons_instance = "\n".join(str(data.get("team")[2]).split(';'))

        daily_font = ImageFont.truetype("src/fonts/pingfang_regular.ttf", size=100)
        fill_color = (0, 0, 0)

        # 时间设置
        draw.text((69 * 4, 143 * 4), today, font=daily_font, fill=fill_color)

        # 大战
        draw.text((69 * 4, 299 * 4), war, font=daily_font, fill=fill_color)

        # 大战
        draw.text((69 * 4, 459 * 4), battle, font=daily_font, fill=fill_color)

        # 五人周常
        draw.text((69 * 4, 619 * 4), five_persons_instance, font=daily_font, fill=fill_color)

        # 十人周常
        draw.text((69 * 4, 862 * 4), ten_persons_instance, font=daily_font, fill=fill_color)

        dpi = (1000, 1000)

        # # 保存图像
        datetime = int(time.time())
        images.save(f"/tmp/daily_{datetime}.png", dpi=dpi)
        return datetime

    async def query_weekly_daily(self):
        response = await api.app_calculate(count=7)
        if response.code != 200:
            nonebot.logger.error("API接口Daily获取信息失败，请查看错误")
            return None
        return response.data