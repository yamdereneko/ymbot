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
import time

import nonebot
from nonebot import get_driver
from nonebot.message import handle_event
import websockets
from nonebot.adapters.onebot.v11 import Bot, MessageSegment
from typing import Optional
from websockets.legacy.client import WebSocketClientProtocol
import src.Data.jxDatas as jxData
from src.Data.database import DataBase
from nonebot import get_bots
from websockets.exceptions import ConnectionClosedError, ConnectionClosedOK
from .jx3_event import WsData, WsNotice
import src.Data.jx3_Redis as redis
from ..brower import browser

driver = get_driver()


async def f1001(data):
    config = jxData.config
    database = DataBase(config)
    await database.connect()
    # 插入数据
    adventure_id = data["data"]["name"]
    adventure_serendipity = data["data"]["serendipity"]
    adventure_time = data["data"]["time"]
    sql = "INSERT INTO `Adventure_History` (`zone`, `server`, `name`, `serendipity`, `level`, `time`) VALUES (%s, %s, %s, %s, %s, %s) "
    await database.execute(sql, (
        data["data"]["zone"], data["data"]["server"],
        adventure_id, adventure_serendipity,
        data["data"]["level"], adventure_time))
    bot, = get_bots().values()
    start_time = time.strftime("%H:%M", time.localtime(adventure_time))
    msg = MessageSegment.text(f'{adventure_id} {start_time} 触发了 {adventure_serendipity}!')
    red = redis.Redis()
    group_list = await red.query_list("group_list")
    for group_id in group_list:
        await bot.send_group_msg(group_id=group_id, message=msg)


async def f2001(data):
    bot, = get_bots().values()
    if data['data']['server'] == jxData.server_binding:
        close_time = time.strftime("%H点%M分", time.localtime(data['data']['time']))
        if data['data']['status'] == 0:
            msg = MessageSegment.text(f'{jxData.server_binding} 在 {close_time}关服了,睡觉吧！')
        elif data['data']['status'] == 1:
            msg = MessageSegment.text(f'{jxData.server_binding} 在 {close_time} 开服了,快冲！')
        else:
            msg = MessageSegment.text(f'开服报错了，看下报错！')
        red = redis.Redis()
        group_list = await red.query_list("group_list")
        for group_id in group_list:
            await bot.send_group_msg(group_id=group_id, message=msg)


async def f2002(data):
    bot, = get_bots().values()
    url = data["data"]['url']
    announce_title = data["data"]['title']
    text = data["data"]['type'] + '\n' + announce_title + '\n' + url
    image = await browser.get_image_from_url(url)
    msg = MessageSegment.image(image)
    red = redis.Redis()
    group_list = await red.query_list("group_list")
    for group_id in group_list:
        await bot.send_group_msg(group_id=group_id, message=text + msg)


class WebSocket:
    connect: Optional[WebSocketClientProtocol] = None
    """ws链接"""
    is_connecting: bool = False

    def __init__(self):
        self.title = "jx3api的ws服务器"
        self.count = 0
        self.handler = {
            1001: f1001,  # 连接成功
            2002: f2002,
            2001: f2001
        }

    def __new__(cls, *args, **kwargs):
        """单例"""
        if not hasattr(cls, "_instance"):
            orig = super(WebSocket, cls)
            cls._instance = orig.__new__(cls, *args, **kwargs)
        return cls._instance

    """是否正在连接"""

    async def init(self) -> Optional[bool]:
        while True:
            try:
                ws_path = jxData.Jx3ApiConfig().ws_path
                ws_token = jxData.Jx3ApiConfig().ws_token
                if ws_token is None:
                    ws_token = ""
                headers = {"token": ws_token}
                # ws = await websocket.Connect(ws_path.ws_path, extra_headers=header)
                nonebot.logger.debug(f"<g>ws_server</g> | 正在链接jx3api的ws服务器：{ws_path}")
                self.is_connecting = True
                for i in range(1, 101):
                    try:
                        nonebot.logger.debug(f"<g>ws_server</g> | 正在开始第 {i} 次尝试")
                        self.connect = await websockets.connect(
                            uri=ws_path,
                            extra_headers=headers,
                            ping_interval=20,
                            ping_timeout=20,
                            close_timeout=10
                        )
                        asyncio.create_task(self._task())
                        nonebot.logger.debug("<g>ws_server</g> | ws连接成功！")
                        # await self._raise_notice("jx3api > ws已连接！")
                        break
                    except Exception as e:
                        nonebot.logger.error(f"<r>链接到ws服务器时发生错误：{str(e)}</r>")
                        await asyncio.sleep(1)

                self.is_connecting = False
                if not self.connect:
                    # 未连接成功，发送消息给bot，如果有
                    self.connect = None
                    await self._raise_notice("jx3api > ws服务器连接失败，请查看日志或者重连。")
                    return False
                return True

            except (ConnectionRefusedError, OSError, asyncio.exceptions.TimeoutError) as echo:  # 异常捕获
                nonebot.logger.info(f"{self.title} > [{self.count}] {echo}")
                if self.count >= 100: return  # 退出连接
                self.count += 1  # 统计连接次数
                nonebot.logger.info(f"{self.title} < [{self.count}] 开始尝试向 WebSocket 服务端建立连接！")
                await asyncio.sleep(10)  # 重连间隔

    async def _raise_notice(self, message: str):
        """
        说明:
            抛出ws通知事件给机器人

        参数:
            * `message`：通知内容
        """
        event = WsNotice(message=message)
        bots = get_bots()
        for _, one_bot in bots.items():
            await handle_event(one_bot, event)

    async def _task(self):
        try:
            while True:
                data = await self.connect.recv()  # 循环接收
                nonebot.logger.info(f"WebSocket > {data}")
                data = json.loads(data)
                if data['action'] in self.handler.keys():
                    asyncio.create_task(self.handler[data['action']](data))  # 创建分发任务
                await asyncio.sleep(0.1)  # 每条消息进行一次睡眠，给服务器一点尊重
        except ConnectionClosedOK:
            nonebot.logger.debug("<g>jx3api > ws链接已主动关闭！</g>")
            self.connect = None
            await self._raise_notice("jx3api > ws已正常关闭！")

        except ConnectionClosedError as e:
            nonebot.logger.error(f"<r>jx3api > ws链接异常关闭：{e.reason}</r>")
            # 自启动
            self.connect = None
            await self.init()

    async def close(self):
        """关闭ws链接"""
        if self.connect:
            await self.connect.close()
            self.connect = None

    @property
    def closed(self) -> bool:
        """ws是否关闭"""
        if self.connect:
            return self.connect.closed
        return True


ws_client = WebSocket()
