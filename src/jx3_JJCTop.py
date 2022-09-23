# -*- coding: utf-8 -*

"""
@Software : PyCharm
@File : 0.py
@Author : 喵
@Time : 2021/09/29 22:39:29
@Docs : 请求推栏战绩例子
"""
import asyncio

import nonebot
from src.internal.tuilanapi import API
import src.Data.jxDatas as jxData
from src.Data.database import DataBase as database

# 请求头
headers = jxData.headers
api = API()


class GetJJCTopRecord:
    def __init__(self, weekly: int, pvp_type: int):
        config = jxData.config
        self.pvp_type = pvp_type
        self.weekly = weekly
        self.server = None
        self.zone = jxData.mainZone(self.server)
        self.database = database(config)
        self.role_id = None
        self.global_role_id = None
        self.person_id = None

    async def get_top_history(self):
        # 准备请求参数
        response = await api.cc_mine_arena_top200(typeName='week', tag=self.weekly, heiMaBang=False)
        if response.code != 0:
            nonebot.logger.error("API接口Daily获取信息失败，请查看错误")
            return None
        data = response.data

        school_top = {}

        for i in jxData.all_school.keys():
            school_top[i] = 0
        failure_list = []

        for x, element in enumerate(data[:self.pvp_type]):
            school = element.get("personInfo").get("force")
            name = element.get("personInfo").get("roleName")
            self.role_id = element.get("personInfo").get("gameRoleId")
            self.server = element.get("personInfo").get("server")
            self.zone = element.get("personInfo").get("zone")
            self.person_id = element.get("personId")
            if school in jxData.much_school:
                response = await api.role_indicator(role_id=self.role_id, server=self.server, zone=self.zone)
                if response.code != 0 or response.data == {}:
                    failure_list.append(element)
                    response = await api.mine_match_person9history(person_id=str(self.person_id), size=10, cursor=0)
                    if response.code != 0:
                        nonebot.logger.error("mine_match_person-history获取信息失败，请查看错误")
                        continue
                    person_history = response.data
                    if person_history is not None:
                        continue_name = person_history[0].get("role_name")
                        print("continueName:" + continue_name)
                        if name == continue_name:
                            continue_kungfu = person_history[0].get("kungfu")
                            value = jxData.school_pinyin[continue_kungfu]
                            school_top[value] = school_top.get(value, 0) + 1
                            print("重新进行添加：" + continue_name)
                            continue
                    continue
                self.global_role_id = response.data["role_info"]["global_role_id"]
                response = await api.cc_mine_match_history(global_role_id=self.global_role_id, size=10, cursor=0)
                jjc_record = response.data
                if jjc_record is None or jjc_record == {}:
                    print(f'{name} 排名{str(x)}: {self.role_id} {school} {self.server} {self.zone} 不存在')
                    failure_list.append(element)
                    continue
                kungfu = jjc_record[1].get("kungfu")
                if kungfu in jxData.school_pinyin:
                    value = jxData.school_pinyin[kungfu]
                    school_top[value] = school_top.get(value, 0) + 1
            else:
                school_top[school] = school_top.get(school, 0) + 1
        print(failure_list)
        return school_top

    async def main(self):
        # 获取所有的数据进行处理
        data = await self.get_top_history()
        print(data)
        # 判断连接池数据是否冲突
        sql = "select week from JJC_rank_weekly"
        await self.database.connect()
        weekly = await self.database.fetchall(sql)
        for week in weekly:
            if week.get("week") == self.weekly:
                print("该周数据已存在...")
                return None

        sql = "insert into JJC_rank_weekly (week, 霸刀, 藏剑, 蓬莱, 无方,云裳,花间,少林,惊羽,丐帮,苍云,紫霞,相知,补天,凌雪,明教,毒经,灵素,天策,田螺,胎虚,离经,莫问,衍天,冰心) values ('%s','%s','%s',%s,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
            self.weekly, data["霸刀"], data["藏剑"], data["蓬莱"], data["无方"], data["云裳"], data["花间"], data["少林"], data["惊羽"],
            data["丐帮"], data["苍云"], data["紫霞"], data["相知"], data["补天"], data["凌雪阁"], data["明教"], data["毒经"], data["灵素"],
            data["天策"], data["田螺"], data["胎虚"], data["离经"], data["莫问"], data["衍天宗"], data["冰心"])
        print(sql)
        if sum(data.values()) == self.pvp_type:
            await self.database.execute(sql)
        else:
            print("门派汇总的人数不到正确值，请人工处理错误信息...")


record = GetJJCTopRecord(37, 200)
print(asyncio.run(record.main()))
