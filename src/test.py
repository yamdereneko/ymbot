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
from src.internal.tuilanapi import API
from src.internal.jx3api import API as jx3API
from src.Data.jxDatas import all_school, much_school, school_pinyin, config
from src.Data.database import DataBase as database
api = API()


response = asyncio.run(api.cc_mine_arena_top200(typeName='week', tag=45, heiMaBang=False))
print(response)