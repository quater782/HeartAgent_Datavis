'''大实验1：对比比较sdt各个维度的是否有显著性变化。默认数据使用非参检验方法'''
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
bpn_start = toolkit.read_survey_data("exp_l_1/data/start_BFNSNF.xlsx")
bpn_mid = toolkit.read_survey_data("exp_l_1/data/mid_BFNSNF.xlsx")
resili_start = toolkit.read_survey_data("exp_l_1/data/start_resilience.xlsx")
resili_mid = toolkit.read_survey_data("exp_l_1/data/mid_resilience.xlsx")

bpn_end = toolkit.read_survey_data("exp_l_1/data/end_BFNSNF.xlsx")
resili_end = toolkit.read_survey_data("exp_l_1/data/end_resilience.xlsx")


# bpn_start, bpn_mid = filter_lists_by_common_userids(bpn_start, bpn_mid)
# resili_start, resili_mid = filter_lists_by_common_userids(resili_start, resili_mid)

bpn_start, bpn_end = filter_lists_by_common_userids(bpn_start, bpn_end)
resili_start, resili_end = filter_lists_by_common_userids(resili_start, resili_end)

bpn_start, bpn_mid = filter_lists_by_common_userids(bpn_start, bpn_mid)
resili_start, resili_mid = filter_lists_by_common_userids(resili_start, resili_mid)

print(resili_mid)

'''json化'''

bpn_start_json = toolkit.list_to_json(bpn_start,db_questioniares.questions_pns)
bpn_mid_json = toolkit.list_to_json(bpn_mid, db_questioniares.questions_pns)
bpn_end_json = toolkit.list_to_json(bpn_end, db_questioniares.questions_pns)

resili_start_json = toolkit.list_to_json(resili_start, db_questioniares.questions_resilience)
resili_mid_json = toolkit.list_to_json(resili_mid,db_questioniares.questions_resilience)
resili_end_json = toolkit.list_to_json(resili_end,db_questioniares.questions_resilience)


filepath =f"exp_l_1\tReport"


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

'''----------'''


def sum(list):
    new = []
    for item in list:
        newlist = item[1:]
        #  print(newlist)
        i = 0
        for score in newlist:
            i+=score
        item.append(i)
        new.append(item)
        print(item)
    return new

bpn_start = sum(bpn_start)
bpn_mid = sum(bpn_mid)
bpn_end = sum(bpn_end)

resili_end = sum(resili_end)
resili_mid= sum(resili_mid)
resili_start = sum(resili_start)

bpn_start_json = toolkit.list_to_json(bpn_start,db_questioniares.questions_pns1)
bpn_end_json = toolkit.list_to_json(bpn_end, db_questioniares.questions_pns1)
resili_start_json = toolkit.list_to_json(resili_start, db_questioniares.questions_resilience1)
resili_end_json = toolkit.list_to_json(resili_end,db_questioniares.questions_resilience1)

filepath =f"exp_l_1\tReport"


SWT(bpn_start_json, 'bpn_start')
SWT(bpn_end_json, 'bpn_end')
SWT(resili_start_json, 'bpn_start')
SWT(resili_end_json, 'bpn_end')

UWtest_json(bpn_start_json, bpn_end_json, 'bpn_start_end')
UWtest_json(resili_start_json, resili_end_json, 'resili_start_end')


UW_extract_stats_and_test(bpn_start_json, bpn_end_json, 'bpn_start_end')
UW_extract_stats_and_test(resili_start_json, resili_end_json, 'resili_start_end')


'''---------'''
bpn_mid_json = toolkit.list_to_json(bpn_mid,db_questioniares.questions_pns1)
bpn_end_json = toolkit.list_to_json(bpn_end, db_questioniares.questions_pns1)
resili_mid_json = toolkit.list_to_json(resili_mid, db_questioniares.questions_resilience1)
resili_end_json = toolkit.list_to_json(resili_end,db_questioniares.questions_resilience1)

filepath =f"exp_l_1\tReport"


SWT(bpn_mid_json, 'bpn_mid')
SWT(bpn_end_json, 'bpn_end')
SWT(resili_mid_json, 'bpn_mid')
SWT(resili_end_json, 'bpn_end')

UWtest_json(bpn_mid_json, bpn_end_json, 'bpn_mid_end')
UWtest_json(resili_mid_json, resili_end_json, 'resili_mid_end')


UW_extract_stats_and_test(bpn_mid_json, bpn_end_json, 'bpn_mid_end')
UW_extract_stats_and_test(resili_mid_json, resili_end_json, 'resili_mid_end')



print(f"reliend:{len(resili_end)}")
print(f"reliend:{len(resili_mid)}")
print(f"reliend:{len(resili_start)}")

print(f"bpn{len(bpn_end)}")
print(f"bpn{len(bpn_mid)}")
print(f"bpn{len(bpn_start)}")

'''线性回归'''

# import pandas as pd
# from sklearn.linear_model import LinearRegression
# import numpy as np
# import statsmodels.api as sm

# # 将数据加载到DataFrame中
# df_group1 = pd.DataFrame(bpn_start_json)
# df_group2 = pd.DataFrame(bpn_mid_json)
# df_group3 = pd.DataFrame(bpn_end_json)

# # 假设我们知道这些数据是顺序一致的，我们可以添加一个时间列来区分前测、中测和后测
# df_group1['time'] = 1
# df_group2['time'] = 2
# df_group3['time'] = 3

# # 合并数据
# df_total = pd.concat([df_group1, df_group2, df_group3], ignore_index=True)

# # 转换为适合进行回归的长格式
# df_long = df_total.melt(id_vars=['user_id', 'time'], var_name='question', value_name='score')

# # 分别对每个问题进行线性回归分析
# results = {}
# questions = df_long['question'].unique()
# for question in questions:
#     df_q = df_long[df_long['question'] == question]
#     X = sm.add_constant(df_q['time'])  # 添加截距项
#     y = df_q['score']
#     model = sm.OLS(y, X).fit()
#     results[question] = model.summary()

# # 输出每个问题的回归分析结果
# for question, result in results.items():
#     print(f"Regression results for {question}:")
#     print(result)

# # 可以根据需求，进一步分析或可视化回归结果

