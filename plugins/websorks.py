# -*- coding: utf-8 -*-
"""
@Software : PyCharm
@File : 0.py
@Author : 喵
@Time : 2021/09/29 22:39:29
@Docs : websocket
"""
import asyncio
import json
import nonebot
from nonebot import get_driver, on, on_regex
import nonebot.drivers.websockets as websocket
from nonebot.adapters.onebot.v11 import Bot, MessageSegment
import src.Data.jxDatas as jxData
from src.Data.database import DataBase
from nonebot import get_bots
from src.Data.jxDatas import group_list
from websockets.exceptions import ConnectionClosedError, ConnectionClosedOK, ConnectionClosed

driver = get_driver()


async def f1001(data):
    config = jxData.config
    database = DataBase(config)
    await database.connect()
    # 插入数据
    adventure_id = data["data"]["name"]
    adventure_serendipity = data["data"]["serendipity"]
    sql = "INSERT INTO `Adventure_History` (`zone`, `server`, `name`, `serendipity`, `level`, `time`) VALUES (%s, %s, %s, %s, %s, %s) "
    await database.execute(sql, (
        data["data"]["zone"], data["data"]["server"],
        adventure_id, adventure_serendipity,
        data["data"]["level"], data["data"]["time"]))
    bot, = get_bots().values()
    msg = MessageSegment.text(f'{adventure_id}触发了{adventure_serendipity}')

    for group_id in group_list:
        await bot.send_group_msg(group_id=group_id, message=msg)


async def f2001(data):
    bot, = get_bots().values()
    if data['data']['server'] == jxData.server_binding:
        msg = MessageSegment.text(f'{jxData.server_binding}开服了,快冲！')
        for group_id in group_list:
            await bot.send_group_msg(group_id=group_id, message=msg)


async def f2002(data):
    bot, = get_bots().values()
    text = data["data"]['type'] + '\n' + data["data"]['title'] + '\n' + data["data"]['url']
    msg = MessageSegment.text(text)
    for group_id in group_list:
        await bot.send_group_msg(group_id=group_id, message=msg)


class WebSocket:
    def __init__(self):
        self.title = "jx3api的ws服务器"
        self.count = 0
        self.handler = {
            # 1001: f1001,  # 连接成功
            2002: f2002,
            2001: f2001
        }

    async def connect(self):
        while True:
            try:
                ws_path = jxData.Jx3ApiConfig()
                header = {'token': ws_path.ws_token}
                ws = await websocket.Connect(ws_path.ws_path, extra_headers=header)
                nonebot.logger.info(f'{self.title} > 建立连接成功！')
                return asyncio.create_task(self.task(ws))  # 创建数据接收任务
            except (ConnectionRefusedError, OSError, asyncio.exceptions.TimeoutError) as echo:  # 异常捕获
                nonebot.logger.info(f"{self.title} > [{self.count}] {echo}")
                if self.count >= 100: return  # 退出连接
                self.count += 1  # 统计连接次数
                nonebot.logger.info(f"{self.title} < [{self.count}] 开始尝试向 WebSocket 服务端建立连接！")
                await asyncio.sleep(10)  # 重连间隔

    async def task(self, ws):
        try:
            while True:
                data = await ws.recv()  # 循环接收
                nonebot.logger.info(f"WebSocket > {data}")
                data = json.loads(data)
                if data['action'] in self.handler.keys():
                    asyncio.create_task(self.handler[data['action']](data))  # 创建分发任务
                await asyncio.sleep(0.1)  # 每条消息进行一次睡眠，给服务器一点尊重
        except (ConnectionClosedError, ConnectionClosedOK, ConnectionClosed) as echo:  # 异常捕获
            if echo.code == 1000:  # 代码 1000 服务端正常关闭连接(关闭帧)
                nonebot.logger.info(f"{self.title} > 连接被关闭！")  # 服务端主动关闭
            else:  # 非正常关闭
                nonebot.logger.info(f"{self.title} > 连接已断开！")  # 服务端内部错误
                asyncio.create_task(self.connect())  # 创建重连任务
            nonebot.logger.info(echo)  # 打印错误代码


ws_client = WebSocket()


async def ws_init():
    """初始化连接ws服务器"""
    nonebot.logger.info("正在链接jx3api的ws服务器...")
    flag = await ws_client.connect()
    if flag:
        nonebot.logger.info("jx3api的ws服务器已链接。")
    else:
        nonebot.logger.info("jx3api的ws服务器连接失败！")


@driver.on_startup
async def _():
    """等定时插件和数据加载完毕后"""
    nonebot.logger.info("<g>正在初始化WS...</g>")
    asyncio.create_task(ws_init())
    # scheduler.add_job(func=ws_init, next_run_time=datetime.now() + timedelta(seconds=2))
