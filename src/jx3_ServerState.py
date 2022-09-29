# -*- coding: utf-8 -*

"""
@Software : PyCharm
@File : 0.py
@Author : 喵
@Time : 2021/09/29 22:39:29
@Docs :
"""
import asyncio

import dufte
import nonebot
import src.Data.jxDatas as jxData
from src.internal.jx3api import API
from matplotlib import pyplot as plt

api = API()
# 请求头
headers = jxData.headers


class ServerState:
    def __init__(self, server=None):
        self.server = jxData.mainServer(server)
        self.zone = jxData.mainZone(self.server)

    async def check_server_state(self):
        response = await api.data_server_check(server=self.server)
        if response.code != 200:
            nonebot.logger.error("API接口next_price获取信息失败，请查看错误: ")
            nonebot.logger.error(f'报错代码: {response.code}, 报错信息:{response.msg}')
            return None
        return response

    async def get_figure(self):
        data = await self.check_server_state()
        fig, ax = plt.subplots(figsize=(8, 9), facecolor='white', edgecolor='white')
        plt.style.use(dufte.style)
        ax.axis([0, 10, 0, 14])
        ax.set_title("区服信息", fontsize=19, color='#303030', fontweight="heavy",
                     verticalalignment='top', )
        ax.axis('off')
        for x, y in enumerate(data):
            mainServer = y.get("mainServer")
            mainZone = y.get("mainZone")
            connectState = y.get("connectState")
            State = connectState is True and "已开服" or "未开服"
            ax.text(1, x, f'{mainServer}', verticalalignment='bottom', horizontalalignment='left',
                    color='#404040')
            ax.text(4, x, f'{mainZone} ', verticalalignment='bottom', horizontalalignment='left', color='#404040')
            fontColor = State == "已开服" and 'green' or 'red'
            ax.text(7, x, f'{State}', verticalalignment='bottom', horizontalalignment='left', color=fontColor)
        plt.savefig(f"/tmp/serverState.png")
        nonebot.logger.info("区服图已重新构筑")
        return True
