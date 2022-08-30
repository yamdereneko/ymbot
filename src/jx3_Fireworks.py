import re
import traceback
import dufte
import matplotlib
import nonebot
import src.Data.jxDatas as jxData
from matplotlib import pyplot as plt
from playwright.async_api import async_playwright

matplotlib.rc("font", family='PingFang HK')


class Fireworks:
    def __init__(self, server, user):
        self.server = jxData.mainServer(server)
        self.zone = jxData.mainZone(self.server)
        self.user = user

    async def query_user_info(self):
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()
            # Go to https://www.jx3pd.com/firework
            await page.goto("https://www.jx3pd.com/firework")
            # Click text=大区
            await page.wait_for_load_state("domcontentloaded")
            await page.locator("text=大区").click()
            # Click text=电信五区
            await page.locator(f"text={self.zone}").first.click()

            # Click text=服务器
            await page.locator("text=服务器").click()
            # Click text=斗转星移
            await page.locator(f"text={self.server}").click()
            # Click [placeholder="在此输入角色名字，按回车键或点击查询"]
            await page.locator("[placeholder=\"在此输入角色名字，按回车键搜索\\.\\.\\.\"]").click()
            await page.locator("[placeholder=\"在此输入角色名字，按回车键搜索\\.\\.\\.\"]").fill(self.user)
            # Click button:has-text("查 询")
            await page.locator("[placeholder=\"在此输入角色名字，按回车键搜索\\.\\.\\.\"]").press("Enter")
            # Click main:has-text("大区电信五区服务器斗转星移查 询烟花赠方收方地图时间真橙之心小疏竹小丛兰侠客岛2022-08-20 14:29:07真橙之心小丛兰小疏竹侠客岛2022-08-2")
            await page.wait_for_load_state("domcontentloaded")
            role_info = await page.locator('tbody.ant-table-tbody').inner_text()
            # ---------------------
            await context.close()
            await browser.close()
            return role_info

    async def check_fireworks(self):
        task = await self.query_user_info()
        role_info_list = [i for i in re.split("[\t\n]", task) if i != ""]
        actions = ["烟花", "赠方", "收方", "地图", "时间"]
        role_list = []
        role_set = {}

        while True:
            if len(role_info_list) == 0:
                break
            for action in actions:
                role_set[action] = role_info_list.pop(0)
            role_list.append(role_set)
            role_set = {}
        return role_list

    async def get_Fig(self):
        try:
            task = await self.check_fireworks()
            if task is None:
                nonebot.logger.error("获取用户信息失败，请查看问题.")
                return None
            elif not task:
                nonebot.logger.error("获取用户信息失败，请查看问题.")
                return None

            fig, ax = plt.subplots(figsize=(11, len(task) / 2), facecolor='white', edgecolor='white')
            plt.style.use(dufte.style)
            task.insert(0, {'烟花': '烟花', "赠方": "赠方", "收方": "收方", "地图": "地图", "时间": "时间"})
            ax.axis([0, 10, 0, len(task) + 2])
            ax.axis('off')
            for floor, element in enumerate(task):
                fire = element.get("烟花")
                fire_map_send = element.get("赠方")
                fire_map_get = element.get("收方")
                fire_map = element.get("地图")
                fire_date = element.get("时间")
                floor = len(task) - floor + 1
                ax.text(0, floor, f'{fire}', horizontalalignment='left',
                        color='#404040', verticalalignment='top')
                ax.text(1.5, floor, f'{fire_map_send}', horizontalalignment='left',
                        color='#404040', verticalalignment='top')
                ax.text(4.5, floor, f'{fire_map_get}', horizontalalignment='left',
                        color='#404040', verticalalignment='top')
                ax.text(7, floor, f'{fire_map}', horizontalalignment='left',
                        color='#404040', verticalalignment='top')
                ax.text(8, floor, f'{fire_date}', horizontalalignment='left',
                        color='#404040', verticalalignment='top')
            ax.set_title(f'{self.user}', fontsize=16, color='#303030',
                         fontweight="heavy", verticalalignment='top', horizontalalignment='center')
            plt.savefig(f"/tmp/fireworks{self.user}.png")
        except Exception as e:
            nonebot.logger.error(e)
            nonebot.logger.error("获取用户信息失败，请查看报错.")
            traceback.print_exc()
            return None
