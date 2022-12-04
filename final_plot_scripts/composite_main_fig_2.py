import pylustrator as pyl
import matplotlib.pyplot as plt

#pyl.start()
pyl.load("../notebooks/figures/ani_aai_plot.png")
pyl.load("../notebooks/figures/runtimes_wall.png", offset=[0,1.0])
pyl.load("../notebooks/figures/memory.png", offset=[0.00,1.0])

plt.savefig('auto_fig2.png')
plt.show()
