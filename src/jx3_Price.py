# -*- coding: utf-8 -*-
import asyncio
import time
import nonebot
from src.internal.jx3api import API
from src.internal.wanbaolouAPI import WangBaoLouAPI
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from httpx import AsyncClient

api = API()


async def image_prospect(image):
    im2 = Image.new('RGBA', image.size, (255, 255, 255, 255))
    im2.paste(image, (0, 0), image)
    return im2


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()


class Price:
    client: AsyncClient

    def __init__(self, mono):
        self.mono = mono
        self.client = AsyncClient()

    async def query_mono_price(self):
        response = await api.data_trade_record(name=self.mono)
        if response.code != 200:
            nonebot.logger.error("API接口next_price获取信息失败，请查看错误: ")
            nonebot.logger.error(f'报错代码: {response.code}, 报错信息:{response.msg}')
            return None
        return response.data

    async def create_price_figure(self):
        task = await self.query_mono_price()
        if task is None:
            nonebot.logger.error("获取物价信息失败，请查看报错信息")
            return None
        flag = 2

        task_name = task.get('name')

        # 定义字体
        master_title_font = ImageFont.truetype("src/fonts/pingfang_bold.ttf", size=90 * flag)
        slave_title_font = ImageFont.truetype("src/fonts/pingfang_regular.ttf", size=22 * flag)
        total_font = ImageFont.truetype("src/fonts/pingfang_bold.ttf", size=30 * flag)
        data_title_font = ImageFont.truetype("src/fonts/pingfang_bold.ttf", size=18 * flag)
        data_font = ImageFont.truetype("src/fonts/pingfang_regular.ttf", size=24 * flag)
        emoji_font = ImageFont.truetype("src/fonts/seguiemj.ttf", size=24 * flag)

        # 设置画布
        image = Image.new("RGB", (1200 * flag, 1900 * flag), "white").convert("RGBA")
        draw = ImageDraw.Draw(image)
        image_width, _ = image.size

        # logo
        draw.text((25 * flag, 20 * flag), 'YMNeko.', fill=(10, 0, 71), font=data_title_font)

        # 标题设置
        title_width = master_title_font.getlength(task_name)
        title_x = (image_width - title_width) / 2
        draw.text((title_x, 175 * flag), task_name, fill=(26, 33, 81), font=master_title_font)

        # 图片生成
        url = task.get('view')
        res = await self.client.get(url=url, timeout=3000)
        title_image = await image_prospect(
            Image.open(BytesIO(res.content)).convert("RGBA").resize((600 * flag, 370 * flag)))
        image.paste(title_image, (300 * flag, 280 * flag))

        # 设置圆角矩形的左上角和右下角坐标，以及圆角半径
        x1, y1 = 300 * flag, 700 * flag
        x2, y2 = 900 * flag, 795 * flag
        radius = 10

        # 绘制圆角矩形框
        radius_color = (211, 217, 243)
        draw.line([(x1 + radius, y1), (x2 - radius, y1)], fill=radius_color, width=2 * flag)
        draw.line([(x2, y1 + radius), (x2, y2 - radius)], fill=radius_color, width=2 * flag)
        draw.line([(x1 + radius, y2), (x2 - radius, y2)], fill=radius_color, width=2 * flag)
        draw.line([(x1, y1 + radius), (x1, y2 - radius)], fill=radius_color, width=2 * flag)
        draw.arc([(x1, y1), (x1 + 2 * radius, y1 + 2 * radius)], 180, 270, fill=radius_color, width=2 * flag)
        draw.arc([(x2 - 2 * radius, y1), (x2, y1 + 2 * radius)], 270, 360, fill=radius_color, width=2 * flag)
        draw.arc([(x2 - 2 * radius, y2 - 2 * radius), (x2, y2)], 0, 90, fill=radius_color, width=2 * flag)
        draw.arc([(x1, y2 - 2 * radius), (x1 + 2 * radius, y2)], 90, 180, fill=radius_color, width=2 * flag)

        # 销售内容
        desc = task.get('desc')
        desc_width = slave_title_font.getlength(desc)
        desc_x = (image_width - desc_width) / 2
        draw.text((desc_x, 734 * flag), desc, fill=(26, 33, 81), font=slave_title_font)

        # 销售背景
        draw.rounded_rectangle((90 * flag, 900 * flag, 570 * flag, 1820 * flag), radius=20, fill=(254, 255, 255),
                               outline=(211, 217, 243), width=2 * flag)
        draw.rounded_rectangle((90 * flag, 900 * flag, 570 * flag, 979 * flag), radius=20, fill=(246, 250, 253),
                               outline=(211, 217, 243), width=2 * flag)

        draw.rounded_rectangle((630 * flag, 900 * flag, 1110 * flag, 1820 * flag), radius=20, fill=(254, 255, 255),
                               outline=(211, 217, 243), width=2 * flag)
        draw.rounded_rectangle((630 * flag, 900 * flag, 1110 * flag, 979 * flag), radius=20, fill=(246, 250, 253),
                               outline=(211, 217, 243), width=2 * flag)

        # 销售类型
        draw.text((285 * flag, 924 * flag), f"公示期", fill=(26, 33, 81), font=total_font)
        draw.text((825 * flag, 924 * flag), f"开售期", fill=(26, 33, 81), font=total_font)

        publication_type = 1
        on_sale_type = 2
        wangbaolou = WangBaoLouAPI()
        response = await wangbaolou.call_api(task_name, publication_type)
        if response.code != 1:
            nonebot.logger.error("官方万宝楼接口获取失败，请查看错误代码")
            nonebot.logger.error(response.msg)
            return None

        # 公示期

        for floor, element in enumerate(response.data.get('list')):
            single_unit_price = element.get('single_unit_price') // 100
            remaining_time = element.get('remaining_time')
            followed_num = element.get('followed_num')
            hours = remaining_time // 3600
            minutes = (remaining_time // 60) % 60

            text_y = 1003.1 * flag + floor * 83 * flag
            text_color = (26, 33, 81)
            draw.text((140.5 * flag, text_y), f"{hours}小时{minutes}分钟", fill=text_color, font=data_font)
            draw.text((349.5 * flag, text_y), f"¥{single_unit_price}", fill=text_color, font=data_font)
            draw.text((468.5 * flag, text_y + 7 * flag), f"❤ {followed_num}", fill=text_color, font=emoji_font)

        # 在售期
        response = await wangbaolou.call_api(task_name, on_sale_type)
        if response.code != 1:
            nonebot.logger.error("官方万宝楼接口获取失败，请查看错误代码")
            nonebot.logger.error(response.msg)
            return None

        # 公示期
        for floor, element in enumerate(response.data.get('list')):
            single_unit_price = element.get('single_unit_price') // 100
            remaining_time = element.get('remaining_time')
            followed_num = element.get('followed_num')
            hours = remaining_time // 3600
            minutes = (remaining_time // 60) % 60

            text_y = 1003.1 * flag + floor * 83 * flag
            text_color = (26, 33, 81)
            draw.text((680.5 * flag, text_y), f"{hours}小时{minutes}分钟", fill=text_color, font=data_font)
            draw.text((889.5 * flag, text_y), f"¥{single_unit_price}", fill=text_color, font=data_font)
            draw.text((1008.5 * flag, text_y + 7 * flag), f"❤ {followed_num}", fill=text_color, font=emoji_font)

        dpi = (1000, 1000)
        # 保存图像
        datetime = int(time.time())
        image.save(f"/tmp/Price_{datetime}.png", dpi=dpi)
        # image.save(f"images/Price_Test.png", dpi=dpi)
        return datetime
