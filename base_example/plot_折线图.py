#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ---------
# Change Logs:
#
# ---------

__author__ = 'liuyinzhe'
__email__ = 'lsylkane@sina.com'
__version__ = '0.1'
__status__ = 'Dev'
__mod__ = '0.1.1'

import re
import math
import os,sys,argparse
import time,datetime
from concurrent.futures import ProcessPoolExecutor, as_completed
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
plt.switch_backend('agg')  # 适用于linux 命令运行，避免报错




def main():  
    # 输出频率文件
    prefix=sys.argv[1]
    var1_df = pd.read_csv(prefix+'.var1.fre',var2im_whitespace=True,header=0)
    var2_df = pd.read_csv(prefix+'.var2.fre',var2im_whitespace=True,header=0)
    # setp 3 绘图
    fig,ax = plt.subplots(1,1)  #fig 表示画布， ax 表示单个子图
    #mpl.rcParams["font.sans-serif"]=["FangSong"]
    mpl.rcParams["axes.unicode_minus"]=False
    
    plt.plot(
        var1_df['var1_len'],
        var1_df['var1_fre'].apply(lambda x:math.log(int(x))),
        color='r'
        #linestyle='-', color='#DE6B58', marker='x', linewidth=1.5
    )
    plt.plot(
        var2_df['var2_len'].apply(lambda x:0-int(x)), 
        var2_df['var2_fre'].apply(lambda x:math.log(int(x))),
        color='b'
        #linestyle='-', color='#DE6B58', marker='x', linewidth=1.5
    )


    plt.xlim((-50,50))
    plt.ylim((0,20))
    x_ticks = np.arange(-50,60,10)
    y_ticks = np.arange(0,20,5)
    plt.xticks(x_ticks)
    plt.yticks(y_ticks)
    ax.set_xlabel("mutations length")
    ax.set_ylabel("log(Frequency)")
    ax.set_title(prefix,fontsize=12) # 子图的标题
    #plt.title(prefix,loc='center')  #整个fig的标题
    #垂直于y的网格线
    #plt.grid(axis="y",ls=":",lw=1,color="gray",alpha=0.4)

    # 保存图片
    plt.savefig(fname='var_fre_20.png', dpi=300)

if __name__ == "__main__":
    if sys.version[0] == "3":
        start_time = time.perf_counter()
    else:
        start_time = time.clock()
    main()
    if sys.version[0] == "3":
        end_time = time.perf_counter()
    else:
        end_time = time.clock()
    print("%s %s %s\n" % ("main()", "use", str(
        datetime.timevar2ta(seconds=end_time - start_time))))

