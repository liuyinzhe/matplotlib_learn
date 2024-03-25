import patchworklib as pw
import matplotlib.pyplot as plt
plt.style.use('ggplot')

#绘制子图1
ax1 = pw.Brick(figsize=(1, 2))  #每个子图调用pw.Brick方法
ax1.bar([1, 2], [1, 2]) # 柱状图
ax1.set_title("ax1")

#绘制子图2
ax2 = pw.Brick(figsize=(1, 3))
ax2.scatter(range(5), range(5)) #散点图
ax2.set_title("ax2")

#绘制子图3
ax3 = pw.Brick(figsize=(2, 1))
ax3.bar([2, 1], [2, 3]) #柱状图
ax3.set_title("ax3")

#绘制子图4
ax4 = pw.Brick(figsize=(2, 2))
ax4.scatter(range(5), range(5)) # 散点图
ax4.set_title("ax4")

#拼图
ax1234 = (ax1 | ax2) | (ax3 / ax4)
ax1234.savefig('matplotlib.patchworklib.png')  #类似plt.show()
