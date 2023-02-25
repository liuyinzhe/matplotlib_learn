

# https://blog.csdn.net/weixin_39724004/article/details/110844560
fig.set_figheight(100)
fig.set_figwidth(100)
# 100代表的是英寸

'''
figure的另一个属性:dpi(dot per inch)
它代表的是每英寸有多少个像素点
默认值是72。
可以使用如下的三种设置中的一种得到(1200,600)像素的图：
'''
# figsize=(宽，高)
figsize=(15,7.5), dpi= 80
figsize=(12,6)  , dpi=100
figsize=( 8,4)  , dpi=150
