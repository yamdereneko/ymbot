# -*- coding: utf-8 -*-
import json
from typing import Any

from functools import partial

import httpx
import requests
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
    data: dict | list[dict]
    """返回数据"""


class API:
    client: AsyncClient

    def __init__(self):
        self.xsk = None
        self.ts = None
        self.client = AsyncClient()

    async def get_xsk(self, data=None):
        data = json.dumps(data)
        res = httpx.post(url="https://www.jx3api.com/token/calculate", params=data).json()
        self.ts, self.xsk = res['data']['ts'], res['data']['sk']

    async def call_api(self, url: str, **data: Any) -> Response:
        """请求api网站数据"""

        try:
            print(data)
            self.ts, self.xsk = await self.get_xsk(param)
            headers = jxData.headers
            headers['X-Sk'] = self.xsk
            print(headers)
            data['ts'] = self.ts
            print(data)
            param = json.dumps(data).replace(" ", "")
            print(param)
            res = await self.client.post(url=url, data=param, headers=headers)
            return Response.parse_obj(res.json())
        except Exception as e:
            logger.error(f"<y>推栏API请求出错：</y> | {str(e)}")
            return Response(code=0, msg=f"{str(e)}", data={}, time=0)

    def __getattr__(self, name: str) -> _ApiCall:
        # 拼接url
        logger.debug(f"<y>推栏API请求功能:</y> | {name}")
        url = "https://m.pvp.xoyo.com/" + name.replace("_", "/", 1)
        return partial(self.call_api, url)
