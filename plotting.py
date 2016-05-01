import matplotlib.pyplot as plt
import numpy as np

x = np.array(range(10))
y = np.random.rand(10)
z = np.random.rand(10)/6.0

radius = 8

plt.scatter(x,y,s=radius**2,c='#ffc34d',edgecolors='none')
plt.errorbar(x,y,fmt=None,yerr=z, ecolor='k', elinewidth=1.5)
plt.title("Stability of Irving Algorithm")
plt.xlabel("Number of People in Match")
plt.ylabel("Percentage with Stable Match Found")
plt.show()
