import asyncio
import random
import redis
from pydantic import BaseModel, Extra, Field
from nonebot import get_driver

config = get_driver().config


class DefaultConfig(BaseModel, extra=Extra.ignore):
    """
    默认设置
    """

    server: str = Field("斗转星移", alias="default_server")
    """默认绑定区服"""
    access_firend: bool = Field(True, alias="default_access_firend")
    """是否接受好友请求"""
    access_group: bool = Field(True, alias="default_access_group")
    """是否接受群请求"""
    robot_status: bool = Field(True, alias="default_robot_status")
    """机器人开关"""
    robot_active: int = Field(10, alias="default_robot_active")
    """机器人活跃"""
    robot_welcome_status: bool = Field("", alias="default_robot_welcome_status")
    """进群欢迎开关"""
    robot_welcome: str = Field(True, alias="defualt_robot_welcome")
    """进群欢迎语"""
    robot_someone_left_status: bool = Field(
        False, alias="defualt_robot_someone_left_status"
    )
    """群友离开说话开关"""
    robot_someone_left: str = Field("", alias="defualt_robot_someone_left")
    """群友离开内容"""
    robot_goodnight_status: bool = Field(True, alias="defulat_robot_goodnight_status")
    """晚安通知开关"""
    robot_goodnight: str = Field("", alias="defulat_robot_goodnight")
    """晚安通知内容"""


class PathConfig(BaseModel, extra=Extra.ignore):
    """
    路径设置
    """

    data: str = Field("", alias="path_data")
    """数据文件"""
    logs: str = Field("", alias="path_logs")
    """日志文件"""
    templates: str = Field("", alias="path_templates")
    """html模板文件"""


default_config = DefaultConfig.parse_obj(config)
path_config = PathConfig.parse_obj(config)
"""路径设置"""
"""
    jx3apiToken
"""
jx3api_ticket = "nrje86v129l78x4g9m"

chat_gpt_apikey = "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"

"""
    推栏token连接池
"""

ticket = ['d44bfd5c36a04558a0ee7a91430ddc89:yandereneko:kingsoft::cjh0NWJlemJsYnp3ZGJweA==',
          '2855868e14774545ba54ad995df0c333:yamdereneko:kingsoft::dGsxM3Y3cG01NWwzNWsxZw==',
          '538e558efd0c4d0d88de9c4852a8a129:yandereneko1:kingsoft::d3NsYTZlcXl3b2ZxZTM2Zw==',
          '3d5c0220d9784acfb2c7de3b01fe62ea:yandereneko2:kingsoft::OXZ4Zmt2Z3Q2bXBzenAzZg==']

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

    ws_path: str = Field("wss://socket.nicemoe.cn", alias="jx3api_ws_path")
    """ws连接地址"""
    ws_token: str = Field("5f2143314ebbec94b7aa80f7fd295856b03e567358a4f966fcbe597949e985e8", alias="jx3api_ws_token")
    """ws的token"""
    api_url: str = Field("", alias="jx3api_url")
    """主站的url"""
    api_token: str = Field("", alias="jx3api_token")
    """主站的token"""


#
# group_list = [549242180]
group_list = ["736734387", "642668185"]
# group_list = ["642668185"]

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

all_school = {'霸刀': 0, '少林': 0, '补天': 0, '蓬莱': 0, '紫霞': 0, '藏剑': 0, '明教': 0, '云裳': 0, '花间': 0, '丐帮': 0,
              '凌雪阁': 0, '田螺': 6, '惊羽': 0, '相知': 0, '胎虚': 0, '苍云': 0, '天策': 0, '无方': 0, '灵素': 0, '冰心': 0, '毒经': 0,
              '衍天宗': 0, '莫问': 0, '离经': 0, '刀宗': 0}

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
        case "凌雪" | "0雪" | "野猪" | "lingxue":
            return "凌雪"
        case "霸刀" | "刀刀" | "貂貂" | "badao":
            return "霸刀"
        case "和尚" | "灯泡" | "大师" | "yijin":
            return "少林"
        case "奶毒" | "毒奶" | "补天决" | "butian":
            return "补天"
        case "蓬莱" | "鸟人" | "雕雕" | "凌海决" | "凌海" | "linghai":
            return "蓬莱"
        case "气纯" | "道长" | "咩咩" | "zixia":
            return "紫霞"
        case "黄鸡" | "鸡哥" | "山居" | "cangjian":
            return "藏剑"
        case "喵喵" | "焚影" | "喵哥" | "喵姐" | "fenying":
            return "明教"
        case "奶秀" | "秀奶" | "秀人" | "yunshang":
            return "云裳"
        case "盆栽" | "花间游" | "huajian":
            return "花间"
        case "丐狗" | "丐人" | "笑尘" | "xiaochen":
            return "丐帮"
        case "田螺" | "天罗" | "tianluo":
            return "田螺"
        case "鲸鱼" | "唐门" | "惊羽决" | "jingyu":
            return "惊羽"
        case "奶歌" | "歌奶" | "奶哥" | "奶鸽" | "鸽奶" | "xiangzhi":
            return "相知"
        case "太虚" | "剑纯" | "阿胎" | "阿胎" | "太虚剑意" | "taixu":
            return "胎虚"
        case "铁王八" | "王八" | "分山" | "fenshan":
            return "苍云"
        case "狗策" | "狗人" | "策人" | "aoxue":
            return "天策"
        case "无方门" | "药毒" | "毒药" | "wufang":
            return "无方"
        case "奶药" | "药奶" | "药药" | "lingsu":
            return "灵素"
        case "冰心决" | "冰心" | "bingxin":
            return "冰心"
        case "毒人" | "毒毒" | "dujing":
            return "毒经"
        case "衍天" | "灯灯" | "taixuan":
            return "衍天"
        case "长歌门" | "莫问决" | "长歌" | "mowen":
            return "莫问"
        case "奶花" | "花奶" | "花花" | "离经易道" | "lijing":
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
