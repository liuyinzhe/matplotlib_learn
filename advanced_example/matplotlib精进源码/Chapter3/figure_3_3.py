# -*- coding:utf-8 -*-

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

mpl.rcParams["font.sans-serif"]=["FangSong"]
mpl.rcParams["axes.unicode_minus"]=False

mu = 60.0
sigma = 2.0
x = mu+sigma*np.random.randn(500)

bins = 50

fig,ax = plt.subplots(1,1)

n,bins,patches = ax.hist(x,
                         bins,
                         normed=True,
                         histtype="bar",
                         facecolor="cornflowerblue",
                         edgecolor="white",
                         alpha=0.75)

y = ((1/(np.power(2*np.pi,0.5)*sigma))*
     np.exp(-0.5*np.power((bins-mu)/sigma,2)))

ax.plot(bins,y,color="orange",ls="--",lw=2)

ax.grid(ls=":",lw=1,color="gray",alpha=0.2)

ax.text(54,0.2,
        r"$y=\frac{1}{\sigma\sqrt{2\pi}}e^{-\frac{(x-\mu)^2}{2\sigma^2}}$",
        {"color": "r", "fontsize": 20})

ax.set_xlabel("体重")
ax.set_ylabel("概率密度")
ax.set_title(r"体重的直方图: $\mu=60.0$, $\sigma=2.0$",fontsize=16)

plt.show()
