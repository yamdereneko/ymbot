# -*- coding: utf-8 -*-

from typing import Any
from loguru import logger
from typing_extensions import Protocol
from pydantic import BaseModel
from httpx import AsyncClient


class _ApiCall(Protocol):
    async def __call__(self, **kwargs: Any) -> Any:
        ...


class Response(BaseModel):
    """返回数据模型"""

    code: int
    """状态码"""
    msg: str
    """返回消息字符串"""
    data: dict | list[dict]
    """返回数据"""


class WangBaoLouAPI:
    client: AsyncClient

    def __init__(self):
        self.client = AsyncClient()

    async def call_api(self, name: str, sale_type: int) -> Response:
        """请求api网站数据"""
        try:
            url = f"https://api-wanbaolou.xoyo.com/api/buyer/goods/list?game_id=jx3&sort[price]=1&filter[state]={sale_type}&filter[role_appearance]={name}&game=jx3&size=10&goods_type=3"
            headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
                'Content-Type': 'application/json'
            }
            res = await self.client.get(url=url, headers=headers, timeout=3000)
            return Response.parse_obj(res.json())
        except Exception as e:
            logger.error(f"<y>JX3API请求出错：</y> | {str(e)}")
            return Response(code=0, msg=f"{str(e)}", data={}, time=0)