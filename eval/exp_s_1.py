import pandas as pd
from sklearn.metrics import cohen_kappa_score

'''
小实验打标比对
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

# 计算准确率函数
def calculate_accuracy(predicted, actual):
    correct = sum(p == a for p, a in zip(predicted, actual))
    return correct / len(actual) * 100

print("## 第一次打标情况分析：")
for i in range (1,5):
    file_path_x = rf'.\eval\label_data1\x{i}.xlsx'  # 替换为你的实际文件路径
    df = pd.read_excel(file_path_x)
    df_label = pd.read_excel(file_path_label)

    # 提取三个维度的标注数据
    autonomy = df['自主力\nAutonomy'].tolist()
    competence = df['胜任力\nCompetence'].tolist()
    relatedness = df['归属\nRelatedness'].tolist()
    intervene = df['干预'].tolist()

    # 提取三个维度的标注数据
    autonomy_label = df_label['自主力\nAutonomy'].tolist()
    competence_label  = df_label['胜任力\nCompetence'].tolist()
    relatedness_label  = df_label['归属\nRelatedness'].tolist()
    intervene_label = df_label['干预'].tolist()

    # 计算每个维度的Kappa系数
    kappa_autonomy = cohen_kappa_score(autonomy, autonomy_label)
    kappa_competence = cohen_kappa_score(competence, competence_label)
    kappa_relatedness = cohen_kappa_score(relatedness, relatedness_label)
    kappa_intervene = cohen_kappa_score(intervene, intervene_label)

    # 打印结果
    print(f'--专家{i}与heartAgent的 Kappa 一致性结果--')
    print(f'Autonomy Kappa: {kappa_autonomy:.2f}')
    print(f'Competence Kappa: {kappa_competence:.2f}')
    print(f'Relatedness Kappa: {kappa_relatedness:.2f}')
    print(f'Intervene Kappa: {kappa_intervene:.2f}')

    # 计算每个维度的准确率
    print(f'--专家{i}与heartAgent的准确率结果--')
    autonomy_accuracy = calculate_accuracy(autonomy, autonomy_label)
    competence_accuracy = calculate_accuracy(competence, competence_label)
    relatedness_accuracy = calculate_accuracy(relatedness, relatedness_label)
    intervene_accuracy = calculate_accuracy(intervene, intervene_label)

    # 打印结果
    print(f'Autonomy Accuracy: {autonomy_accuracy:.2f}%')
    print(f'Competence Accuracy: {competence_accuracy:.2f}%')
    print(f'Relatedness Accuracy: {relatedness_accuracy:.2f}%')
    print(f'Intervene Accuracy: {intervene_accuracy:.2f}%')

print("---")
print("## 第二次打标情况分析：")

for i in range (1,5):
    
    file_path_x = rf'.\eval\label_data2\x{i}.xlsx'  # 替换为你的实际文件路径
    df = pd.read_excel(file_path_x)
    df_label = pd.read_excel(file_path_label)

    # 提取三个维度的标注数据
    autonomy = df['自主力\nAutonomy'].tolist()
    competence = df['胜任力\nCompetence'].tolist()
    relatedness = df['归属\nRelatedness'].tolist()
    intervene = df['干预'].tolist()

    # 提取三个维度的标注数据
    autonomy_label = df_label['自主力\nAutonomy'].tolist()
    competence_label  = df_label['胜任力\nCompetence'].tolist()
    relatedness_label  = df_label['归属\nRelatedness'].tolist()
    intervene_label = df_label['干预'].tolist()

    # 计算每个维度的Kappa系数
    kappa_autonomy = cohen_kappa_score(autonomy, autonomy_label)
    kappa_competence = cohen_kappa_score(competence, competence_label)
    kappa_relatedness = cohen_kappa_score(relatedness, relatedness_label)
    kappa_intervene = cohen_kappa_score(intervene, intervene_label)

    # 打印结果
    print(f'--专家{i}与heartAgent的 Kappa 一致性结果--')
    print(f'Autonomy Kappa: {kappa_autonomy:.2f}')
    print(f'Competence Kappa: {kappa_competence:.2f}')
    print(f'Relatedness Kappa: {kappa_relatedness:.2f}')
    print(f'Intervene Kappa: {kappa_intervene:.2f}')

    # 计算每个维度的准确率
    print(f'--专家{i}与heartAgent的准确率结果--')
    autonomy_accuracy = calculate_accuracy(autonomy, autonomy_label)
    competence_accuracy = calculate_accuracy(competence, competence_label)
    relatedness_accuracy = calculate_accuracy(relatedness, relatedness_label)
    intervene_accuracy = calculate_accuracy(intervene, intervene_label)

    # 打印结果
    print(f'Autonomy Accuracy: {autonomy_accuracy:.2f}%')
    print(f'Competence Accuracy: {competence_accuracy:.2f}%')
    print(f'Relatedness Accuracy: {relatedness_accuracy:.2f}%')
    print(f'Intervene Accuracy: {intervene_accuracy:.2f}%')