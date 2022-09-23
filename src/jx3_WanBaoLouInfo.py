import asyncio
from httpx import AsyncClient
import src.Data.jxDatas as jxData


async def request_api(size, school, page):
    client = AsyncClient()
    bodyType = jxData.bodyType
    role_experience_point = '100000' + "," + '1000000'
    school_type = jxData.school_number
    url = "https://api-wanbaolou.xoyo.com/api/buyer/goods/list?req_id=uMgUXwDzog9NvLr8DooaK88r1mT96RXL&game_id=jx3" \
          "&zone_id=&server_id=&filter[account_type]=1&filter[price]=0&filter[state]=0&filter[tags]=0&filter[" \
          "role_sect]={0}&filter[role_shape]={1}&filter[role_camp]=0&filter[role_equipment_point]=0&filter[" \
          "role_experience_point]={3}&filter[role_level]=0&filter[role_appearance]=&filter[" \
          "role_zixing_point]=0&filter[role_homeland_level]=0&game=jx3&page={2}&size=10&goods_type=2&sort[" \
          "role_experience_point]=0".format(school_type[school], bodyType[size], page, role_experience_point)
    # url = "https://api-wanbaolou.xoyo.com/api/buyer/goods/list?game_id=jx3&filter%5Brole_sect%5D={0}&filter%5Brole_shape%5D={1}&game=jx3&page={2}&size=10&goods_type=2&sort[role_experience_point]=0".format(
    #     school_type[school], bodyType[size], page)
    payload = {}
    headers = {"Content-Type": "application/json"}
    response = await client.get(url=url, headers=headers, params=payload)
    print(response)
    if response.status_code != 200:
        print('网站不能正确响应，请查看具体返回')
    elif response.json()['code'] != 1:
        print('网站不能正确响应，请查看具体返回')
    print(response.json())
    return response.json()


async def main(size, school, page: int = 1):
    man = await request_api(size, school, page)
    if man.get('code') == -1:
        roles_dict = "-11"
        return roles_dict, 0
    # print(man.get("data").get("total_record"))
    roles_dict = []
    roles = {}
    role_sum = man.get("data").get("total_record")
    for role in man.get("data").get("list"):
        # print(role)
        # roles["门派"] = role.get("attrs").get("role_sect")
        # roles["装分"] = role.get("attrs").get("role_equipment_point")
        # roles["资历"] = role.get("attrs").get("role_experience_point")
        # roles["阵营"] = role.get("attrs").get("role_camp")
        # roles["体型"] = role.get("attrs").get("role_shape")
        # roles["价格"] = role.get("single_unit_price") / 100
        # roles["点赞"] = role.get("followed_num")
        # roles["服务器"] = role.get("info").split("-")[1]
        # roles["链接"] = "https://jx3.seasunwbl.com/role?consignment_id=" + role.get("consignment_id")
        roles_dict.append(role)
    print(roles_dict)
    return roles_dict, role_sum
