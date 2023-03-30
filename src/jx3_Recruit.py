# -*- coding: utf-8 -*-
import asyncio
import time
import traceback
from io import BytesIO
import nonebot
import src.Data.jxDatas as jxData
from src.internal.jx3api import API
from PIL import Image, ImageDraw, ImageFont

api = API()


class Recruit:
    """
    说明:
        各个服务器的招募信息，根据输入的参数进行查询。

    参数:
        * `keyword`：可选，参数
    """

    def __init__(self, server, keyword=None):
        self.server = jxData.mainServer(server)
        self.zone = jxData.mainZone(self.server)
        self.keyword = keyword

    async def query_server_recruit(self):
        response = await api.data_member_recruit(server=self.server, keyword=self.keyword)
        if response.code != 200:
            nonebot.logger.error("API接口next_recruit获取信息失败，请查看错误")
            nonebot.logger.error(f'报错代码: {response.code}, 报错信息:{response.msg}')
            return None
        return response.data

    async def create_recruit_image(self):
        try:
            task = await self.query_server_recruit()
            if task is None:
                nonebot.logger.error("获取用户信息失败，请查看问题.")
                return None
            data = task['data']

            # 设置总体比例
            flag = 2

            # 定义字体
            title_font = ImageFont.truetype("src/fonts/pingfang_bold.ttf", size=52 * flag)
            logo_font = ImageFont.truetype("src/fonts/pingfang_bold.ttf", size=18 * flag)
            slave_title_font = ImageFont.truetype("src/fonts/pingfang_regular.ttf", size=32 * flag)
            info_title_font = ImageFont.truetype("src/fonts/pingfang_bold.ttf", size=22 * flag)
            font = ImageFont.truetype("src/fonts/pingfang_regular.ttf", size=18 * flag)

            # 创建一个空白的图像对象
            image = Image.new("RGB", (1360 * flag, 281 * flag + len(data) * 45 * flag), "white").convert("RGBA")
            draw = ImageDraw.Draw(image)
            images_width, _ = image.size

            # logo
            draw.text((25 * flag, 20 * flag), 'YMNeko.', fill=(10, 0, 71), font=logo_font)

            # 大标题设置
            draw.text((628 * flag, 74 * flag), '招募', fill=(101, 109, 121), font=title_font)

            # 小标题设置
            server_text = self.zone + " " + self.server
            server_text_width = slave_title_font.getlength(server_text)
            server_size_width = (images_width - server_text_width) / 2
            draw.text((server_size_width, 142 * flag), server_text, fill=(101, 109, 121), font=slave_title_font)

            # 信息标题
            draw.text((90 * flag, 230.5 * flag), '活动', fill=(0, 0, 0), font=info_title_font)
            draw.text((320 * flag, 230.5 * flag), '团长', fill=(0, 0, 0), font=info_title_font)
            draw.text((570 * flag, 230.5 * flag), '人数', fill=(0, 0, 0), font=info_title_font)
            draw.text((680 * flag, 230.5 * flag), '内容', fill=(0, 0, 0), font=info_title_font)
            draw.text((1180 * flag, 230.5 * flag), '时间', fill=(0, 0, 0), font=info_title_font)

            for floor, element in enumerate(data):
                activity = element.get("activity")
                leader = element.get("leader")
                number = element.get("number")
                max_number = element.get("maxNumber")
                content = element.get("content")
                create_time = element.get("createTime")

                # 招募活动的排列
                recruit_activity_x = 90 * flag
                recruit_activity_y = 281 * flag + floor * 45 * flag
                draw.text((recruit_activity_x, recruit_activity_y), activity, fill="black", font=font)

                # 招募团长的排列
                recruit_leader_x = 320 * flag
                recruit_leader_y = 281 * flag + floor * 45 * flag
                draw.text((recruit_leader_x, recruit_leader_y), leader, fill="black", font=font)

                # 招募人数的排列
                recruit_number_x = 570 * flag
                recruit_number_y = 281 * flag + floor * 45 * flag
                draw.text((recruit_number_x, recruit_number_y), f'{number}/{max_number}', fill="black", font=font)

                # 招募内容的排列
                recruit_content_x = 680 * flag
                recruit_content_y = 281 * flag + floor * 45 * flag
                draw.text((recruit_content_x, recruit_content_y), content, fill="black", font=font)

                # 招募时间添加
                recruit_time_x = 1180 * flag
                recruit_time_y = 281 * flag + floor * 45 * flag
                delta_time = int(time.time() - create_time)
                if delta_time < 60:
                    # 少于1分钟
                    war_time = f"{delta_time}秒前"
                elif delta_time < 3600:
                    # 少于1小时
                    delta_time //= 60
                    war_time = f"{delta_time}秒前"
                elif delta_time < 86400:
                    # 少于1天
                    delta_time //= 3600
                    war_time = f"{delta_time}小时前"
                else:
                    # 大于等于1天
                    delta_time //= 86400
                    war_time = f"{delta_time}天前"
                draw.text((recruit_time_x, recruit_time_y), war_time, font=font, fill="black")

            dpi = (1000, 1000)

            # # 保存图像
            buffer = BytesIO()
            buffer.seek(0)
            image.save(buffer, dpi=dpi, format='PNG')
            # image.save(f"images/record_image.png", dpi=dpi)
            return buffer

        except Exception as e:
            nonebot.logger.error(e)
            nonebot.logger.error("获取用户信息失败，请查看报错.")
            traceback.print_exc()
            return None
