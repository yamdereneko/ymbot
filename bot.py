#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nonebot
from nonebot.adapters.onebot.v11 import Adapter
from nonebot.log import logger, default_format
# import FastApi as fastAPI

nonebot.init(_env_file=".env.dev", apscheduler_autostart=True)
app = nonebot.get_asgi()


driver = nonebot.get_driver()
driver.register_adapter(Adapter)
nonebot.load_from_toml("pyproject.toml")

# nonebot.load_plugins("plugins")
logger.add("logs/error.log")

if __name__ == "__main__":
    nonebot.logger.warning("请使用指令[nb run]来运行此项目!")
    nonebot.run(app=app, host="0.0.0.0", port=8080)
