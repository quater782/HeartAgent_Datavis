'''正态性检验'''
import sys
# 将父目录添加到系统路径
import os

import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import db_questioniares as questions
from scipy.stats import shapiro
import json
import numpy as np

# 读取Excel文件
def read_survey_data(file_path: str):
    # 读取 Excel 文件中的数据
    df = pd.read_excel(file_path)

    # 初始化一个空的 list 来存储结果
    survey_data_list = []

    # 遍历每一行，将数据提取成一个 list 并添加到 survey_data_list 中
    for index, row in df.iterrows():
        # 将用户名和问题的得分转换为一个 list
        user_data = [row[0]] + list(row[1:])
        survey_data_list.append(user_data)

    return survey_data_list

def excel_to_json(file_path: str, questioniares):
    data = read_survey_data(file_path)
    # print(data)
    data_json = questions.questioniare_data_json(data, questioniares)
    print(f"{data_json}")
    return data_json

def list_to_json(list, questioniares):
    # print(data)
    data_json = questions.questioniare_data_json(list, questioniares)
    print(f"{data_json}")
    return data_json


filepath = "t_tests/data/mid_resilience.xlsx"


def adapt_demension_score(data_json):
    max_score = 5  # 假设最高分为5
    for entry in data_json:
        for key, value in entry.items():

            if "反向题" in key:
                print(f"{key},{value}")
                print(f"reversed one question, original socre is {value}\n")
                entry[key] = max_score + 1 - value
    df = pd.DataFrame(data_json)

    # 生成题目得分列表
    questions_scores = []
    dimension_scores = {}

    for index, row in df.iterrows():
        user_id = row.pop('user_id')
        for key, value in row.items():
            dimension, question_type, question_name = key.split(' - ')
            questions_scores.append({'user_id': user_id, 'question': question_name, 'dimension': dimension, 'score': value})
            if dimension not in dimension_scores:
                dimension_scores[dimension] = []
            dimension_scores[dimension].append(value)
#    print(f"{dimension_scores}\n\n{df}")
    return questions_scores, dimension_scores, df

'''独立性t检验'''
def shaprio_wilk(dimension_scores, df):

    treport = []
    # 计算维度得分平均值
    average_scores = {dim: np.mean(scores) for dim, scores in dimension_scores.items()}
    # 输出2: 维度得分平均值
    treport.append(json.dumps(average_scores, indent=4, ensure_ascii=False)) 

    for question in set(df.columns) - {'user_id'}:
        stat, p_value = shapiro(df[question].dropna())
        treport.append(f"正态性测试 - {question}: p-value = {p_value}")

    # 维度得分正态性
    # for dim, scores in dimension_scores.items():
    #     stat, p_value = shapiro(scores)
    #     treport.append(f"正态性测试 - {dim}: p-value = {p_value}")

    return treport

'''      '''
# questions_scores, dimension_scores, df =  adapt_demension_score(excel_to_json('t_tests/data/mid_resilience.xlsx', questions.questions_resilience))

# print(json.dumps(questions_scores, indent=4, ensure_ascii=False))



# 正态性检验
# 题目得分正态性
