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
            # print(response)
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

    async def circle_corner(self, img, radii):
        # 画圆（用于分离4个角）
        circle = Image.new('L', (radii * 2, radii * 2), 0)  # 创建黑色方形
        # circle.save('1.jpg','JPEG',qulity=100)
        draw = ImageDraw.Draw(circle)
        draw.ellipse((0, 0, radii * 2, radii * 2), fill=255)  # 黑色方形内切白色圆形
        # circle.save('2.jpg','JPEG',qulity=100)

        # 原图转为带有alpha通道（表示透明程度）
        img = img.convert("RGBA")
        w, h = img.size

        # 画4个角（将整圆分离为4个部分）
        alpha = Image.new('L', img.size, 255)  # 与img同大小的白色矩形，L 表示黑白图
        # alpha.save('3.jpg','JPEG',qulity=100)
        alpha.paste(circle.crop((0, 0, radii, radii)), (0, 0))  # 左上角
        alpha.paste(circle.crop((radii, 0, radii * 2, radii)), (w - radii, 0))  # 右上角
        alpha.paste(circle.crop((radii, radii, radii * 2, radii * 2)), (w - radii, h - radii))  # 右下角
        alpha.paste(circle.crop((0, radii, radii, radii * 2)), (0, h - radii))  # 左下角
        # alpha.save('4.jpg','JPEG',qulity=100)

        img.putalpha(alpha)  # 白色区域透明可见，黑色区域不可见

        return img

    async def create_images(self):
        data = await self.equips()
        if data is None:
            return None
        kungfu = data.get("Kungfu").get("Name")
        equip_score = data.get("MatchDetail").get("score")

        equip_treat = 0

        if kungfu in jxData.treat_pinyin.keys():
            images = Image.open("src/images/equip_treat.jpg").convert("RGBA")
            equip_treat = 1
        else:
            images = Image.open("src/images/equip.jpg").convert("RGBA")

        # 大区以及主大区
        main_zone = jxData.mainZone(self.server)
        main_server = jxData.mainServer(self.server)

        # 给心法图标去背景
        kungfu_image = Image.open(f"src/images/KungfuIcon/{kungfu}.png").convert("RGBA").resize((54 * 4, 54 * 4))
        im2 = Image.new('RGBA', kungfu_image.size, (242, 246, 255, 255))
        im2.paste(kungfu_image, (0, 0), kungfu_image)
        images.paste(im2, (291 * 4, 53 * 4))

        # 创建一个可绘制的对象
        draw = ImageDraw.Draw(images)

        # 定义要添加的文本和字体
        font = ImageFont.truetype("src/fonts/pingfang_regular.ttf", size=60)
        src_font = ImageFont.truetype("src/fonts/pingfang_bold.ttf", size=120)
        equip_score_font = ImageFont.truetype("src/fonts/pingfang_bold.ttf", size=84)
        title_font = ImageFont.truetype("src/fonts/pingfang_regular.ttf", size=68)

        # 指定文本的颜色为黑色
        fill_color = (0, 0, 0)

        flag = 0
        kind_flag = 0

        # 标题 名字
        title_color = (61, 62, 66)
        draw.text((356 * 4, 43 * 4), self.role, font=src_font, fill=title_color)
        draw.text((356 * 4, 82 * 4), main_zone + " " + main_server, font=title_font, fill=title_color)

        # 装备分数
        draw.text((105 * 4, 515 * 4), str(equip_score), font=equip_score_font, fill=fill_color)

        for equip in data['Equips']:
            equips_name = equip.get('Name')
            quality = equip.get('Quality')
            sub_kind = equip.get("Icon").get("SubKind")
            equip_url = equip.get("Icon").get("FileName")

            if equip.get("Icon").get("Kind") == "武器" or equip.get("Icon").get("Kind") == "任务特殊" and kind_flag == 0:
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

            width = 46 * 4
            height = 46 * 4
            overlay_image = await self.circle_corner(Image.open(BytesIO(response.read())).resize((width, height)), 40)

            match sub_kind:
                case "帽子":
                    x = 81 * 4
                    y = 572 * 4
                case "护臂":
                    x = 313 * 4
                    y = 572 * 4
                case "项链":
                    x = 545 * 4
                    y = 572 * 4

                case "上衣":
                    x = 81 * 4
                    y = 637 * 4
                case "裤子":
                    x = 313 * 4
                    y = 637 * 4
                case "腰坠":
                    x = 545 * 4
                    y = 637 * 4

                case "腰带":
                    x = 81 * 4
                    y = 702 * 4
                case "鞋":
                    x = 313 * 4
                    y = 702 * 4
                case "戒指1":
                    x = 545 * 4
                    y = 702 * 4

                case x if "囊" in x:
                    x = 81 * 4
                    y = 767 * 4
                case "武器":
                    x = 313 * 4
                    y = 767 * 4
                case "戒指2":
                    x = 545 * 4
                    y = 767 * 4
                case _:
                    x = 0
                    y = 0
                    equips_name = ""
                    quality = ""

            # images.paste(overlay_image, (x, y))
            image1 = Image.new('RGBA', overlay_image.size, (242, 246, 255, 255))
            image1.paste(overlay_image, (0, 0), overlay_image)
            images.paste(image1, (x, y))

            draw.text((x + 58 * 4, y), equips_name, font=font, fill=fill_color)
            draw.text((x + 58 * 4, y + 26 * 4), quality, font=font, fill=fill_color)

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
                    x = 141 * 4
                    y = 215 * 4
                case "攻击力":
                    x = 371 * 4
                    y = 215 * 4

                case "基础攻击力":
                    x = 606 * 4
                    y = 215 * 4
                case "治疗量":
                    x = 371 * 4
                    y = 215 * 4

                case "会心":
                    x = 141 * 4
                    y = 277 * 4
                case "会心效果":
                    x = 371 * 4
                    y = 277 * 4
                case "破防":
                    x = 606 * 4
                    y = 277 * 4

                case "加速":
                    if equip_treat == 1:
                        x = 606 * 4
                        y = 277 * 4
                    else:
                        x = 141 * 4
                        y = 341 * 4
                case "破招":
                    if equip_treat == 1:
                        x = 606 * 4
                        y = 341 * 4
                    else:
                        x = 371 * 4
                        y = 341 * 4
                case "无双":
                    x = 606 * 4
                    y = 341 * 4

                case "根骨" | "身法" | "元气" | "力道":
                    if equip_treat == 1:
                        x = 606 * 4
                        y = 215 * 4
                    else:
                        x = 141 * 4
                        y = 405 * 4
                case "化劲":
                    if equip_treat == 1:
                        x = 141 * 4
                        y = 341 * 4
                    else:
                        x = 371 * 4
                        y = 405 * 4
                case "御劲":
                    if equip_treat == 1:
                        x = 371 * 4
                        y = 341 * 4
                    else:
                        x = 606 * 4
                        y = 405 * 4
                case _:
                    panel_name = ""
                    panel_value = ""
                    x = 0
                    y = 0

            draw.text((x, y), panel_name, font=font, fill=fill_color)
            draw.text((x, y + 27 * 4), panel_value, font=font, fill=fill_color)

        dpi = (2000, 2000)

        # 将文本添加到图像中

        # # 保存图像
        datetime = int(time.time())
        images.save(f"/tmp/equip_image_{datetime}.png", dpi=dpi)

        # 使用系统默认的图像查看器显示图像
        return datetime
