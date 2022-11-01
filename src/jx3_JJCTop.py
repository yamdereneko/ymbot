"""
@Software : PyCharm
@File : 0.py
@Author : 喵
@Time : 2021/09/29 22:39:29
@Docs : 请求推栏战绩例子
"""
import asyncio
import time

import nonebot
from src.internal.tuilanapi import API
from src.internal.jx3api import API as jx3API
from src.Data.jxDatas import all_school, much_school, school_pinyin, config
from src.Data.database import DataBase as database

# 请求头
jx3api = jx3API()
api = API()


class GetJJCTopRecord:
    def __init__(self, weekly: int, pvp_type: int):
        self.pvp_type = pvp_type
        self.weekly = weekly
        self.database = database(config)

    async def get_top_history(self):
        school_top = []
        try:
            # 准备请求参数
            response = await api.cc_mine_arena_top200(typeName='week', tag=self.weekly, heiMaBang=False)
            print(response)
            if response.code != 0:
                nonebot.logger.error("API接口cc_mine_arena_top200获取信息失败，请查看错误")
                return None
            data = response.data

            school_top = {}

            for i in all_school.keys():
                school_top[i] = 0
            failure_list = []

            for x, element in enumerate(data[:self.pvp_type], start=1):
                print(x)
                print(element)
                school = element.get("personInfo").get("force")

                name = element.get("personInfo").get("roleName")
                role_id = element.get("personInfo").get("gameRoleId")
                server = element.get("personInfo").get("server")
                zone = element.get("personInfo").get("zone")
                person_id = element.get('personId')

                if school == "":
                    response = await jx3api.data_role_roleInfo(server=server, name=name)
                    print(response)
                    if response.code != 200:
                        nonebot.logger.error("API接口role_roleInfo获取信息失败，请查看错误")
                        continue
                    role_id = response.data['globalRoleId']

                    response = await api.cc_mine_match_history(global_role_id=role_id, size=10, cursor=0)
                    print(x)
                    print(school)
                    print(element)
                    if response.data is []:
                        nonebot.logger.error("API接口cc_mine_match_history获取信息失败，请查看错误")
                        continue
                    kungfu = response.data[0]["kungfu"]
                    school_top[kungfu] = school_top.get(kungfu, 0) + 1
                    continue

                if school in much_school:
                    response = await api.role_indicator(role_id=role_id, server=server, zone=zone)

                    if response.msg != 'success' or response.data['person_info'] is None:
                        print(f'{name} 排名{str(x)}: {role_id} {school} {server} {zone} 不存在')
                        res = await api.mine_match_person9history(person_id=str(person_id), size=10, cursor=0)
                        nonebot.logger.error("mine_match_person-history获取信息失败，请查看错误")
                        nonebot.logger.error(res)
                        failure_list.append(element)
                        continue

                    global_role_id = response.data["role_info"]["global_role_id"]
                    time.sleep(1)

                    response = await api.cc_mine_performance_kungfu(global_role_id=str(global_role_id))

                    if response.msg != 'success' or response.data == []:
                        print(f'{name} 排名{str(x)}: {role_id} {school} {server} {zone} 不存在')
                        failure_list.append(element)
                        continue
                    #
                    z = 0
                    while len(response.data[z]["skills"]) < 8:
                        z += 1
                    print(z)
                    print(response.data[z].values())
                    print(response.data)
                    print('====' * 30)
                    kungfu = response.data[z]['name']
                    if kungfu is None or kungfu == []:
                        print(f'{name} 排名{str(x)}: {role_id} {school} {server} {zone} 不存在')
                        failure_list.append(element)
                        continue

                    if kungfu in school_pinyin:
                        value = school_pinyin[kungfu]
                        school_top[value] = school_top.get(value, 0) + 1
                else:
                    school_top[school] = school_top.get(school, 0) + 1
            print(failure_list)
            print(school_top)
            return school_top
        except Exception as e:
            print(school_top)
            print(e)

    async def main(self):
        # 获取所有的数据进行处理
        data = await self.get_top_history()
        print(data)
        # 判断连接池数据是否冲突
        sql = f"select week from JJC_rank50_weekly"
        await self.database.connect()
        weekly = await self.database.fetchall(sql)
        for week in weekly:
            if week.get("week") == self.weekly:
                print("该周数据已存在...")
                return None

        sql = "insert into JJC_rank50_weekly (week, 霸刀, 藏剑, 蓬莱, 无方,云裳,花间,少林,惊羽,丐帮,苍云,紫霞,相知,补天,凌雪,明教,毒经,灵素,天策,田螺,胎虚,离经,莫问,衍天,冰心,刀宗) values ('%s','%s','%s',%s,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
            self.weekly, data["霸刀"], data["藏剑"], data["蓬莱"], data["无方"], data["云裳"], data["花间"], data["少林"], data["惊羽"],
            data["丐帮"], data["苍云"], data["紫霞"], data["相知"], data["补天"], data["凌雪阁"], data["明教"], data["毒经"], data["灵素"],
            data["天策"], data["田螺"], data["胎虚"], data["离经"], data["莫问"], data["衍天宗"], data["冰心"], data["刀宗"])
        print(sql)
        if sum(data.values()) == self.pvp_type:
            await self.database.execute(sql)
        else:
            print("门派汇总的人数不到正确值，请人工处理错误信息...")


record = GetJJCTopRecord(44, 50)
print(asyncio.run(record.main()))
