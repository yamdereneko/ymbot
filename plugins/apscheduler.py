import asyncio
from contextlib import closing, suppress
from datetime import datetime
from functools import wraps
from itertools import count
from typing import Callable, List
from urllib.request import urlopen
from src.Data.jxDatas import group_list
from src import jx3_Daily as jx3_Daily
import nonebot
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot import require, get_bots

monitoring = require("nonebot_plugin_apscheduler").scheduler


def retry(attempt: int = 3) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def warpper(*args, **kwargs) -> bool:
            counter = count()
            while True:
                if await func(*args, **kwargs):
                    return True
                if (c := next(counter)) == attempt:
                    return False
                await asyncio.sleep(c)

        return warpper

    return decorator


@retry()
async def socket_connector(host: str, port: str, timeout: int = 3) -> bool:
    with suppress(Exception):
        _, w = await asyncio.wait_for(
            asyncio.open_connection(host, port), timeout=timeout
        )
        w.close()
        return True
    return False


async def check(
        server: str, host: str, port: str, *, timeout: int = 3
) -> None:
    while True:
        if await socket_connector(host=host, port=port, timeout=timeout):
            # Launched
            await asyncio.to_thread(msg_box, server)
            return


def check_verson() -> str:
    with closing(
            urlopen(
                "https://jx3hdv4.autoupdate.kingsoft.com/jx3hd_v4/zhcn_hd/autoupdateentry.txt"
            )
    ) as resp:
        return resp.read().decode("utf-8").splitlines()[1].split("=")[1]


def msg_box(server: str):
    msg = MessageSegment.text(
        f"{datetime.now():%F %H:%M:%S}\n {server} 已开服！！\n"
        f"当前客户端版本: {check_verson()}\n"
        f"{server} 已开服！！"
    )
    return msg


async def main(servers: List[str]) -> None:
    server_set = set()

    with closing(
            urlopen(
                "http://jx3comm.xoyocdn.com/jx3hd/zhcn_hd/serverlist/serverlist.ini"
            )
    ) as resp:
        server_list = resp.read().decode("gbk").splitlines()

    tasks = []

    for line in server_list:
        _, server, _, host, port, *_ = line.split("\t")
        if server in servers and server not in server_set:
            server_set.add(server)
            tasks.append((server, host, port))
    nonebot.logger.info("开服监控已开启")
    await asyncio.gather(*[check(*server) for server in tasks])
    msg = [msg_box(server) for server, _, _ in tasks]

    nonebot.logger.info(msg)
    bot, = get_bots().values()
    for group_id in group_list:
        await bot.send_group_msg(group_id=group_id, message=msg)


async def run_daily():
    bot, = get_bots().values()
    daily = jx3_Daily.GetDaily()
    await daily.query_daily_figure()
    nonebot.logger.info("日常播报已正常播报")
    msg = MessageSegment.image(f"file:///tmp/daily斗转星移0.png")
    for group_id in group_list:
        await bot.send_group_msg(group_id=group_id, message=msg)


@monitoring.scheduled_job("cron", hour='7', id="send_monitoring")
def monitoringServer():
    asyncio.run(run_daily())
    asyncio.run(main(["斗转星移"]))
