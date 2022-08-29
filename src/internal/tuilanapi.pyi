from httpx import AsyncClient
from pydantic import BaseModel

class Response(BaseModel):
    """返回数据模型"""

    code: int
    """状态码"""
    msg: str
    """返回消息字符串"""
    data: dict | list[dict]
    """返回数据"""

class API:
    """jx3api接口类"""

    client: AsyncClient
    """浏览器客户端"""


    async def role_indicator(self, *, role_id: str, server: str , zone: str = ...) -> Response:
        """
        说明：
            今天、明天、后天等的日常任务，七点自动更新。

        参数：
            * `server`：服务器名
            * `next`: 可选，查询天数，默认为0
        """
