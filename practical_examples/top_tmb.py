
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import os,re
import numpy as np
from matplotlib.pyplot import MultipleLocator
#从pyplot导入MultipleLocator类，这个类用于设置刻度间隔
from matplotlib import ticker

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
#plt.rcParams['font.sans-serif'] = ['STZhongsong'] # 指定默认字体：解决plot不能显示中文问题
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

# 设置 ggplot 格式
# print(plt.style.available)
plt.style.use('ggplot')

'''
ggplot  #灰暗
seaborn-v0_8 # 灰暗
seaborn-v0_8-darkgrid # 亮色
bmh
fivethirtyeight
'''
# 设置画布为 snow 色调
#plt.rcParams['axes.facecolor']='snow'


# 假设样品 TMB = 12.86589
sample_TMB = 12.86589


class Range():
    '''
    支持浮点 step 数值
    '''
    def __init__(self,start, end, step):
        self.start = start - step
        self.end = end
        self.step = step
 
    def __iter__(self):
        return self
 
    def __next__(self):
        self.start += self.step
        if self.start >= self.end :
            raise StopIteration
        return self.start

def calc_quantile(numlist,method='nearest'):
    '''
    计算四分位三个数值
    input : numlist 
    method
    ['linear', 'lower', 'higher', 'midpoint', 'nearest']
    https://numpy.org/doc/stable/reference/generated/numpy.quantile.html
    '''
    lower_q = np.quantile(numlist,0.25,method=method)
    median = np.quantile(numlist,0.5,method=method)
    higher_q = np.quantile(numlist,0.75,method=method)
    
    return lower_q,median,higher_q

# 跳转脚本所在目录
pwd = os.path.split(os.path.realpath(__file__))[0]
os.chdir(pwd)

cancer_type_tmb_dic = {}
tmb_value = []
with open('data/base_info.tsv',mode='r',encoding='utf-8') as fh:
    for line in fh:
        record = re.split('\t',line.strip())
        #print(record)
        patient_id,sex,OS_months,OS_status,cancer_type,TMB_nonsynonymous = record
        # 是否保留 tmb 等于 0 的记录
        # if float(TMB_nonsynonymous) == 0:
        #     continue
        tmb_value.append(float(TMB_nonsynonymous))
        if cancer_type not in cancer_type_tmb_dic:
            cancer_type_tmb_dic[cancer_type] = []
            cancer_type_tmb_dic[cancer_type].append([float(TMB_nonsynonymous),float(OS_months)])
        else:
            cancer_type_tmb_dic[cancer_type].append([float(TMB_nonsynonymous),float(OS_months)])

# tmb_value排序前，将样品TMB 加入 
tmb_value.append(sample_TMB)
tmb_sorted_value = sorted(tmb_value,reverse=True)
sample_len= len(tmb_sorted_value)

# 四分位数值，计算index占总数量的百分比
lower_q,median,higher_q = calc_quantile(tmb_sorted_value)
print(lower_q,median,higher_q)
lower_q_precent = tmb_sorted_value.index(lower_q)/sample_len
higher_q_precent = tmb_sorted_value.index(higher_q)/sample_len

percent_lst = []
sorted_tmb_value_lst = []
Quartile_x=[]  # percent
Quartile_y=[]  # tmb
sample_percent = 0.0
for index,tmb in enumerate(tmb_sorted_value):
    percent = index/sample_len
    percent_lst.append(percent)
    sorted_tmb_value_lst.append(tmb)
    # 获得样品的 sample_percent 百分比位置(这里是浮点小数)
    if tmb == sample_TMB:
        sample_percent = percent
    # 获得25% 与 75%的数值
    if int(percent*100)==25 or int(percent*100)==75:
        Quartile_x.append(percent)
        Quartile_y.append(tmb)


# 建立画框，与绘图区
fig,ax = plt.subplots()



'''
s 大小
marker 形状
c  color 颜色
'''
ax.scatter(percent_lst,sorted_tmb_value_lst,s=10,c='b')
#https://www.jb51.net/article/226542.htm
#latex 常见字符 https://www.cnblogs.com/auspice/p/16596300.html
ax.scatter([lower_q_precent,higher_q_precent],[lower_q,higher_q],s=20,marker=r"o",facecolors='w',edgecolors='r')
# 绘制 样品坐标
ax.scatter([sample_percent,],[sample_TMB,],s=100,marker=r"*",facecolors='w',edgecolors='r')
# ax.plot([0.2,0],[0.2,75],lw=1,color="b",alpha=0.65)

plt.annotate("下四分位值TMB:{0}".format(round(lower_q,2)), xy=(lower_q_precent, lower_q+5), fontsize=8, xycoords='data')
plt.annotate("上四分位值TMB:{0}".format(round(higher_q,2)), xy=(higher_q_precent, higher_q+5), fontsize=8, xycoords='data')

# 
plt.annotate("样品TMB:{0}".format(round(sample_TMB,2)), xy=(sample_percent, sample_TMB+5), fontsize=8, xycoords='data')


# ax.set_xlabels('')
#ax.set_xticks(0,0.2,0.4,0.6,0.8,1.0)
#ax.set_xlabel('','20%','40%','60%','80%','100%')
'''
背景

'''

for i in Range(0, 1, .4):
    #plt.axhspan(i, i+.2, facecolor='0.2', alpha=0.5)
    plt.axvspan(i, i+.2, facecolor='b', alpha=0.1)

# 标注
# https://zhuanlan.zhihu.com/p/205110001
plt.annotate('Sample TMB:{}\n Top {}%'.format(round(sample_TMB,2),round(sample_percent*100,2)), 
            xy=(sample_percent,sample_TMB), # 点的坐标
            xytext=(sample_percent+0.1,sample_TMB+15), # 文字坐标
            fontsize=8,
            horizontalalignment='center',
            verticalalignment='center',
             arrowprops=dict(facecolor='#74C476', 
                             alpha=0.3,
                             arrowstyle='fancy',#'-|>',
                             connectionstyle='angle3',#有多个参数可选
                             color='r',
                            ),
            textcoords='data',
            #添加文字背景色
            bbox={'facecolor': '#74C476', #填充色
                'edgecolor':'b',#外框色
                'alpha': 0.5, #框透明度
                'pad': 0.8,#本文与框周围距离 
                'boxstyle':'round'
                }
            )

# 设置展示区间
plt.xlim(0, 1)
plt.ylim(0, 75)

# 刻度间隔
x_major_locator=MultipleLocator(0.2)
#把x轴的刻度间隔设置为1，并存在变量里
y_major_locator=MultipleLocator(10)
#把y轴的刻度间隔设置为10，并存在变量里

ax.xaxis.set_major_locator(x_major_locator)
#把x轴的主刻度设置为1的倍数
ax.yaxis.set_major_locator(y_major_locator)
#把y轴的主刻度设置为10的倍数

# 刻度内容
#plt.xticks(percent_lst,['','20%','40%','60','80%','100%'],rotation=15)
# plt.yticks(y,['100k','200k','300k','400k','500k','600k','700k','800k',],rotation=30,fontsize=10,color='red',fontweight='bold',backgroundcolor='black')
# #rotation设置刻度值倾斜角度

# 标签
# plt.xlabel("销售月份",fontsize=10,color='red',fontweight='bold',loc='center',backgroundcolor='black',labelpad=6)
# #显示横坐标标题 fontsize设置字体大小,color设置字的颜色，fontweight设置标签是否加粗
# #loc设置标签位置(具体值有center left right) backgroundcolor设置标签的背景颜色 labelpad与轴的距离
# plt.ylabel("销售数量")

plt.xlabel("Rank",fontsize=10,)#color='red',fontweight='bold',loc='center',backgroundcolor='black',labelpad=6)
plt.ylabel("TMB")

# 设置百分比刻度显示
ax.xaxis.set_major_formatter(ticker.PercentFormatter(xmax=1,decimals=0))


# 设置网格线
# https://zhuanlan.zhihu.com/p/474231286
# plt.grid(color = 'r', linestyle = '--', linewidth = 0.5)

plt.show()
