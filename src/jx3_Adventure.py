import asyncio
import traceback
import dufte
import matplotlib
import nonebot
import src.Data.jxDatas as jxData
import json
import re
from contextlib import closing, suppress
from matplotlib import pyplot as plt
from playwright.async_api import async_playwright

matplotlib.rc("font", family='PingFang HK')


class Adventure:
    def __init__(self, server, user):
        self.server = jxData.mainServer(server)
        self.zone = jxData.mainZone(self.server)
        self.user = user

    async def query_user_info(self):
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()
            page.set_default_timeout(5000)

            await page.goto("https://www.jx3pd.com/serendipity")
            await page.locator("text=大区").click()
            await page.locator(f"text={self.zone}").click()
            await page.locator("text=服务器").click()
            await page.locator(f"text={self.server}").click()
            await page.locator("[placeholder=\"在此输入角色名字，按回车键或点击查询\"]").click()
            await page.locator("[placeholder=\"在此输入角色名字，按回车键或点击查询\"]").fill(self.user)
            await page.locator("[placeholder=\"在此输入角色名字，按回车键或点击查询\"]").press("Enter")
            await page.wait_for_load_state("domcontentloaded")
            task = await page.locator('tbody.ant-table-tbody').inner_text()
            # ---------------------
            await context.close()
            await browser.close()
            return task

    async def check_serendipity(self):
        task = await self.query_user_info()
        role_info_list = [i for i in re.split("[\t\n]", str(task)) if i != ""]
        with closing(
                open("sec/Data/serendipity.json")
        ) as resp:
            serendipity_json = json.load(resp)

        serendipity_Independent = []
        for line in serendipity_json:
            if line["type"] == "绝世奇遇" or line["type"] == "世界奇遇":
                serendipity_Independent.append(line["name"])

        role_list = []
        role_set = {}
        actions = ["用户名","奇遇","时间"]
        while True:
            if len(role_info_list) == 0:
                break
            for action in actions:
                role_set[action] = role_info_list.pop(0)
            role_list.append(role_set)
            role_set = {}

        role_Independent = []
        for task in role_list:
            if task["奇遇"] in serendipity_Independent:
                role_Independent.append(task)
        nonebot.logger.info(role_Independent)
        return role_Independent

    async def get_Fig(self):
        try:
            task = await self.check_serendipity()
            if task is None:
                nonebot.logger.error("获取用户信息失败，请查看问题.")
                return None
            elif not task:
                nonebot.logger.error("获取用户信息失败，请查看问题.")
                return None

            fig, ax = plt.subplots(figsize=(5, len(task) / 2), facecolor='white', edgecolor='white')
            plt.style.use(dufte.style)

            ax.axis([0, 5, 0, len(task) + 2])
            ax.axis('off')
            for floor, element in enumerate(task, start=1):
                adventure = element.get("奇遇")
                date = element.get("时间")
                floor = len(task) - floor + 1
                ax.text(0.5, floor, f'{adventure}', horizontalalignment='left',
                        color='#404040', verticalalignment='top')
                ax.text(2, floor, f'{date}', horizontalalignment='left',
                        color='#404040', verticalalignment='top')
            ax.text(2, len(task) + 2, f'{self.user}', fontsize=16, color='#303030',
                    fontweight="heavy", verticalalignment='top', horizontalalignment='center')

            plt.savefig(f"/tmp/adventure{self.user}.png")
        except Exception as e:
            nonebot.logger.error(e)
            nonebot.logger.error("获取用户信息失败，请查看报错.")
            traceback.print_exc()
            return None

