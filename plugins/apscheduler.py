import nonebot
from nonebot import require, get_bots
from nonebot.adapters.onebot.v11 import MessageSegment
from src import jx3_Daily as jx3_Daily

__plugin_name__ = 'timing'
__plugin_usage__ = '用法：在规定时间触发发送的信息。'

timing = require("nonebot_plugin_apscheduler").scheduler


@timing.scheduled_job("cron", hour='7', minute='01', id="send_daily")
async def run_daily():
    bot, = get_bots().values()
    daily = jx3_Daily.GetDaily()
    await daily.QueryDailyFigure()
    nonebot.logger.info("日常播报已正常播报")
    msg = MessageSegment.image(f"file:///tmp/daily斗转星移0.png")
    await bot.send_group_msg(group_id=1077830347, message=msg)
