# Import libraries
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import random, time
 
# Change the Size of Graph using
# Figsize
fig = plt.figure(figsize=(10, 10))
 
# Generating a 3D sine wave
ax = plt.axes(projection='3d')

# Turn Interactive mode on
# plt.ion()


# Creating array points using
# numpy
x = np.arange(0, 20, 0.1)
y = np.sin(x)
z = y*np.sin(x)
c = x + y
 
# To create a scatter graph
ax.scatter(x, y, z, c=c)
 
# trun off/on axis
plt.axis('on')
plt.show(block=False)

time.sleep(5)

for i in range(100):
    xn = random.randrange(20)
    yn = random.randrange(20)
    zn = random.randrange(20)

    x = np.append(x, xn)
    y = np.append(y, yn)
    z = np.append(z, zn)
 
    ax.scatter(x, y, z)
    plt.draw()
    time.sleep(1)
