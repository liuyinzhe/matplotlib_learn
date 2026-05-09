# 导入 matplotlib 的 pyplot 模块，用于绘图
import matplotlib.pyplot as plt
# 导入 pandas，用于数据组织和处理
import pandas as pd

# ==================== 数据准备 ====================

# 创建数据字典，包含样本名称（Sample）以及两个已知的百分比列
data = {
    'Sample': ['A', 'B', 'C'],
    # 注意：原表格中的 Class3 列实际是 Class1 的比例
    'Class1': [66.17, 58.16, 48.15],
    'Class2': [16.24, 13.95, 11.99],
    'Class3': [17.58, 27.87, 39.85],
}
# 将字典转换为 DataFrame 以便后续计算
df = pd.DataFrame(data)
# # 计算 Class3 作为剩余比例（100% 减去 Class1 和 Class2）
# df['Class3'] = 100 - df['Class1'] - df['Class2']

# ==================== 颜色定义 ====================

# 定义三个类别对应的颜色（十六进制色码）
colors = {'Class1': '#00A087',    # 
          'Class2': '#F4A261',  # 
          'Class3': '#E76F51'}   # 

# ==================== 创建图形和坐标轴 ====================

# 创建一个图形 (figure) 和一个坐标轴 (ax)，设置图形尺寸为宽10英寸、高4.5英寸
fig, ax = plt.subplots(figsize=(10, 4.5))

# ==================== 绘制横向堆积条形图 ====================

# 第一段：Class1（深橙色），这是堆积的最左段
# barh 绘制水平条形图，y 为样本名，width 为 Class1 的值
bars_on = ax.barh(df['Sample'], df['Class1'], color=colors['Class1'], label='Class1')

# 第二段：Class2（橙黄色），堆积在 Class1 的右侧
# left 参数指定该段条形图的起始位置为 Class1 的结束位置
bars_near = ax.barh(df['Sample'], df['Class2'],
                    left=df['Class1'],          # 从 Class1 之后开始
                    color=colors['Class2'], label='Class2')

# 第三段：Class3（绿色），堆积在 Class2 的右侧
# left 参数为 Class1 + Class2 之和的位置
bars_off = ax.barh(df['Sample'], df['Class3'],
                    left=df['Class1'] + df['Class2'],  # 从前两段之后开始
                    color=colors['Class3'], label='Class3')

# ==================== 在 Class1 段上添加百分比标注 ====================

# 遍历每个样本，i 为索引（0 开始），on_val 为对应的 Class1 值
for i, on_val in enumerate(df['Class1']):
    # 标注文本置于 Class1 段的中央 (x = on_val/2, y = i)
    # 颜色为白色，加粗，字号 10
    ax.text(on_val / 2, i, f'{on_val:.1f}%',
            va='center', ha='center', fontsize=10,
            color='white', fontweight='bold')

# ==================== 自定义图例 ====================

# 获取当前图例的“句柄”和“标签”（按绘图顺序排列）
handles, labels = ax.get_legend_handles_labels()
# 定义希望显示的图例顺序（Class1, Class2, Class3）
order = ['Class1', 'Class2', 'Class3']
# 根据 order 列表重新组合句柄
new_handles = [handles[labels.index(l)] for l in order]
# 添加图例：置于图上方居中，水平排列 3 列，无边框
ax.legend(new_handles, order,
          loc='upper center',                # 图例定位在上方中间
          bbox_to_anchor=(0.5, 1.12),        # 微调图例垂直位置，避免与标题重叠
          ncol=3, frameon=False)             # 3 列显示，无图例框

# ==================== 标题与坐标轴设置 ====================

# 设置图表标题，loc='left' 使标题左对齐，pad=15 增加标题与图之间的间距
ax.set_title('Distribution by Sample', loc='left', pad=15)
# 设置 x 轴标签
ax.set_xlabel('Percentage (%)')
# 设置 x 轴显示范围，留出一些空白以便标注完整显示
ax.set_xlim(0, 105)
# 反转 y 轴，使第一个样本 CRD 显示在顶部
ax.invert_yaxis()
# 添加 x 轴方向的虚线网格，半透明
ax.xaxis.grid(True, linestyle='--', alpha=0.6)

# ==================== 图表布局与保存 ====================

# 自动调整子图参数，使元素不重叠（尤其考虑标题和图例的调整后）
plt.tight_layout()
# 保存为 PNG 格式，分辨率 300 DPI，裁剪紧贴内容
plt.savefig('Stacked_bar_chart_vertical.png', dpi=300, bbox_inches='tight')
# 保存为 PDF 格式（矢量图），同样裁剪
plt.savefig('Stacked_bar_chart_vertical.pdf', bbox_inches='tight')
# 显示图形（在交互式环境中弹出窗口）
plt.show()