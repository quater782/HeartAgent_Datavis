import pandas as pd
from sklearn.metrics import cohen_kappa_score

'''
小实验: 成长需求比例（有多少的对话是需要干预的）
'''

data_correspondence = {
    'x1':'cyx',
    'x2':'hq',
    'x3':'ksx',
    'x4':'ww',
    'label':'heartAgent'
}

# file_path_x = r'.\eval\data\x1.xlsx'  # 替换为你的实际文件路径
file_path_label = r'.\eval\data\heartAgent.xlsx'  # 替换为你的实际文件路径

def calculate_ratio(predicted):
    count = sum(res == 1 for res in predicted)  # 统计列表中'1'的数量
    ratio = count / len(predicted) * 100  # 计算比例并转换为百分比
    return ratio

df_label = pd.read_excel(file_path_label)


# 提取三个维度的标注数据
autonomy_label = df_label['自主力\nAutonomy'].tolist()
competence_label  = df_label['胜任力\nCompetence'].tolist()
relatedness_label  = df_label['归属\nRelatedness'].tolist()
intervene_label = df_label['干预'].tolist()
print(intervene_label)

intervene_ratio = calculate_ratio(intervene_label)

# 打印结果

print(f'intervene Ratio: {intervene_ratio:.2f}%')
