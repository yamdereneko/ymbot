import asyncio
import json
import nonebot
import src.Data.jx3_Redis as redis
from contextlib import closing, suppress
from datetime import datetime
from functools import wraps
from itertools import count
from typing import Callable, List
from urllib.request import urlopen
from src.Data.jxDatas import group_list
from src import jx3_Daily as jx3_Daily
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot import require, get_bots

monitoring = require("nonebot_plugin_apscheduler").scheduler
flag = 0


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
    global flag
    with suppress(Exception):
        _, w = await asyncio.wait_for(
            asyncio.open_connection(host, port), timeout=timeout
        )
        w.close()
        monitoring.resume()
        return True
    flag += 1
    monitoring.pause()
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


async def main(servers: List[str]):
    global flag
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
    res = await asyncio.gather(*[check(*server) for server in tasks])
    msg = [msg_box(server) for server, _, _ in tasks]
    nonebot.logger.info(msg)

    return msg


async def run_daily():
    daily = jx3_Daily.GetDaily()

    daily_data = await daily.get_daily()
    red = redis.Redis()

    await red.add('daily', daily_data)
    daily_image = await daily.query_daily_figure()
    frame = f"/tmp/daily_{daily_image}.png"
    await red.insert_image('daily_image', frame)
    msg = MessageSegment.image('file:' + frame)
    return msg


async def async_run():
    task1 = asyncio.shield(run_daily())
    res = await asyncio.gather(task1, return_exceptions=True)
    bot, = get_bots().values()
    for group_id in group_list:
        for msg in res:
            await bot.send_group_msg(group_id=group_id, message=msg)


@monitoring.scheduled_job("cron", hour='7', id="send_monitoring", max_instances=3)
def monitoringServer():
    asyncio.run(async_run())
