# -*- coding: utf-8 -*
"""
@Software : PyCharm
@File : message.py
@Author : 喵
@Time : 2022/08/11 22:39:29
@Docs : 回复插件开发
"""
import json
import re
import nonebot
from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.rule import keyword
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.params import CommandArg
from plugins.brower import browser
from src.Data.jxDatas import server_binding
import src.Data.jx3_Redis as redis
import src.Data.jxDatas as jx3Data
import src.jx3_GetJJCTopRecord as jx3JJCInfo
import src.jx3_JJCRecord as JJCRecord
import src.jx3_ServerState as ServerState
import src.jx3_PersonHistory as PersonHistory
import src.jx3_Daily as DailyInfo
import src.jx3_Adventure as jx3_Adventure
import src.jx3_Fireworks as jx3_Fireworks
import src.jx3_Multifunction as jx3_Multifunction
import src.jx3_Recruit as jx3_Recruit
import src.jx3_Price as jx3_Price
import src.jx3_JJCTop as jx3_JJCTop
import src.chatGPT.Chat_GPT_API as Chat_API

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
Recruit = on_command("Recruit", rule=keyword("招募"), aliases={"招募"}, priority=5)
Price = on_command("Price", rule=keyword("物价"), aliases={"物价"}, priority=5)
Flatterer = on_command("Flatterer", rule=keyword("舔狗日志"), aliases={"舔狗日志"}, priority=5)
Announce = on_command("Announce", rule=keyword("公告"), aliases={"公告"}, priority=5)
Sand = on_command("Sand", rule=keyword("沙盘"), aliases={"沙盘"}, priority=5)
Chat = on_command("Chat", rule=keyword("提问", "疑问"), aliases={"提问", "疑问"}, priority=5)
CreateJJCTopDataToDataBase = on_command("CreateJJCTopDataToDataBase", rule=keyword("生成JJC趋势图"), aliases={"生成JJC趋势图"},
                                        priority=5)


@RoleJJCRecord.handle()
async def onMessage_RoleJJCRecord(matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
    plain_text = re.sub(r'[ ]+', ' ', plain_text)
    if plain_text.find(" ") != -1:
        server = plain_text.split(" ")[0]
        role_name = plain_text.split(" ")[1]
    else:
        server = jx3Data.server_binding
        role_name = plain_text
    server_right = jx3Data.mainServer(server)
    if server_right:
        jjc_record = JJCRecord.GetPersonRecord(role_name, server)
        record = await jjc_record.get_person_record()
        if record:
            red = redis.Redis()
            frame = f"/tmp/record{role_name}.png"
            redis_record_data = await red.query('record_' + role_name)
            if redis_record_data:
                res = json.loads(redis_record_data)
                if res == record:
                    await red.get_image('record_' + role_name + '_image', frame)
                    msg = MessageSegment.image('file:' + frame)
                    await RoleJJCRecord.finish(msg)
                else:
                    await red.delete('record_' + role_name)
                    await red.delete('record_' + role_name + '_image')

            await red.add('record_' + role_name, record)
            record_image = await jjc_record.get_person_record_figure(record)
            frame = f"/tmp/record{record_image}.png"
            await red.insert_image('record_' + role_name + '_image', frame)
            msg = MessageSegment.image('file:' + frame)
            await RoleJJCRecord.finish(msg)
        else:
            nonebot.logger.error(f"{role_name} JJC战绩查询不存在,请重试")
            await RoleJJCRecord.reject(f"{server} {role_name} JJC战绩查询不存在,请重试")
    else:
        nonebot.logger.error(f"{server} 大区不存在,请重试")


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
                top_type = plain_text.split(" ")[0]
                week = plain_text.split(" ")[1]
                table = "JJC_rank_weekly"
                if top_type == "200":
                    table = "JJC_rank_weekly"
                elif top_type == "50":
                    table = "JJC_rank50_weekly"

                jjc_info = jx3JJCInfo.GetJJCTopInfo(table, int(week), "")
                record = await jjc_info.get_JJCWeeklyRecord()
                red = redis.Redis()
                frame = f"/tmp/top{table}.png"
                redis_record_data = await red.query('top_' + table + '_' + week)
                if redis_record_data:
                    res = json.loads(redis_record_data)
                    if res == record:
                        await red.get_image('top_' + table + '_image_' + week, frame)
                        msg = MessageSegment.image('file:' + frame)
                        await JJCTop.finish(msg)
                    else:
                        await red.delete('top_' + table + '_' + week)
                        await red.delete('top_' + table + '_image_' + week)

                await red.add('top_' + table + '_' + week, record)
                person_image = await jjc_info.get_JJCWeeklyRecord_figure(record)
                frame = f"/tmp/top{person_image}.png"
                await red.insert_image('top_' + table + '_image_' + week, frame)
                msg = MessageSegment.image('file:' + frame)
                await JJCTop.finish(msg)
            else:
                if jx3Data.school(plain_text) in jx3Data.all_school.keys():
                    table = "JJC_rank_weekly"
                    jjc_info = jx3JJCInfo.GetJJCTopInfo(table, 0, plain_text)

                    record = await jjc_info.get_JJCWeeklySchoolRecord()
                    red = redis.Redis()
                    frame = f"/tmp/SchoolTop{table}.png"
                    redis_record_data = await red.query('SchoolTop_' + table + '_' + plain_text)
                    if redis_record_data:
                        res = json.loads(redis_record_data)
                        if res == record:
                            await red.get_image('SchoolTop_' + table + '_image_' + plain_text, frame)
                            msg = MessageSegment.image('file:' + frame)
                            await JJCTop.finish(msg)
                        else:
                            await red.delete('SchoolTop_' + table + '_' + plain_text)
                            await red.delete('SchoolTop_' + table + '_image_' + plain_text)

                    await red.add('SchoolTop_' + table + '_' + plain_text, record)
                    person_image = await jjc_info.get_JJCWeeklySchoolRecord_figure(record)
                    frame = f"/tmp/SchoolTop{person_image}.png"
                    await red.insert_image('SchoolTop_' + table + '_image_' + plain_text, frame)
                    msg = MessageSegment.image('file:' + frame)
                    await JJCTop.finish(msg)
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
            server_right = jx3Data.mainServer(server)
            if server_right is not None:
                role = plain_text.split(" ")[1]
                person_info = PersonHistory.GetPersonInfo(role, server)
                role_info = await person_info.get_person_info()
                red = redis.Redis()
                frame = f"/tmp/role{role}.png"
                redis_person_data = await red.query('person_' + role)

                if redis_person_data:
                    res = json.loads(redis_person_data)
                    if res == role_info:
                        await red.get_image('person_' + role + '_image', frame)
                        msg = MessageSegment.image('file:' + frame)
                        await PersonInfo.finish(msg)
                    else:
                        await red.delete('person_' + role)
                        await red.delete('person_' + role + '_image')

                await red.add('person_' + role, role_info)
                person_image = await person_info.get_Fig(role_info)
                frame = f"/tmp/role{person_image}.png"
                await red.insert_image('person_' + role + '_image', frame)
                msg = MessageSegment.image('file:' + frame)
                await PersonInfo.finish(msg)
            else:
                nonebot.logger.error("区服输入错误，请重试")
                await PersonInfo.reject("区服输入错误，请重试")
    else:
        nonebot.logger.error("请求错误,请参考: 角色 区服 用户名")
        await PersonInfo.reject("请求错误,请参考: 角色 区服 用户名")


@ServerCheck.handle()
async def onMessage_ServerCheck(args: Message = CommandArg()):
    plain_text = args.extract_plain_text()
    if plain_text == "":
        plain_text = jx3Data.server_binding
    server_state = ServerState.ServerState(plain_text)
    server_data = await server_state.check_server_state()
    nonebot.logger.info(server_data)
    if server_data.code == 200:
        state = server_data.data['status'] == 1 and plain_text + "已开服" or plain_text + "未开服"
        await ServerCheck.finish(state)
    else:
        nonebot.logger.error("开服数据未得到，请检查")


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
async def onMessage_Daily():
    daily = DailyInfo.GetDaily()
    daily_data = await daily.get_daily()
    red = redis.Redis()
    frame = f"/tmp/daily.png"
    redis_daily_data = await red.query('daily')
    if redis_daily_data:
        res = json.loads(redis_daily_data)
        if res == daily_data:
            await red.get_image('daily_image', frame)
            msg = MessageSegment.image('file:' + frame)
            await Daily.finish(msg)
        else:
            await red.delete('daily')
            await red.delete('daily_image')

    await red.add('daily', daily_data)
    daily_image = await daily.query_daily_figure(daily_data)
    frame = f"/tmp/daily{daily_image}.png"
    await red.insert_image('daily_image', frame)
    msg = MessageSegment.image('file:' + frame)
    await Daily.finish(msg)


@Adventure.handle()
async def onMessage_Adventure(matcher: Matcher, args: Message = CommandArg()):
    if args.extract_plain_text() != "":
        plain_text = args.extract_plain_text()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
        if plain_text.find(" ") != -1:
            server = jx3Data.mainServer(re.split('[ ]+', plain_text)[0])
            user = re.split('[ ]+', plain_text)[1]
        else:
            server = server_binding
            user = plain_text
        adventure = jx3_Adventure.Adventure(server, user)
        user_adventure_data = await adventure.query_user_info()
        if user_adventure_data is None:
            await Adventure.reject('数据异常，请联系管理员')
        nonebot.logger.info(user_adventure_data)
        red = redis.Redis()
        frame = f"/tmp/adventure{user}.png"
        redis_adventure_data = await red.query('adventure_' + user)
        if redis_adventure_data:
            res = json.loads(redis_adventure_data)
            if res == user_adventure_data:
                await red.get_image('adventure_' + user + '_image', frame)
                msg = MessageSegment.image('file:' + frame)
                await Adventure.finish(msg)
            else:
                await red.delete('adventure_' + user)
                await red.delete('adventure_' + user + '_image')
        await red.add('adventure_' + user, user_adventure_data)
        user_adventure_image = await adventure.get_Fig(user_adventure_data)
        frame = f"/tmp/adventure{user_adventure_image}.png"
        await red.insert_image('adventure_' + user + '_image', frame)
        msg = MessageSegment.image('file:' + frame)
        await Adventure.finish(msg)
    else:
        nonebot.logger.error("请求错误,请参考: 奇遇 区服 角色名")
        await Adventure.reject("请求错误,请参考: 奇遇 区服 角色名")


@Fireworks.handle()
async def onMessage_Fireworks(matcher: Matcher, args: Message = CommandArg()):
    if args.extract_plain_text() != "":
        plain_text = args.extract_plain_text()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
        if plain_text.find(" ") != -1:
            server = jx3Data.mainServer(re.split('[ ]+', plain_text)[0])
            user = re.split('[ ]+', plain_text)[1]
        else:
            server = server_binding
            user = plain_text
        fireworks = jx3_Fireworks.Fireworks(server, user)
        user_fireworks_data = await fireworks.query_user_firework_info()
        red = redis.Redis()
        frame = f"/tmp/fireworks{user}.png"
        redis_fireworks_data = await red.query('fireworks_' + user)
        if redis_fireworks_data:
            res = json.loads(redis_fireworks_data)
            if res == user_fireworks_data:
                await red.get_image('fireworks_' + user + '_image', frame)
                msg = MessageSegment.image('file:' + frame)
                await Fireworks.finish(msg)
            else:
                await red.delete('fireworks_' + user)
                await red.delete('fireworks_' + user + '_image')

        await red.add('fireworks_' + user, user_fireworks_data)
        user_fireworks_image = await fireworks.get_Fig()
        frame = f"/tmp/fireworks{user_fireworks_image}.png"
        await red.insert_image('fireworks_' + user + '_image', frame)
        msg = MessageSegment.image('file:' + frame)
        await Fireworks.finish(msg)

    else:
        nonebot.logger.error("请求错误,请参考: 烟花 区服 角色名")
        await Fireworks.reject("请求错误,请参考: 烟花 区服 角色名")


# 骚话部分
@SaoHua.handle()
async def onMessage_SaoHua():
    saohua = await jx3_Multifunction.get_random()
    msg = MessageSegment.text(saohua['text'])
    await SaoHua.finish(msg)


@Flatterer.handle()
async def onMessage_Flatterer():
    flatterer = await jx3_Multifunction.get_flatterer()
    msg = MessageSegment.text(flatterer['text'])
    await Flatterer.finish(msg)


@Announce.handle()
async def onMessage_Announce():
    announce = await jx3_Multifunction.get_announce()
    announce_title = announce[0]['title']
    text = announce[0]['type'] + '\n' + announce[0]['title'] + '\n' + announce[0]['date'] + '\n' + announce[0]['url']
    frame = f"/tmp/Announce_{announce_title}.png"
    red = redis.Redis()
    redis_announce_title = await red.exist('announce_' + announce_title)
    if redis_announce_title:
        await red.get_image('announce_' + announce_title, frame)
        msg = MessageSegment.image('file:' + frame)
    else:
        images = await browser.get_image_from_url(announce[0]['url'])
        await red.insert_image_encode('announce_' + announce_title, images)
        msg = MessageSegment.image(images)
    await Announce.finish(text + msg)


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


@Sand.handle()
async def onMessage_Sand(matcher: Matcher, args: Message = CommandArg()):
    if args.extract_plain_text() != "":
        plain_text = args.extract_plain_text()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海

        sand = await jx3_Multifunction.get_sand_map(jx3Data.mainServer(plain_text))
        image_url = sand['url']
        msg = MessageSegment.image(image_url)
        await Sand.finish(msg)
    else:
        nonebot.logger.error("请求错误,请参考: 沙盘 服务器")
        await Sand.reject("请求错误,请参考: 沙盘 服务器")


@Recruit.handle()
async def onMessage_Recruit(matcher: Matcher, args: Message = CommandArg()):
    if args.extract_plain_text() != "":
        plain_text = args.extract_plain_text()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
        if plain_text.find(" ") != -1:
            server = jx3Data.mainServer(re.split('[ ]+', plain_text)[0])
            recruit_text = re.split('[ ]+', plain_text)[1]
        else:
            server = server_binding
            recruit_text = plain_text

        recruit = jx3_Recruit.Recruit(server, recruit_text)
        recruit_total = await recruit.get_Fig()
        if recruit_total:
            recruit_image = f"/tmp/recruit{recruit_total}.png"
            msg = MessageSegment.image('file:' + recruit_image)
            await Recruit.finish(msg)
        else:
            msg = MessageSegment.text("获取不到招募信息，请稍后再试")
            await Recruit.reject(msg)
    else:
        recruit = jx3_Recruit.Recruit(server_binding)
        recruit_total = await recruit.get_Fig()
        if recruit_total:
            recruit_image = f"/tmp/recruit{recruit_total}.png"
            msg = MessageSegment.image('file:' + recruit_image)
            await Recruit.finish(msg)
        nonebot.logger.error("招募获取大区信息失败，请重试")
        await Recruit.reject("招募获取大区填写失败，请重试")


@Price.handle()
async def onMessage_Price(args: Message = CommandArg()):
    if args.extract_plain_text() != "":
        plain_text = args.extract_plain_text()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
        price = jx3_Price.Price(plain_text)
        price_data = await price.query_mono_price()
        red = redis.Redis()
        frame = f"/tmp/price.png"
        redis_price_data = await red.query('price_' + plain_text)
        if redis_price_data:
            res = json.loads(redis_price_data)
            if res == price_data.data:
                await red.get_image('price_image_' + plain_text, frame)
                msg = MessageSegment.image('file:' + frame)
                await Price.finish(msg)
            else:
                await red.delete('price')
                await red.delete('price_image_' + plain_text)

        await red.add('price_' + plain_text, price_data.data)
        price_image = await price.create_price_figure()
        frame = f"/tmp/price{price_image}.png"
        await red.insert_image('price_image_' + plain_text, frame)
        msg = MessageSegment.image('file:' + frame)
        await Price.finish(msg)
    else:
        nonebot.logger.error("物价信息填写失败，请重试")
        await Price.reject("物价信息填写失败，请重试")


@Chat.handle()
async def onMessage_Chat(args: Message = CommandArg()):
    if args.extract_plain_text() != "":
        plain_text = args.extract_plain_text()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
        await Chat.send("正在思考中...")
        chat = Chat_API.ChatGPTAPI()
        chat_result = await chat.call_api(plain_text)
        msg_text = chat_result.choices
        msg = msg_text[0]["text"].replace('\n\n', '\n')
        await Chat.finish(msg)
    else:
        nonebot.logger.error("信息填写失败，请重试")
        await Chat.reject("信息填写失败，请重试")


@CreateJJCTopDataToDataBase.handle()
async def onMessage_CreateJJCTopDataToDataBase(args: Message = CommandArg()):
    plain_text = args.extract_plain_text()
    if plain_text != "":
        if plain_text.find(" ") != -1:
            pvp_type = re.split('[ ]+', plain_text)[0]
            weekly = re.split('[ ]+', plain_text)[1]
        else:
            pvp_type = 200
            weekly = plain_text
        top_data = jx3_JJCTop.GetJJCTopRecord(weekly=weekly, pvp_type=pvp_type)
        top_data_to_database = await top_data.create_top_history_to_database()
        if top_data_to_database is None:
            msg = MessageSegment.text('JJC数据同步失败，请查看报错')
            await CreateJJCTopDataToDataBase.finish(msg)
        else:
            msg = MessageSegment.text('JJC数据同步成果')
            await CreateJJCTopDataToDataBase.finish(msg)
    else:
        await CreateJJCTopDataToDataBase.finish("1111")

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
