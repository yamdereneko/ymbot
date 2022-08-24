# import asyncio
# import json
# import traceback
# import nonebot
# import requests
# import src.Data.jxDatas as jxData
#
# headers = jxData.headers
#
# async def get_xsk(data=None):
#     try:
#         data = json.dumps(data)
#         res = requests.post(url="https://www.jx3api.com/token/calculate", data=data).json()
#         return res['data']['ts'], res['data']['sk']
#     except Exception as e:
#         nonebot.logger.error(e)
#         nonebot.logger.error("get_xsk失败，请查看问题.")
#         traceback.print_exc()
#
#
# async def get_person_history(person_id):
#     # 准备请求参数
#     try:
#         if person_id is None:
#             nonebot.logger.error("person_id 未获取到，返回空")
#             return None
#         param = {'person_id': str(person_id), "size": 20, "cursor": 0}
#         ts, xsk = await get_xsk(param)  # 获取ts和xsk， data 字典可以传ts,不传自动生成
#         param['ts'] = ts  # 给参数字典赋值ts参数
#         param = json.dumps(param).replace(" ", "")  # 记得格式化，参数需要提交原始json，非已格式化的json
#         headers['X-Sk'] = xsk  # 修改请求中的xsk
#         data = requests.post(url="https://m.pvp.xoyo.com/mine/match/person-history", data=param,
#                              headers=headers).json()
#         print(data)
#         return data
#     except Exception as e:
#         nonebot.logger.error(e)
#         nonebot.logger.error("获取用户信息失败，请查看问题.")
#         traceback.print_exc()
#         return None
#
# asyncio.run(get_person_history("fccddb1df1b8401f81fded4640899fe6"))

#
#
# import asyncio
# import time
# from playwright.async_api import async_playwright
#
# time_start = time.time()
#
# async def role_server(playwright, school):
#     try:
#         # 开启浏览器，默认设置浏览器引擎为chromium。
#         browser = await playwright.chromium.launch(headless=True)
#         context = await browser.new_context()
#         page = await context.new_page()
#         page.set_default_timeout(3000)
#         # 进入网站去获取各个门派总号数
#         await page.goto("https://jx3.seasunwbl.com/buyer?t=role")
#         await page.click("text=更多筛选条件")
#         await page.click("text=" + school)
#         await page.click("[aria-label=\"icon\\: search\"] svg")
#         await page.wait_for_timeout(2000)
#
#         dict_role = {}
#
#         # 查询成男号的数量
#         if await page.locator("text=" + school).first.text_content() != "七秀坊":
#             size = '成男'
#             Total = await searchBodySize(page, size)
#             dict_role[school+size] = Total
#
#         # 查询成女号的数量
#         if await page.locator("text=" + school).first.text_content() != "少林寺":
#             size = '成女'
#             Total = await searchBodySize(page, size)
#             dict_role[school+size] = Total
#
#         # 查询萝莉号数量
#         if await page.locator("text=" + school).first.text_content() != "少林寺":
#             size = '萝莉'
#             Total = await searchBodySize(page, size)
#             dict_role[school+size] = Total
#
#         # 查询正太号数量
#         size = '正太'
#         Total = await searchBodySize(page, size)
#         dict_role[school+size] = Total
#
#         await context.close()
#         await browser.close()
#         print(dict_role)
#         return dict_role
#     except Exception as e:
#         print("门派获取失败")
#         print(e)
#
#
# async def searchBodySize(page, size):
#     await page.wait_for_load_state('domcontentloaded')
#     await page.click("text=" + size)
#     await page.click("text=查询")
#     await page.wait_for_timeout(1000)
#     await page.wait_for_load_state('domcontentloaded')
#     if not await page.locator("//*[@id='app']/div/div[3]/div/div[3]/div[4]/ul/li[9]").is_visible(timeout=2000):
#         for i in range(7, 2, -1):
#             if await page.locator("//*[@id='app']/div/div[3]/div/div[3]/div[4]/ul/li["+str(i)+"]").is_visible(timeout=2000):
#                 await page.wait_for_timeout(500)
#                 size_count = await page.locator("//*[@id='app']/div/div[3]/div/div[3]/div[4]/ul/li["+str(i)+"]").text_content()
#                 await page.wait_for_timeout(500)
#                 await page.locator("//*[@id='app']/div/div[3]/div/div[3]/div[4]/ul/li["+str(i)+"]").click()
#                 await page.wait_for_timeout(500)
#                 rows = await page.locator("div.app-web-components-role-item-styles-index-m__roleItem--1R4F8").all_text_contents()
#                 sizeCount = (int(size_count) - 1) * 10 + len(rows)
#                 await page.wait_for_timeout(200)
#                 await page.locator("text=" + size).click()
#                 return sizeCount
#         rows = await page.locator("div.app-web-components-role-item-styles-index-m__roleItem--1R4F8").all_text_contents()
#         sizeCount = len(rows)
#         return sizeCount
#     elif int(await page.locator("//*[@id='app']/div/div[3]/div/div[3]/div[4]/ul/li[9]").text_content()) < 10:
#         for i in range(11, 2, -1):
#             await page.wait_for_timeout(500)
#             if not await page.locator("//*[@id='app']/div/div[3]/div/div[3]/div[4]/ul/li["+str(i)+"]").is_visible(timeout=2000):
#                 continue
#             elif await page.locator("//*[@id='app']/div/div[3]/div/div[3]/div[4]/ul/li["+str(i)+"]").text_content() == "下一页":
#                 continue
#             else:
#                 await page.wait_for_timeout(500)
#                 size_count = await page.locator("//*[@id='app']/div/div[3]/div/div[3]/div[4]/ul/li["+str(i)+"]").text_content()
#                 await page.wait_for_timeout(500)
#                 await page.locator("//*[@id='app']/div/div[3]/div/div[3]/div[4]/ul/li["+str(i)+"]").click()
#                 await page.wait_for_timeout(500)
#                 rows = await page.locator("div.app-web-components-role-item-styles-index-m__roleItem--1R4F8").all_text_contents()
#                 sizeCount = (int(size_count) - 1) * 10 + len(rows)
#                 await page.wait_for_timeout(200)
#                 await page.locator("text=" + size).click()
#                 return sizeCount
#     else:
#         await page.wait_for_timeout(500)
#         size_count = await page.locator("//*[@id='app']/div/div[3]/div/div[3]/div[4]/ul/li[9]").text_content()
#         await page.wait_for_timeout(500)
#         await page.locator("//*[@id='app']/div/div[3]/div/div[3]/div[4]/ul/li[9]").click()
#         await page.wait_for_timeout(500)
#         rows = await page.locator("div.app-web-components-role-item-styles-index-m__roleItem--1R4F8").all_text_contents()
#         sizeCount = (int(size_count) - 1) * 10 + len(rows)
#         await page.wait_for_timeout(200)
#         await page.locator("text=" + size).click()
#         return sizeCount
#
# async def role(school):
#     async with async_playwright() as playwright:
#         role_choose = await role_server(playwright, school)
#     return role_choose
#
# print(asyncio.run(role("大侠")))
# time_end = time.time()
# time_sum = time_start - time_end
# print(time_sum)
import asyncio
import json
import re
from contextlib import closing, suppress

text = """芋泥泥	万灵当歌
2022-08-23 13:41:59

芋泥泥	黑白路
2022-08-01 19:56:10

芋泥泥	兔江湖
2022-07-13 16:58:54

芋泥泥	劝学记
2022-07-07 10:06:58

芋泥泥	谜书生
2021-06-19 02:02:53

芋泥泥	尘网中
2021-01-16 00:13:16

芋泥泥	白月皎
2021-01-15 23:54:05

芋泥泥	太行道
2020-11-24 21:13:04

芋泥泥	瀛洲梦
2020-11-12 04:24:35

芋泥泥	沧海笛
2020-11-03 20:08:51

芋泥泥	滴水恩
2020-10-14 20:26:53

芋泥泥	秘宝图
2020-09-24 05:32:05

芋泥泥	莫贪杯
2020-09-17 04:10:21

芋泥泥	露园事
2020-07-27 14:10:49

芋泥泥	一念间
2020-05-13 11:03:39

芋泥泥	江湖录
2020-03-06 10:41:36

芋泥泥	北行镖
2020-01-31 17:12:36"""


async def check_serendipity():
    role_info_list = [i for i in re.split("[\t\n]", text) if i != ""]
    with closing(
            open("Data/serendipity.json")
    ) as resp:
        serendipity_json = json.load(resp)

    serendipity_Independent = []
    for line in serendipity_json:
        if line["type"] == "绝世奇遇" or line["type"] == "世界奇遇":
            serendipity_Independent.append(line["name"])

    role_list = []
    role_set = {}

    while True:
        if len(role_info_list) == 0:
            break
        role_set["用户名"] = role_info_list.pop(0)
        role_set["奇遇"] = role_info_list.pop(0)
        role_set["时间"] = role_info_list.pop(0)
        role_list.append(role_set)
        role_set = {}

    role_Independent = []
    for task in role_list:
        if task["奇遇"] in serendipity_Independent:
            role_Independent.append(task)

    print(role_Independent)


asyncio.run(check_serendipity())
