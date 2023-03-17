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

        publication_type = 1
        on_sale_type = 2
        task_name = task.get('name')
        wangbaolou = WangBaoLouAPI()
        response = await wangbaolou.call_api(task_name, 0)

        # 定义字体
        master_title_font = ImageFont.truetype("src/fonts/pingfang_bold.ttf", size=24 * flag)
        slave_title_font = ImageFont.truetype("src/fonts/pingfang_bold.ttf", size=18 * flag)
        total_font = ImageFont.truetype("src/fonts/pingfang_bold.ttf", size=20 * flag)
        data_title_font = ImageFont.truetype("src/fonts/pingfang_bold.ttf", size=18 * flag)
        data_font = ImageFont.truetype("src/fonts/pingfang_regular.ttf", size=14 * flag)

        # 设置画布
        image = Image.new("RGB", (1043 * flag, 477 * flag + len(response.data.get('list')) * 56 * flag),
                          "white").convert("RGBA")
        draw = ImageDraw.Draw(image)
        image_width, _ = image.size

        # 标题设置
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        draw.text((24 * flag, 26 * flag), '物价', fill=(59, 62, 69), font=master_title_font)
        draw.text((24 * flag, 67 * flag), current_time, fill=(59, 62, 69), font=slave_title_font)

        # 图片生成
        url = task.get('view')
        res = await self.client.get(url=url, timeout=3000)
        title_image = await image_prospect(
            Image.open(BytesIO(res.content)).convert("RGBA").resize((459 * flag, 259 * flag)))
        image.paste(title_image, (442 * flag, 119 * flag))

        # 总数
        total = response.data.get('total_record')
        draw.text((28 * flag, 386 * flag), f"目前在楼总数: {total}", fill=(9, 44, 76), font=total_font)

        # 价格标题
        data_title_height = 449
        draw.text((55 * flag, data_title_height * flag), f"名字", fill=(59, 62, 69), font=data_title_font)
        draw.text((248.2 * flag, data_title_height * flag), f"价格", fill=(59, 62, 69), font=data_title_font)
        draw.text((441.4 * flag, data_title_height * flag), f"时间", fill=(59, 62, 69), font=data_title_font)
        draw.text((634.6 * flag, data_title_height * flag), f"状态", fill=(59, 62, 69), font=data_title_font)
        draw.text((827.8 * flag, data_title_height * flag), f"关注", fill=(59, 62, 69), font=data_title_font)

        for floor, element in enumerate(response.data.get('list')):
            single_unit_price = element.get('single_unit_price') // 100
            remaining_time = element.get('remaining_time')
            state = element.get('state')
            followed_num = element.get('followed_num')
            hours = remaining_time // 3600
            minutes = (remaining_time // 60) % 60

            task_name_bbox = data_font.getbbox(task_name)
            text_height = task_name_bbox[3] - task_name_bbox[1]

            text_y = 493 * flag + floor * 54 * flag
            line_text_y = text_y + text_height * flag

            draw.text((55 * flag, text_y), task_name, fill=(59, 62, 69), font=data_font)
            draw.text((248.2 * flag, text_y), str(single_unit_price), fill=(59, 62, 69), font=data_font)
            draw.text((441.4 * flag, text_y), f"{hours}小时{minutes}分钟", fill=(59, 62, 69), font=data_font)
            if state == 3:
                sale_state = "公示期"
            else:
                sale_state = "在售期"
            draw.text((634.6 * flag, text_y), sale_state, fill=(59, 62, 69), font=data_font)
            draw.text((827.8 * flag, text_y), str(followed_num), fill=(59, 62, 69), font=data_font)

            draw.line((39 * flag, line_text_y, 1015 * flag, line_text_y), width=2, fill=(220, 223, 227))

        dpi = (2000, 2000)
        # 保存图像
        datetime = int(time.time())
        image.save(f"/tmp/Price_{datetime}.png", dpi=dpi)
        # image.save(f"images/Price_Test.png", dpi=dpi)
        return datetime


# price = Price("狐金")
# asyncio.run(price.create_price_figure())
