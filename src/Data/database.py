import asyncio
from typing import Union
import aiomysql
import nonebot


class DataBase:
    def __init__(self, config: dict):
        self.pool = None
        self.config = config

    async def connect(self):
        nonebot.logger.info("MySQL > 开始建立连接...")
        try:
            self.pool = await aiomysql.create_pool(**self.config)
            nonebot.logger.info("MySQL > 建立连接成功...")
        except Exception as e:
            nonebot.logger.error("MySQL > 建立连接错误 [%s] ！" % e)

    async def cursor(self):
        conn = await self.pool.acquire()
        cur = await conn.cursor(aiomysql.DictCursor)
        return conn, cur

    async def fetchall(self, query, param=None) -> Union[dict, list, None]:
        """查询多条数据"""
        conn, cur = await self.cursor()
        try:
            await cur.execute(query, param)
            return await cur.fetchall()
        except Exception as e:
            nonebot.logger.error("MySQL > SQL Execute [%s] Error (%s)！" % (query, e))
        finally:
            await self.close(conn, cur)

    async def fetchone(self, query, param=None) -> Union[dict, list, None]:
        """查询一条数据"""
        conn, cur = await self.cursor()
        try:
            await cur.execute(query, param)
            return await cur.fetchone()
        except Exception as e:
            nonebot.logger.error("MySQL > SQL Execute [%s] Error (%s)！" % (query, e))
        finally:
            await self.close(conn, cur)

    async def execute(self, query, param=None) -> bool:
        """新增、更新"""
        conn, cur = await self.cursor()
        try:
            await cur.execute(query, param)
            return True if cur.rowcount else False
        except Exception as e:
            nonebot.logger.error("MySQL > SQL Execute [%s] Error (%s)！" % (query, e))
        finally:
            await self.close(conn, cur)

    async def close(self, conn, cur):
        if cur:
            await cur.close()
        await self.pool.release(conn)

