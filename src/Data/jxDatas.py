import asyncio
import random
import redis
from pydantic import BaseModel, Extra, Field

"""
    jx3apiToken
"""
jx3api_ticket = "nrje86v129l78x4g9m"

"""
    推栏token连接池
"""

ticket = ['143d202ba5034faea12dc232cd8f0429:yandereneko:kingsoft::dzEyNG43ZWxuYXp5ZGN0Mw==',
          '9d57f8159597435889bd0b7e77ad92db:yamdereneko:kingsoft::dTByZXBhemFkNjY0dGdseA==',
          '2a1ca92bf2114d3eaacb0be40e04319f:yandereneko1:kingsoft::MGxmbnQ1NGRoZ2Rpa3ZrZA==',
          'f4f2a4465f4f464a99f50691024792d1:yandereneko2:kingsoft::bmRqcDA2aG9zcXRjeHFjag==']

server_binding = "斗转星移"

redis_config = redis.Redis(
    host='114.115.181.82',  # ip地址
    port=6379,  # 端口号
    db=0,
    decode_responses=True,
    password="qinhao123"
    # 设置为True存的数据格式就是str类型
)

headers = {
    "accept": "application/json",
    "platform": "ios",
    "gamename": "jx3",
    "clientkey": "1",
    "cache-control": "no-cache",
    "apiversion": "1",
    "sign": "true",
    "Content-Type": "application/json",
    "Host": "m.pvp.xoyo.com",
    "Connection": "Keep-Alive",
    "Accept-Encoding": "gzip",
    "token": random.choice(ticket),
    "User-Agent": "SeasunGame/193 CFNetwork/1333.0.4 Darwin/21.5.0",
    "X-Sk": None
}


class Jx3ApiConfig(BaseModel, extra=Extra.ignore):
    """
    jx3api的配置
    """

    ws_path: str = Field("", alias="jx3api_ws_path")
    """ws连接地址"""
    ws_token: str = Field("", alias="jx3api_ws_token")
    """ws的token"""
    api_url: str = Field("", alias="jx3api_url")
    """主站的url"""
    api_token: str = Field("", alias="jx3api_token")
    """主站的token"""

#

group_list = ["1077830347", "642668185"]

# group_list = ["549242180"]

config = {
    'host': '114.115.181.82',  # 连接主机名。
    'user': 'root',  # 用户账号
    'password': 'Qinhao123.',  # 用户密码
    'db': 'farbnamen',  # 数据库名
    'port': 3306,  # 连接端口
    'charset': 'utf8',  # 数据编码
    'minsize': 12,  # 连接池最小值
    'maxsize': 96,  # 连接池最大值
    'autocommit': True,  # 自动提交模式
}

all_school = {'霸刀': 10, '少林': 12, '补天': 12, '蓬莱': 14, '紫霞': 14, '藏剑': 13, '明教': 7, '云裳': 17, '花间': 12, '丐帮': 5,
              '凌雪阁': 8, '田螺': 6, '惊羽': 5, '相知': 14, '胎虚': 5, '苍云': 5, '天策': 8, '无方': 11, '灵素': 6, '冰心': 3, '毒经': 6,
              '衍天宗': 2, '莫问': 1, '离经': 3}



bodyType = {
    "成男": 1,
    "成女": 2,
    "正太": 3,
    "萝莉": 4
}
school_number = {
    "大侠": 99,
    "凌雪阁": 1,
    "蓬莱": 2,
    "霸刀": 3,
    "长歌": 4,
    "苍云": 5,
    "丐帮": 6,
    "明教": 7,
    "唐门": 8,
    "五毒": 9,
    "藏剑": 10,
    "天策": 11,
    "纯阳": 12,
    "少林": 13,
    "七秀": 14,
    "万花": 15,
    "衍天宗": 16,
    "北天药宗": 17
}
much_school = {
    "长歌": 4,
    "唐门": 8,
    "五毒": 9,
    "纯阳": 12,
    "七秀": 14,
    "万花": 15,
    "北天药宗": 17
}

school_pinyin = {
    "huajian": "花间",
    "lijing": "离经",
    "yunshang": "云裳",
    "bingxin": "冰心",
    "wufang": "无方",
    "lingsu": "灵素",
    "mowen": "莫问",
    "xiangzhi": "相知",
    "tianluo": "田螺",
    "jingyu": "惊羽",
    "dujing": "毒经",
    "butian": "补天",
    "zixia": "紫霞",
    "taixu": "胎虚",
}

'''
0101 = 长安城
0115 = 龙争虎斗
0126 = 蝶恋花
0502 = 梦江南
0505 = 唯我独尊
0524 = 剑胆琴心
0519 = 幽月轮
0514 = 乾坤一掷
0515 = 斗转星移
0807 = 绝代天骄
2106 = 破阵子
2107 = 天鹅坪
2204 = 飞龙在天
2402 = 青梅煮酒

10002 = 洗髓经
10003 = 易筋经
10028 = 离经易道
10021 = 花间游
10062 = 铁牢律
10026 = 傲血战意
10014 = 紫霞功
10015 = 太虚剑意
10080 = 云裳心经
10081 = 冰心诀
10176 = 补天诀
10175 = 毒经
10145 = 山居剑意
10225 = 天罗诡道
10224 = 惊羽诀
10243 = 明尊琉璃体
10242 = 焚影圣诀
10268 = 笑尘诀
10389 = 铁骨衣
10390 = 分山劲
10448 = 相知
10447 = 莫问
10464 = 北傲诀
10533 = 凌海诀
10585 = 隐龙诀
10615 = 太玄经
10626 = 灵素
10627 = 无方
10628 = 孤锋诀

1 = 少林
2 = 万花
3 = 天策
4 = 纯阳
5 = 七秀
6 = 五毒
7 = 唐门
8 = 藏剑
9 = 丐帮
10 = 明教
21 = 苍云
22 = 长歌
23 = 霸刀
24 = 蓬莱
25 = 凌雪
211 = 衍天
212 = 药宗
213 = 刀宗
'''

def school(method):
    match method:
        case "凌雪" | "0雪" | "野猪":
            return "凌雪"
        case "霸刀" | "刀刀" | "貂貂":
            return "霸刀"
        case "和尚" | "灯泡" | "大师":
            return "少林"
        case "奶毒" | "毒奶" | "补天决":
            return "补天"
        case "蓬莱" | "鸟人" | "雕雕" | "凌海决" | "凌海":
            return "蓬莱"
        case "气纯" | "道长" | "咩咩":
            return "紫霞"
        case "黄鸡" | "鸡哥" | "山居":
            return "藏剑"
        case "喵喵" | "焚影" | "喵哥" | "喵姐":
            return "明教"
        case "奶秀" | "秀奶" | "秀人":
            return "云裳"
        case "盆栽" | "花间游":
            return "花间"
        case "丐狗" | "丐人" | "笑尘":
            return "丐帮"
        case "田螺" | "天罗":
            return "田螺"
        case "鲸鱼" | "唐门" | "惊羽决":
            return "惊羽"
        case "奶歌" | "歌奶" | "奶哥" | "奶鸽" | "鸽奶":
            return "相知"
        case "太虚" | "剑纯" | "阿胎" | "阿胎" | "太虚剑意":
            return "胎虚"
        case "铁王八" | "王八" | "分山":
            return "苍云"
        case "狗策" | "狗人" | "策人":
            return "天策"
        case "无方门" | "药毒" | "毒药":
            return "无方"
        case "奶药" | "药奶" | "药药":
            return "灵素"
        case "冰心决":
            return "冰心"
        case "毒人" | "毒毒":
            return "毒经"
        case "衍天" | "灯灯":
            return "衍天"
        case "长歌门" | "莫问决" | "长歌":
            return "莫问"
        case "奶花" | "花奶" | "花花" | "离经易道":
            return "离经"
        case _:
            return method


def mainServer(method):
    match method:
        case "青梅煮酒" | "青梅":
            return "青梅煮酒"
        case "天鹅坪" | "纵月":
            return "天鹅坪"
        case "破阵子" | "念破":
            return "破阵子"
        case "飞龙在天" | "飞龙":
            return "飞龙在天"
        case "长安城" | "长安" | "电一长安":
            return "长安城"
        case "龙争虎斗" | "龙虎" | "电一龙虎":
            return "龙争虎斗"
        case "蝶恋花" | "蝶服":
            return "蝶恋花"
        case "幽月轮" | "六合一" | "七合一":
            return "幽月轮"
        case "剑胆琴心" | "煎蛋" | "剑胆":
            return "剑胆琴心"
        case "乾坤一掷" | "华乾" | "花钱":
            return "乾坤一掷"
        case "斗转星移" | "姨妈" | "大姨妈":
            return "斗转星移"
        case "唯我独尊" | "唯满侠" | "鹅服":
            return "唯我独尊"
        case "梦江南" | "如梦令" | "双梦":
            return "梦江南"
        case "绝代天骄" | "绝代" | "电八":
            return "绝代天骄"
        case _:
            return None


def mainZone(method):
    match method:
        case "青梅煮酒" | "青梅":
            return "双线四区"
        case "天鹅坪" | "纵月" | "破阵子" | "念破":
            return "双线一区"
        case "飞龙在天" | "飞龙":
            return "双线二区"
        case "长安城" | "长安" | "电一长安" | "龙争虎斗" | "龙虎" | "电一龙虎" | "蝶恋花" | "蝶服":
            return "电信一区"
        case "幽月轮" | "六合一" | "七合一" | "剑胆琴心" | "煎蛋" | "剑胆" | "乾坤一掷" | "华乾" | "花钱" | "斗转星移" | "姨妈" | "大姨妈" | "唯我独尊" | "唯满侠" | "鹅服" | "梦江南" | "如梦令" | "双梦":
            return "电信五区"
        case "绝代天骄" | "绝代" | "电八":
            return "电信八区"
        case _:
            return method
