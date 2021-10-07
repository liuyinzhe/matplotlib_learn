import matplotlib.pyplot as plt

# create a new figure
fig = plt.figure()

# figure picture
# use "r" to avoid escape sequence \f 
imageData1 = plt.imread(r"D:\figure_image\captain-bird.png")
# add an image to the figure
fig.figimage(imageData1,200,100,origin="upper",alpha=0.05,resize=True,zorder=1)

# axes pictrue
imageData2 = plt.imread(r"D:\figure_image\treasure-map.png")
# display an image i.e. data on a 2D raster
plt.imshow(imageData2,alpha=1.0)
plt.axis("off")

# set several points
plt.scatter([348,445,657],[387,523,415],c="black",edgecolor="w",s=50)

bboxs=dict(facecolor="navy",edgecolor="navy",alpha=0.8)
plt.text(299,369,r"#1$\ \Re\Game\Im$",fontsize=15,color="w",bbox=bboxs)
plt.text(404,504,r"#2$\ \ss\ell\wp$",fontsize=15,color="w",bbox=bboxs)
plt.text(614,399,r"#3$\ \hslash\imath\jmath$",fontsize=15,color="w",bbox=bboxs)

plt.annotate("where to go...",xy=(552,363),
             xycoords="data",
             xytext=(555,308),
             textcoords="data",
             weight="black",
             color="#000000",
             arrowprops=dict(arrowstyle="<|-",
                             relpos=(0.2,0.0)))

# set a diagram describing the points
diagramContent = r"#1$\ \ $"+r"$\bigstar$"*3+"\n"+\
                 r"#2$\ \ $"+r"$\bigstar$"*4+"\n"+\
                 r"#3$\ \ $"+r"$\bigstar$"*1+"\n"+\
                 r"#?$\ \ $"+"???"
bbox={"boxstyle":"round","facecolor":"#F3F0ED",
      "edgecolor":"#453B34","linewidth":2,
      "linestyle":"--","alpha":0.8}
plt.text(688,162,diagramContent,
         fontsize=25,
         color="#453B34",
         rotation=-5,
         bbox=bbox)

plt.text(663,62,"Potential Treasure",fontsize=20,color="k",weight="bold",rotation=-5)

# save a SVG file
fig.savefig(r"D:\figure_image\figure_image.svg")
