import matplotlib.pyplot as plt

# print(plt.rcParams.keys()) #获取 rcParams 键的完整列表

plt.rcParams['font.sans-serif'] = ['SimHei']
#plt.rcParams['axes.unicode_minus'] = False
plt.style.use("_classic_test_patch")   #  ggplot Solarize_Light2 _classic_test_patch _mpl-gallery-nogrid
#_classic_test_patch

#print(plt.style.available)

x=[1,2,3,4,5]  # 确定柱状图数量,可以认为是x方向刻度
y=[5,7,4,3,1]  # y方向刻度

color=["#E6956F","#788FCE","#A6BA96","#CDC3D4","#A88AD2"]
x_label= ['DUP','INS', 'DEL', 'INV', 'BND']
plt.xticks(x, x_label)  # 绘制x刻度标签
plt.bar(x, y,color=color)  # 绘制y刻度标签


#https://www.delftstack.com/zh/howto/matplotlib/how-to-set-the-figure-title-and-axes-labels-font-size-in-matplotlib/
# print(plt.rcParams.keys()) #获取 rcParams 键的完整列表
# 键	描述
# axes.labelsize	x 和 y 标签的字体大小
# axes.titlesize	轴标题的字体大小
# figure.titlesize	图形标题的大小（figure.suptitle()）
# xtick.labelsize	刻度标签的字体大小
# ytick.labelsize	刻度标签的字体大小
# legend.fontsize	图例的字体大小（plt.legend()，fig.legend()）
# legend.title_fontsize	图例标题的字体大小，无设置为默认轴。
# print("xtick.labelsize",plt.rcParams['xtick.labelsize'])
# print("ytick.labelsize",plt.rcParams['ytick.labelsize'])
# parameters = {"xtick.labelsize": 10, "ytick.labelsize": 10}
# plt.rcParams.update(parameters)

#设置网格刻度
plt.grid(True,linestyle='--',color='#BFBFBF',alpha=0.8)
plt.xlabel("SV Type",fontsize=15)
plt.ylabel("Number",fontsize=15)

plt.savefig(fname='SV_type.png', dpi=600,bbox_inches='tight',pad_inches=0.1)
