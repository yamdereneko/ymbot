# -*- coding: utf-8 -*-
import asyncio
import json
import nonebot
import io
import base64
from PIL import Image
from src.Data.jxDatas import redis_config


class Redis:
    def __init__(self):
        self.conn = redis_config

    async def add(self, key, data):
        if await self.query(key):
            nonebot.logger.warning(f"Redis该数据已存在！{key}")
            return False
        else:
            self.conn.set(key, json.dumps(data))  # 添加
            nonebot.logger.info(f"Redis添加成功!:{key}")
            return True

    async def exist(self, key):
        if self.conn.exists(key) == 1:
            return True
        else:
            return False

    async def query(self, key):
        return self.conn.get(key)  # 拿出key对应所有值

    async def delete(self, key):
        self.conn.delete(key)  # 删除key键

    async def exit(self, key, data):
        return self.conn.sismember(key, data)  # 判断key里是否有data，有则返回true

    async def insert_list(self, list_name, info):
        self.conn.rpush(list_name, info)

    async def query_list(self, list_name):
        return self.conn.lrange(list_name, 0, -1)

    async def delete_list(self, list_name, element):
        return self.conn.lrem(list_name, 0, element)

    async def insert_image(self, frame_id, frame):
        with open(frame, "rb") as f:  # 打开01.png图片
            # b64encode是编码，b64decode是解码
            base64_data = base64.b64encode(f.read())  # 读取图片转换的二进制文件，并给赋值
            # base64.b64decode(base64data)
            self.conn.set(frame_id, base64_data)

    async def get_image(self, frame_id, frame):
        # 从redis中取出序列化的图片并进行反序列化
        # im = pickle.loads(self.conn.get(frame_id))
        var = self.conn.get(frame_id)
        image_data = base64.b64decode(var)  # 把二进制文件解码，并复制给data
        with open(frame, "wb") as f:  # 写入生成一个jd.png
            f.write(image_data)

    async def insert_image_encode(self, frame_id, image):
        base64_data = base64.b64encode(image)
        self.conn.set(frame_id, base64_data)

    async def get_image_encode(self, frame_id):
        # 从redis中取出序列化的图片并进行反序列化
        # im = pickle.loads(self.conn.get(frame_id))
        image_data = self.conn.get(frame_id)
        image = Image.open(io.BytesIO(image_data))
        return image

#
# red = Redis()
# # for _ in ticket:
# #     asyncio.run(red.insert_list("ticket_list", _))
# # print(res)
# #
# ticket_list = asyncio.run(red.query_list("ticket_list"))
# print(ticket_list)

# print(res)
# print(res)
# # daily = {'date': '2022-09-15', 'week': '四', 'war': '英雄剑冢惊变', 'battle': '三国古战场', 'camp': '藏剑·乱世',
# #          'prestige': ['引仙水榭', '微山书院', '白帝水宫', '永王行宫·花月别院'], 'relief': '万花·乱世',
# #          'team': ['五台山·无遮大会;太原·大军反击摧胡车', '英雄微山书院;英雄梵空禅院;英雄引仙水榭', '河阳之战;永王行宫·仙侣庭园;龙渊泽']}
# #

#
# res = asyncio.run(red.delete('daily_image'))
