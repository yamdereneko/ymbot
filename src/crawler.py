import asyncio
import src.Data.jxDatas as jxData
from playwright.async_api import async_playwright


class Fireworks:
    def __init__(self, server, user):
        self.server = jxData.mainServer(server)
        self.zone = jxData.mainZone(self.server)
        self.user = user

    async def query_user_info(self):
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch(headless=False)
            context = await browser.new_context()
            page = await context.new_page()
            # Go to https://www.jx3pd.com/firework
            await page.goto("https://www.jx3pd.com/firework")
            # Click text=大区
            await page.locator("text=大区").click()
            # Click text=电信五区
            await page.locator(f"text={self.zone}").first.click()

            # Click text=服务器
            await page.locator("text=服务器").click()
            # Click text=斗转星移
            await page.locator(f"text={self.server}").click()
            # Click [placeholder="在此输入角色名字，按回车键或点击查询"]
            await page.locator("[placeholder=\"在此输入角色名字，按回车键或点击查询\"]").click()
            await page.locator("[placeholder=\"在此输入角色名字，按回车键或点击查询\"]").fill(self.user)
            # Click button:has-text("查 询")
            await page.locator("button:has-text(\"查 询\")").click()
            # Click main:has-text("大区电信五区服务器斗转星移查 询烟花赠方收方地图时间真橙之心小疏竹小丛兰侠客岛2022-08-20 14:29:07真橙之心小丛兰小疏竹侠客岛2022-08-2")
            await page.wait_for_load_state("domcontentloaded")
            rows = await page.locator('tbody.ant-table-tbody').inner_text()
            print(rows)

            # ---------------------
            await context.close()
            await browser.close()


fireworks = Fireworks("斗转星移","芋泥泥")
asyncio.run(fireworks.query_user_info())