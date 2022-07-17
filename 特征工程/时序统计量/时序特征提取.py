# -*- coding: utf-8 -*-#

#-------------------------------------------------------------------------------
# Name:         beautiful
# Description:  
# Author:       shichao
# Date:         2019/5/8
#-------------------------------------------------------------------------------

import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import time
import datetime

# 核心代码，设置显示的最大列、宽等参数，消掉打印不完全中间的省略号
pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 1000)


# 读取数据
def read_df(file_name):
    file_dir = './'
    file_path = os.path.join(file_dir, file_name)
    file_path = open(file_path)
    df_file = pd.read_csv(file_path)
    df_file['DateTime'] = pd.to_datetime(df_file['DateTime'])
    df_file = df_file.sort_values(by='DateTime')
    return df_file


# 对 x 增加特征：date_ymd 年月日、把年月日时分秒转化为秒数utc时间
def add_features(df_file):
    date_list = []
    for date in list(df_file['DateTime']):
        date_str = str(date).split(' ')[0]
        date_list.append(date_str)
    df_file['date_ymd'] = date_list
    time_stamp_list = []
    for time_stamp in list(df_file['DateTime']):
        time_s = time.mktime(time.strptime(str(time_stamp), '%Y-%m-%d %H:%M:%S'))
        # time_s = time.mktime(time.strptime(time_stamp, '%Y/%m/%d %H:%M:%S'))
        time_stamp_list.append(time_s)
    df_file['time_stamp'] = time_stamp_list
    # date_ymdh_list = []
    # for time_stamp in list(df_file['DateTime']):
    #     date_ymdh = str(time_stamp).split(':')[0]
    #     date_ymdh_list.append(date_ymdh)
    # df_file['date_ymdh'] = date_ymdh_list
    return df_file


# 对缺失的温度进行插补
def repair_tem(df_data_by_date):
    # 去除重复列，默认所有列无重复记录
    df_data_by_date.duplicated()
    df_data_by_date = df_data_by_date.reset_index(drop=True)
    term_list_1 = list(df_data_by_date['Temperature'])
    term_list_date = list(df_data_by_date['date_ymd'])
    n = len(term_list_1)
    date_list = []
    temp_temp_list = []
    # 采样频率
    sample_frequency = 10
    for i in range(n):
        if (i >= 0 and i + 1 <= n - 1):
            temp_temp_list.append(term_list_1[i])
            date_list.append(term_list_date[i])
            # 对中间缺失的温度值进行插补
            if (df_data_by_date.loc[i + 1]['time_stamp'] - df_data_by_date.loc[i]['time_stamp'] >= (sample_frequency + 1) * 60):
                n_temp = int(np.ceil((df_data_by_date.loc[i + 1]['time_stamp'] - df_data_by_date.loc[i]['time_stamp']) / (sample_frequency * 60.0)))
                for j in range(n_temp - 1):
                    temp_temp = (df_data_by_date.loc[i + 1]['Temperature'] + df_data_by_date.loc[i]['Temperature']) / 2
                    temp_temp_list.append(temp_temp)
                    date_list.append(term_list_date[-1])
    temp_temp_list.append(term_list_1[-1])
    date_list.append(term_list_date[-1])
    # 如果开始连续缺失数量少于 5%, 用均值补齐
    df_data_by_date = df_data_by_date.reset_index(drop=True)
    #date_ = term_list_date[1]
    continue_list = []
    time_s = time.mktime(time.strptime(str(term_list_date[1]), '%Y-%m-%d'))
    if(df_data_by_date.loc[0]['time_stamp'] - time_s > (sample_frequency + 1) * 60):
        # 开头缺失
        n_temp = int(np.ceil((df_data_by_date.loc[0]['time_stamp'] - time_s) / (sample_frequency * 60.0)))
        #for j in range(n_temp - 1):
        for j in range(int(24*60/sample_frequency) - len(term_list_1)):
            continue_list.append(round(np.mean(term_list_1), 2))
            date_list.append(term_list_date[-1])
        continue_list.extend(temp_temp_list)
        temp_temp_list = continue_list
    else:
        # 结尾缺失
        for j in range(int(24*60/sample_frequency) - len(term_list_1)):
            continue_list.append(round(np.mean(term_list_1), 2))
            date_list.append(term_list_date[-1])
        temp_temp_list.extend(continue_list)
    df_repair = pd.DataFrame()
    df_repair['date_ymd'] = date_list
    df_repair['Temperature'] = temp_temp_list
    return df_repair


# 对温度曲线做分段常数逼近处理，用均值逼近, 1个小时内的温度值取一次均值
def constant_appro(df_data_by_date_tem):
    df_data_by_date_tem = df_data_by_date_tem.reset_index(drop=True)
    combine_date = []
    date_list = []
    temp = list(df_data_by_date_tem['Temperature'])
    for i in range(len(temp)):
        # 0 1 2   345   678
        # i*2  i*2+1   i*2+2
        # 3 个数据取平均 ，半小时
        # if(i*2 + i +2<=len(temp)-1):
        #     temp_combine = (temp[i*2 + i] + temp[i*2 + i + 1] + temp[i*2 + i + 2])/3.0
        #     combine_date.append(round(temp_combine, 2))
        # 6 个数取平均，1 小时
        if (i * 5 + i + 5 <= len(temp) - 1):
            temp_combine = (temp[i*5 + i] + temp[i*5 + i + 1] + temp[i*5 + i + 2] + temp[i*5 + i + 3] + temp[i*5 + i + 4] + temp[i*5 + i + 5])/6.0
            # temp_combine = (
            # temp[i * 5 + i] + temp[i * 5 + i + 1] + temp[i * 5 + i + 2] + temp[i * 5 + i + 3] + temp[i * 5 + i + 4] +
            # temp[i * 5 + i + 5])
            combine_date.append(round(temp_combine, 2))
            date_list.append(df_data_by_date_tem.loc[0]['date_ymd'])
    # 对温度做差分平滑处理
    diff_1 = [round(combine_date[i] - combine_date[i + 1], 2)for i in range(len(combine_date) - 1)]
    del date_list[1]
    df_appro = pd.DataFrame()
    df_appro['date_ymd'] = date_list
    df_appro['Temperature'] = diff_1
    return df_appro



# 对 x 进行特征提取,
from tsfresh import extract_relevant_features
from tsfresh import extract_features
import tsfresh as tsf
def get_features(df_appro):
    #extracted_features = extract_features(df_appro, column_id='date_ymd')
    #ts = pd.Series(x)  # 数据x假设已经获取
    ts = df_appro['Temperature']
    # 一阶差分绝对和
    abs_sum = tsf.feature_extraction.feature_calculators.absolute_sum_of_changes(ts)
    abs_sum = round(abs_sum, 2)
    # 各阶自相关系数的聚合统计特征
    param_statis = [{'f_agg': 'mean', 'maxlag': 2}]
    diff_statis = tsf.feature_extraction.feature_calculators.agg_autocorrelation(ts, param_statis)
    diff_statis = diff_statis[0][1]
    diff_statis = round(diff_statis, 2)
    # ADF 检测统计值
    param_adf = [{'attr': 'pvalue'}]
    adf = tsf.feature_extraction.feature_calculators.augmented_dickey_fuller(ts, param_adf)
    adf = adf[0][1]
    adf = round(adf, 2)
    # 峰度
    peak = tsf.feature_extraction.feature_calculators.kurtosis(ts)
    peak = round(peak, 2)
    # 时序数据复杂度
    complexity = tsf.feature_extraction.feature_calculators.cid_ce(ts, True)
    complexity = round(complexity, 2)
    # 线性回归分析
    param_line = [{'attr': 'pvalue'}]
    line = tsf.feature_extraction.feature_calculators.linear_trend(ts, param_line)
    line = list(zip(line))[0][0][1]
    line = round(line, 2)
    # 分组熵
    bin_entropy = tsf.feature_extraction.feature_calculators.binned_entropy(ts, 10)
    bin_entropy = round(bin_entropy, 2)
    # 近似熵
    appro_entropy = tsf.feature_extraction.feature_calculators.approximate_entropy(ts, 6, 0.1)
    appro_entropy = round(appro_entropy, 2)
    # 傅里叶变换频谱统计量
    param_fly = [{'aggtype': 'skew'}]
    fly = tsf.feature_extraction.feature_calculators.fft_aggregated(ts, param_fly)
    fly = list(zip(fly))[0][0][1]
    fly = round(fly, 2)
    # 傅里叶变换系数
    param_fly_change = [{'coeff': 2, 'attr': 'angle'}]
    fly_change = tsf.feature_extraction.feature_calculators.fft_coefficient(ts, param_fly_change)
    fly_change = list(zip(fly_change))[0][0][1]
    fly_change = round(fly_change, 2)
    # 小坡变换
    param_cwt = [{'widths': tuple([2, 2, 2]), 'coeff': 2, 'w': 2}]
    cwt = tsf.feature_extraction.feature_calculators.cwt_coefficients(ts, param_cwt)
    cwt = list(zip(cwt))[0][0][1]
    cwt = round(cwt, 2)

    return abs_sum, adf, peak, complexity, line, bin_entropy, appro_entropy, fly, fly_change, cwt



# 对每天的温度进行特征提取
def get_features_everday(df_data):
    date_ymd_field = df_data['date_ymd']
    date_ymds = []
    for i in date_ymd_field:
        if i not in date_ymds:
            date_ymds.append(i)
    df_features = pd.DataFrame()
    for date_ymd in date_ymds:
        #date_ymd = '2019-03-07'
        abs_sum_list = []
        adf_list = []
        peak_list = []
        complexity_list = []
        line_list = []
        bin_entropy_list = []
        appro_entropy_list = []
        fly_list = []
        fly_change_list = []
        cwt_list = []
        date_ymd_list = []
        df_data_by_date = df_data[df_data['date_ymd'] == date_ymd]
        # 缺失值大于 5% 的直接舍弃
        abondon_thr = int(144 * 0.95)
        if (len(df_data_by_date) <= abondon_thr):
            continue
        # 用插值补全温度值
        df_data_by_date_tem = repair_tem(df_data_by_date)
        # 如果是连续性缺失，则舍弃
        if (len(df_data_by_date_tem) <= abondon_thr):
            continue
        # 分段常数逼近，温度差分处理
        df_appro = constant_appro(df_data_by_date_tem)
        temp_array = np.array(list(df_appro['Temperature']))
        temp_array = temp_array.reshape(1, 23)
        # 分段常数逼近特征列名: 23 个
        columns_name = ['t1', 't2', 't3', 't4', 't5', 't6', 't7', 't8', 't9', 't10', 't11', 't12', 't13',
                        't14', 't15', 't16', 't17', 't18', 't19', 't20', 't21', 't22', 't23']
        df_x = pd.DataFrame(temp_array, columns=columns_name)
        #used_columns = ['date_ymd', 'Temperature']
        #df_data_by_date_tem = df_data_by_date[used_columns]
        abs_sum, adf, peak, complexity, line, bin_entropy, appro_entropy, fly, fly_change, cwt = get_features(df_appro)
        abs_sum_list.append(abs_sum)
        adf_list.append(adf)
        peak_list.append(peak)
        complexity_list.append(complexity)
        line_list.append(line)
        bin_entropy_list.append(bin_entropy)
        appro_entropy_list.append(appro_entropy)
        fly_list.append(fly)
        fly_change_list.append(fly_change)
        cwt_list.append(cwt)
        date_ymd_list.append(date_ymd)
        # 统计特征列名： 8
        df_x['abs_sum'] = abs_sum_list
        df_x['adf'] = adf_list
        df_x['peak'] = peak_list
        df_x['complexity'] = complexity_list
        df_x['line'] = line_list
        df_x['fly'] = fly_list
        df_x['fly_change'] = fly_change_list
        df_x['cwt'] = cwt_list
        # 信息熵特征：数据片段相似性  2 个
        df_x['bin_entropy'] = bin_entropy_list
        df_x['appro_entropy'] = appro_entropy_list
        df_x['date_ymd'] = date_ymd_list

        df_features = pd.concat([df_features, df_x], axis=0)
    return df_features



# 提取目标 y
def get_targets(df_file):
    df_file['hum_label'] = df_file['hum_label'].astype(str)
    df_file_label = df_file[df_file['hum_label']=='1.0']
    if 'Unnamed: 5' in df_file_label.columns:
        del df_file_label['Unnamed: 5']
    label_preprocess_dir = 'label_preprocess/'
    label_preprocess_path = os.path.join(label_preprocess_dir, file_name)
    #df_file_label.to_csv(label_preprocess_path, index=False)
    return df_file_label


# 给 label y 增加辅助列
def add_y_col(df_file):
    date_list = []
    for date in list(df_file['DateTime']):
        date_str = str(date).split(' ')[0]
        date_list.append(date_str)
    df_file['date_ymd'] = date_list
    return df_file


# 对 y 进行补全、筛选处理
def complete_targets(file_name_label):
    label_dir = './label_preprocess/'
    label_path = os.path.join(label_dir, file_name_label)
    label_path = open(label_path)
    df_label = pd.read_csv(label_path)
    df_label['correct'] = df_label['correct'].astype(str)
    df_label['across'] = df_label['across'].astype(str)
    df_laebl_temp_1 = df_label[df_label['correct']=='1.0']
    df_laebl_temp_2 = df_label[df_label['across']=='1.0']
    # 对 label y 进行整理
    n_cnt = 5  #除霜次数
    df_laebl_temp_1 = df_laebl_temp_1.reset_index(drop=True)
    df_laebl_temp_2 = df_laebl_temp_2.reset_index(drop=True)
    df_laebl_temp_1 = add_y_col(df_laebl_temp_1)
    df_laebl_temp_2 = add_y_col(df_laebl_temp_2)
    # 保存在 label_process_1 下人工检查日期
    save_dir = './label_preprocess_1/'
    save_path_1 = os.path.join(save_dir, file_name_label.split('.')[0] + '_1.csv')
    #df_laebl_temp_1.to_csv(save_path_1, index=False)
    save_path_2 = os.path.join(save_dir, file_name_label.split('.')[0] + '_2.csv')
    #df_laebl_temp_2.to_csv(save_path_2, index=False)
    print ()


# 把 label y 按日期变成一行
def label_to_hor(df_data):
    # 除霜次数
    cnt = 5
    df_data = df_data.reset_index(drop=True)
    date_ymd_field = df_data['date_ymd']
    date_ymds = []
    for i in date_ymd_field:
        if i not in date_ymds:
            date_ymds.append(i)
    df_features = pd.DataFrame()
    for date_ymd in date_ymds:
        date_list = []
        df_data_by_date = df_data[df_data['date_ymd'] == date_ymd]
        date_list.append(date_ymd)
        temp_array = np.array(list(df_data_by_date['DateTime']))
        temp_array = temp_array.reshape(1, cnt*2)
        df_y = pd.DataFrame(temp_array)
        df_y['date_ymd'] = date_list
        df_features = pd.concat([df_features, df_y], axis=0)
    return df_features



# 对 y 进行合并排序
def combine_label():
    file_name_label_1 = 'HLK-23F01(-18℃)_label_1.csv'
    label_dir = './label_preprocess_1/'
    label_path_1 = os.path.join(label_dir, file_name_label_1)
    label_path_1 = open(label_path_1)
    df_label_1 = pd.read_csv(label_path_1)
    file_name_label_2 = 'HLK-23F01(-18℃)_label_2.csv'
    label_path_2 = os.path.join(label_dir, file_name_label_2)
    label_path_2 = open(label_path_2)
    df_label_2 = pd.read_csv(label_path_2)
    # 检查日期，人工检查
    import collections
    a = collections.Counter(df_label_1['date_ymd'])
    b = collections.Counter(df_label_2['date_ymd'])
    # 把 label y 按照每天日期排列成一行
    df_label_y_1 = label_to_hor(df_label_1)
    df_label_y_2 = label_to_hor(df_label_2)
    df_y = pd.concat([df_label_y_1, df_label_y_2], axis=0)
    df_y['date_ymd'] = pd.to_datetime(df_y['date_ymd'])
    df_y = df_y.sort_values(by='date_ymd')
    #df_y.to_csv(label_dir + file_name_label_1.split('_')[0] + '_y.csv', index=False)
    print()


# 时间字符串格式转换
def time_format_trans(ser_list):
    ser_list = list(ser_list)
    ser_new = []
    for ser in ser_list:
        ser = str(ser).strip()
        if('/' in list(str(ser))):
            ser = str(ser).replace('/', '-')
        ser_new.append(ser)
    return ser_new


# 整合 x 和 y, 与匹配的日期对应起来, 对应产出在 label_preprocess_2/ 文件夹下
def merge_features_target(file_name):
    features_dir = './label_preprocess/'
    target_dir = './label_preprocess_1/'
    features_path = os.path.join(features_dir, file_name + '_x.csv')
    features_path = open(features_path)
    target_path = os.path.join(target_dir, file_name + '_y.csv')
    target_path = open(target_path)
    df_features = pd.read_csv(features_path)
    df_target = pd.read_csv(target_path)
    # 添加辅助列 date_ymd_1: 为了匹配用昨天的温度预测下一天的时间
    df_target['date_ymd'] = pd.to_datetime(df_target['date_ymd'])
    df_target = df_target.sort_values(by='date_ymd')
    # 获取当前日期前一天日期
    before_days = 1
    #before_days_date = now_date + datetime.timedelta(days=-before_days)
    df_target['date_ymd'] = df_target['date_ymd'].apply(lambda x: x + datetime.timedelta(days=-before_days))

    df_target['date_ymd'] = df_target['date_ymd'].astype(str)
    # 时间字符串格式转换
    df_features['date_ymd'] = pd.to_datetime(df_features['date_ymd'])
    df_features = df_features.sort_values(by='date_ymd')
    df_features['date_ymd'] = df_features['date_ymd'].astype(str)
    # 合并 x 和 y
    df_data = pd.merge(df_features, df_target, on='date_ymd')
    data_merge_dir = './label_preprocess_2/'
    data_merge_path = os.path.join(data_merge_dir, file_name + '_feature_target.csv')
    del df_data['date_ymd']
    #df_data.to_csv(data_merge_path, index=False)
    print ()










if __name__ == '__main__':
    # 处理特征 X
    # file_name = 'HLK-20C02(4℃).csv'
    # file_name = 'HLK-21C02(4℃).csv'
    file_name = 'HLK-23F01(-18℃).csv'
    df_file = read_df(file_name)
    df_file = add_features(df_file)
    df_features = get_features_everday(df_file)
    #df_features.to_csv('HLK-23F01(-18℃)_x.csv', index=False)
    #df_features.to_csv('HLK-20C02(4℃)_x.csv', index=False)
    #df_file_y = get_targets(df_file)
    # 处理标签 Y
    file_name_label = file_name.split('.')[0] + '_label' + '.csv'
    complete_targets(file_name_label)
    combine_label()
    # 整合 x 和 y
    merge_features_target(file_name.split('.')[0])

    print ()
