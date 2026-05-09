import matplotlib.pyplot as plt

# ---------- 数据 ----------
# 所有样本及其 Mean Depth，并标注类型
samples = ['A', 'B', 'C','D','E','F','G','H','I']
depths  = [295.95, 288.97, 292.61,214.81,292.08,202.32,283.48,278.88,253.37]
types   = ['treatment', 'treatment', 'treatment','treatment','control','control','control','control','control']  # 用于配色

# 颜色映射
color_map = {
            'treatment': '#3082F1',   #
            'control':  '#af8dc3' # 浅紫
             }   

# ---------- 绘图 ----------
fig, ax = plt.subplots(figsize=(9, 5))

# 生成水平柱状图，y 轴反转让第一个样本在上方（可选）
bars = ax.barh(samples[::-1], depths[::-1],  # 反转顺序让 Sample5BD 在顶部
               color=[color_map[t] for t in types[::-1]],
               edgecolor='white', height=0.6)

# 标题与轴标签
ax.set_title('Mean Target Coverage', fontsize=14, fontweight='bold')
ax.set_xlabel('Mean Depth (X)', fontsize=12)
ax.set_ylabel('Sample', fontsize=12)

# 在柱末端添加数值标签
for bar, val in zip(bars, depths[::-1]):
    # print(bar)
    # Rectangle(xy=(0, -0.3), width=253.37, height=0.6, angle=0)
    # https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.text.html
    # Axes.text(x, y, s, fontdict=None, **kwargs)
    ax.text(val + 2, bar.get_y() + bar.get_height()/2, # x 上移动， y 定位在柱子中间
            str(val), va='center', fontsize=9)

# 设置起始位置和结束位置（例如从0到1000，每隔200添加一条线）
start = 0
end = 601
interval = 200

# 循环添加垂直虚线
for i in range(start, end, interval):
    ax.axvline(x=i, color='gray', linestyle='--')

# 手动创建图例(不重复)
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor=color_map['treatment'], label='Treatment'),
                   Patch(facecolor=color_map['control'],  label='Control')
                   ]
ax.legend(handles=legend_elements, loc='lower right')

# 移除多余边框
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# 调整布局
plt.tight_layout()

# ---------- 保存 ----------
plt.savefig('bar_chart.png', dpi=300, bbox_inches='tight')
plt.savefig('bar_chart.pdf', bbox_inches='tight')
plt.show()