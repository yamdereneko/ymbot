# -*- coding: utf-8 -*-
import json
from typing import Any

from functools import partial
import aiohttp
from loguru import logger
from typing_extensions import Protocol
from pydantic import BaseModel
from httpx import AsyncClient
import src.Data.jxDatas as jxData


class _ApiCall(Protocol):
    async def __call__(self, **kwargs: Any) -> Any:
        ...


class Response(BaseModel):
    """返回数据模型"""

    code: int
    """状态码"""
    msg: str
    """返回消息字符串"""
    data: Any


class API:
    client: AsyncClient

    def __init__(self):
        self.client = AsyncClient()

    async def get_xsk(self, data=None):
        async with aiohttp.ClientSession() as session:
            url = "https://www.jx3api.com/token/calculate"
            async with session.post(url, data=json.dumps(data)) as resp:
                res = await resp.json()
                return res['data']['ts'], res['data']['sk']

    async def call_api(self, url: str, **data: Any) -> Response:
        """请求api网站数据"""

        try:
            ts, xsk = await self.get_xsk(data)
            headers = jxData.headers
            # headers['token'] = jxData.ticket[]
            headers['X-Sk'] = xsk
            data['ts'] = ts
            data = json.dumps(data).replace(" ", "")
            res = await self.client.post(url=url, data=data, headers=headers)
            return Response.parse_obj(res.json())
        except Exception as e:
            logger.error(f"<y>推栏API请求出错：</y> | {str(e)}")
            return Response(code=0, msg=f"{str(e)}", data={}, time=0)

    def __getattr__(self, name: str) -> _ApiCall:
        # 拼接url
        url = "https://m.pvp.xoyo.com/" + name.replace("_", "/").replace("cc", "3c").replace('9', '-')
        logger.debug(f"<y>推栏API请求功能:</y> | {url}")
        return partial(self.call_api, url)
