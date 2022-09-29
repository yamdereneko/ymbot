#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nonebot
from nonebot.adapters.onebot.v11 import Adapter
from nonebot.log import logger, default_format
import FastApi as fastAPI

nonebot.init(_env_file=".env.dev")
app = fastAPI.app

driver = nonebot.get_driver()
driver.register_adapter(Adapter)
nonebot.load_from_toml("pyproject.toml")
# nonebot.load_plugins("plugins")

logger.add("logs/error.log")

if __name__ == "__main__":
    nonebot.logger.warning("Always use `nb run` to start the bot instead of manually running!")
    nonebot.run(app=app, host="0.0.0.0", port=8081)
