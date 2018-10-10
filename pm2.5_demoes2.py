
"""
    文件名:    main.py
    功能：     主程序

    实战案例1-1：中国五大城市PM2.5数据分析 (1)
    任务：
        - 五城市污染状态
        - 五城市每个区空气质量的月度差异

    数据集来源：https://www.kaggle.com/uciml/pm25-data-for-five-chinese-cities

    案例文档：readme.pdf
"""

import csv
import os
import numpy as np
import study_numpy.config


def load_data(data_file, usecols):
    """
        参数：
            - data_file:    文件路径
            - usecols:      所使用的列
        返回：
            - data_arr:     数据的多维数组表示
    """
    data = []
    with open(data_file, 'r') as csvfile:
        data_reader = csv.DictReader(csvfile)
        print(data_reader)
        # === Step 2. 数据处理 ===
        for row in data_reader:
            # 取出每行数据，组合为一个列表放入数据列表中
            row_data = []
            # 注意csv模块读入的数据全部为字符串类型
            for col in usecols:
                str_val = row[col]
                # 数据类型转换为float，如果是'NA'，则返回nan
                row_data.append(float(str_val) if str_val != 'NA' else np.nan)
            # 如果行数据中不包含nan才保存该行记录
            if not any(np.isnan(row_data)):
                data.append(row_data)

    # 将data转换为ndarray
    data_arr = np.array(data)
    return data_arr


def get_polluted_perc(data_arr):
    """       获取污染占比的小时数
        规则：
            重度污染(heavy)     PM2.5 > 150
            中度污染(medium)    75 < PM2.5 <= 150
            轻度污染(light)     35 < PM2.5 <= 75
            优良空气(good)      PM2.5 <= 35
        参数：
            - data_arr: 数据的多维数组表示
        返回：
            - polluted_perc_list: 污染小时数百分比列表
    """
    # 将每个区的PM值平均后作为该城市小时的PM值
    # 按行取平均值
    hour_val = np.mean(data_arr[:, 2:], axis=1)
    # 总小时数
    n_hours = hour_val.shape[0]
    # 重度污染小时数
    n_heavy_hours = hour_val[hour_val > 150].shape[0]
    # 中度污染小时数
    n_medium_hours = hour_val[(hour_val > 75) & (hour_val <= 150)].shape[0]
    # 轻度污染小时数
    n_light_hours = hour_val[(hour_val > 35) & (hour_val <= 75)].shape[0]
    # 优良空气小时数
    n_good_hours = hour_val[hour_val <= 35].shape[0]
    polluted_perc_list = [n_heavy_hours / n_hours, n_medium_hours / n_hours,
                          n_light_hours / n_hours, n_good_hours / n_hours]
    return polluted_perc_list


def get_avg_pm_per_month(data_arr):
    """
        获取每个区每月的平均PM值
        参数：
            - data_arr: 数据的多维数组表示
        返回：
            - results_arr:  多维数组结果
    """
    results = []
   # 获取年份
    years = np.unique(data_arr[:, 0])
    for year in years:
        # 获取当前年份数据
        year_data_arr = data_arr[data_arr[:, 0] == year]
        # 获取数据的月份
        month_list = np.unique(year_data_arr[:, 1])

        for month in month_list:
            # 获取月份的所有数据
            month_data_arr = year_data_arr[year_data_arr[:, 1] == month]
            # 计算当前月份PM的均值
            mean_vals = np.mean(month_data_arr[:, 2:], axis=0).tolist()

            # 格式化字符串
            row_data = ['{:.0f}-{:02.0f}'.format(year, month)] + mean_vals
            results.append(row_data)
    results_arr = np.array(results)
    return results_arr


def save_stats_to_csv(results_arr, save_file, headers):
    """
        将统计结果保存至csv文件中
        参数：
            - results_arr:   多维数组结果
            - save_file:    文件保存路径
            - headers:      csv表头
    """
    with open(save_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        for row in results_arr.tolist():
            writer.writerow(row)


def main():
    """
        主函数
    """
    polluted_state_list = []

    for city_name, (filename, cols) in study_numpy.config.data_config_dict.items():
        # === Step 1+2. 数据获取 + 数据处理 ===
        data_file = os.path.join(study_numpy.config.dataset_path, filename)
        usecols = study_numpy.config.common_cols + ['PM_' + col for col in cols]
        data_arr = load_data(data_file, usecols)

        print('{}共有{}行有效数据'.format(city_name, data_arr.shape[0]))
        # 预览前10行数据
        print('{}的前10行数据：'.format(city_name))
        print(data_arr[:10])

        # === Step 3. 数据分析 ===
        # 五城市污染状态，统计污染小时数的占比
        polluted_perc_list = get_polluted_perc(data_arr)
        polluted_state_list.append([city_name] + polluted_perc_list)
        print('{}的污染小时数百分比{}'.format(city_name, polluted_perc_list))

        # 五城市每个区空气质量的月度差异，分析计算每个月，每个区的平均PM值
        results_arr = get_avg_pm_per_month(data_arr)
        print('{}的每月平均PM值预览：'.format(city_name))
        print(results_arr[:10])

        # === Step 4. 结果展示 ===
        # 4.1 保存月度统计结果至csv文件
        save_filename = city_name + '_month_stats.csv'
        save_file = os.path.join(study_numpy.config.output_path, save_filename)
        save_stats_to_csv(results_arr, save_file, headers=['month'] + cols)
        print('月度统计结果已保存至{}'.format(save_file))
        print()
    # 4.2 污染状态结果保存
    save_file = os.path.join(study_numpy.config.output_path, 'polluted_percentage.csv')
    with open(save_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['city', 'heavy', 'medium', 'light', 'good'])
        for row in polluted_state_list:
            writer.writerow(row)
    print('污染状态结果已保存至{}'.format(save_file))
if __name__ == '__main__':
    main()
