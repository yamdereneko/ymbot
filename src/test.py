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
#
# text = """金鸾喻情	老猹子@梦江南	小卫兰@梦江南	侠客岛
# 2022-08-18 22:43:06
#
# 真橙之心	小卫兰@梦江南	老猹子@梦江南	成都
# 2022-08-11 21:13:03
#
# 慕佳期	小焦迈奇	老猹子@梦江南	苍云
# 2022-08-06 18:06:34
#
# 吹落心雨	小焦迈奇	老猹子@梦江南	苍云
# 2022-08-06 18:06:14
#
# 此间心同	小焦迈奇	老猹子@梦江南	苍云
# 2022-08-06 18:06:11
#
# 岁星流金	小焦迈奇	老猹子@梦江南	苍云
# 2022-08-06 18:06:07
#
# 山河回响	老猹子@梦江南	小焦迈奇	苍云
# 2022-08-06 18:01:39
#
# 任行逍遥	老猹子@梦江南	小焦迈奇	苍云
# 2022-08-06 18:01:37
#
# 任行逍遥	老猹子@梦江南	小焦迈奇	苍云
# 2022-08-06 18:01:35
#
# 鹊桥引仙	老猹子@梦江南	小焦迈奇	苍云
# 2022-08-06 18:01:34
#
# 万家灯火	老猹子@梦江南	小焦迈奇	苍云
# 2022-08-06 18:01:32
#
# 海誓山盟	老猹子@梦江南	小疏竹	成都
# 2022-08-04 22:45:01
#
# 山河回响	老猹子@梦江南	甜酒酿汤圆2@梦江南	成都
# 2022-08-04 22:42:25
#
# 任行逍遥	甜酒酿汤圆2@梦江南	老猹子@梦江南	成都
# 2022-08-04 22:41:59
#
# 福倒了	甜酒酿汤圆2@梦江南	老猹子@梦江南	成都
# 2022-08-04 22:41:57
#
# 海誓山盟	老猹子@梦江南	甜酒酿汤圆2@梦江南	成都
# 2022-08-04 22:37:47
# """


# async def check_serendipity():
#     role_info_list = [i for i in re.split("[\t\n]", text) if i != ""]
#     actions = ["烟花", "赠方", "收方", "地图", "时间"]
#     role_list = []
#     role_set = {}
#
#     while True:
#         if len(role_info_list) == 0:
#             break
#         for action in actions:
#             role_set[action] = role_info_list.pop(0)
#         role_list.append(role_set)
#         role_set = {}
#     print(role_list)
#
#
# asyncio.run(check_serendipity())
import asyncio
import httpx


async def main():
    async with httpx.AsyncClient() as client:
        param = {'server': "斗转星移", 'next': 1}
        response = await client.get('https://www.jx3api.com/app/daily',params=param)
        print(response.json())


asyncio.run(main())
