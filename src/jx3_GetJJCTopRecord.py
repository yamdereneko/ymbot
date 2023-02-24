import asyncio
import time
import matplotlib.pyplot as plt
import pandas as pd
import src.Data.jxDatas as jxData
from sqlalchemy import create_engine


class GetJJCTopInfo:
    def __init__(self, table: int, weekly: int, school_type: str):
        self.table = table
        self.weekly = weekly
        self.school_type = school_type

    # 获取每周每个门派趋势图，返回DICT结果，并打印趋势图至相关目录
    async def from_sql_create_figure(self):
        db_config = jxData.sql_config
        engine = create_engine(f"mysql+mysqlconnector://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['db']}")

        if self.school_type == "奶妈":
            match self.table:
                case 50:
                    table_name = 'JJC_rank50_weekly'
                    ylim_size = 20
                case 100:
                    table_name = 'JJC_rank100_weekly'
                    ylim_size = 20
                case _:
                    table_name = 'JJC_rank_weekly'
                    ylim_size = 30
            query = f"SELECT 云裳, 相知, 补天, 灵素, 离经 FROM {table_name} where week='{self.weekly}'"

        else:
            match self.table:
                case 50:
                    table_name = 'JJC_rank50_weekly'
                    ylim_size = 20
                case 100:
                    table_name = 'JJC_rank100_weekly'
                    ylim_size = 30
                case _:
                    table_name = 'JJC_rank_weekly'
                    ylim_size = 50
            query = f"SELECT 霸刀, 藏剑, 蓬莱, 无方,花间,少林,惊羽,丐帮,苍云,紫霞,凌雪,明教,毒经,天策,田螺,胎虚,莫问,衍天,冰心,刀宗 FROM {table_name} where week='{self.weekly}'"

        df_raw = pd.read_sql(query, engine)
        df_raw.index = ['数量']
        df = df_raw.transpose()
        df.sort_values(by='数量', inplace=True, ascending=False)
        fig, ax = plt.subplots(figsize=(22, 10), facecolor='white', dpi=150)
        ax.vlines(x=df.index, ymin=0, ymax=df.数量, color='firebrick', alpha=0.7, linewidth=32)
        for i, cty in enumerate(df.数量):
            ax.text(i, cty + 0.5, round(cty, 1), horizontalalignment='center', fontdict={'size': 22})
        ax.set_title(f'【横刀断浪】第{self.weekly + 9}周 个人前{self.table} {self.school_type}数据', fontdict={'size': 30})
        ax.set(ylim=(0, ylim_size))

        ax.set_ylabel('人数', fontdict={'size': 22, 'horizontalalignment': 'right'}, loc="center")

        plt.xticks(df.index, df.index.str.upper(), rotation=60, horizontalalignment='right', fontsize=22)
        datetime = int(time.time())
        plt.savefig(f"/tmp/top{datetime}.png")
        return datetime
