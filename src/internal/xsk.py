# -*- coding: utf-8 -*-
import datetime
import requests
import hashlib
import hmac
import json


def format_body(data: dict) -> str:
    return json.dumps(data, separators=(',', ':'))


def gen_ts() -> str:
    return f"{datetime.datetime.now():%Y%m%d%H%M%S%f}"[:-3]


def gen_xsk(data: str) -> str:
    data += "@#?.#@"
    secret = "MaYoaMQ3zpWJFWtN9mqJqKpHrkdFwLd9DDlFWk2NnVR1mChVRI6THVe6KsCnhpoR"
    return hmac.new(secret.encode(), msg=data.encode(), digestmod=hashlib.sha256).hexdigest()


def get_arena_data(zone_name: str, server_name: str, role_id: str,  token: str) -> dict:
    param = {
        "role_id": role_id,
        "zone": zone_name,
        "server": server_name,
        "ts": gen_ts()
    }
    param = format_body(param)
    headers = {
        'Host': 'm.pvp.xoyo.com',
        'accept': 'application/json',
        'platform': 'ios',
        'gamename': 'jx3',
        'clientkey': '1',
        'cache-control': 'no-cache',
        'apiversion': '1',
        'sign': 'true',
        'token': token,
        'Content-Type': 'application/json',
        'Connection': 'Keep-Alive',
        'User-Agent': 'SeasunGame/178 CFNetwork/1240.0.2 Darwin/20.5.0',
        "X-Sk": gen_xsk(param)
    }
    data = requests.post(url="https://m.pvp.xoyo.com/role/indicator", data=param, headers=headers)
    return data.json()


if __name__ == '__main__':
    result = get_arena_data(
        zone_name="电信五区",
        server_name="斗转星移",
        role_id="16624814",
        token="b30ce6955e7b4e569e56d2cc0b0f2ac5:yamdereneko:kingsoft::ZGc2OHR4dzZ2NzJmMmh2aQ=="
    )
    print(result)
