import asyncio
import json
import time
from io import BytesIO
import matplotlib.pyplot as plt
import pandas as pd
import src.Data.jxDatas as jxData
import mysql.connector
import src.Data.jx3_Redis as redis


class GetJJCTopInfo:
    def __init__(self, table: int, weekly: int, school_type: str):
        self.table = table
        self.weekly = weekly
        self.school_type = school_type
        self.red = redis.Redis()

    # 获取每周每个门派趋势图，返回DICT结果，并打印趋势图至相关目录

    async def redis_check(self, data, respective_data, respective_data_image):
        red_data = await self.red.query(respective_data)
        if red_data is not None:
            if json.loads(red_data) == data:
                red_data_image = await self.red.get_image_decode(respective_data_image)
                new_buffer = BytesIO(red_data_image)
                new_buffer_contents = new_buffer.getvalue()
                # Read the contents of the new buffer
                return new_buffer_contents
        await self.red.add(respective_data, data)
        return None

    async def from_sql_create_figure(self):
        respective_data = f"JJC_Top_{self.school_type}_{self.weekly}_{self.table}"
        respective_data_image = f"JJC_Top_{self.school_type}_{self.weekly}_{self.table}_image"

        db_config = jxData.sql_config
        cnx = mysql.connector.connect(user=db_config['user'], password=db_config['password'],
                                      host=db_config['host'], database=db_config['db'])
        # engine = create_engine('mysql+mysqlconnector://', creator=lambda: cnx)

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
                    ylim_size = 30
                case 100:
                    table_name = 'JJC_rank100_weekly'
                    ylim_size = 40
                case _:
                    table_name = 'JJC_rank_weekly'
                    ylim_size = 50
            query = f"SELECT 霸刀, 藏剑, 蓬莱, 无方,花间,少林,惊羽,丐帮,苍云,紫霞,凌雪,明教,毒经,天策,田螺,胎虚,莫问,衍天,冰心,刀宗 FROM {table_name} where week='{self.weekly}'"

        df_raw = pd.read_sql(query, cnx)
        df_raw.index = ['数量']
        df = df_raw.transpose()
        json_str = df_raw.to_json(orient='records')
        redis_check = await self.redis_check(json_str, respective_data, respective_data_image)
        if redis_check is not None:
            return redis_check
        df.sort_values(by='数量', inplace=True, ascending=False)
        fig, ax = plt.subplots(figsize=(22, 10), facecolor='white', dpi=150)
        ax.vlines(x=df.index, ymin=0, ymax=df.数量, color='firebrick', alpha=0.7, linewidth=32)
        for i, cty in enumerate(df.数量):
            ax.text(i, cty + 0.5, round(cty, 1), horizontalalignment='center', fontdict={'size': 22})
        ax.set_title(f'【横刀断浪】第{self.weekly + 9}周 个人前{self.table} {self.school_type}数据', fontdict={'size': 30})
        ax.set(ylim=(0, ylim_size))

        ax.set_ylabel('人数', fontdict={'size': 22, 'horizontalalignment': 'right'}, loc="center")

        plt.xticks(df.index, df.index.str.upper(), rotation=60, horizontalalignment='right', fontsize=22)

        buffer = BytesIO()
        buffer.seek(0)
        plt.savefig(buffer)
        await self.red.insert_image_encode(respective_data_image, buffer.getvalue())
        # image.save(f"images/record_image.png", dpi=dpi)
        return buffer
