# -*- coding: utf-8 -*-
"""
@Software : PyCharm
@File : 0.py
@Author : 喵
@Time : 2021/09/29 22:39:29
@Docs : 请求推栏战绩例子
"""
from websockets.exceptions import ConnectionClosedError, ConnectionClosedOK, ConnectionClosed
import websockets
import asyncio
import json
import src.Data.jxDatas as jxData
from src.Data.database import DataBase


async def f1001(data):
    config = jxData.config
    database = DataBase(config)
    await database.connect()
    # 插入数据
    sql = "INSERT INTO `Adventure_History` (`zone`, `server`, `name`, `serendipity`, `level`, `time`) VALUES (%s, %s, %s, %s, %s, %s) "
    await database.execute(sql, (
        data["data"]["zone"], data["data"]["server"],
        data["data"]["name"], data["data"]["serendipity"],
        data["data"]["level"], data["data"]["time"]))
    return


async def f2002(data):

    return


class WebSocket:
    def __init__(self):
        self.title = "WebSocket"
        self.count = 0
        self.handler = {
            1001: f1001,  # 连接成功
            2002: f2002,
        }

    async def connect(self, loop):
        while True:
            try:
                ws = await websockets.connect('wss://socket.nicemoe.cn', extra_headers={
                    'token': '5f2143314ebbec94b7aa80f7fd295856b03e567358a4f966fcbe597949e985e8'})
                print(f'{self.title} > 建立连接成功！')
                return loop.create_task(self.task(loop, ws))  # 创建数据接收任务
            except (ConnectionRefusedError, OSError, asyncio.exceptions.TimeoutError) as echo:  # 异常捕获
                print(f"{self.title} > [{self.count}] {echo}")
                if self.count >= 100: return  # 退出连接
                self.count += 1  # 统计连接次数
                print(f"{self.title} < [{self.count}] 开始尝试向 WebSocket 服务端建立连接！")
                await asyncio.sleep(10)  # 重连间隔

    async def task(self, loop, ws):
        try:
            while True:
                data = await ws.recv()  # 循环接收
                print(f"WebSocket > {data}")
                data = json.loads(data)
                if data['action'] in self.handler.keys():
                    loop.create_task(self.handler[data['action']](data))  # 创建分发任务
                await asyncio.sleep(0.1)  # 每条消息进行一次睡眠，给服务器一点尊重
        except (ConnectionClosedError, ConnectionClosedOK, ConnectionClosed) as echo:  # 异常捕获
            if echo.code == 1000:  # 代码 1000 服务端正常关闭连接(关闭帧)
                print(f"{self.title} > 连接被关闭！")  # 服务端主动关闭
            else:  # 非正常关闭
                print(f"{self.title} > 连接已断开！")  # 服务端内部错误
                loop.create_task(self.connect(loop))  # 创建重连任务
            print(echo)  # 打印错误代码


if __name__ == '__main__':
    client = WebSocket()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(client.connect(loop))
    loop.run_forever()
