# -*- coding: utf-8 -*-
import asyncio
import json
import time
import traceback
import dufte
import nonebot
import random
import src.Data.jxDatas as jxData
from src.internal.tuilanapi import API
from src.internal.jx3api import API as jx3API
from matplotlib import pyplot as plt
from functools import partial
from PIL import Image, ImageDraw, ImageFont

api = API()
jx3api = jx3API()


async def image_prospect(image):
    im2 = Image.new('RGBA', image.size, (255, 255, 255, 255))
    im2.paste(image, (0, 0), image)
    return im2


class Adventure:
    def __init__(self, server, user):
        self.server = jxData.mainServer(server)
        self.zone = jxData.mainZone(self.server)
        self.user = user

    async def query_user_info(self):
        response = await jx3api.data_lucky_serendipity(server=self.server, name=self.user,
                                                       ticket=random.choice(jxData.ticket))
        if response.code != 200:
            nonebot.logger.error("API接口next_serendipity获取信息失败，请查看错误")
            return None
        adventure_info = []
        for _ in response.data:
            if _['level'] < 3:
                adventure_info.append(_)
        return adventure_info

    async def create_figure(self):
        task = await self.query_user_info()
        if task is None:
            nonebot.logger.error("获取用户信息失败，请查看问题.")
            return None
        response = await jx3api.data_role_roleInfo(server=self.server, name=self.user)
        if response.code != 200:
            nonebot.logger.error("API接口role_roleInfo获取信息失败，请查看错误")
            return None
        force_id = response.data.get('forceId')
        # 设置总体比例
        flag = 2

        # 定义字体
        font = ImageFont.truetype("src/fonts/pingfang_regular.ttf", size=32 * flag)
        bold_font = ImageFont.truetype("src/fonts/pingfang_bold.ttf", size=42 * flag)
        id_font = ImageFont.truetype("src/fonts/pingfang_bold.ttf", size=58 * flag)
        server_font = ImageFont.truetype("src/fonts/pingfang_regular.ttf", size=32 * flag)

        # 创建一个空白的图像对象
        image = Image.new("RGB", (800 * flag, 288 * flag + len(task) * 62 * flag), "white").convert("RGBA")
        draw = ImageDraw.Draw(image)

        # 心法图标
        total_kungfu_icon = await image_prospect(
            Image.open(f"src/images/TotalKungfu/{force_id}.png").convert("RGBA").resize((75 * flag, 50 * flag)))
        image.paste(total_kungfu_icon, (269 * flag, 80 * flag))

        # ID还有区服
        draw.text((340 * flag, 60 * flag), self.user, fill=(61, 62, 66), font=id_font)
        draw.text((342 * flag, 125 * flag), self.server, fill=(0, 0, 0), font=server_font)

        # 标题设置
        draw.text((99 * flag, 200 * flag), '奇遇', fill=(166, 166, 166), font=bold_font)
        draw.text((358 * flag, 200 * flag), '时间', fill=(166, 166, 166), font=bold_font)
        draw.text((612.5 * flag, 200 * flag), '距今', fill=(166, 166, 166), font=bold_font)

        # 绝世奇遇小图标显示
        precious = await image_prospect(
            Image.open(f"src/images/precious.png").convert("RGBA").resize((11 * flag, 26 * flag)))

        # 逐个字符添加文本
        for h, element in enumerate(task):
            # 定义
            adventure_name = element.get('serendipity')
            level = element.get('level')
            adventure_time = element.get('time')

            # 奇遇的排列
            adventure_x = 79 * flag
            adventure_y = 288 * flag + h * 60 * flag
            if len(adventure_name) == 3:
                adventure_x += 16
                draw.text((adventure_x, adventure_y), adventure_name, fill="black", font=font)
            if len(adventure_name) == 4:
                draw.text((adventure_x, adventure_y), adventure_name, fill="black", font=font)

            # 奇遇等级，一般标志绝世奇遇在显示的左上角
            if level == 2:
                image.paste(precious, (adventure_x - 13 * flag, adventure_y - 1 * flag))

            # 将时间戳转换为时间元组
            time_tuple = time.localtime(adventure_time)

            # 构造日期字符串
            date_string = time.strftime('%Y-%m-%d', time_tuple)
            adventure_time_x = 306 * flag
            adventure_time_y = 288 * flag + h * 60 * flag
            if adventure_time == 0:
                draw.text((adventure_time_x + 62 * flag, adventure_time_y), "未知", fill="black", font=font)
            else:
                draw.text((adventure_time_x, adventure_time_y), date_string, fill="black", font=font)

            # 计算时间戳是多久的
            delta_time = int(time.time() - adventure_time)
            ago_time_x = 602 * flag
            ago_time_y = 288 * flag + h * 60 * flag

            if adventure_time == 0:
                draw.text((ago_time_x + 27 * flag, ago_time_y), "未知", font=font, fill="black")
            elif delta_time < 86400:
                # 少于1天
                delta_time //= 3600
                war_time = f"{delta_time}小时前"
                draw.text((ago_time_x, ago_time_y), war_time, font=font, fill="black")
            else:
                # 大于等于1天
                delta_time //= 86400
                war_time = f"{delta_time}天前"
                draw.text((ago_time_x, ago_time_y), war_time, font=font, fill="black")
        dpi = (2000, 2000)
        # 保存图像
        datetime = int(time.time())
        image.save(f"/tmp/adventure_{datetime}.png", dpi=dpi)
        return datetime

