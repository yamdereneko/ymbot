import asyncio
import src.Data.jxDatas as jxData
from playwright.async_api import async_playwright
import json
import re
from contextlib import closing, suppress


class Adventure:
    def __init__(self, server, user):
        self.server = jxData.mainServer(server)
        self.zone = jxData.mainZone(self.server)
        self.user = user

    async def query_user_info(self):
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch(headless=False)
            context = await browser.new_context()
            page = await context.new_page()
            page.set_default_timeout(2000)

            await page.goto("https://www.jx3pd.com/serendipity")
            await page.locator("text=大区").click()
            await page.locator(f"text={self.zone}").click()
            await page.locator("text=服务器").click()
            await page.locator(f"text={self.server}").click()
            await page.locator("[placeholder=\"在此输入角色名字，按回车键或点击查询\"]").click()
            await page.locator("[placeholder=\"在此输入角色名字，按回车键或点击查询\"]").fill("芋泥泥")
            await page.wait_for_load_state("domcontentloaded")
            task = await page.locator('tbody.ant-table-tbody').inner_text()
            print(task)
            # ---------------------
            await context.close()
            await browser.close()

    async def check_serendipity(self):
        task = await self.query_user_info()
        role_info_list = [i for i in re.split("[\t\n]", str(task)) if i != ""]
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


adventure = Adventure("斗转星移", "芋泥泥")
asyncio.run(adventure.query_user_info())
