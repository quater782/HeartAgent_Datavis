'''大实验1：对比比较sdt各个维度的是否有显著性变化。默认数据使用非参检验方法'''
import sys
# 将父目录添加到系统路径
import os

import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import db_questioniares as questions
from scipy.stats import shapiro
from scipy import stats
from scipy.stats import mannwhitneyu
from scipy import stats

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




def UW_extract_stats_and_test(df1, df2, name):
    # print(df1)
    # print(df2)
    # print(f"\n")
    df1 = pd.DataFrame(df1)
    df2 = pd.DataFrame(df2)
    # print(df1)
    # print(df2)
    # print(f"\n")
    results = {}
    questions = set(df1.columns) - {'user_id'}
    print(questions)

    for question in questions:
        stats1 = df1[question].describe()
        stats2 = df2[question].describe()

        # print(stats1)
        # print(stats2)

        # Mann-Whitney U检验
        # stat, p_value = mannwhitneyu(df1[question], df2[question], alternative='two-sided')
        # print(f"{df1[question]}, {df2[question]}")
        stat, p_value = stats.ttest_rel(df1[question], df2[question], alternative='two-sided')


        # 比较中位数判断得分趋势
        if stats2['50%'] > stats1['50%']:
            trend = "增大" 
        if stats2['50%'] == stats1['50%']:
            trend = "维持"
        if stats2['50%'] < stats1['50%']:
            trend = "减小"

        if stats2['mean'] > stats1['mean']:
            trend = f"{trend}, 均值增大"

        if p_value<0.01:
            trend = f"(**)极显著 {trend}"
        elif p_value<0.05:
            trend = f"(*)显著 {trend}"
        elif p_value<0.1:
            trend = f"(-)轻微显著 {trend}"


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
    filename = f'SW_ttest_report_{name}.txt'

    # 使用 'with' 语句打开文件，确保正确关闭文件
    with open(filename, 'w', encoding='utf-8') as file:
        # 使用 json.dump 将数据写入文件，确保使用utf-8编码
        json.dump(results, file, ensure_ascii=False,indent=4)

    # 输出结果
    # for question, res in results.items():
    #     print(f"Question: {question}")


'''----------'''
bpn_start = toolkit.read_survey_data("exp_l_1/data/start_BFNSNF.xlsx")
bpn_mid = toolkit.read_survey_data("exp_l_1/data/mid_BFNSNF.xlsx")
resili_start = toolkit.read_survey_data("exp_l_1/data/start_resilience.xlsx")
resili_mid = toolkit.read_survey_data("exp_l_1/data/mid_resilience.xlsx")
bpn_end = toolkit.read_survey_data("exp_l_1/data/end_BFNSNF.xlsx")
resili_end = toolkit.read_survey_data("exp_l_1/data/end_resilience.xlsx")


bpn_start, bpn_end = filter_lists_by_common_userids(bpn_start, bpn_end)
resili_start, resili_end = filter_lists_by_common_userids(resili_start, resili_end)

print(f"len reliend:{len(resili_end)}") # 29
print(f"len reliend:{len(resili_mid)}")
print(f"len reliend:{len(resili_start)}")

print(f"len bpn{len(bpn_end)}")
print(f"len bpn{len(bpn_mid)}")
print(f"len bpn{len(bpn_start)}")
# print(resili_mid)

'''json化'''
bpn_start_json = toolkit.list_to_json(bpn_start,db_questioniares.questions_pns)
bpn_mid_json = toolkit.list_to_json(bpn_mid, db_questioniares.questions_pns)
bpn_end_json = toolkit.list_to_json(bpn_end, db_questioniares.questions_pns)

resili_start_json = toolkit.list_to_json(resili_start, db_questioniares.questions_resilience)
resili_mid_json = toolkit.list_to_json(resili_mid,db_questioniares.questions_resilience)
resili_end_json = toolkit.list_to_json(resili_end,db_questioniares.questions_resilience)

filepath =f"exp_l_1\tReport"

# # 数据独立性检验
SWT(bpn_start_json, 'bpn_start')
SWT(bpn_mid_json, 'bpn_mid')
SWT(resili_start_json, 'bpn_start')
SWT(resili_mid_json, 'bpn_mid')


bpn_start_json = toolkit.list_to_json(bpn_start,db_questioniares.questions_pns)
bpn_end_json = toolkit.list_to_json(bpn_end, db_questioniares.questions_pns)
resili_start_json = toolkit.list_to_json(resili_start, db_questioniares.questions_resilience)
resili_end_json = toolkit.list_to_json(resili_end,db_questioniares.questions_resilience)

'''---------'''




bpn_mid_json = toolkit.list_to_json(bpn_mid,db_questioniares.questions_pns)
bpn_end_json = toolkit.list_to_json(bpn_end, db_questioniares.questions_pns)
resili_mid_json = toolkit.list_to_json(resili_mid, db_questioniares.questions_resilience)
resili_end_json = toolkit.list_to_json(resili_end,db_questioniares.questions_resilience)

filepath =f"exp_l_1\tReport"


# SWT(bpn_mid_json, 'bpn_mid')
# SWT(bpn_end_json, 'bpn_end')
# SWT(resili_mid_json, 'bpn_mid')
# SWT(resili_end_json, 'bpn_end')

# UWtest_json(bpn_mid_json, bpn_end_json, 'bpn_mid_end')
# UWtest_json(resili_mid_json, resili_end_json, 'resili_mid_end')


# UW_extract_stats_and_test(bpn_mid_json, bpn_end_json, 'bpn_mid_end')
# UW_extract_stats_and_test(resili_mid_json, resili_end_json, 'resili_mid_end')


'''----------'''




print(f"reliend:{len(resili_end)}")
print(f"reliend:{len(resili_mid)}")
print(f"reliend:{len(resili_start)}")

print(f"bpn{len(bpn_end)}")
print(f"bpn{len(bpn_mid)}")
print(f"bpn{len(bpn_start)}")


## 这部分打印下来好多hhh
# for i in range(len(resili_end_json)):
#     print(f"{resili_end_json[i]}\n{resili_start_json[i]}\n\n")

# for i in range(len(bpn_end_json)):
#     print(f"{bpn_end_json[i]}\n{bpn_start_json[i]}\n\n")

# for item in bpn_start:
#     print(item)

# print(f"\n\n")

# for item in bpn_mid:
#     print(item)

# print(f"\n\n")

# for item in bpn_end:
#     print(item)

'''--------------------计算各个维度的总分，以及总分的差异----------------------'''
def sum(list, quesionaire):
    sum= []
    list1 = list
    #对于每一个问题：提取到各个维度，并且同时计算总分。
    for i in range(len(list)):
        user_score_cluster = {}
        user_score_cluster["user_id"] = str(list1[i][0])
        user_score_cluster["sumscore"] = 0
        q_scores = list1[i][1:]
        for m in range(len(q_scores)):
            parsed_q = quesionaire[m].split(" - ")
            if len(parsed_q)>1:
                if("我觉得我所做的事情大多都是出于不得已才去做的" in parsed_q[2]):
                    print("skipped problem item")
                    # continue
                if len(parsed_q)>1:
                    demension = parsed_q[0]
                    user_score_cluster["sumscore"]+=q_scores[m]
                    if demension not in user_score_cluster:
                        user_score_cluster[demension] = q_scores[m]
                    else:
                        user_score_cluster[demension]+=q_scores[m]
            else:
                # print(f"error in parsing question:{quesionaire[m]}")
                break
        sum.append(user_score_cluster)
        # print(f"one user sum socres added as {user_score_cluster}")
    # print(sum)
    return sum




resili_end_sum = sum(resili_end, questions.questions_resilience)
resili_mid_sum= sum(resili_mid, questions.questions_resilience)
resili_start_sum = sum(resili_start, questions.questions_resilience)

bpn_start_sum = sum(bpn_start, questions.questions_pns)
bpn_mid_sum = sum(bpn_mid,  questions.questions_pns)
bpn_end_sum = sum(bpn_end,  questions.questions_pns)

UW_extract_stats_and_test(resili_start_sum, resili_end_sum,"sum_demension_ttest_resili")
UW_extract_stats_and_test(bpn_start_sum, bpn_end_sum, "sum_demension_ttest_bpn")




dimension_compare_bpn = {
    "自主":0,
    "关联" : 0,
    "能力" : 0,
    "sum" : 0,
    "count" : 0
}


dimension_compare_resi = {
    "坚韧":0,
    "力量" : 0,
    "乐观" : 0,
    "sum" : 0,
    "count" : 0
}

print(f"len(resili_end_sum): {len(resili_end_sum)}")
# Comparing resilience dimensions
for item in resili_end_sum:
    for i in resili_start_sum:
        if i["user_id"] == item["user_id"]:
            dimension_compare_resi["count"] += 1
            # Compare "坚韧" dimension
            if item["坚韧"] > i["坚韧"]:
                dimension_compare_resi["坚韧"] += 1
            # Compare "力量" dimension
            if item["力量"] > i["力量"]:
                dimension_compare_resi["力量"] += 1
            # You can add more comparisons as needed
            if item["乐观性"] > i["乐观性"]:
                dimension_compare_resi["乐观"] += 1
            if item["sumscore"] > i["sumscore"]:
                dimension_compare_resi["sum"] += 1

# Comparing basic psychological needs dimensions
for item in bpn_end_sum:
    for i in bpn_start_sum:
        if i["user_id"] == item["user_id"]:
            dimension_compare_bpn["count"] += 1
            # Compare "自主" dimension
            if item["自主性"] > i["自主性"]:
                dimension_compare_bpn["自主"] += 1
            # Compare "关联" dimension
            if item["关联性"] > i["关联性"]:
                dimension_compare_bpn["关联"] += 1
            # Compare "能力" dimension
            if item["能力"] > i["能力"]:
                dimension_compare_bpn["能力"] += 1
            if item["sumscore"] > i["sumscore"]:
                dimension_compare_bpn["sum"] += 1

print(dimension_compare_bpn)
print(dimension_compare_resi)
            


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

'''得到现有数据中，得分比初测低的值（修正后）'''
def getlowerscores_pns(start, end):
    for s in start:
        q_s = []
        q_e = []
        for e in end:
            if s[0]==e[0]:
                q_s = s[1:]
                q_e = e[1:]
                break
        i = 0
        for i in range(len(q_s)):
            list = []
            notice  = ""
            if(q_e[i]<q_s[i]):
                notice = f"低于前测：{questions.questions_pns[i]};前:{q_s[i]},后: {q_e[i]}"
                list.append(notice)
        for notices in list:
            print(f"")
                
        
