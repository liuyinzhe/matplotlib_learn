    #透明
    #alpha=0
    
    #图层绘画前后顺序
    #zorder=0

    #添加空白axes
    #[left, bottom, width, height] ,为axes 坐标轴起点在figure 上的起点x,y
    ax = fig.add_axes([0.4,0.5,1,1],alpha=0,zorder=0,)
    ax.axis('off')
    # 优雅的给所有ax 设置关闭坐标轴
    #fig, axes = plt.subplots(col, row)
    #np.vectorize(lambda ax:ax.axis('off'))(axes)
