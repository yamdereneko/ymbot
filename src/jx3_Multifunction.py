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
    response = await api.app_strategy(name=name)
    if response.code != 200:
        nonebot.logger.error("API接口get_strategy获取信息失败，请查看错误")
        return None
    return response.data


async def get_random():
    response = await api.app_random()
    if response.code != 200:
        nonebot.logger.error("API接口get_random获取信息失败，请查看错误")
        return None
    return response.data


async def get_require(name: str):
    response = await api.app_require(name=name)
    if response.code != 200:
        nonebot.logger.error("API接口get_require获取信息失败，请查看错误")
        return None
    return response.data


async def next_recruit(server: str, keyword: str):
    response = await api.next_recruit(server=server, keyword=keyword)
    print(response.json())
    if response.code != 200:
        nonebot.logger.error("API接口next_recruit获取信息失败，请查看错误")
        return None

    return response.data

asyncio.run(next_recruit('斗转星移','河阳'))


class Multifunction:
    def __init__(self):
        print('调用多功能场景')
