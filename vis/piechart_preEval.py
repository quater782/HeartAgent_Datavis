import sys
import matplotlib.pyplot as plt
import numpy as np

# Sample data
data = [
    {'dim1': 0.8, 'dim2': 0.4, 'dim3': 0.6},
    {'dim1': 0.3, 'dim2': 0.7, 'dim3': 0.5},
    {'dim1': 0.9, 'dim2': 0.2, 'dim3': 0.8},
    {'dim1': 0.5, 'dim2': 0.6, 'dim3': 0.7},
    {'dim1': 0.2, 'dim2': 0.9, 'dim3': 0.3},
]

# Define base colors for each dimension
base_colors = {
    'dim1': np.array([1, 0, 0]),  # Red
    'dim2': np.array([0, 1, 0]),  # Green
    'dim3': np.array([0, 0, 1])   # Blue
}

# Prepare figure and axes
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(8, 8))
size = 0.3  # Thickness of each ring
inner_radius = 0.5  # Radius of hollow core
num_data = len(data)
angles = np.linspace(0, 2 * np.pi, num_data, endpoint=False)

# Draw each ring
for i, dim in enumerate(['dim1', 'dim2', 'dim3']):
    radii = np.array([d[dim] for d in data])
    width = 2 * np.pi / num_data
    colors = [base_colors[dim] * value + np.array([0.5, 0.5, 0.5]) * (1 - value) for value in radii]
    print(radii)
    radii2 = radii+1 #或者采用归一法，让所有的值都变成1（最大的）
    ax.bar(angles, radii2, width=width, bottom=inner_radius + i * size, color=colors, edgecolor='white')

# Final touches
# ax.set_theta_direction(-1)
# ax.set_theta_zero_location('N')
ax.set_xticks([])
ax.set_yticks([])
ax.set_ylim(0, inner_radius + 3 * size)


# Show plot
plt.show()