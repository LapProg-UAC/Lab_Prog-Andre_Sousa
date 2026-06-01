import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

x = np.linspace(-5, 5, 150)
y = np.linspace(-5, 5, 150)
X, Y = np.meshgrid(x, y)

R = np.sqrt(X**2 + Y**2)

Z1 = np.sin(np.sqrt(X**2 + Y**2))

Z2 = np.zeros_like(X)

cores_Z2 = np.sin(R * 3)

fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

surf1 = ax.plot_surface(
    X, Y, Z1,
    cmap='plasma',
    alpha=0.8,
    edgecolor='none',
    antialiased=True
)

ax.contour(x, y, Z1,
           zdir='z',
           cmap='plasma',
           offset=0.0,
           levels=50,
           linewidths=1.5,
           antialiased=True)

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

ax.view_init(elev=25, azim=45)

plt.show()