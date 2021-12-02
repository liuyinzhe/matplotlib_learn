#单纯为了好看，没有特别意义
#作为颜色控制的学习素材

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

# 字体设置
plt.rcParams['font.sans-serif']=['Noto Sans S Chinese Regular']
# 风格设置
plt.style.use('default')

'''
print(matplotlib.style.use.style.available)
['Solarize_Light2', '_classic_test_patch',
'_mpl-gallery', '_mpl-gallery-nogrid',
'bmh', 'classic', 'dark_background', 'fast',
'fivethirtyeight', 'ggplot',
'grayscale',
'seaborn','seaborn-bright', 'seaborn-colorblind',
'seaborn-dark', 'seaborn-dark-palette',
'seaborn-darkgrid','seaborn-deep', 'seaborn-muted',
'seaborn-notebook', 'seaborn-paper', 'seaborn-pastel',
'seaborn-poster', 'seaborn-talk', 'seaborn-ticks',
'seaborn-white', 'seaborn-whitegrid',
'tableau-colorblind10']
'''
def normlization(x):
    '''
    numpy array
    归一化到区间{0,1]
    '''
    _range = np.max(x) - np.min(x)
    return (x - np.min(x)) / _range

def standardization(x):
    '''
    numpy array
    将输入的x 正态标准化 (x-mu)/sigma ~ N(0,1)
    正态分布，总和为1
    '''
    mu = np.mean(x,axis=0)
    sigma = np.std(x,axis=0)
    return (x-mu)/sigma

# 参考:https://moonbooks.org/Articles/How-to-plot-a-bar-chart-with-a-colorbar-using-matplotlib-in-python-/
import matplotlib.pyplot as plt
from matplotlib.cm import ScalarMappable

data_x = [0,1,2,3]
data_hight = [60,60,80,100]

# 缩放到0和1之间，保留原始数据的分布(Normalization——Normalizer())
# https://www.zhihu.com/question/20467170
data_hight_normalized = [x / max(data_hight) for x in data_hight]

fig, ax = plt.subplots(figsize=(15, 4))

# my_cmap = plt.cm.GnBu
my_cmap = plt.cm.get_cmap('GnBu')
# 使用normalized 后数值[0,1] 映射 对应过度色的准确颜色(RGBa)
colors = my_cmap(data_hight_normalized)

# 绘图
rects = ax.bar(data_x, data_hight, color=colors)

# A mixin class to map scalar data to RGBA. #这里 将 data_hight 进行 normalized 处理形成[0,1] 的列表 norm
sm = ScalarMappable(cmap=my_cmap, norm=plt.Normalize(0,max(data_hight)))

# 上面rects, Normalize 步骤也可以用 ScalarMappable 对象进行
#rects = ax.bar(data_x, data_hight, color=sm.to_rgba(data_hight))

## fix bug before matplotlib v3.1.0 ;you need add .set_array([])
#I believe matplotlib v3.1.0 is the version where this behaviour changed and you no longer need to set_array
#https://stackoverflow.com/questions/63754046/when-adding-colorbar-for-a-matplotlib-tricontourf-typeerror-you-must-first-se
#sm.set_array([])

cbar = plt.colorbar(sm)
cbar.set_label('Color', rotation=270,labelpad=15)
# rotation 角度
# labelpad 横坐标距离
plt.xticks(data_x)    
plt.ylabel("Y")

plt.title('How to plot a bar chart with a colorbar with matplotlib ?')

#plt.savefig("bar_chart_with_colorbar_03.png", bbox_inches='tight')
plt.show()
