import asyncio
import time
import traceback
from time import gmtime
import dufte
import nonebot
import matplotlib
import matplotlib.pyplot as plt
import src.Data.jxDatas as jxData
from src.Data.database import DataBase as database
import requests
import json
headers = jxData.headers

async def get_xsk(data=None):
    try:
        data = json.dumps(data)
        res = requests.post(url="https://www.jx3api.com/token/calculate", data=data).json()
        return res['data']['ts'], res['data']['sk']
    except Exception as e:
        nonebot.logger.error(e)
        nonebot.logger.error("get_xsk失败，请查看问题.")
        traceback.print_exc()


async def get_person_history(person_id):
    # 准备请求参数
    try:
        if person_id is None:
            nonebot.logger.error("person_id 未获取到，返回空")
            return None
        param = {'person_id': str(person_id), "size": 20, "cursor": 0}
        ts, xsk = await get_xsk(param)  # 获取ts和xsk， data 字典可以传ts,不传自动生成
        param['ts'] = ts  # 给参数字典赋值ts参数
        param = json.dumps(param).replace(" ", "")  # 记得格式化，参数需要提交原始json，非已格式化的json
        headers['X-Sk'] = xsk  # 修改请求中的xsk
        data = requests.post(url="https://m.pvp.xoyo.com/mine/match/person-history", data=param,
                             headers=headers).json()
        print(data)
        return data
    except Exception as e:
        nonebot.logger.error(e)
        nonebot.logger.error("获取用户信息失败，请查看问题.")
        traceback.print_exc()
        return None

asyncio.run(get_person_history("fccddb1df1b8401f81fded4640899fe6"))