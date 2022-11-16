# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*
"""
@Software : PyCharm
@File : 0.py
@Author : 喵
@Time : 2021/09/29 22:39:29
@Docs : 请求推栏战绩例子
"""
import asyncio

import typer
from rich import inspect
from rich import print
from src.jx3_Daily import GetDaily
from rich.console import Console

console = Console()
app = typer.Typer()


@app.command()
def hello(name: str):
    print(f"Hello {name}")


@app.command()
def daily():
    daily_command = asyncio.run(GetDaily().get_daily())
    print(daily_command,locals())
    console.log(daily_command, log_locals=True)


@app.command()
def goodbye(name: str, formal: bool = False):
    if formal:
        print(f"Goodbye Ms. {name}. Have a good day.")
    else:
        print(f"Bye {name}!")


# inspect(my_list)

if __name__ == "__main__":
    app()
