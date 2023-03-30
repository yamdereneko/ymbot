# -*- coding: utf-8 -*-
import asyncio
import re
import time
import traceback
from io import BytesIO

import dufte
import nonebot
import src.Data.jxDatas as jxData
from src.internal.jx3api import API
from matplotlib import pyplot as plt
from PIL import Image, ImageDraw, ImageFont

api = API()


class Fireworks:
    def __init__(self, server, user):
        self.server = jxData.mainServer(server)
        self.zone = jxData.mainZone(self.server)
        self.user = user

    async def query_user_firework_info(self):

        response = await api.data_role_firework(server=self.server, name=self.user)
        print(response)
        if response.code != 200:
            nonebot.logger.error("API接口role_fireworky获取信息失败，请查看错误")
            return None
        return response.data

    async def create_figure_from_firework(self):
        task = await self.query_user_firework_info()
        if not task:
            nonebot.logger.error("获取用户信息失败，请查看问题.")
            return None

        flag = 2

        # 字体设置
        master_title_font = ImageFont.truetype("src/fonts/pingfang_bold.ttf", size=52 * flag)
        slave_title_font = ImageFont.truetype("src/fonts/pingfang_bold.ttf", size=32 * flag)
        font = ImageFont.truetype("src/fonts/pingfang_regular.ttf", size=18 * flag)
        title_bold_font = ImageFont.truetype("src/fonts/pingfang_bold.ttf", size=22 * flag)
        logo_font = ImageFont.truetype("src/fonts/pingfang_bold.ttf", size=18 * flag)

        # 颜色设置
        title_color = (101, 109, 121)

        # 画布设置
        image = Image.new("RGB", (1200 * flag, 270 * flag + len(task) * 55 * flag), "white").convert("RGBA")
        draw = ImageDraw.Draw(image)
        images_width, _ = image.size

        # logo
        draw.text((25 * flag, 20 * flag), 'YMNeko.', fill=(10, 0, 71), font=logo_font)

        # ID
        id_text_width = master_title_font.getlength(self.user)
        id_size_width = (images_width - id_text_width) / 2
        draw.text((id_size_width, 74 * flag), self.user, fill=title_color, font=master_title_font)

        # 区服
        server = f'{self.zone} {self.server}'
        server_text_width = slave_title_font.getlength(server)
        server_size_width = (images_width - server_text_width) / 2
        draw.text((server_size_width, 138 * flag), server, fill=title_color, font=slave_title_font)

        # 标题设置
        draw.text((97 * flag, 210 * flag), "烟花名称", fill='black', font=title_bold_font)
        draw.text((345 * flag, 210 * flag), "赠送方", fill='black', font=title_bold_font)
        draw.text((571 * flag, 210 * flag), "接收方", fill='black', font=title_bold_font)
        draw.text((797 * flag, 210 * flag), "地图", fill='black', font=title_bold_font)
        draw.text((1001 * flag, 210 * flag), "时间", fill='black', font=title_bold_font)

        for floor, element in enumerate(task):
            firework_name = element.get('name')
            firework_sender = element.get('sender')
            firework_recipient = element.get('recipient')
            firework_map = element.get('map')
            firework_time = element.get('time')

            if firework_time == 0:
                start_time = '时间未详'
            elif firework_time == "时间":
                start_time = "时间"
            else:
                if time.altzone == 0:
                    start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(firework_time + 28800))
                else:
                    start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(firework_time))

            firework_y = (266 + floor * 55) * flag

            if len(firework_name) == 3:
                firework_name_x = 105
            elif len(firework_name) > 3:
                firework_name_x = 105 - (len(firework_name) - 3) * 5
            else:
                firework_name_x = 105 + (3 - len(firework_name)) * 5
            draw.text((firework_name_x * flag, firework_y), firework_name, fill='black', font=font)
            draw.text((345 * flag, firework_y), firework_sender, fill='black', font=font)
            draw.text((576 * flag, firework_y), firework_recipient, fill='black', font=font)
            draw.text((736 * flag, firework_y), firework_map, fill='black', font=font)
            draw.text((950 * flag, firework_y), start_time, fill='black', font=font)

        dpi = (1000, 1000)
        # # 保存图像
        buffer = BytesIO()
        buffer.seek(0)
        image.save(buffer, dpi=dpi, format='PNG')
        # image.save(f"images/record_image.png", dpi=dpi)
        return buffer
