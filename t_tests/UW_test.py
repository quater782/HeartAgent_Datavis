'''正态性检验'''
import sys
# 将父目录添加到系统路径
import os

import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import db_questioniares as questions
from scipy.stats import shapiro
from scipy.stats import mannwhitneyu
import json
import numpy as np

import toolkit_shapiro_wilk as toolkit
import db_questioniares

def filter_lists_by_common_userids(list1, list2):
    # 提取两个列表中的 userids
    userids_1 = set(sublist[0] for sublist in list1)
    userids_2 = set(sublist[0] for sublist in list2)
    
    # 找出共有的 userids
    common_userids = userids_1.intersection(userids_2)
    
    # 过滤出同时存在于两个列表中的元素
    filtered_list1 = [item for item in list1 if item[0] in common_userids]
    filtered_list2 = [item for item in list2 if item[0] in common_userids]

    print(f"{filtered_list1}\n{filtered_list2}")
    
    return filtered_list1, filtered_list2

bpn_start = []
bpn_mid = []
resili_start = []
resili_mid = []




'''---------func-----------'''


# 数据独立性检验
def SWT(jsondata, name:str):
    questions_scores, dimension_scores, df = toolkit.adapt_demension_score(jsondata)
    report = toolkit.shaprio_wilk(dimension_scores, df)

    # 指定要写入的文件名
    filename = f'正态性报告_{name}.txt'

    # 使用 'with' 语句打开文件，确保正确关闭文件
    with open(filename, 'w', encoding='utf-8') as file:
        # 使用 json.dump 将数据写入文件，确保使用utf-8编码
        json.dump(report, file, ensure_ascii=False,indent=4)


def UWtest_json(group1_data, group2_data, name:str):
    # 转换成DataFrame
    df1 = pd.DataFrame(group1_data)
    df2 = pd.DataFrame(group2_data)

    # 提取问题和维度

    # 处理数据
    group1_scores = extract_dimension_and_question(df1)
    group2_scores = extract_dimension_and_question(df2)

    # 进行Mann-Whitney U检验
    results = {}
    for dimension in group1_scores:
        if dimension not in results:
            results[dimension] = {}
        for question in group1_scores[dimension]:
            if question in group2_scores[dimension]:  # 确保两组都有相同的问题
                score1 = group1_scores[dimension][question]
                score2 = group2_scores[dimension][question]
                stat, p_value = mannwhitneyu(score1, score2, alternative='two-sided')
                results[dimension][question] = {'U-statistic': stat, 'p-value': p_value}

    # 输出结果
    for dim, questions in results.items():
        for q, res in questions.items():
            print(f"Dimension: {dim}, Question: {q}, U-statistic: {res['U-statistic']}, p-value: {res['p-value']:.3f}")

    # 输出结果
        # 指定要写入的文件名
    filename = f'UW报告_{name}.txt'

    # 使用 'with' 语句打开文件，确保正确关闭文件
    with open(filename, 'w', encoding='utf-8') as file:
        # 使用 json.dump 将数据写入文件，确保使用utf-8编码
        json.dump(results, file, ensure_ascii=False, indent=4)



def extract_dimension_and_question(df):
    scores = {}
    for index, row in df.iterrows():
        for key in row.index:
            if key.startswith('user_id'):
                continue
            dimension, question_type, question = key.split(' - ')
            if dimension not in scores:
                scores[dimension] = {}
            if question not in scores[dimension]:
                scores[dimension][question] = []
            scores[dimension][question].append(row[key])
    return scores


def UW_extract_stats_and_test(df1, df2, name):
    df1 = pd.DataFrame(df1)
    df2 = pd.DataFrame(df2)
    results = {}
    questions = set(df1.columns) - {'user_id'}
    for question in questions:
        stats1 = df1[question].describe()
        stats2 = df2[question].describe()

        # Mann-Whitney U检验
        stat, p_value = mannwhitneyu(df1[question], df2[question], alternative='two-sided')

        # 比较中位数判断得分趋势
        if stats2['50%'] > stats1['50%']:
            trend = "增大" 
        if stats2['50%'] == stats1['50%']:
            trend = "维持"
        if stats2['50%'] < stats1['50%']:
            trend = "减小"

        if stats2['mean'] > stats1['mean']:
            trend = f"{trend}, 均值增大"

        results[question] = {
            'start_Mean': stats1['mean'],
            'start_SD': stats1['std'],
            'start_Median': stats1['50%'],
            'start_25th': stats1['25%'],
            'start_75th': stats1['75%'],
            'end_Mean': stats2['mean'],
            'end_SD': stats2['std'],
            'end_Median': stats2['50%'],
            'end_25th': stats2['25%'],
            'end_75th': stats2['75%'],
            'U-statistic': stat,
            'p-value': p_value,
            'Trend': trend
        }
        # 指定要写入的文件名
    filename = f'UW分位报告_{name}.txt'

    # 使用 'with' 语句打开文件，确保正确关闭文件
    with open(filename, 'w', encoding='utf-8') as file:
        # 使用 json.dump 将数据写入文件，确保使用utf-8编码
        json.dump(results, file, ensure_ascii=False,indent=4)

    # 输出结果
    for question, res in results.items():
        print(f"Question: {question}")


'''----------'''
bpn_start = toolkit.read_survey_data("t_tests/data/start_BFNSNF.xlsx")
bpn_mid = toolkit.read_survey_data("t_tests/data/mid_BFNSNF.xlsx")
resili_start = toolkit.read_survey_data("t_tests/data/start_resilience.xlsx")
resili_mid = toolkit.read_survey_data("t_tests/data/mid_resilience.xlsx")

bpn_start, bpn_mid = filter_lists_by_common_userids(bpn_start, bpn_mid)
resili_start, resili_mid = filter_lists_by_common_userids(resili_start, resili_mid)

print(resili_mid)

bpn_start_json = toolkit.list_to_json(bpn_start,db_questioniares.questions_pns)
bpn_mid_json = toolkit.list_to_json(bpn_mid, db_questioniares.questions_pns)
resili_start_json = toolkit.list_to_json(resili_start, db_questioniares.questions_resilience)
resili_mid_json = toolkit.list_to_json(resili_mid,db_questioniares.questions_resilience)

filepath =f"t_tests\tReport"


SWT(bpn_start_json, 'bpn_start')
SWT(bpn_mid_json, 'bpn_mid')
SWT(resili_start_json, 'bpn_start')
SWT(resili_mid_json, 'bpn_mid')

UWtest_json(bpn_start_json, bpn_mid_json, 'bpn_start_mid')
UWtest_json(resili_start_json, resili_mid_json, 'resili_start_mid')


UW_extract_stats_and_test(bpn_start_json, bpn_mid_json, 'bpn_start_mid')
UW_extract_stats_and_test(resili_start_json, resili_mid_json, 'resili_start_mid')

for item in resili_mid:
    print(item[0])