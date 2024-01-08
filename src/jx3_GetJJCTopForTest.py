import asyncio
from collections import Counter
from loguru import logger
from src.internal.tuilanapi import API
from src.internal.jx3api import API as jx3API
from src.Data.jxDatas import all_school, much_school, school_pinyin, config
from src.Data.database import DataBase as database

# 请求头
jx3api = jx3API()
api = API()


class GetJJCTopRecord:

    def __init__(self):
        self.database = database(config)

    async def get_top_history(self, weekly):
        try:
            # 准备请求参数
            response = await api.cc_mine_arena_top200(typeName='week', tag=weekly, heiMaBang=False)
            logger.info(response.json())
            if response.code != 0:
                logger.error("API接口cc_mine_arena_top200获取信息失败，请查看错误")
                return None
            data = response.data

            school_top = Counter(all_school)
            failure_list = []
            total_list = []
            for x, element in enumerate(data, start=1):
                if x == 51 or x == 101:
                    total_list.append(dict(school_top))
                logger.info(x)
                logger.info(element)
                school = element.get("personInfo").get("force")
                name = element.get("personInfo").get("roleName")
                role_id = element.get("personInfo").get("gameRoleId")
                server = element.get("personInfo").get("server")
                zone = element.get("personInfo").get("zone")
                person_id = element.get('personId')

                if not school:
                    response = await jx3api.data_role_detailed(server=server, name=name)
                    logger.info(response)
                    if response.code != 200:
                        logger.error("API接口role_roleInfo获取信息失败，请查看错误")
                        continue
                    role_id = response.data['globalRoleId']

                    response = await api.cc_mine_match_history(global_role_id=role_id, size=10, cursor=0)
                    if response.data is []:
                        logger.error("API接口cc_mine_match_history获取信息失败，请查看错误")
                        continue
                    kungfu = response.data[0]["kungfu"]
                    school_top.update([kungfu])
                    continue

                if school in much_school:
                    response = await api.role_indicator(role_id=role_id, server=server, zone=zone)

                    if response.msg != 'success' or response.data['person_info'] is None:
                        logger.info(f'{name} 排名{str(x)}: {role_id} {school} {server} {zone} 不存在')
                        res = await api.mine_match_person9history(person_id=str(person_id), size=10, cursor=0)
                        if res.msg != 'success':
                            logger.error(f"mine_match_person-history获取信息失败，请查看错误 : {res}")
                            failure_list.append(element)
                        else:
                            values_list = [item['kungfu'] for item in res.data]
                            if len(set(values_list)) == 1:
                                field_value = school_pinyin.get(values_list[0])
                                print(f"All values are the same {field_value}")
                                school_top.update([field_value])
                            else:
                                print("Values are not all the same")
                                failure_list.append(element)
                        continue

                    global_role_id = response.data["role_info"]["global_role_id"]
                    await asyncio.sleep(0.5)

                    response = await api.cc_mine_performance_kungfu(global_role_id=str(global_role_id))
                    logger.info(response.data)
                    if response.msg != 'success' or response.data == []:
                        logger.info(f'{name} 排名{str(x)}: {role_id} {school} {server} {zone} 不存在')
                        failure_list.append(element)
                        continue
                    #
                    if response.data is None:
                        logger.info('该数据有问题')
                        continue
                    if len(response.data) == 1:
                        kungfu = response.data[0]['name']
                    else:
                        if response.data[0]['name'] != response.data[1]['name']:
                            response = await api.cc_mine_match_history(global_role_id=global_role_id, size=10, cursor=0)
                            res = {}
                            for i in range(0, 10):
                                value = response.data[i]['kungfu']
                                res[value] = res.get(value, 0) + 1
                            if len(res.keys()) == 1:
                                kungfu = ''.join(res.keys())

                            else:
                                logger.info('这个人玩了多心法，仔细人工查找下')
                                failure_list.append(element)
                                kungfu = None
                        else:
                            kungfu = response.data[0]['name']

                    if kungfu is None or kungfu == []:
                        logger.info(f'{name} 排名{str(x)}: {role_id} {school} {server} {zone} 不存在')
                        failure_list.append(element)
                        continue

                    if kungfu in school_pinyin:
                        value = school_pinyin[kungfu]
                        logger.info(value)
                        school_top.update([value])
                else:
                    logger.info(school)
                    school_top.update([school])
            total_list.append(dict(school_top))
            logger.info(failure_list)
            logger.info('==' * 50)
            logger.info(total_list)

            return total_list
        except Exception as e:
            logger.info(school_top)
            logger.info(e)

    async def create_top_history_to_database(self):
        table_name = 'JJC_rank200_weekly_WLDG'
        await self.database.connect()
        sql = f'SELECT MAX(week) FROM {table_name}'

        result = await self.database.fetchall(sql)
        max_week = result[0]['MAX(week)']
        today = max_week + 1
        top_record = await self.get_top_history(today - 10)
        pvp_type = ['JJC_rank50_weekly_WLDG', 'JJC_rank100_weekly_WLDG', 'JJC_rank200_weekly_WLDG']

        for table_name, record_data in zip(pvp_type, top_record):
            sql = f"insert into {table_name} (week, 霸刀, 藏剑, 蓬莱, 无方,云裳,花间,少林,惊羽,丐帮,苍云,紫霞,相知,补天,凌雪,明教,毒经,灵素,天策,田螺,太虚,离经,莫问,衍天,冰心,刀宗,万灵) values ('%s','%s','%s',%s,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                today, record_data["霸刀"], record_data["藏剑"], record_data["蓬莱"], record_data["无方"],
                record_data["云裳"], record_data["花间"], record_data["少林"], record_data["惊羽"],
                record_data["丐帮"], record_data["苍云"], record_data["紫霞"], record_data["相知"], record_data["补天"],
                record_data["凌雪阁"], record_data["明教"], record_data["毒经"], record_data["灵素"],
                record_data["天策"], record_data["田螺"], record_data["太虚"], record_data["离经"], record_data["莫问"],
                record_data["衍天宗"], record_data["冰心"], record_data["刀宗"], record_data["万灵山庄"])
            await self.database.execute(sql)


# # # #
Record = GetJJCTopRecord()
asyncio.run(Record.create_top_history_to_database())
