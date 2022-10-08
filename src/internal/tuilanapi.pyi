from httpx import AsyncClient
from pydantic import BaseModel
from typing import Any
class Response(BaseModel):
    """返回数据模型"""

    code: int
    """状态码"""
    msg: str
    """返回消息字符串"""
    data: Any

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

    async def cc_mine_match_history(self, *, global_role_id: str, size: int, cursor: int = ...) -> Response:
        """
        说明：
            今天、明天、后天等的日常任务，七点自动更新。

        参数：
            * `server`：服务器名
            * `next`: 可选，查询天数，默认为0
        """
    async def mine_match_person9history(self, *, person_id: str, size: int, cursor: int = ...) -> Response:
        """
        说明：
            今天、明天、后天等的日常任务，七点自动更新。

        参数：
            * `server`：服务器名
            * `next`: 可选，查询天数，默认为0
        """

    async def cc_mine_arena_top200(self, *, typeName: str, tag: int, heiMaBang: bool = ...) -> Response:
        """
        说明：
            今天、明天、后天等的日常任务，七点自动更新。

        参数：
            * `server`：服务器名
            * `next`: 可选，查询天数，默认为0
        """

    async def mine_equip_get9role9equip(self, *, game_role_id: str, server: str, zone: str = ...) -> Response:
        """
        说明：
            今天、明天、后天等的日常任务，七点自动更新。

        参数：
            * `server`：服务器名
            * `next`: 可选，查询天数，默认为0
        """
    async def cc_mine_match_detail(self, *, match_id: int = ...) -> Response:
        """
        说明：
            今天、明天、后天等的日常任务，七点自动更新。

        参数：
            * `server`：服务器名
            * `next`: 可选，查询天数，默认为0
        """
    async def cc_mine_performance_kungfu(self, *, global_role_id: str = ...) -> Response:
        """
        说明：
            今天、明天、后天等的日常任务，七点自动更新。

        参数：
            * `server`：服务器名
            * `next`: 可选，查询天数，默认为0
        """