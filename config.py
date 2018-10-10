# -*- coding: utf-8 -*-

"""

    版本:     1.0
    日期:     2018/02
    文件名:    config.py
    功能：     配置文件

"""
import os

# 指定数据集路径
dataset_path = './data'

# 结果保存路径
output_path = './output'
if not os.path.exists(output_path):
    os.makedirs(output_path)

# 公共列
common_cols = ['year', 'month']

# 每个城市对应的文件名及所需分析的列名
# 以字典形式保存，如：{城市：(文件名, 列名)}
data_config_dict = {'beijing': ('E:\python\Data1\study_numpy\data\BeijingPM20100101_20151231.csv',
                                ['Dongsi', 'Dongsihuan', 'Nongzhanguan']),
                    'chengdu': ('E:\python\Data1\study_numpy\data\ChengduPM20100101_20151231.csv',
                                ['Caotangsi', 'Shahepu']),
                    'guangzhou': ('E:\python\Data1\study_numpy\data\GuangzhouPM20100101_20151231.csv',
                                  ['City Station', '5th Middle School']),
                    'shanghai': ('E:\python\Data1\study_numpy\data\ShanghaiPM20100101_20151231.csv',
                                 ['Jingan', 'Xuhui']),
                    'shenyang': ('E:\python\Data1\study_numpy\data\ShenyangPM20100101_20151231.csv',
                                 ['Taiyuanjie', 'Xiaoheyan'])
                    }
