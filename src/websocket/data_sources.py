# -*- coding: utf-8 -*-
from enum import Enum, auto
import src.websocket._jx3_event as Event
from src.websocket.jx3_websocket import ws_client


class GroupSetting(Enum):
    """
    群设置枚举
    """

    进群通知 = auto()
    离群通知 = auto()
    晚安通知 = auto()
    开服推送 = auto()
    新闻推送 = auto()
    奇遇推送 = auto()
    抓马监控 = auto()
    扶摇监控 = auto()


async def ws_init():
    """初始化连接ws服务器"""
    print("<g>正在链接jx3api的ws服务器...</g>")
    flag = await ws_client.init()
    if flag:
        print("<y>jx3api的ws服务器已链接。</y>")
    else:
        print("<r>jx3api的ws服务器连接失败！</r>")


async def get_ws_status(group_id: int, event: Event.RecvEvent) -> bool:
    """
    说明:
        获取ws通知开关，robot为关闭时返回False

    参数:
        * `group_id`：QQ群号
        * `event`：接收事件类型

    返回:
        * `bool`：ws通知开关
    """

    if isinstance(event, Event.ServerStatusEvent):
        recv_type = GroupSetting.开服推送
    if isinstance(event, Event.NewsRecvEvent):
        recv_type = GroupSetting.新闻推送
    if isinstance(event, Event.SerendipityEvent):
        recv_type = GroupSetting.奇遇推送
    if isinstance(event, Event.HorseRefreshEvent) or isinstance(
            event, Event.HorseCatchedEvent
    ):
        recv_type = GroupSetting.抓马监控
    if isinstance(event, Event.FuyaoRefreshEvent) or isinstance(
            event, Event.FuyaoNamedEvent
    ):
        recv_type = GroupSetting.扶摇监控

    print(recv_type)
