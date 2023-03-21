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
import nonebot
import src.Data.jxDatas as jxData
from src.internal.tuilanapi import API as tuilanAPI
from src.internal.jx3api import API as jx3API
from src.Data.database import DataBase as database
from PIL import ImageFont
from PIL import Image, ImageDraw

# 请求头
api = tuilanAPI()
jx3api = jx3API()


async def image_prospect(image):
    im2 = Image.new('RGBA', image.size, (255, 255, 255, 255))
    im2.paste(image, (0, 0), image)
    return im2


class GetPersonRecord:
    def __init__(self, role: str, server: str):
        config = jxData.config
        self.role = role
        self.server = jxData.mainServer(server)
        self.zone = jxData.mainZone(self.server)
        self.database = database(config)
        self.global_role_id = None

    async def get_person_record(self):
        response = await jx3api.data_role_roleInfo(server=self.server, name=self.role)
        if response.code != 200:
            nonebot.logger.error("API接口role_roleInfo获取信息失败，请查看错误")
            return None
        self.global_role_id = response.data['globalRoleId']

        response = await api.cc_mine_match_history(global_role_id=self.global_role_id, size=10, cursor=0)
        if response.data is []:
            nonebot.logger.error("API接口cc_mine_match_history获取信息失败，请查看错误")
            return None
        return response.data

    async def get_person_record_figure(self):
        data = await self.get_person_record()
        if data is None:
            return None

        # images = Image.open("src/images/record.png").convert("RGBA")
        flag = 2
        image = Image.new("RGB", (1363 * flag, 1063 * flag), "white").convert("RGBA")
        draw = ImageDraw.Draw(image)
        title_font = ImageFont.truetype("src/fonts/pingfang_bold.ttf", size=53 * flag)
        small_title_font = ImageFont.truetype("src/fonts/pingfang_regular.ttf", size=32 * flag)
        logo_font = ImageFont.truetype("src/fonts/pingfang_bold.ttf", size=18 * flag)
        data_title_font = ImageFont.truetype("src/fonts/pingfang_bold.ttf", size=26 * flag)
        title_color = (143, 151, 163)

        images_width, _ = image.size

        # logo
        draw.text((25 * flag, 20 * flag), 'YMNeko.', fill=(10, 0, 71), font=logo_font)

        # Set title
        title_text_width = title_font.getlength(self.role)
        title_width = (images_width - title_text_width) / 2
        draw.text((title_width, 38 * flag), self.role, font=title_font, fill=title_color)

        # Set Small title
        small_title_text_width = small_title_font.getlength(self.zone + " " + self.server)
        small_title_width = (images_width - small_title_text_width) / 2
        draw.text((small_title_width, 102 * flag), self.zone + " " + self.server, font=small_title_font, fill=title_color)

        # Set data title
        draw.line((0, 158 * flag, 1363 * flag, 158 * flag), fill=(143, 151, 163), width=2 * flag)

        draw.text((30.5 * flag, 181.7 * flag), '心法', font=data_title_font, fill=title_color)
        draw.text((141.75 * flag, 181.7 * flag), '段位', font=data_title_font, fill=title_color)
        draw.text((415 * flag, 181.7 * flag), '阵容', font=data_title_font, fill=title_color)
        draw.text((738.5 * flag, 181.7 * flag), '胜负', font=data_title_font, fill=title_color)
        draw.text((905.5 * flag, 181.7 * flag), '分数', font=data_title_font, fill=title_color)
        draw.text((1029 * flag, 181.7 * flag), '战斗时间', font=data_title_font, fill=title_color)
        draw.text((1219 * flag, 181.7 * flag), '时间', font=data_title_font, fill=title_color)

        draw.line((0, 239 * flag, 1363 * flag, 239 * flag), fill=(143, 151, 163), width=2 * flag)

        for floor, element in enumerate(data):
            won = element.get("won")
            kungfu = element.get("kungfu")
            avg_grade = element.get("avg_grade")
            mmr = element.get("mmr")
            total_mmr = element.get("total_mmr")
            start_time = element.get("start_time")
            end_time = element.get("end_time")

            # 心法图片的添加
            kungfu_image = await image_prospect(
                Image.open(f"src/images/KungfuIcon/{kungfu}.png").convert("RGBA").resize((41 * flag, 41 * flag)))
            kungfu_x = 37
            kungfu_y = 267
            image.paste(kungfu_image, (kungfu_x * flag, kungfu_y * flag + floor * 80 * flag))

            # 段位的添加
            avg_grade_font = ImageFont.truetype("src/fonts/pingfang_bold.ttf", size=25 * flag)
            avg_grade_font_color = (69, 75, 84)
            avg_grade_x = 152
            avg_grade_y = 269
            draw.text((avg_grade_x * flag, avg_grade_y * flag + floor * 80 * flag), str(avg_grade), font=avg_grade_font,
                      fill=avg_grade_font_color)

            # 阵容的添加
            team1 = {}
            team2 = {}
            match_id = element.get("match_id")
            response = await api.cc_mine_match_detail(match_id=match_id)
            for team_info in response.data.get("team1").get("players_info"):
                team1[team_info.get("role_name")] = team_info.get("kungfu")
            for team_info in response.data.get("team2").get("players_info"):
                team2[team_info.get("role_name")] = team_info.get("kungfu")
            if self.role in list(team1.keys()):
                prime_team = team1
                backup_team = team2
            elif self.role in list(team2.keys()):
                prime_team = team2
                backup_team = team1
            else:
                prime_team = None
                backup_team = None
            team_flag = 0
            # 主队伍
            prime_team_list = sorted(list(prime_team.values()), key=lambda x: 0 if x == kungfu else 1)
            for kungfu_team in prime_team_list:
                if kungfu_team in jxData.treat_pinyin:
                    rescue_image = await image_prospect(
                        Image.open(f"src/images/KungfuIcon/{kungfu_team}.png").convert("RGBA").resize((41 * flag, 41 * flag)))
                    rescue_x = 358
                    rescue_y = 265
                    image.paste(rescue_image, (rescue_x * flag, rescue_y * flag + floor * 80 * flag))
                else:
                    dps_image = await image_prospect(
                        Image.open(f"src/images/KungfuIcon/{kungfu_team}.png").convert("RGBA").resize((41 * flag, 41 * flag)))
                    dps_x = 260 + team_flag * 49
                    dps_y = 265
                    image.paste(dps_image, (dps_x * flag, dps_y * flag + floor * 80 * flag))
                    team_flag += 1
                vs_image = await image_prospect(
                    Image.open(f"src/images/VS.png").convert("RGBA").resize((41 * flag, 41 * flag)))
                image.paste(vs_image, (422 * flag, 264 * flag + floor * 80 * flag))

            # 副队伍
            team_flag = 0
            for kungfu_team in list(backup_team.values()):
                if kungfu_team in jxData.treat_pinyin:
                    rescue_image = await image_prospect(
                        Image.open(f"src/images/KungfuIcon/{kungfu_team}.png").convert("RGBA").resize((41 * flag, 41 * flag)))
                    rescue_x = 580
                    rescue_y = 265
                    image.paste(rescue_image, (rescue_x * flag, rescue_y * flag + floor * 80 * flag))
                else:
                    dps_image = await image_prospect(
                        Image.open(f"src/images/KungfuIcon/{kungfu_team}.png").convert("RGBA").resize((41 * flag, 41 * flag)))
                    dps_x = 482 + team_flag * 49
                    dps_y = 267
                    image.paste(dps_image, (dps_x * flag, dps_y * flag + floor * 80 * flag))
                    team_flag += 1
                # defeated_image = await image_prospect(
                #     Image.open(f"images/defeated.png").convert("RGBA").resize((16 * 4, 16 * 4)))
                won_image = await image_prospect(
                    Image.open(f"src/images/won.png").convert("RGBA").resize((16 * flag, 16 * flag)))
                if won is False:
                    # images.paste(defeated_image, (252 * 4, 100 * 4 + floor * 80 * 4))
                    image.paste(won_image, (616 * flag, 257 * flag + floor * 80 * flag))
                else:
                    image.paste(won_image, (252 * flag, 257 * flag + floor * 80 * flag))
                    # images.paste(defeated_image, (616 * 4, 100 * 4 + floor * 80 * 4))

            # 胜负添加
            won_font = ImageFont.truetype("src/fonts/pingfang_regular.ttf", size=25 * flag)
            won_font_color = (69, 75, 84)
            won_x = 726
            won_y = 270
            center = (699 * flag, 285 * flag + floor * 80 * flag)
            radius = 13

            if won is False:
                won_ellipse_color = 'red'
                won_text = "失败"
            else:
                won_ellipse_color = 'green'
                won_text = "胜利"
                mmr = "+" + str(mmr)
            draw.ellipse((center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius),
                         fill=won_ellipse_color)
            draw.text((won_x * flag, won_y * flag + floor * 80 * flag), won_text, font=won_font, fill=won_font_color)
            draw.text((789 * flag, won_y * flag + floor * 80 * flag), str(mmr), font=won_font, fill=won_font_color)

            # 分数添加
            draw.text((904 * flag, 270 * flag + floor * 80 * flag), str(total_mmr), font=won_font, fill=won_font_color)

            # 战斗时间添加
            seconds = time.mktime(time.localtime(end_time)) - time.mktime(time.localtime(start_time))
            expect_seconds = seconds % 60
            minutes = seconds // 60
            finally_time = f"{int(minutes)}分{int(expect_seconds)}秒"
            draw.text((1033 * flag, 270 * flag + floor * 80 * flag), finally_time, font=won_font, fill=won_font_color)

            # 计算时间戳是多少秒前的

            delta_time = int(time.time() - end_time)
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
            draw.text((1210 * flag, 270 * flag + floor * 80 * flag), war_time, font=won_font, fill=won_font_color)

        dpi = (1000, 1000)

        # # 保存图像
        datetime = int(time.time())
        image.save(f"/tmp/record_{datetime}.png", dpi=dpi)
        # image.save(f"images/record_image.png", dpi=dpi)
        # 使用系统默认的图像查看器显示图像
        return datetime
