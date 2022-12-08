# -*- coding: utf-8 -*-
import asyncio

import nonebot
from pydantic import BaseModel
from httpx import AsyncClient
from src.Data.jxDatas import chat_gpt_apikey


class Response(BaseModel):
    """返回数据模型"""

    id: str
    """状态码"""
    object: str
    created: int
    model: str
    choices: list
    """返回消息字符串"""
    usage: dict | list[dict]
    """返回数据"""


class ChatGPTAPI:
    client: AsyncClient

    def __init__(self):
        self.client = AsyncClient()
        self.apikey = chat_gpt_apikey

        self.url = "https://api.openai.com/v1/completions"

    async def call_api(self, prompt) -> Response:
        """请求api网站数据"""
        headers = {
            'Authorization': f'Bearer {self.apikey}',
            'OpenAI-Organization': 'org-edezPivp1WlSWoGOgDLfzmz5',
            'Content-Type': 'application/json'
        }
        data = {
            "model": "text-davinci-003",
            "prompt": prompt,
            "max_tokens": 1000,
            "temperature": 0
        }

        res = await self.client.post(url=self.url, json=data, headers=headers, timeout=3000)
        nonebot.logger.info(res.text)
        return Response.parse_obj(res.json())
