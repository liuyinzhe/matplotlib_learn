
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#plt.switch_backend('agg')  # 适用于linux 命令运行，避免报错
from matplotlib.ticker import FormatStrFormatter

# 设置画布figure大小，避免过于紧凑
figure = plt.figure(figsize=[9.4, 7.8])
#figsize=[6.4, 4.8],constrained_layout=True,layout='constrained'
#figure = plt.figure(layout='constrained')
#figsize=None (width, height) in inches
#dpi=None, facecolor=None, edgecolor=None, linewidth=0.0,
#layout{'constrained', 'tight'}


#fig,ax = plt.subplots()
#print(type(fig))
#print(type(ax))
#<class 'matplotlib.figure.Figure'>
#<class 'matplotlib.axes._subplots.AxesSubplot'>
axes1 = figure.add_subplot(2,2,1)
axes2 = figure.add_subplot(2,2,2)
axes3 = figure.add_subplot(2,2,3)
axes4 = figure.add_subplot(2,2,4)


handles, labels = axes1.get_legend_handles_labels()
figure.legend(handles, labels,loc='upper right')
#plt.legend(handles, labels,bbox_to_anchor=(0.5, 0., 0.5, 0.0))

# 指定y轴文字format
axes2.yaxis.set_major_formatter(FormatStrFormatter(r'$%.2f$'))
