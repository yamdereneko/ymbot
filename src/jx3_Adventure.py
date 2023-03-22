# -*- coding: utf-8 -*-
import asyncio
import json
import time
from io import BytesIO
import nonebot
import random
import src.Data.jxDatas as jxData
from src.internal.tuilanapi import API
from src.internal.jx3api import API as jx3API
from src.jx3_TopnRoles import GetTopnRoles
from PIL import Image, ImageDraw, ImageFont
import src.Data.jx3_Redis as redis

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
        self.red = redis.Redis()

    async def query_user_info(self):
        ticket_list = await self.red.query_list("ticket_list")
        response = await jx3api.data_luck_adventure(server=self.server, name=self.user,
                                                    ticket=random.choice(ticket_list))
        if response.code != 200:
            nonebot.logger.error("API接口data_luck_adventure获取信息失败，请查看错误")
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
        # 设置总体比例
        flag = 2

        # 定义字体
        font = ImageFont.truetype("src/fonts/pingfang_regular.ttf", size=32 * flag)
        bold_font = ImageFont.truetype("src/fonts/pingfang_bold.ttf", size=29 * flag)
        id_font = ImageFont.truetype("src/fonts/pingfang_bold.ttf", size=52 * flag)
        server_font = ImageFont.truetype("src/fonts/pingfang_regular.ttf", size=32 * flag)

        # 创建一个空白的图像对象
        image = Image.new("RGB", (800 * flag, 337 * flag + len(task) * 62 * flag), "white").convert("RGBA")
        draw = ImageDraw.Draw(image)
        images_width, _ = image.size
        # 心法图标
        # total_kungfu_icon = await image_prospect(
        #     Image.open(f"images/TotalKungfu/{force_id}.png").convert("RGBA").resize((75 * flag, 50 * flag)))
        # image.paste(total_kungfu_icon, (269 * flag, 80 * flag))

        # ID
        id_text_width = id_font.getlength(self.user)
        id_size_width = (images_width - id_text_width) / 2
        draw.text((id_size_width, 58 * flag), self.user, fill=(101, 109, 121), font=id_font)

        # 资历
        roles = GetTopnRoles(self.server, self.user)
        value = await roles.get_topn_data()
        topn = f'资历：{value}'
        topn_text_width = server_font.getlength(topn)
        topn_size_width = (images_width - topn_text_width) / 2
        draw.text((topn_size_width, 140 * flag), topn, fill=(101, 109, 121), font=server_font)

        # 区服
        server = f'{self.zone} {self.server}'
        server_text_width = server_font.getlength(server)
        server_size_width = (images_width - server_text_width) / 2
        draw.text((server_size_width, 185 * flag), server, fill=(101, 109, 121), font=server_font)

        # 标题设置
        draw.text((110 * flag, 273 * flag), '奇遇', fill=(166, 166, 166), font=bold_font)
        draw.text((371 * flag, 273 * flag), '时间', fill=(166, 166, 166), font=bold_font)
        draw.text((632 * flag, 273 * flag), '距今', fill=(166, 166, 166), font=bold_font)

        # 绝世奇遇小图标显示
        precious = await image_prospect(
            Image.open(f"src/images/precious.png").convert("RGBA").resize((11 * flag, 26 * flag)))

        # 逐个字符添加文本
        for h, element in enumerate(task):
            # 定义
            adventure_name = element.get('event')
            level = element.get('level')
            adventure_time = element.get('time')

            # 奇遇的排列
            adventure_x = 79 * flag
            adventure_y = 337 * flag + h * 60 * flag
            if len(adventure_name) == 3:
                adventure_x += 20
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
            adventure_time_y = 337 * flag + h * 60 * flag
            if adventure_time == 0:
                draw.text((adventure_time_x + 62 * flag, adventure_time_y), "未知", fill="black", font=font)
            else:
                draw.text((adventure_time_x, adventure_time_y), date_string, fill="black", font=font)

            # 计算时间戳是多久的
            delta_time = int(time.time() - adventure_time)
            ago_time_x = 622 * flag
            ago_time_y = 337 * flag + h * 60 * flag

            if adventure_time == 0:
                draw.text((ago_time_x, ago_time_y), "未知", font=font, fill="black")
            elif delta_time < 86400:
                # 少于1天
                delta_time //= 3600
                war_time = f"{delta_time}小时前"
                draw.text((ago_time_x, ago_time_y), war_time, font=font, fill="black")
            else:
                # 大于等于1天
                delta_time //= 86400
                war_time = f"{delta_time}天前"
                indentation = len(war_time) - 3
                draw.text((ago_time_x - indentation * 20, ago_time_y), war_time, font=font, fill="black")

        dpi = (2000, 2000)
        # # 保存图像
        buffer = BytesIO()
        buffer.seek(0)
        image.save(buffer, dpi=dpi, format='PNG')
        # image.save(f"images/record_image.png", dpi=dpi)
        return buffer
