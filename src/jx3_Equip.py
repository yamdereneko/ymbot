# -*- coding: utf-8 -*
"""
@Software : PyCharm
@File : 0.py
@Author : 喵
@Time : 2021/09/29 22:39:29
@Docs : 请求推栏战绩例子
"""
import asyncio
import time
import traceback
import httpx
import nonebot
import src.Data.jxDatas as jxData
from src.Data.database import DataBase as database
from src.internal.tuilanapi import API
from src.internal.jx3api import API as jx3API
from rich import print
from PIL import ImageFont
from io import BytesIO
from PIL import Image, ImageDraw

# 请求头

api = API()
jx3api = jx3API()


class GetRoleEquip:
    def __init__(self, server: str, role: str):
        config = jxData.config
        self.role = role
        self.server = jxData.mainServer(server)
        self.zone = jxData.mainZone(self.server)
        self.database = database(config)
        self.role_id = None
        self.person_id = None
        self.role_name = None
        self.globalRoleId = None

    async def equips(self):
        try:
            response = await jx3api.data_role_roleInfo(server=self.server, name=self.role)
            if response.code != 200:
                nonebot.logger.error("API接口role_roleInfo获取信息失败，请查看错误")
                return None
            #print(response)
            self.globalRoleId = response.data["globalRoleId"]
            self.role_id = response.data["roleId"]
            response = await api.role_indicator(role_id=self.role_id, server=self.server, zone=self.zone)
            if response.code != 0:
                nonebot.logger.error("API接口role_indicator获取信息失败，请查看错误")
                return None
            # print(response)

            self.person_id = response.data['person_info']['person_id']

            # response = await api.mine_match_person9history(person_id=str(self.person_id), size=10, cursor=0)
            # if response.code != 0:
            #     nonebot.logger.error("API接口Daily获取信息失败，请查看错误")
            #     return None
            # print(response.data)
            # # self.role_id = response.data[0]["role_id"]
            # self.server = response.data[0]["server"]
            # self.zone = response.data[0]["zone"]
            # print(response)

            # print('==' * 50)
            response = await api.mine_equip_get9role9equip(game_role_id=self.role_id, server=self.server,
                                                           zone=self.zone)
            if response.code != 0:
                nonebot.logger.error("API接口mine_equip_get9role9equip获取信息失败，请查看错误")
                return None
            return response.data

        except Exception as e:
            nonebot.logger.error(e)
            nonebot.logger.error("获取用户信息失败，请查看问题.")
            traceback.print_exc()
            return None

    async def create_images(self):
        data = await self.equips()
        if data is None:
            return None
        kungfu = data.get("Kungfu").get("Name")
        equip_score = data.get("MatchDetail").get("score")
        images = Image.open("src/images/equip.jpg").convert("RGBA")
        kungfu_image = Image.open(f"src/images/KungfuIcon/{kungfu}.png").convert("RGBA").resize((48 * 4, 48 * 4))

        im2 = Image.new('RGBA', kungfu_image.size, (242, 246, 255, 255))
        im2.paste(kungfu_image, (0, 0), kungfu_image)
        images.paste(im2, (280 * 4, 40 * 4))

        # 创建一个可绘制的对象
        draw = ImageDraw.Draw(images)

        # 定义要添加的文本和字体
        font = ImageFont.truetype("src/fonts/pingfang_regular.ttf", size=55)
        src_font = ImageFont.truetype("src/fonts/pingfang_bold.ttf", size=100)
        equip_score_font = ImageFont.truetype("src/fonts/pingfang_bold.ttf", size=54)

        # 指定文本的颜色为红色
        fill_color = (0, 0, 0)

        flag = 0
        kind_flag = 0

        # 标题 名字
        draw.text((337 * 4, 47 * 4), self.role, font=src_font, fill=fill_color)

        # 装备分数
        draw.text((136 * 4, 472 * 4), str(equip_score), font=equip_score_font, fill=fill_color)

        for equip in data['Equips']:
            equips_name = equip.get('Name')
            quality = equip.get('Quality')
            sub_kind = equip.get("Icon").get("SubKind")
            equip_url = equip.get("Icon").get("FileName")

            if equip.get("Icon").get("Kind") == "武器" and kind_flag == 0:
                if "囊" in sub_kind:
                    print(1)
                else:
                    sub_kind = "武器"
                    kind_flag = 1

            if sub_kind == "戒指" and flag == 0:
                sub_kind = "戒指1"
                flag = 1
            elif sub_kind == "戒指" and flag == 1:
                sub_kind = "戒指2"

            response = httpx.get(equip_url)

            width = 40 * 4
            height = 40 * 4
            overlay_image = Image.open(BytesIO(response.read())).resize((width, height))

            match sub_kind:
                case "帽子":
                    x = 101 * 4
                    y = 543 * 4
                case "护臂":
                    x = 342 * 4
                    y = 543 * 4
                case "项链":
                    x = 583 * 4
                    y = 543 * 4

                case "上衣":
                    x = 101 * 4
                    y = 608 * 4
                case "裤子":
                    x = 342 * 4
                    y = 608 * 4
                case "腰坠":
                    x = 583 * 4
                    y = 608 * 4

                case "腰带":
                    x = 101 * 4
                    y = 674 * 4
                case "鞋":
                    x = 342 * 4
                    y = 674 * 4
                case "戒指1":
                    x = 583 * 4
                    y = 674 * 4

                case x if "囊" in x:
                    x = 101 * 4
                    y = 739 * 4
                case "武器":
                    x = 342 * 4
                    y = 739 * 4
                case "戒指2":
                    x = 583 * 4
                    y = 739 * 4
                case _:
                    x = 0
                    y = 0
                    equips_name = ""
                    quality = ""

            draw.text((x, y), equips_name, font=font, fill=fill_color)
            draw.text((x, y + 25 * 4), quality, font=font, fill=fill_color)
            images.paste(overlay_image, (x - 52 * 4, y + 4 * 4))

            # source = equip.get('equipBelongs')
            # if source is None:
            #     source = "未知"
            # else:
            #     source = [i.get("source") for i in equip.get('equipBelongs')]
            # print("来源: " + ''.join(source))
            # print(("属性: \n" + '\n'.join([i.get("Attrib").get("GeneratedMagic") for i in equip.get("ModifyType")])))

        personal_panel = data['PersonalPanel']
        for element in personal_panel:
            panel_name = element.get("name")
            panel_value = str(element.get("value"))
            match panel_name:
                case "气血":
                    x = 140 * 4
                    y = 166 * 4
                case "攻击力":
                    x = 340 * 4
                    y = 166 * 4
                case "基础攻击力":
                    x = 540 * 4
                    y = 166 * 4
                case "会心":
                    x = 140 * 4
                    y = 230 * 4
                case "会心效果":
                    x = 340 * 4
                    y = 230 * 4
                case "破防":
                    x = 540 * 4
                    y = 230 * 4
                case "加速":
                    x = 140 * 4
                    y = 295 * 4
                case "破招":
                    x = 340 * 4
                    y = 295 * 4
                case "无双":
                    x = 540 * 4
                    y = 295 * 4
                case "根骨" | "身法" | "元气" | "力道":
                    x = 140 * 4
                    y = 359 * 4
                case "化劲":
                    x = 340 * 4
                    y = 359 * 4
                case "御劲":
                    x = 540 * 4
                    y = 359 * 4
                case _:
                    panel_name = ""
                    panel_value = ""
                    x = 0
                    y = 0

            draw.text((x, y), panel_name, font=font, fill=fill_color)
            draw.text((x, y + 25 * 4), panel_value, font=font, fill=fill_color)

        dpi = (2000, 2000)

        # 将文本添加到图像中

        # # 保存图像
        datetime = int(time.time())
        images.save(f"/tmp/equip_image_{datetime}.png", dpi=dpi)

        # 使用系统默认的图像查看器显示图像
        return datetime
