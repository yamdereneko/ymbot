# -*- coding: utf-8 -*-

"""
@Software : PyCharm
@File : 0.py
@Author : 喵
@Time : 2021/09/29 22:39:29
@Docs : 骚话
"""
import asyncio

import nonebot
from src.internal.jx3api import API

# 请求头
api = API()


async def get_strategy(name: str):
    response = await api.data_lucky_strategy(name=name)
    if response.code != 200:
        nonebot.logger.error("API接口get_strategy获取信息失败，请查看错误")
        return None
    return response.data


async def get_random():
    response = await api.data_chat_random()
    if response.code != 200:
        nonebot.logger.error("API接口get_random获取信息失败，请查看错误")
        return None
    return response.data


async def get_require(name: str):
    response = await api.data_lucky_require(name=name)
    if response.code != 200:
        nonebot.logger.error("API接口get_require获取信息失败，请查看错误")
        return None
    return response.data


async def get_flatterer():
    response = await api.data_useless_flatterer()
    if response.code != 200:
        nonebot.logger.error("API接口data_useless_flatterer获取信息失败，请查看错误")
        return None
    return response.data


async def get_announce():
    response = await api.data_web_announce()
    if response.code != 200:
        nonebot.logger.error("API接口data_web_announce获取信息失败，请查看错误")
        return None
    return response.data


async def get_sand_map(server: str):
    response = await api.view_sand_search(server=server)
    if response.code != 200:
        nonebot.logger.error("API接口get_sand_map获取信息失败，请查看错误")
        return None
    return response.data


async def get_chutianshe():
    response = await api.data_active_chutianshe()
    if response.code != 200:
        nonebot.logger.error("API接口data_active_chutianshe获取信息失败，请查看错误")
        return None
    text_now_list = ["目前", "地图：" + response.data['now']['map'], "名称：" + response.data['now']['name'],
                     "地点：" + response.data['now']['site'], "任务：" + response.data['now']['desc'],
                     "任务内容：" + response.data['now']['tasks'],
                     "时间：" + response.data['now']['time'],
                     "接下来", "地图：" + response.data['next']['map'],
                     "名称：" + response.data['next']['name'],
                     "地点：" + response.data['next']['site'], "任务：" + response.data['next']['desc'],
                     "任务内容：" + response.data['next']['tasks'],
                     "时间：" + response.data['next']['time']]
    text_now = '\n'.join(text_now_list)
    return text_now


class Multifunction:
    def __init__(self):
        print('调用多功能场景')
