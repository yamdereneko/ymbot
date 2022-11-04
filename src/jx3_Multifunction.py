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


class Multifunction:
    def __init__(self):
        print('调用多功能场景')