from matplotlib import pyplot as plt

data_1 = [1,2,2,4]
data_2 = [2,3,1,2]

fig = plt.figure()
ax = fig.add_axes([0.1, 0.1, 0.4, 0.5])

ax.plot(data_1, '--', label='d1')
#ax.plot(data_2, '++', label='d2')
#ax.legend(loc='best')
print(ax)
plt.show()
