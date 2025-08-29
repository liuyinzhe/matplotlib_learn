import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# import seaborn as sns
# from matplotlib.ticker import FuncFormatter
import re
# 设置中文字体支持（如果需要显示中文）
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# # 生成模拟数据 - 在实际应用中替换为您的测序reads长度数据
# np.random.seed(42)
# # 模拟不同长度的reads，大部分集中在较短的区域，少部分长reads
# reads_lengths = np.concatenate([
#     np.random.normal(150, 20, 5000),  # 短reads
#     np.random.normal(1000, 100, 2000),  # 中等长度reads
#     np.random.normal(5000, 500, 500),  # 长reads
#     np.random.normal(10000, 1000, 100)  # 超长reads
# ])
reads_lengths = []
#seqkit fx2tab -n -l -g r84130_241210_001_1_D01.fasta.gz.fasta.gz | cut -f 2- > len_gc
with open("len_gc",mode='r') as fh:
    for line in fh:
        record = re.split("\s",line.strip())
        length,gc = record[0],record[0]
        reads_lengths.append(int(length))

# 确保所有长度都是正数
reads_lengths = np.abs(reads_lengths)

# 创建DataFrame
df = pd.DataFrame(reads_lengths, columns=['length'])

# 按照1000bp分bin
bin_size = 1000
max_length = int(np.ceil(df['length'].max() / bin_size)) * bin_size
bins = range(0, max_length + bin_size, bin_size)
#np.ceil 是 NumPy 库中用于向上取整的函数，其核心功能是将输入的数值（或数组中的每个元素）向上调整到最近的整数

# 为每个read分配bin
df['bin'] = pd.cut(df['length'], bins=bins, right=False)
# pandas.cut() 是用于数据分箱的函数;right（区间是否包含右边界）

# 计算每个bin的reads数量
bin_counts = df['bin'].value_counts().sort_index(ascending=False) # 倒叙排序
#print(bin_counts)

# 计算每个bin的总长度（每个bin中所有reads长度的总和）
bin_total_length = df.groupby('bin')['length'].sum().sort_index(ascending=False) # 倒叙排序
#print(bin_total_length)
# 计算累积总长度(从长到短累加)
cumulative_total_length = bin_total_length.cumsum()

# 准备绘图数据
bin_labels = [f"{int(int(bin.left)/1000)}-{int(int(bin.right)/1000)}" for bin in bin_counts.index]
counts = bin_counts.values

# 创建图形和主坐标轴
fig, ax1 = plt.subplots(figsize=(14, 8))

# 绘制柱状图
bars = ax1.bar(range(len(bin_labels)), counts, color='#5975A4', alpha=0.7)# "#5975A4" ,skyblue
ax1.set_xlabel('Range of Reads Length (kb)', fontsize=12)
ax1.set_ylabel('Number of Reads', fontsize=12, color='#5975A4')
ax1.tick_params(axis='y', labelcolor='#5975A4')

# 设置标题
plt.title('Length Distribution of Reads', fontsize=16, fontweight='bold')

# 创建第二个y轴用于绘制累积曲线
ax2 = ax1.twinx()
# 绘制累积曲线
line = ax2.plot(range(len(bin_labels)), cumulative_total_length.values, 
                color='#D76154', marker='o', linestyle='-', linewidth=1, markersize=1) # red
ax2.set_ylabel('Cumulative Bases', fontsize=12, color='#D76154')
ax2.tick_params(axis='y', labelcolor='#D76154')

# 设置x轴标签
ax1.set_xticks(range(len(bin_labels)))
ax1.set_xticklabels(bin_labels, rotation=45, ha='right')

# 格式化y轴标签
def format_y_ticks(value, tick_number):
    if value >= 1000:
        return f'{value/1000:.0f}K'
    return str(int(value))

ax1.yaxis.set_major_formatter(plt.FuncFormatter(format_y_ticks))

# 格式化第二个y轴标签（累积总长度）
def format_cumulative_ticks(value, tick_number):
    if value >= 1000000000:
        return f'{value/1000000000:.0f}GB'
    elif value >= 1000000:
        return f'{value/1000000:.0f}MB'
    elif value >= 1000:
        return f'{value/1000:.0f}kB'
    return str(int(value))

ax2.yaxis.set_major_formatter(plt.FuncFormatter(format_cumulative_ticks))

# 在柱子上添加数值标签（只显示较大的值）
for i, v in enumerate(counts):
    if v > max(counts) * 0.01:  # 只在大约柱子顶部1%以上的柱子上添加标签
        ax1.text(i, v + max(counts)*0.01, str(int(v)), ha='center', va='bottom', fontsize=9)

# 添加图例
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], color='#5975A4', lw=4, label='Number of Reads'),
    Line2D([0], [0], color='#D76154', marker='.', linestyle='-', lw=1, label='Cumulative Bases')
]
ax1.legend(handles=legend_elements, loc='right')

# 调整布局
plt.tight_layout()

# 显示图形
# plt.show()

# 可选：保存图像
plt.savefig('reads_length_distribution_with_cumulative.png', dpi=300, bbox_inches='tight')
