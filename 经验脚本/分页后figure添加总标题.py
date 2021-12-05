
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#plt.switch_backend('agg')  # 适用于linux 命令运行，避免报错
from matplotlib.ticker import FormatStrFormatter

#参考：https://matplotlib.org/devdocs/api/_as_gen/matplotlib.pyplot.suptitle.html
# 这里的图可以取看，参考网页最下下面的几个例子
# 

'''
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

axes1.set_title('Map1')
axes2.set_title('Map2')
axes3.set_title('Map3')
axes4.set_title('Map4')

figure.suptitle("Big Suptitle")
'''

fig, axs = plt.subplots(2, 2, figsize=(4, 4), constrained_layout=True)
for ax in axs.flat:
    im = ax.pcolormesh(arr, **pc_kwargs)
fig.colorbar(im, ax=axs, shrink=0.6)
fig.suptitle('Big Suptitle')
