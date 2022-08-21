#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from src.Data import jxDatas
from src import jx3_GetJJCTopRecord as GetJJCTopRecord
from src import jx3_JJCRecord as JJCRecord
from src import jx3_WanBaoLouInfo as WanBaoLouInfo
from src import jx3_PersonHistory as PersonInfo
from src import jx3_ServerState as ServerState
from src import jx3_Daily
from pydantic import BaseModel
from typing import Union
import nonebot
from fastapi.responses import JSONResponse
from fastapi import FastAPI, HTTPException, Request

nonebot.init(_env_file=".env.dev", apscheduler_autostart=True)
app: FastAPI = nonebot.get_asgi()


class UnicornException(Exception):
    def __init__(self, name: str, content: str):
        self.name = name
        self.content = content


class RoleName(BaseModel):
    Role_name: Union[str, None] = None
    Server: Union[str, None] = None


class personInfo(BaseModel):
    Role_name: Union[str, None] = None
    Server: Union[str, None] = None


class Transaction(BaseModel):
    Shape: Union[str, None] = None
    School: Union[str, None] = None


class JJCWeekly(BaseModel):
    Week: Union[int, None] = None


class ServerStateModel(BaseModel):
    Server: Union[str, None] = None


class Daily(BaseModel):
    Server: Union[str, None] = None
    Next: Union[int, None] = None


# ************************************************
# 代码实现部分 实际代码为异步

def roles(shape, school):
    role = WanBaoLouInfo.main(shape, school)
    return role


def get_jjc_Record(role_name, server):
    role_JJC_Record = JJCRecord.GetPersonRecord(role_name, server)
    person_JJC_Record = role_JJC_Record.get_person_record()
    return person_JJC_Record


def get_person_history(role_name, server):
    person_info = PersonInfo.GetPersonInfo(role_name, server)
    person_history_res = person_info.main()
    return person_history_res


def get_JJCTop_Record(table, week):
    jjcRecord = GetJJCTopRecord.GetJJCTopInfo(table, week, "")
    jjcTopRecord = jjcRecord.get_JJCWeeklyRecord()
    return jjcTopRecord


def get_ServerState(server=None):
    State = ServerState.ServerState(server)
    server_state = State.get_server_list()
    return server_state


def get_Daily(server=None, daily_next=None):
    daily = jx3_Daily.GetDaily(server, daily_next)
    daily_info = daily.QueryTodayDaily()
    return daily_info


# ***************************************
# 接口部分(以下)

@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=404,
        content={"code": "404", "msg": f"\'{exc.name}\'{exc.content}，请重新尝试.", "data": {}},
    )


# JJC个人战绩查询
# 入参 { "Role_name": "笋笋","Server":"姨妈" }
@app.get("/jx3/jjc")
async def jjc_record_api(
        role: Union[RoleName, None] = None
):
    if role is None:
        raise HTTPException(status_code=500, detail="参数未填，请填入参数，如：{ 'Role_name': '笋笋', 'Server':'姨妈' }")
    jjc_record = await get_jjc_Record(role.Role_name, role.Server)
    if jjc_record is None:
        raise UnicornException(name=role.Role_name, content="该用户信息不存在")
    nonebot.logger.info(jjc_record)
    return {"code": 0, "msg": "success", "role_name": role.Role_name, "data": jjc_record}


# 推栏个人查询
# 入参 { "Role_name": "笋笋" }
@app.get("/jx3/person")
async def person_history_api(
        role: Union[personInfo, None] = None,
):
    if role is None:
        raise HTTPException(status_code=500, detail="参数未填，请填入参数，如：{ 'Role_name': '笋笋' }")
    person_res = await get_person_history(role.Role_name, role.Server)
    if person_res is None:
        raise UnicornException(name=role.Role_name, content="该用户信息不存在")
    nonebot.logger.info(person_res)
    return {"code": 0, "msg": "success", "role_name": role.Role_name, "server": role.Server,
            "data": person_res}


# 万宝楼情况查询
# 入参 { "Shape": "萝莉", School: "蓬莱" }
@app.get("/jx3/role")
async def jx3_Role_Api(
        transaction: Union[Transaction, None] = None
):
    if transaction is None:
        raise HTTPException(status_code=500, detail="参数未填，请填入参数，如：{ 'Shape': '萝莉', School: '蓬莱' }")
    school_dict = jxDatas.school_number
    shape_dict = jxDatas.bodyType
    if transaction.School not in school_dict:
        raise UnicornException(name="门派", content="该门派不存在，请重试")
    if transaction.Shape not in shape_dict:
        raise UnicornException(name="体型", content="该体型不存在，请重试")
    roleInfo, role_sum = await roles(transaction.Shape, transaction.School)
    if roleInfo == "-11":
        raise UnicornException(name="", content="网站维护中...")
    nonebot.logger.info(roleInfo)
    return {"code": 0, "msg": "success", "school": transaction.School, "shape": transaction.Shape,
            "roles_sum": role_sum,
            "data": roleInfo}


# JJC TOP200查询
# 入参 { "Week": 30 }
@app.get("/jx3/jjcTop200")
async def jjc_TopRecord_api(
        weekly: Union[JJCWeekly, None] = None
):
    if weekly is None:
        raise HTTPException(status_code=500, detail="参数未填，请填入参数，如：{ 'Week': 32 }")
    table = "JJC_rank_weekly"
    jjcTopRecord = await get_JJCTop_Record(table, weekly.Week)
    if jjcTopRecord is None:
        raise UnicornException(name=str(weekly.Week), content="该周竞技场信息不存在")
    nonebot.logger.info(jjcTopRecord)
    return {"code": 0, "msg": "success", "Type": "Top200", "weekly": weekly.Week, "data": jjcTopRecord}


# JJC TOP50查询
# 入参 { "Week": 30 }
@app.get("/jx3/jjcTop50")
async def jjc_TopRecord_api(
        weekly: Union[JJCWeekly, None] = None
):
    if weekly is None:
        raise HTTPException(status_code=500, detail="参数未填，请填入参数，如：{ 'Week': 32 }")
    table = "JJC_rank50_weekly"
    jjcTopRecord = await get_JJCTop_Record(table, weekly.Week)
    if jjcTopRecord is None:
        raise UnicornException(name=str(weekly.Week), content="该周竞技场信息不存在")
    nonebot.logger.info(jjcTopRecord)
    return {"code": 0, "msg": "success", "Type": "Top50", "weekly": weekly.Week, "data": jjcTopRecord}


# 服务器状态查询
@app.get("/jx3/check")
async def check_ServerState(
        SingleServerState: Union[ServerStateModel, None] = None
):
    if SingleServerState is None:
        serverInfo = await get_ServerState()
    else:
        serverInfo = await get_ServerState(SingleServerState.Server)
        for info in serverInfo:
            if info.get("mainServer") == jxDatas.mainServer(SingleServerState.Server):
                return {"code": 0, "msg": "success", "data": info}
    if serverInfo is None:
        raise UnicornException(name=str(), content="区服信息查询失败")
    return {"code": 0, "msg": "success", "data": serverInfo}


# 服务器状态查询
@app.get("/jx3/daily")
async def daily_api(
        daily: Daily = None
):
    if daily is None:
        dailyInfo = await get_Daily()
    else:
        dailyInfo = await get_Daily(daily.Server, daily.Next)
    if dailyInfo is None:
        raise UnicornException(name=str(), content="日常查询失败")
    return {"code": 0, "msg": "success", "data": dailyInfo}
