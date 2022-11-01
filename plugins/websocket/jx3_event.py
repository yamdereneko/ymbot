# -*- coding: utf-8 -*-

from nonebot import escape_tag
from nonebot.adapters.onebot.v11.message import Message
from nonebot.adapters import Event as BaseEvent
from nonebot.typing import overrides
from pydantic import BaseModel


class WsData(BaseModel):
    """
    ws数据模型
    """

    action: int
    """ws消息类型"""
    data: dict
    """消息数据"""


class WsNotice(BaseEvent):
    """
    ws通知主人事件
    """

    __event__ = "WsNotice"
    post_type: str = "WsNotice"
    message: str
    """通知内容"""

    @overrides(BaseEvent)
    def get_type(self) -> str:
        return self.post_type

    @overrides(BaseEvent)
    def get_event_name(self) -> str:
        return self.post_type

    @overrides(BaseEvent)
    def get_event_description(self) -> str:
        return escape_tag(str(self.dict()))

    @overrides(BaseEvent)
    def get_message(self) -> Message:
        raise ValueError("Event has no message!")

    @overrides(BaseEvent)
    def get_plaintext(self) -> str:
        raise ValueError("Event has no message!")

    @overrides(BaseEvent)
    def get_user_id(self) -> str:
        raise ValueError("Event has no message!")

    @overrides(BaseEvent)
    def get_session_id(self) -> str:
        raise ValueError("Event has no message!")

    @overrides(BaseEvent)
    def is_tome(self) -> bool:
        return False
