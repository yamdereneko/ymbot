# -*- coding: utf-8 -*-
import asyncio
import base64

import redis
import pickle

from matplotlib import pyplot as plt


class Redis:
    def __init__(self):
        self.conn = redis.Redis(
            host='114.115.181.82',  # ip地址
            port=6379,  # 端口号
            db=0,
            decode_responses=True,
            password="qinhao123"
            # 设置为True存的数据格式就是str类型
        )

    async def add(self, key, data):
        if await self.exit(key, data):
            print("该数据已存在！")
            return False
        else:
            self.conn.sadd(key, data)  # 添加
            print("添加成功")
            return True

    async def query(self, key):
        return self.conn.smembers(key)  # 拿出key对应所有值

    async def delete(self, key):
        self.conn.delete(key)  # 删除key键

    async def exit(self, key, data):
        return self.conn.sismember(key, data)  # 判断key里是否有data，有则返回true

    async def insert_image(self, frame_id, frame):
        # 将图片序列化存入redis中
        # b = pickle.dumps(frame)  # frame is numpy.ndarray
        # self.conn.set(frame_id, b)

        with open(frame, "rb") as f:  # 打开01.png图片
            # b64encode是编码，b64decode是解码
            base64_data = base64.b64encode(f.read())  # 读取图片转换的二进制文件，并给赋值
            # base64.b64decode(base64data)
            print(base64_data)
            self.conn.set(frame_id, base64_data)

    async def get_image(self, frame_id, frame):
        # 从redis中取出序列化的图片并进行反序列化
        # im = pickle.loads(self.conn.get(frame_id))
        var = self.conn.get(frame_id)
        data = base64.b64decode(var)  # 把二进制文件解码，并复制给data
        with open(frame, "wb") as f:  # 写入生成一个jd.png
            f.write(data)


red = Redis()
# asyncio.run(red.add('url','123123'))
# print(asyncio.run(red.insert_image('daily','file:/tmp/daily1663146826.png')))
asyncio.run(red.get_image('daily1', '/tmp/daily.png'))
