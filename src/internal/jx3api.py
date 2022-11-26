# -*- coding: utf-8 -*-

from typing import Any
from functools import partial
from src.Data.jxDatas import jx3api_ticket
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
    time: int
    """时间戳"""


class API:
    client: AsyncClient

    def __init__(self):
        self.client = AsyncClient()

    async def call_api(self, url: str, **data: Any) -> Response:
        """请求api网站数据"""
        try:
            headers = {
                'token': jx3api_ticket,
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
                'Content-Type': 'application/json'
            }
            res = await self.client.get(url=url, params=data, headers=headers)
            return Response.parse_obj(res.json())
        except Exception as e:
            logger.error(f"<y>JX3API请求出错：</y> | {str(e)}")
            return Response(code=0, msg=f"{str(e)}", data={}, time=0)

    def __getattr__(self, name: str) -> _ApiCall:
        # 拼接url
        url = "https://www.jx3api.com/" + name.replace("_", "/")
        logger.debug(f"<y>JX3API请求功能:{url}</y>")
        return partial(self.call_api, url)
