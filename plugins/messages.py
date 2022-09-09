# -*- coding: utf-8 -*
"""
@Software : PyCharm
@File : message.py
@Author : 喵
@Time : 2022/08/11 22:39:29
@Docs : 回复插件开发
"""
import re
import nonebot
from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.rule import keyword
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.params import CommandArg
from nonebot.log import logger, default_format
import src.Data.jxDatas as jx3Data
import src.jx3_GetJJCTopRecord as jx3JJCInfo
import src.jx3_JJCRecord as JJCRecord
import src.jx3_ServerState as ServerState
import src.jx3_PersonHistory as PersonHistory
import src.jx3_Daily as DailyInfo
import src.jx3_Adventure as jx3_Adventure
import src.jx3_Fireworks as jx3_Fireworks
import src.jx3_Multifunction as jx3_Multifunction

RoleJJCRecord = on_command("RoleJJCRecord", rule=keyword("战绩", "JJC信息"), aliases={"战绩", "JJC信息"}, priority=5)
JJCTop = on_command("JJCTop", rule=keyword("JJC趋势图"), aliases={"JJC趋势图"}, priority=5)
JJCTop50 = on_command("JJCTop50", rule=keyword("JJC50趋势图"), aliases={"JJC50趋势图"}, priority=5)
ServerCheck = on_command("ServerCheck", rule=keyword("开服"), aliases={"开服"}, priority=5)
AllServerState = on_command("AllServerState", rule=keyword("区服"), aliases={"区服"}, priority=5)
PersonInfo = on_command("PersonInfo", rule=keyword("角色"), aliases={"角色"}, priority=5)
Daily = on_command("Daily", rule=keyword("日常"), aliases={"日常"}, priority=5)
Adventure = on_command("Adventure", rule=keyword("奇遇"), aliases={"奇遇"}, priority=5)
Fireworks = on_command("Fireworks", rule=keyword("烟花"), aliases={"烟花"}, priority=5)
SaoHua = on_command("SaoHua", rule=keyword("骚话"), aliases={"骚话"}, priority=5)
Strategy = on_command("Strategy", rule=keyword("奇遇攻略"), aliases={"奇遇攻略"}, priority=5)
Require = on_command("Require", rule=keyword("奇遇前置"), aliases={"奇遇前置"}, priority=5)


@RoleJJCRecord.handle()
async def onMessage_RoleJJCRecord(matcher: Matcher, args: Message = CommandArg()):
    if args.extract_plain_text() != "":
        plain_text = args.extract_plain_text()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
        if plain_text.find(" ") != -1:
            plain_text = re.sub(r'[ ]+', ' ', plain_text)
            server = plain_text.split(" ")[0]
            server_right = jx3Data.mainServer(server)
            if server_right is not None:
                role_name = plain_text.split(" ")[1]
                jjc_record = JJCRecord.GetPersonRecord(role_name, server)
                res = await jjc_record.get_person_record()
                if res is not None:
                    msg = MessageSegment.image(f"file:/tmp/record{res}.png")
                    await RoleJJCRecord.finish(msg)
                else:
                    nonebot.logger.error(f"{role_name} JJC战绩查询不存在,请重试")
                    await RoleJJCRecord.reject(f"{server} {role_name} JJC战绩查询不存在,请重试")
            else:
                nonebot.logger.error(f"{server} 大区不存在,请重试")
    else:
        nonebot.logger.error("请求错误,请参考: 战绩 区服 用户名")
        await RoleJJCRecord.reject("请求错误,请参考: 战绩 区服 用户名")


# 接收 JJC趋势图
# JJC趋势图 31或者门派 ==> 调用存储在/tmp目录下得图片
# 图片形式发送
@JJCTop.handle()
async def onMessage_JJCTop(matcher: Matcher, args: Message = CommandArg()):
    if args.extract_plain_text() != "":
        plain_text = args.extract_plain_text()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
        if plain_text is not None:
            if plain_text.find(" ") != -1:
                plain_text = re.sub(r'[ ]+', ' ', plain_text)
                topType = plain_text.split(" ")[0]
                week = plain_text.split(" ")[1]
                table = "JJC_rank_weekly"
                if topType == "200":
                    table = "JJC_rank_weekly"
                elif topType == "50":
                    table = "JJC_rank50_weekly"
                jjcInfo = jx3JJCInfo.GetJJCTopInfo(table, int(week), "")
                record_figure = await jjcInfo.get_JJCWeeklyRecord()
                if record_figure is not None:
                    msg = MessageSegment.image(f"file:///tmp/top{table}.png")
                    await JJCTop.finish(msg)
                else:
                    nonebot.logger.error("创建趋势图失败，请检查报错")
            else:
                if jx3Data.school(plain_text) in jx3Data.all_school.keys():
                    table = "JJC_rank_weekly"
                    jjcInfo = jx3JJCInfo.GetJJCTopInfo(table, 0, plain_text)
                    record_figure = await jjcInfo.get_JJCWeeklySchoolRecord()
                    if record_figure is not None:
                        msg = MessageSegment.image(f"file:/tmp/schoolTop{jx3Data.school(plain_text)}.png")
                        await JJCTop.finish(msg)
                    else:
                        nonebot.logger.error("创建趋势图失败，请检查报错")
                else:
                    nonebot.logger.error("输入错误，请检查报错")
        else:
            nonebot.logger.error("参数错误，请重新输入正确参数")
            await JJCTop.reject("参数错误，请重新输入正确参数")
    else:
        nonebot.logger.error("请求错误,请参考: JJC趋势图 31或者门派")
        await JJCTop.reject("请求错误,请参考: JJC趋势图 31或者门派")


# 接收 角色信息 查询本地角色最近游玩的角色的JJC战绩
# 角色 区服 用户名 ==> 目前的角色JJC战绩
# 图片形式发送
@PersonInfo.handle()
async def onMessage_PersonInfo(matcher: Matcher, args: Message = CommandArg()):
    if args.extract_plain_text() != "":
        plain_text = args.extract_plain_text()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
        if plain_text.find(" ") != -1:
            plain_text = re.sub(r'[ ]+', ' ', plain_text)
            server = plain_text.split(" ")[0]
            serverRight = jx3Data.mainServer(server)
            if serverRight is not None:
                roleName = plain_text.split(" ")[1]
                personInfo = PersonHistory.GetPersonInfo(roleName, server)
                role_name = await personInfo.get_Fig()
                if role_name is not None:
                    msg = MessageSegment.image(f"file:/tmp/role{role_name}.png")
                    await PersonInfo.finish(msg)
                else:
                    nonebot.logger.error("用户信息未成功获取，请重试")
                    await PersonInfo.reject("用户信息未成功获取，请重试")
            else:
                nonebot.logger.error("区服输入错误，请重试")
                await PersonInfo.reject("区服输入错误，请重试")
    else:
        nonebot.logger.error("请求错误,请参考: 角色 区服 用户名")
        await PersonInfo.reject("请求错误,请参考: 角色 区服 用户名")


@ServerCheck.handle()
async def onMessage_ServerCheck(matcher: Matcher, args: Message = CommandArg()):
    if args.extract_plain_text() != "":
        plain_text = args.extract_plain_text().replace(" ", "")
        all_serverState = ServerState.ServerState(plain_text)
        serverState = await all_serverState.get_server_list()
        serverName = jx3Data.mainServer(plain_text)
        if serverName is not None:
            for info in serverState:
                if info.get("mainServer") == serverName:
                    server_state = info.get("connectState")
                    state = server_state is True and serverName + "已开服" or serverName + "未开服"
                    await ServerCheck.finish(state)
            nonebot.logger.info("开服数据未得到，请检查")
            await ServerCheck.reject("未找到区服,请重新输入")
        else:
            nonebot.logger.error("开服数据未得到，请检查")
    else:
        nonebot.logger.error("请求错误,请参考:开服 姨妈 ")
        await ServerCheck.reject("请求错误,请参考:开服 姨妈 ")


@AllServerState.handle()
async def onMessage_AllServerState(matcher: Matcher, args: Message = CommandArg()):
    if args.extract_plain_text() == "":
        plain_text = args.extract_plain_text()
        all_serverState = ServerState.ServerState(plain_text)
        if await all_serverState.get_figure() is True:
            msg = MessageSegment.image(f"file:/tmp/serverState.png")
            await AllServerState.finish(msg)
        else:
            nonebot.logger.error("全区服图未正常创建，请查看")
            await AllServerState.reject("未找到区服,请重新输入")
    else:
        await AllServerState.reject("请求错误,请参考:区服")


@Daily.handle()
async def onMessage_Daily(matcher: Matcher, args: Message = CommandArg()):
    if args.extract_plain_text() != "":
        plain_text = args.extract_plain_text()
        if plain_text.find(" ") != -1:
            plain_text = re.sub(r'[ ]+', ' ', plain_text)
            server = jx3Data.mainServer(plain_text.split(" ")[1])
            if server is not None:
                daily_date = plain_text.split(" ")[0]
                match daily_date:
                    case "明天":
                        day = 1
                    case "后天" | "第二天":
                        day = 2
                    case "大后天" | "第三天":
                        day = 3
                    case _:
                        day = 0
                daily = DailyInfo.GetDaily(server, day)
                state = await daily.query_daily_figure()
                if state is not None:
                    msg = MessageSegment.image(f"file:/tmp/daily{state}.png")
                    await Daily.finish(msg)
        else:
            nonebot.logger.error("请求错误,请参考:日常 大区 明天")
            await Daily.reject("请求错误,请参考:日常 大区 明天")
    else:
        daily = DailyInfo.GetDaily()
        datetime = await daily.query_daily_figure()
        if datetime is not None:
            msg = MessageSegment.image(f"file:/tmp/daily{datetime}.png")
            await Daily.finish(msg)
        else:
            await Daily.reject("日常请求失败")


@Adventure.handle()
async def onMessage_Adventure(matcher: Matcher, args: Message = CommandArg()):
    if args.extract_plain_text() != "":
        plain_text = args.extract_plain_text()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
        if plain_text.find(" ") != -1:
            server = jx3Data.mainServer(re.split('[ ]+', plain_text)[0])
            if server is not None:
                user = re.split('[ ]+', plain_text)[1]
                adventure = jx3_Adventure.Adventure(server, user)
                datetime = await adventure.get_Fig()
                if datetime is not None:
                    msg = MessageSegment.image(f"file:/tmp/adventure{datetime}.png")
                    await Adventure.finish(msg)
            else:
                nonebot.logger.error("奇遇获取大区信息填写失败，请重试")
                await Adventure.reject("奇遇获取大区信息填写失败，请重试")
        else:
            nonebot.logger.error("奇遇获取输入错误，请重试，参考：奇遇 区服 角色名")
            await Adventure.reject("奇遇获取输入错误，请重试，参考：奇遇 区服 角色名")
    else:
        nonebot.logger.error("请求错误,请参考: 奇遇 区服 角色名")
        await Adventure.reject("请求错误,请参考: 奇遇 区服 角色名")


@Fireworks.handle()
async def onMessage_Fireworks(matcher: Matcher, args: Message = CommandArg()):
    if args.extract_plain_text() != "":
        plain_text = args.extract_plain_text()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
        if plain_text.find(" ") != -1:
            server = jx3Data.mainServer(re.split('[ ]+', plain_text)[0])
            if server is not None:
                user = re.split('[ ]+', plain_text)[1]
                fireworks = jx3_Fireworks.Fireworks(server, user)
                datetime = await fireworks.get_Fig()
                if datetime is not None:
                    msg = MessageSegment.image(f"file:/tmp/fireworks{datetime}.png")
                    await Fireworks.finish(msg)
            else:
                nonebot.logger.error("烟花获取大区信息填写失败，请重试")
                await Fireworks.reject("烟花获取大区信息填写失败，请重试")
        else:
            nonebot.logger.error("烟花获取输入错误，请重试，参考：奇遇 区服 角色名")
            await Fireworks.reject("烟花获取输入错误，请重试，参考：奇遇 区服 角色名")
    else:
        nonebot.logger.error("请求错误,请参考: 烟花 区服 角色名")
        await Fireworks.reject("请求错误,请参考: 烟花 区服 角色名")


# 骚话部分
@SaoHua.handle()
async def onMessage_SaoHua():
    saohua = await jx3_Multifunction.get_random()
    msg = MessageSegment.text(saohua['text'])
    await SaoHua.finish(msg)


@Strategy.handle()
async def onMessage_Strategy(matcher: Matcher, args: Message = CommandArg()):
    if args.extract_plain_text() != "":
        plain_text = args.extract_plain_text()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
        strategy = await jx3_Multifunction.get_strategy(plain_text)
        image_url = strategy['url']
        msg = MessageSegment.image(image_url)
        await Strategy.finish(msg)
    else:
        nonebot.logger.error("请求错误,请参考: 奇遇攻略 奇遇名")
        await Strategy.reject("请求错误,请参考: 奇遇攻略 奇遇名")


@Require.handle()
async def onMessage_Strategy(matcher: Matcher, args: Message = CommandArg()):
    if args.extract_plain_text() != "":
        plain_text = args.extract_plain_text()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
        require = await jx3_Multifunction.get_require(plain_text)
        image_url = require['upload']
        msg = MessageSegment.image(image_url)
        await Require.finish(msg)
    else:
        nonebot.logger.error("请求错误,请参考: 奇遇前置 奇遇名")
        await Require.reject("请求错误,请参考: 奇遇前置 奇遇名")

# @roleJJCRecord.got("role", prompt="你想查询哪个角色信息呢？")
# async def handle_city(role: Message = Arg(), roleName: str = ArgPlainText("role")):
#     await roleJJCRecord.reject(role.template("你想查询的角色 {role} 暂不支持，请重新输入！"))


#
# @roleJJCRecord.got("role", prompt="你想查询哪个角色信息呢？")
# async def handle_city(role: Message = Arg(), roleName: str = ArgPlainText("role")):
#     nonebot.logger.info(role)
#     if roleName not in ["笋笋"]:  # 如果参数不符合要求，则提示用户重新输入
#         # 可以使用平台的 Message 类直接构造模板消息
#         await roleJJCRecord.reject(role.template("你想查询的角色 {role} 暂不支持，请重新输入！"))
#     role_info = await get_roleInfo(roleName)
#     await roleJJCRecord.finish(role_info)
#

# 在这里编写获取JJC信息的函数
# async def get_roleJJCInfo(role: str) -> str:
#     # params = {'Role_name': role}
#     # JJCInfo = httpx.get('https://localhost:8080/jjc', params=params).json()
#     data = await jx3API.get_jjc_Record(role)
#     if data is None:
#         await roleJJCRecord.reject(f"你想查询的角色{role}不存在")
#     for i in data:
#         match_id = i.get("match_id")
#         print(i)
#     return f"{data}"
