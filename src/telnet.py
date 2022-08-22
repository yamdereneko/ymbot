import asyncio
import ctypes
from contextlib import closing, suppress
from datetime import datetime
from functools import wraps
from itertools import count
from typing import Callable, List
from urllib.request import urlopen


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


def msg_box(server: str) -> None:
    ctypes.windll.user32.MessageBoxW(
        0,
        f"{datetime.now():%F %H:%M:%S}\n {server} 已开服！！\n"
        f"当前客户端版本: {check_verson()}",
        f"{server} 已开服！！",
        0,
    )


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

    await asyncio.gather(*[check(*server) for server in tasks])


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser("开服监控")
    parser.add_argument("server", type=str, nargs="*")

    args = parser.parse_args()

    asyncio.run(main(args.server))