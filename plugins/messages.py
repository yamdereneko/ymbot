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
import pathlib
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
import src.jx3_Equip as jx3_Equip
import src.jx3_JJCTop as jx3_JJCTop
import src.chatGPT.Chat_GPT_API as Chat_API

RoleJJCRecord = on_command("RoleJJCRecord", rule=keyword("战绩", "JJC信息"), aliases={"战绩", "JJC信息"}, priority=5)
Equip = on_command("Equip", rule=keyword("装备"), aliases={"装备"}, priority=5)
JJCTop = on_command("JJCTop", rule=keyword("JJC趋势图"), aliases={"JJC趋势图"}, priority=5)
ServerCheck = on_command("ServerCheck", rule=keyword("开服"), aliases={"开服"}, priority=5)
AllServerState = on_command("AllServerState", rule=keyword("区服"), aliases={"区服"}, priority=5)
PersonInfo = on_command("PersonInfo", rule=keyword("角色"), aliases={"角色"}, priority=5)
Daily = on_command("Daily", rule=keyword("日常"), aliases={"日常"}, priority=5)
Adventure = on_command("Adventure", rule=keyword("奇遇"), aliases={"奇遇"}, priority=5)
Fireworks = on_command("Fireworks", rule=keyword("烟花"), aliases={"烟花"}, priority=5)
SaoHua = on_command("SaoHua", rule=keyword("骚话"), aliases={"骚话"}, priority=5)
Strategy = on_command("Strategy", rule=keyword("奇遇攻略", "攻略"), aliases={"奇遇攻略", "攻略"}, priority=5)
Require = on_command("Require", rule=keyword("奇遇前置"), aliases={"奇遇前置"}, priority=5)
Recruit = on_command("Recruit", rule=keyword("招募"), aliases={"招募"}, priority=5)
Price = on_command("Price", rule=keyword("物价"), aliases={"物价"}, priority=5)
Flatterer = on_command("Flatterer", rule=keyword("舔狗日志"), aliases={"舔狗日志"}, priority=5)
Announce = on_command("Announce", rule=keyword("公告"), aliases={"公告"}, priority=5)
Sand = on_command("Sand", rule=keyword("沙盘"), aliases={"沙盘"}, priority=5)
Chat = on_command("Chat", rule=keyword("提问", "疑问"), aliases={"提问", "疑问"}, priority=5)
CreateJJCTopDataToDataBase = on_command("CreateJJCTopDataToDataBase", rule=keyword("生成JJC趋势图"), aliases={"生成JJC趋势图"},
                                        priority=5)
Chutianshe = on_command("Chutianshe", rule=keyword("楚天社", "行侠"), aliases={"楚天社", "行侠"}, priority=5)
Serverd_Group = on_command("Serverd_Group", rule=keyword("群组"), aliases={"群组"}, priority=5)


async def redis_check_operation(frame, frame_name, data, image_frame):
    red = redis.Redis()
    red_data = await red.query(frame_name)
    if red_data:
        if json.loads(red_data) == data:
            await red.get_image(frame_name + '_image', frame)
            msg = MessageSegment.image('file:' + frame)
            return msg
        else:
            await red.delete(frame_name)
            await red.delete(frame_name + '_image')
    await red.add(frame_name, data)
    await red.insert_image(frame_name + '_image', image_frame)
    msg = MessageSegment.image('file:' + image_frame)
    return msg


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
            record_image = await jjc_record.get_person_record_figure()
            msg = MessageSegment.image(record_image)
            await RoleJJCRecord.finish(msg)
        else:
            nonebot.logger.error(f"{role_name} JJC战绩查询不存在,请重试")
            await RoleJJCRecord.reject(f"{server} {role_name} JJC战绩查询不存在,请重试")
    else:
        nonebot.logger.error(f"{server} 大区不存在,请重试")


@JJCTop.handle()
async def onMessage_JJCTop(matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text()
    if plain_text:
        # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
        if len(plain_text.split(' ')) >= 3:
            plain_text = re.sub(r'[ ]+', ' ', plain_text)
            top_type = plain_text.split(" ")[0]
            week = plain_text.split(" ")[1]
            school_type = plain_text.split(" ")[2]

            jjc_info = jx3JJCInfo.GetJJCTopInfo(table=int(top_type), weekly=int(week), school_type=school_type)
            jjc_data = await jjc_info.from_sql_create_figure()

            frame = f"/tmp/top_{jjc_data}.png"
            frame_name = 'top_' + top_type + '_' + week + '_' + school_type
            msg = await redis_check_operation(frame, frame_name, jjc_data, frame)
            await JJCTop.finish(msg)


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
    daily_image = await daily.query_daily_figure()
    msg = MessageSegment.image(daily_image)
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
            await Adventure.reject('该用户未被收录')
        nonebot.logger.info(user_adventure_data)
        user_adventure_image = await adventure.create_figure()
        msg = MessageSegment.image(user_adventure_image)
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
        if user_fireworks_data:
            frame = f"/tmp/fireworks_{user}.png"
            frame_name = 'fireworks_' + user
            user_fireworks_image = await fireworks.get_Fig()
            image_frame = f"/tmp/fireworks{user_fireworks_image}.png"
            msg = await redis_check_operation(frame, frame_name, user_fireworks_data, image_frame)
            await Fireworks.finish(msg)
        else:
            msg = "该用户不存在"
            await Fireworks.reject(msg)
    else:
        nonebot.logger.error("请求错误,请参考: 烟花 区服 角色名")
        await Fireworks.reject("请求错误,请参考: 烟花 区服 角色名")


# 楚天社部分
@Chutianshe.handle()
async def onMessage_Chutianshe():
    chutianshe_data = await jx3_Multifunction.get_chutianshe()
    msg = MessageSegment.text(chutianshe_data)
    await Chutianshe.finish(msg)


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
        adventure = jx3Data.adventure(plain_text)
        if adventure is None:
            await Strategy.reject("请重新输入正确的奇遇名词")
        else:
            frame = f"/tmp/{adventure}.png"
            file_obj = pathlib.Path(frame)
            if not file_obj.exists():
                red = redis.Redis()
                await red.get_image(adventure, frame)
            msg = MessageSegment.image('file:' + frame)
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


@Equip.handle()
async def onMessage_Equip(matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text()
    if plain_text:
        # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
        if plain_text.find(" ") != -1:
            server = jx3Data.mainServer(re.split('[ ]+', plain_text)[0])
            role_name = re.split('[ ]+', plain_text)[1]
            equip_info = jx3_Equip.GetRoleEquip(server, role_name)
            equip_info_time = await equip_info.create_images()
            if equip_info_time:
                msg = MessageSegment.image(equip_info_time)
                await Equip.finish(msg)
        else:
            nonebot.logger.error("格式错误，请尝试: 装备 大区 名字")
            await Equip.reject("格式错误，请尝试: 装备 大区 名字")
    else:
        nonebot.logger.error("格式错误，请尝试: 装备 大区 名字")
        await Equip.reject("格式错误，请尝试: 装备 大区 名字")


@Price.handle()
async def onMessage_Price(args: Message = CommandArg()):
    if args.extract_plain_text() != "":
        plain_text = args.extract_plain_text()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
        price = jx3_Price.Price(plain_text)
        price_data = await price.query_mono_price()
        if price_data:
            price_image = await price.create_price_figure()
            msg = MessageSegment.image(price_image)
            await Price.finish(msg)
        else:
            msg = "该物价不存在，请重新填写"
            await Price.reject(msg)
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


@Serverd_Group.handle()
async def onMessage_Serverd_Group(args: Message = CommandArg()):
    plain_text = args.extract_plain_text()
    red = redis.Redis()
    command = plain_text.split(' ')[0]
    if command:
        match command:
            case "查看":
                group_list = await red.query_list("group_list")
                group_list_text = '\n'.join(group_list)
                msg = f"目前正在提供服务的群: \n{group_list_text}"
            case "添加":
                if plain_text.find(" ") != -1:
                    command_info = plain_text.split(' ')[1]
                    await red.insert_list("group_list", command_info)
                    msg = f"添加服务的群为: {command_info}"
                else:
                    msg = f"请在命令后面添加具体的群组信息"
            case "移除" | "删除":
                if plain_text.find(" ") != -1:
                    command_info = plain_text.split(' ')[1]
                    await red.delete_list("group_list", command_info)
                    msg = f"正在移除服务的群为: {command_info}"
                else:
                    msg = f"请在命令后面添加具体的群组信息"
            case _:
                msg = f"错误的命令: {command}, 正确的命令有： 添加 移除 查看"
        await Serverd_Group.finish(msg)
    else:
        await Serverd_Group.reject("命令失败，请重试")
