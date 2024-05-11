

# 查询当前系统所有字体
from matplotlib.font_manager import FontManager

mpl_fonts = set(f.name for f in FontManager().ttflist)

print('all font list get from matplotlib.font_manager:')
for f in sorted(mpl_fonts):
    print('\t' + f)

# YouYuan 幼圆字体
# SimHei 微软雅黑
# SimSun 宋体
# KaiTi 楷体
# Microsoft YaHei 微软雅黑
# Microsoft JhengHei 微软正黑
# Adobe Fangsong Std 仿宋
# Adobe Heiti Std 黑体
# Adobe Kaiti Std 楷体

# 字体和font-family对照表
# https://blog.csdn.net/lunhui1994_/article/details/80507970




# 全局字体（1）
#import matplotlib
#matplotlib.rc("font",family='SimSun')
plt.rc('font',family='SimSun') 


# 彻底解决Python里matplotlib不显示中文的问题
# https://zhuanlan.zhihu.com/p/104081310


# 全局字体（2）

from matplotlib import font_manager
# 指定字体
font_dirs = ['/data/home/liuyinzhe/tmp/lqy/Lefse/fonts']
font_files = font_manager.findSystemFonts(fontpaths=font_dirs)
# 添加扫描的字体
for font_file in font_files:
    font_manager.fontManager.addfont(font_file)
# 输出所有字体 以及对应目录
for font in font_manager.fontManager.ttflist:
    print(font.name, '-', font.fname)


'''
matplotlib的字体的家族（font-family)一共有五类字体，他们分别是serif，sans-serif，cursive，fantasy，monospace，下面介绍下常用的三类。
serif：衬线字体， 宋体，Times News Romas属于这类字体
sans-serif：无衬线字体，黑体，Arial等都属于这类字体
monospace： 等宽字体，网络web端用的比较多
'''
# set font
plt.rcParams['font.sans-serif'] = 'Kristen ITC'
#plt.rcParams['font.sans-serif']=['SimHei','Songti SC','STFangsong']
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# set font
plt.rcParams['font.family'] = 'SimHei'
plt.rcParams['axes.unicode_minus']=False  # 用来正常显示负号


# 局部使用
fname='/home/user1/myapp/font/myfont.ttf'
myfont=fm.FontProperties(fname=fname)
ax1.set_title('title test',fontproperties=myfont)

