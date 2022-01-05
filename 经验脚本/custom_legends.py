from matplotlib import rcParams, cycler
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

#ref# https://www.matplotlib.org.cn/gallery/text_labels_and_annotations/custom_legends.html

# Fixing random state for reproducibility
np.random.seed(19680801)

N = 10
data = (np.geomspace(1, 10, 100) + np.random.randn(N, 100)).T
cmap = plt.cm.coolwarm
rcParams['axes.prop_cycle'] = cycler(color=cmap(np.linspace(0, 1, N)))


custom_lines = [Line2D([0], [0], color=cmap(0.), lw=4),
                Line2D([0], [0], color=cmap(.5), lw=4),
                Line2D([0], [0], color=cmap(1.), lw=4)]

fig, ax = plt.subplots()
lines = ax.plot(data)
ax.legend(custom_lines, ['Cold', 'Medium', 'Hot'])

'''
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

legend_elements = [Line2D([0], [0], color='b', lw=4, label='Line'),
                   Line2D([0], [0], marker='o', color='w', label='Scatter',
                          markerfacecolor='g', markersize=15),
                   Patch(facecolor='orange', edgecolor='r',
                         label='Color Patch')]

# Create the figure
fig, ax = plt.subplots()
ax.legend(handles=legend_elements, loc='center')

plt.show()
'''


'''
正常获得legend

    # 必须有相应的lable,单个子图
    #plot_handle, plot_labels = axes[0,0].get_legend_handles_labels()
    #violin_handle, violin_labels = axe1.get_legend_handles_labels()
    
    #fig.legend((plot_obj,violin_obj),labels=['pearson corr','mut count'])
    #fig.legend(labels=['pearson corr','mut count'],labelcolor=['r','b'])
    
    # 多个子图
    # lines_labels = [ax.get_legend_handles_labels() for ax in fig.axes]
    # lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]
    # fig.legend(lines, labels)

    #handles, labels = axes[0,0].get_legend_handles_labels()
    #fig.legend(handles, labels, loc='upper center')
'''
fig, ax = plt.subplots()
lines = ax.plot(data)
ax.legend()
