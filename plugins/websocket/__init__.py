# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
"""
@Software : PyCharm
@File : 0.py
@Author : 喵
@Time : 2021/09/29 22:39:29
@Docs : websocket
"""
import asyncio
import nonebot
from nonebot import get_driver, on_regex
from nonebot.adapters.onebot.v11 import PrivateMessageEvent, MessageSegment
from nonebot.permission import SUPERUSER
from .jx3_websocket import ws_client


driver = get_driver()

check_ws = on_regex(pattern=r"^查看连接$",  priority=2, block=True)
connect_ws = on_regex(pattern=r"^连接服务$",  priority=2, block=True)
close_ws = on_regex(pattern=r"^关闭连接$", priority=2, block=True)


async def ws_init():
    """初始化连接ws服务器"""
    nonebot.logger.info("正在链接jx3api的ws服务器...")
    flag = await ws_client.init()
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


@check_ws.handle()
async def _(event: PrivateMessageEvent):
    """查看连接"""
    if ws_client.closed:
        msg = "jx3api > ws连接已关闭！"
    else:
        msg = "jx3api > ws连接正常！"
    msg = MessageSegment.text(msg)
    await check_ws.finish(msg)


@connect_ws.handle()
async def _(event: PrivateMessageEvent):
    """连接服务器"""
    if not ws_client.closed:
        await connect_ws.finish("连接正常，请不要重复连接。")

    if ws_client.is_connecting:
        await connect_ws.finish("正在连接中，请不要重复连接。")

    await connect_ws.send("正在连接服务器...")
    flag = await ws_client.init()
    msg = None
    if flag:
        msg = "jx3api > ws已连接！"
    msg = MessageSegment.text(msg)
    await connect_ws.finish(msg)


@close_ws.handle()
async def _(event: PrivateMessageEvent):
    """关闭连接"""
    if not ws_client.closed:
        await ws_client.close()
        msg = MessageSegment.text("jx3api > ws连接已关闭！")
    else:
        msg = MessageSegment.text("jx3api > ws连接未关闭！")
    await close_ws.finish(msg)

