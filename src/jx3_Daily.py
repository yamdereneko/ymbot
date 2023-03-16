# -*- coding: utf-8 -*-

"""
@Software : PyCharm
@File : 0.py
@Author : 喵
@Time : 2021/09/29 22:39:29
@Docs : 请求推栏战绩例子
"""
import time
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
        draw.text((today_size_width, 165 * redouble), today, font=daily_font, fill=fill_color)

        # 大战
        war_text_width = daily_font.getlength(war)
        war_size_width = (images_width - war_text_width) / 2
        draw.text((war_size_width, 315.68 * redouble), war, font=daily_font, fill=fill_color)

        # 大战
        battle_text_width = daily_font.getlength(battle)
        battle_size_width = (images_width - battle_text_width) / 2
        draw.text((battle_size_width, 469.37 * redouble), battle, font=daily_font, fill=fill_color)

        # 五人周常
        for floor, element in enumerate(five_persons_instance_respective):
            five_persons_instance_text_width = daily_font.getlength(element)
            five_persons_instance_size_width = (images_width - five_persons_instance_text_width) / 2
            draw.text((five_persons_instance_size_width, 624.06 * redouble + floor * 127), element, font=daily_font, fill=fill_color)

        # 十人周常
        for floor, element in enumerate(ten_persons_instance_respective):
            ten_persons_instance_text_width = daily_font.getlength(element)
            ten_persons_instance_size_width = (images_width - ten_persons_instance_text_width) / 2
            draw.text((ten_persons_instance_size_width, 858.11 * redouble + floor * 127), element, font=daily_font, fill=fill_color)

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
