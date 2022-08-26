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
import matplotlib
import nonebot
import requests
import json
import src.Data.jxDatas as jxData
from matplotlib import pyplot as plt

matplotlib.rc("font", family='PingFang HK')

# 请求头
headers = jxData.headers


class ServerState:
    def __init__(self, server=None):
        self.server = jxData.mainServer(server)
        self.zone = jxData.mainZone(self.server)

    async def get_xsk(self, data=None):
        data = json.dumps(data)
        res = requests.post(url="https://www.jx3api.com/token/calculate", data=data).json()
        return res['data']['ts'], res['data']['sk']

    async def get_server_list(self):
        # 准备请求参数
        gameName = "jx3"
        param = {'gameName': gameName}
        ts, xsk = await self.get_xsk(param)  # 获取ts和xsk， data 字典可以传ts,不传自动生成
        param['ts'] = ts  # 给参数字典赋值ts参数
        param = json.dumps(param).replace(" ", "")  # 记得格式化，参数需要提交原始json，非已格式化的json
        headers['X-Sk'] = xsk  # 修改请求中的xsk
        data = requests.post(url="https://m.pvp.xoyo.com/msgr-http/get-jx3-server-list", data=param,
                             headers=headers).json()

        if data.get("code") != 0:
            nonebot.logger.error("服务器状态有问题")
            return None

        ServerStates = []
        for info in data.get("data"):
            flag = 0
            ServerState = {}
            server = info.get("mainServer")
            if jxData.mainServer(server) is None:
                break
            for i in ServerStates:
                if i.get("mainServer") == server:
                    flag = 1
                    break
            if flag == 1:
                continue
            ServerState["mainServer"] = server
            ServerState["mainZone"] = info.get("mainZone")
            ServerState["connectState"] = info.get("connectState")
            ServerState["ipAddress"] = info.get("ipAddress")
            ServerState["ipPort"] = info.get("ipPort")
            ServerStates.append(ServerState)
        return ServerStates

    async def get_figure(self):
        data = await self.get_server_list()
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
