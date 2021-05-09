import matplotlib.pyplot as plt

fig = plt.figure()
data = []
subplotNum = [421, 422, 423, 424, 425, 426, 427, 428]
colors = ['r', 'g', 'b', 'y', 'm', 'c', 'k', 'r']
for i in range(8):
	plt.subplot(subplotNum[i])
	file = open("Data\\data_chan" + str(i) + "_0.txt", 'r')
	for line in file.readlines():
		data.append(int(line))
	plt.plot(data, colors[i])
	data = []
plt.show()
