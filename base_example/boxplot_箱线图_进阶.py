#matplotlib可视化箱线图
#https://zhuanlan.zhihu.com/p/38199913
import matplotlib.pyplot as plt
import numpy as np
all_data=[np.random.normal(0,std,100) for std in range(1,4)]

figure,axes=plt.subplots() #得到画板、轴
bplot=axes.boxplot(all_data,patch_artist=True) #描点上色
plt.setp(axes, xticks=[1,2,3],
         xticklabels=['x1', 'x2', 'x3'])

colors = ['pink', 'lightblue', 'lightgreen']
for patch, color in zip(bplot['boxes'], colors):
        # 设置前景色
        #patch.set_facecolor(color)
        # 设置中位数medians线条颜色和宽度
        for patch in bplot["medians"]:
            patch.set_color('w')  #设置为白色
            #patch.set_linewidth(2)

        # 设置 中间线条 颜色和宽度
        for patch in bplot["whiskers"]:
            patch.set_color('r')  #设置为红色
            #patch.set_linewidth(2)


        # 设置 最小值，最大值线条 颜色和宽度
        for patch in bplot["caps"]:
            patch.set_color('b')  #设置为蓝色
            #patch.set_linewidth(2)
plt.show() #展示
