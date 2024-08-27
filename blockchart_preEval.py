import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# 设置基色，这里我们选择蓝色为基色
base_color = np.array([0, 0, 1])  # RGB for blue

data = np.random.rand(138)

# 生成23x6的随机数据
data_matrix = data.reshape(6, 23)

# 创建一个与数据相同大小的颜色数组
colors = np.zeros((6, 23, 3))  # 初始化为黑色

for i in range(6):
    for j in range(23):
        # 根据数据值调整颜色，接近1则趋向于基色，接近0则趋向于灰色
        colors[i, j] = base_color * data_matrix[i, j] + np.array([0.5, 0.5, 0.5]) * (1 - data_matrix[i, j])

# 创建图形和坐标轴
fig, ax = plt.subplots()
# 显示颜色方格
c = ax.pcolor(colors, edgecolors='k', linewidths=1)

# 设置坐标轴的范围和显示设置
ax.set_xlim(0, 23)  # 设置x轴范围
ax.set_ylim(0, 6)  # 设置y轴范围
ax.set_aspect('equal')  # 确保每个格子都是正方形

# 隐藏坐标轴的刻度
ax.set_xticks([])
ax.set_yticks([])

# 显示图形
plt.show()