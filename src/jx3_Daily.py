# -*- coding: utf-8 -*-

"""
@Software : PyCharm
@File : 0.py
@Author : 喵
@Time : 2021/09/29 22:39:29
@Docs : 请求推栏战绩例子
"""
import asyncio
import json
import time
from io import BytesIO
import nonebot
import src.Data.jxDatas as jxData
from src.internal.jx3api import API
from PIL import ImageFont
from PIL import Image, ImageDraw
import src.Data.jx3_Redis as redis

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
        self.red = redis.Redis()
        if self.daily_next is None:
            self.daily_next = 0

    async def redis_check(self, data, respective_data, respective_data_image):
        red_data = await self.red.query(respective_data)
        if red_data is not None:
            if json.loads(red_data) == data:
                red_data_image = await self.red.get_image_decode(respective_data_image)
                new_buffer = BytesIO(red_data_image)
                new_buffer_contents = new_buffer.getvalue()
                # Read the contents of the new buffer
                return new_buffer_contents
        await self.red.add(respective_data, data)
        return None

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

        respective_data = f"Daily"
        respective_data_image = f"Daily_image"
        redis_check = await self.redis_check(data, respective_data, respective_data_image)
        if redis_check is not None:
            return redis_check

        images = await image_prospect(Image.open("src/images/daily.png").convert("RGBA"))
        draw = ImageDraw.Draw(images)
        today = data.get("date") + " 星期" + data.get("week")
        war = data.get("war")
        battle = data.get("battle")
        five_persons_instance_respective = str(data.get("team")[1]).split(';')
        ten_persons_instance_respective = str(data.get("team")[2]).split(';')

        images_width = images.width
        # 倍数
        redouble = 4
        daily_font = ImageFont.truetype("src/fonts/pingfang_regular.ttf", size=31 * redouble)
        fill_color = (69, 75, 84)

        # 时间设置
        today_text_width = daily_font.getlength(today)
        today_size_width = (images_width - today_text_width) / 2
        draw.text((today_size_width, 212 * redouble), today, font=daily_font, fill=fill_color)

        # 大战
        war_text_width = daily_font.getlength(war)
        war_size_width = (images_width - war_text_width) / 2
        draw.text((war_size_width, 384.16 * redouble), war, font=daily_font, fill=fill_color)

        # 战场
        battle_text_width = daily_font.getlength(battle)
        battle_size_width = (images_width - battle_text_width) / 2
        draw.text((battle_size_width, 555.18 * redouble), battle, font=daily_font, fill=fill_color)

        # 五人周常
        for floor, element in enumerate(five_persons_instance_respective):
            five_persons_instance_text_width = daily_font.getlength(element)
            five_persons_instance_size_width = (images_width - five_persons_instance_text_width) / 2
            draw.text((five_persons_instance_size_width, 726.18 * redouble + floor * 51 * 4), element, font=daily_font,
                      fill=fill_color)

        # 十人周常
        for floor, element in enumerate(ten_persons_instance_respective):
            ten_persons_instance_text_width = daily_font.getlength(element)
            ten_persons_instance_size_width = (images_width - ten_persons_instance_text_width) / 2
            draw.text((ten_persons_instance_size_width, 992.18 * redouble + floor * 51 * 4), element, font=daily_font,
                      fill=fill_color)

        dpi = (1000, 1000)

        # # 保存图像
        buffer = BytesIO()
        buffer.seek(0)
        images.save(buffer, dpi=dpi, format='PNG')
        # images.save(f"images/daily_new.png", dpi=dpi)
        await self.red.insert_image_encode(respective_data_image, buffer.getvalue())
        return buffer

    async def query_weekly_daily(self):
        response = await api.app_calculate(count=7)
        if response.code != 200:
            nonebot.logger.error("API接口Daily获取信息失败，请查看错误")
            return None
        return response.data

