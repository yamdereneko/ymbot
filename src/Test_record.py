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
from io import BytesIO
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

        images = Image.open("src/images/record.png").convert("RGBA")
        draw = ImageDraw.Draw(images)

        for floor, element in enumerate(data):
            print(element)
            won = element.get("won")
            kungfu = element.get("kungfu")
            avg_grade = element.get("avg_grade")
            mmr = element.get("mmr")
            total_mmr = element.get("total_mmr")
            start_time = element.get("start_time")
            end_time = element.get("end_time")

            # 心法图片的添加
            kungfu_image = await image_prospect(
                Image.open(f"src/images/KungfuIcon/{kungfu}.png").convert("RGBA").resize((41 * 4, 41 * 4)))
            kungfu_x = 37
            kungfu_y = 108
            images.paste(kungfu_image, (kungfu_x * 4, kungfu_y * 4 + floor * 80 * 4))

            # 段位的添加
            avg_grade_font = ImageFont.truetype("src/fonts/pingfang_bold.ttf", size=100)
            avg_grade_font_color = (69, 75, 84)
            avg_grade_x = 152
            avg_grade_y = 110
            draw.text((avg_grade_x * 4, avg_grade_y * 4 + floor * 80 * 4), str(avg_grade), font=avg_grade_font,
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
                        Image.open(f"src/images/KungfuIcon/{kungfu_team}.png").convert("RGBA").resize((41 * 4, 41 * 4)))
                    rescue_x = 358
                    rescue_y = 108
                    images.paste(rescue_image, (rescue_x * 4, rescue_y * 4 + floor * 80 * 4))
                else:
                    dps_image = await image_prospect(
                        Image.open(f"src/images/KungfuIcon/{kungfu_team}.png").convert("RGBA").resize((41 * 4, 41 * 4)))
                    dps_x = 260 + team_flag * 49
                    dps_y = 108
                    images.paste(dps_image, (dps_x * 4, dps_y * 4 + floor * 80 * 4))
                    team_flag += 1
                vs_image = await image_prospect(
                    Image.open(f"src/images/VS.png").convert("RGBA").resize((41 * 4, 41 * 4)))
                images.paste(vs_image, (422 * 4, 107 * 4 + floor * 80 * 4))

            # 副队伍
            team_flag = 0
            for kungfu_team in list(backup_team.values()):
                if kungfu_team in jxData.treat_pinyin:
                    rescue_image = await image_prospect(
                        Image.open(f"src/images/KungfuIcon/{kungfu_team}.png").convert("RGBA").resize((41 * 4, 41 * 4)))
                    rescue_x = 580
                    rescue_y = 108
                    images.paste(rescue_image, (rescue_x * 4, rescue_y * 4 + floor * 80 * 4))
                else:
                    dps_image = await image_prospect(
                        Image.open(f"src/images/KungfuIcon/{kungfu_team}.png").convert("RGBA").resize((41 * 4, 41 * 4)))
                    dps_x = 482 + team_flag * 49
                    dps_y = 108
                    images.paste(dps_image, (dps_x * 4, dps_y * 4 + floor * 80 * 4))
                    team_flag += 1
                # defeated_image = await image_prospect(
                #     Image.open(f"images/defeated.png").convert("RGBA").resize((16 * 4, 16 * 4)))
                won_image = await image_prospect(
                    Image.open(f"src/images/won.png").convert("RGBA").resize((16 * 4, 16 * 4)))
                if won is False:
                    # images.paste(defeated_image, (252 * 4, 100 * 4 + floor * 80 * 4))
                    images.paste(won_image, (616 * 4, 100 * 4 + floor * 80 * 4))
                else:
                    images.paste(won_image, (252 * 4, 100 * 4 + floor * 80 * 4))
                    # images.paste(defeated_image, (616 * 4, 100 * 4 + floor * 80 * 4))

            # 胜负添加
            won_ellipse_image = await image_prospect(
                Image.open(f"src/images/won_green_ellipse.png").convert("RGBA").resize((14 * 4, 14 * 4)))
            defeated_ellipse_image = await image_prospect(
                Image.open(f"src/images/defeated_red_ellipse.png").convert("RGBA").resize((14 * 4, 14 * 4)))
            won_font = ImageFont.truetype("src/fonts/pingfang_regular.ttf", size=100)
            won_font_color = (69, 75, 84)
            won_x = 726
            won_y = 111
            if won is False:
                images.paste(defeated_ellipse_image, (699 * 4, 121 * 4 + floor * 80 * 4))
                won_text = "失败"
            else:
                images.paste(won_ellipse_image, (699 * 4, 121 * 4 + floor * 80 * 4))
                won_text = "胜利"
                mmr = "+" + str(mmr)
            draw.text((won_x * 4, won_y * 4 + floor * 80 * 4), won_text, font=won_font, fill=won_font_color)
            draw.text((789 * 4, won_y * 4 + floor * 80 * 4), str(mmr), font=won_font, fill=won_font_color)

            # 分数添加
            draw.text((904 * 4, 111 * 4 + floor * 80 * 4), str(total_mmr), font=won_font, fill=won_font_color)

            # 战斗时间添加
            seconds = time.mktime(time.localtime(end_time)) - time.mktime(time.localtime(start_time))
            expect_seconds = seconds % 60
            minutes = seconds // 60
            finally_time = f"{int(minutes)}分{int(expect_seconds)}秒"
            draw.text((1033 * 4, 111 * 4 + floor * 80 * 4), finally_time, font=won_font, fill=won_font_color)

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
            draw.text((1210 * 4, 111 * 4 + floor * 80 * 4), war_time, font=won_font, fill=won_font_color)
            print("**" * 20)

        dpi = (1000, 1000)

        # # 保存图像
        datetime = int(time.time())
        images.save(f"/tmp/record_{datetime}.png", dpi=dpi)

        # 使用系统默认的图像查看器显示图像
        return datetime
