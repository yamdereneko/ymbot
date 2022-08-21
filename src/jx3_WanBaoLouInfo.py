import requests
import pymysql
import src.Data.jxDatas as jxData
import datetime


async def connect_Mysql(shape, shcool, role_sum):
    try:
        db = pymysql.connect(host="localhost", user="root", password="Qinhao123.", database="farbnamen", charset="utf8")
        cursor = db.cursor()
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sql = "insert into wanbaolou_number (shape, school, quantity, time) values ('%s', '%s',%s,'%s')" % (shape, shcool, role_sum, now_time)
        cursor.execute(sql)
        db.commit()
        cursor.fetchall()
        db.close()
    except Exception as e:
        print(e)
        print("连接数据库异常")


async def request_api(size, school, page):
    bodyType = jxData.bodyType
    school_type = jxData.school_number
    url = "https://api-wanbaolou.xoyo.com/api/buyer/goods/list?game_id=jx3&filter%5Brole_sect%5D={0}&filter%5Brole_shape%5D={1}&game=jx3&page={2}&size=10&goods_type=2".format(
        school_type[school], bodyType[size], page)
    payload = {}
    headers = {"Content-Type": "application/json"}
    response = requests.get(url, headers=headers, data=payload)
    return response.json()


async def main(size, school, page: int = 1):
    man = await request_api(size, school, page)
    if man.get("code") == -11:
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
    await connect_Mysql(size, school, role_sum)
    return roles_dict, role_sum
