# -*- coding: utf-8 -*-
import json
from typing import Any

from functools import partial
import hashlib
import hmac
import datetime
from loguru import logger
from typing_extensions import Protocol
from pydantic import BaseModel
from httpx import AsyncClient
from src.Data.jxDatas import headers


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


async def gen_xsk(data: str) -> str:
    data += "@#?.#@"
    secret = "MaYoaMQ3zpWJFWtN9mqJqKpHrkdFwLd9DDlFWk2NnVR1mChVRI6THVe6KsCnhpoR"
    return hmac.new(secret.encode(), msg=data.encode(), digestmod=hashlib.sha256).hexdigest()


async def gen_ts() -> str:
    return f"{datetime.datetime.now():%Y%m%d%H%M%S%f}"[:-3]


async def format_body(data: dict) -> str:
    return json.dumps(data, separators=(',', ':'))


class API:
    client: AsyncClient

    def __init__(self):
        self.client = AsyncClient()

    async def call_api(self, url: str, **data: Any) -> Response:
        """请求api网站数据"""

        try:
            data['ts'] = await gen_ts()
            param = await format_body(data)
            headers['X-Sk'] = await gen_xsk(param)
            res = await self.client.post(url=url, content=param, headers=headers)
            return Response.parse_obj(res.json())
        except Exception as e:
            logger.error(f"<y>推栏API请求出错：</y> | {str(url)}")
            logger.error(f"<y>推栏API请求出错：</y> | {str(e)}")
            return Response(code=0, msg=f"{str(e)}", data={}, time=0)

    def __getattr__(self, name: str) -> partial:
        # 拼接url
        url = "https://m.pvp.xoyo.com/" + name.replace("_", "/").replace("cc", "3c").replace('9', '-')
        logger.debug(f"<y>推栏API请求功能:</y> | {url}")
        return partial(self.call_api, url)
