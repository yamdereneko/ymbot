# -*- coding: utf-8 -*

"""
@Software : PyCharm
@File : 0.py
@Author : 喵
@Time : 2021/09/29 22:39:29
@Docs : 请求推栏战绩例子
"""
import asyncio
import traceback
import nonebot
import requests
import json
from .jxDatas import jx3Data as jxData
from .database import DataBase as database

# 请求头
headers = jxData.headers


class GetJJCTop200Record:
    def __init__(self, weekly: int):
        config = jxData.config
        jx3Data = jxData()
        self.weekly = weekly
        self.server = None
        self.zone = jx3Data.mainZone(self.server)
        self.database = database(config)
        self.role_id = None
        self.ts = None
        self.xsk = None
        self.global_role_id = None
        self.personId = None

    async def get_xsk(self, data=None):
        data = json.dumps(data)
        res = requests.post(url="https://www.jx3api.com/token/calculate", data=data).json()
        return res['data']['ts'], res['data']['sk']

    async def get_global_role_id(self):
        # 准备请求参数
        try:
            param = {'role_id': self.role_id, 'server': self.server, "zone": self.zone}
            self.ts, self.xsk = await self.get_xsk(param)  # 获取ts和xsk， data 字典可以传ts,不传自动生成
            param['ts'] = self.ts  # 给参数字典赋值ts参数
            param = json.dumps(param).replace(" ", "")  # 记得格式化，参数需要提交原始json，非已格式化的json
            headers['X-Sk'] = self.xsk  # 修改请求中的xsk
            data = requests.post(url="https://m.pvp.xoyo.com/role/indicator", data=param, headers=headers).json()
            if data.get("code") != 0:
                print("获取全局role_id失败，请重试")
                return None
            if data.get('data').get('role_info') is None:
                print("获取角色失败，请重试")
                return None
            if data.get("data").get("person_info") is None:
                return None
            self.global_role_id = data.get("data").get("role_info").get("global_role_id")
        except Exception as e:
            print(e)

    async def get_jjc_record(self):
        # 准备请求参数
        param = {'global_role_id': self.global_role_id, "size": 10, "cursor": 0}
        self.ts, self.xsk = await self.get_xsk(param)  # 获取ts和xsk， data 字典可以传ts,不传自动生成
        param['ts'] = self.ts  # 给参数字典赋值ts参数
        param = json.dumps(param).replace(" ", "")  # 记得格式化，参数需要提交原始json，非已格式化的json
        headers['X-Sk'] = self.xsk  # 修改请求中的xsk
        data = requests.post(url="https://m.pvp.xoyo.com/3c/mine/match/history", data=param, headers=headers).json()
        if data.get("code") != 0:
            print("获取JJC战绩失败，请重试")
            return None
        if not data.get('data'):
            print("没有JJC战绩，请重试")
            return None
        return data

    async def get_person_history(self):
        # 准备请求参数
        try:
            if self.personId is None:
                nonebot.logger.error("person_id 未获取到，返回空")
                return None
            param = {'person_id': str(self.personId), "size": 10, "cursor": 0}
            ts, xsk = await self.get_xsk(param)  # 获取ts和xsk， data 字典可以传ts,不传自动生成
            param['ts'] = ts  # 给参数字典赋值ts参数
            param = json.dumps(param).replace(" ", "")  # 记得格式化，参数需要提交原始json，非已格式化的json
            headers['X-Sk'] = xsk  # 修改请求中的xsk
            data = requests.post(url="https://m.pvp.xoyo.com/mine/match/person-history", data=param,
                                 headers=headers).json()
            return data

        except Exception as e:
            nonebot.logger.error(e)
            nonebot.logger.error("获取用户信息失败，请查看问题.")
            traceback.print_exc()
            return None

    async def get_top200_history(self, typeName: str, heiMaBang: bool):
        # 准备请求参数
        param = {'typeName': typeName, 'tag': self.weekly, "heiMaBang": heiMaBang}
        self.ts, self.xsk = await self.get_xsk(param)  # 获取ts和xsk， data 字典可以传ts,不传自动生成
        param['ts'] = self.ts  # 给参数字典赋值ts参数
        param = json.dumps(param).replace(" ", "")  # 记得格式化，参数需要提交原始json，非已格式化的json
        headers['X-Sk'] = self.xsk  # 修改请求中的xsk
        data = requests.post(url="https://m.pvp.xoyo.com/3c/mine/arena/top200", data=param, headers=headers).json()
        school_top = {}
        for i in jxData.all_school.keys():
            school_top[i] = 0
        failure_list = []
        for element in data.get("data"):
            self.role_id = element.get("personInfo").get("gameRoleId")
            school = element.get("personInfo").get("force")
            self.server = element.get("personInfo").get("server")
            self.zone = element.get("personInfo").get("zone")
            name = element.get("personInfo").get("roleName")
            self.personId = element.get("personId")
            if school in jxData.much_school:
                await self.get_global_role_id()
                if self.global_role_id is None:
                    failure_list.append(element)
                    print(self.role_id + " " + school + " " + self.server + " " + self.zone + " " + name + " 不存在")
                    person_history = await self.get_person_history()
                    if person_history.get("data") is not None:
                        continueName = person_history.get("data")[0].get("role_name")
                        print("continueName:" + continueName)
                        if name == continueName:
                            continueKungfu = person_history.get("data")[0].get("kungfu")
                            value = jxData.school_pinyin[continueKungfu]
                            school_top[value] = school_top.get(value, 0) + 1
                            print("重新进行添加：" + continueName)
                            continue
                    continue

                jjc_record = await self.get_jjc_record()
                if jjc_record is None:
                    print(self.role_id + " " + school + " " + self.server + " " + self.zone + " 战绩不存在")
                    failure_list.append(element)
                    continue

                kungfu = jjc_record.get("data")[1].get("kungfu")
                if kungfu in jxData.school_pinyin:
                    value = jxData.school_pinyin[kungfu]
                    school_top[value] = school_top.get(value, 0) + 1
            else:
                school_top[school] = school_top.get(school, 0) + 1
        print(failure_list)
        return school_top

    async def main(self):
        # 获取所有的数据进行处理
        data = await self.get_top200_history('week', False)
        print(data)
        # 判断连接池数据是否冲突
        sql = "select week from JJC_rank_weekly"
        await self.database.connect()
        weekly = await self.database.fetchall(sql)
        for week in weekly:
            if week.get("week") == self.weekly:
                print("该周数据已存在...")
                return None

        sql = "insert into JJC_rank_weekly (week, 霸刀, 藏剑, 蓬莱, 无方,云裳,花间,少林,惊羽,丐帮,苍云,紫霞,相知,补天,凌雪,明教,毒经,灵素,天策,田螺,胎虚,离经,莫问,衍天,冰心) values ('%s','%s','%s',%s,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (self.weekly, data["霸刀"], data["藏剑"], data["蓬莱"], data["无方"], data["云裳"], data["花间"], data["少林"],data["惊羽"],data["丐帮"],data["苍云"], data["紫霞"], data["相知"], data["补天"], data["凌雪阁"], data["明教"], data["毒经"], data["灵素"],data["天策"],data["田螺"], data["胎虚"], data["离经"], data["莫问"], data["衍天宗"], data["冰心"])
        print(sql)
        if sum(data.values()) == 200:
            await self.database.execute(sql)
        else:
            print("门派汇总的人数不到正确值，请人工处理错误信息...")


getJJCTopRecord = GetJJCTop200Record(32)
asyncio.run(getJJCTopRecord.main())

