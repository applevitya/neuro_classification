from neuron import LIF_simple
from parameters import num_in_neu,num_out_neu, range_stdp,epochs
from encoding import Poisson_generator, read_img,reconst_weights,spikes_graph
from STDP import update
import numpy as np
import matplotlib.pyplot as plt
import cv2
import csv



############ Random Weights #####################

W = np.random.uniform(0.1,0.3,size = [num_in_neu,num_out_neu])
# W = np.ones((num_in_neu,num_out_neu))*0.2
#################################
# time series

T = 22 #ms
dt = 0.1
time = np.arange(0,T+dt,dt)





##### learning ########

for ep in range(epochs):

	### input/output spikes #########################
	in_spikes = np.empty(shape=(num_in_neu, len(time)))
	out_spikes = np.zeros(shape=(num_out_neu, len(time)))

	# creating the output layer of neurons
	out_neurons = []
	# for i in range(num_out_neu):
	# 	a = LIF_simple()
	# 	out_neurons.append(a)

	for m in range(1,3):
		in_spikes = np.zeros(shape=(num_in_neu, len(time)))
		out_spikes = np.zeros(shape=(num_out_neu, len(time)))
		out_neurons = []
		for i in range(num_out_neu):
			a = LIF_simple()
			out_neurons.append(a)

		img = read_img(str(m)+".png")
		for l in range(num_in_neu):
			in_spikes[l] = Poisson_generator(T, dt, 0 + img[l], 1)

		spikes_graph(in_spikes,m)
		I = np.zeros(shape=(num_out_neu,))
		for t in range(len(time)):
			for j,neu in enumerate(out_neurons):
				I[j] = 0
				for i in range(num_in_neu):
					# I[j] = 0
					I[j] += np.dot(W[i][j],in_spikes[i][t])
				if t>=neu.initRefrac:
						v = neu.vprev + (-neu.vprev + I[j] * neu.R) / neu.tau_m * dt  # LIF

						# v= neu.vprev + np.dot(W[i][j],in_spikes[i][t])
						if (v > neu.v_base):
							v -= 0.012
							if v < neu.v_base:
								v = neu.v_base
								pass
						if v >= neu.v_thresh:
							neu.num += 1
							out_spikes[j][t] = 1
							neu.initRefrac = t + neu.refracTime

							neu.v_thresh += 0.001
				neu.vprev = v

			max_index = 0
			max_value = out_neurons[0].vprev
			for i in range(0,len(out_neurons)):
				if out_neurons[i].vprev > max_value:
					max_index = i
					max_value = out_neurons[i].vprev

			for j, neu in enumerate(out_neurons):
				neu.vprev = 0
				if j!= max_index:
					out_spikes[j][t] = 0
					pass

			for j,neu in enumerate(out_neurons):
				for i in range(num_in_neu):
					for t1 in range(-1, -range_stdp, -1):
						if 0 <= t + t1 < len(time):
							if in_spikes[i][t + t1] == 1 and out_spikes[j][t] == 1:
								W[i][j] = update(W[i][j], t1)
					for t1 in range(1, range_stdp, 1):
						if 0 <= t + t1 < len(time):
							if in_spikes[i][t + t1] == 1 and out_spikes[j][t] == 1:
								W[i][j] = update(W[i][j], t1)






######### testing ################

data = W
aspect_ratio = float(data.shape[1]) / data.shape[0]

# plt.imshow(data, cmap='plasma', aspect=aspect_ratio, extent=[0, data.shape[1], 0, data.shape[0]])
# Устанавливаем только целые значения больше нуля по осям X и Y
fig1, ax1 = plt.subplots()
xlabels = [i for i in range(1, W.shape[1]+1) if i % 1 == 0]
ylabels = [i for i in range(1, W.shape[0]+1) if i % 1 == 0]
plt.xticks(np.arange(W.shape[1]), xlabels)
plt.yticks(np.arange(W.shape[0]), ylabels)


plt.imshow(data, cmap='plasma')
plt.colorbar()
plt.title('Значения весов нейронной сети')

plt.savefig('results/gradient.png', dpi=500)
plt.show()



result1 = cv2.hconcat(reconst_weights(W[:,0]))
cv2.imwrite("results/neuron_0.png", result1)
result2 = cv2.hconcat(reconst_weights(W[:,1]))
cv2.imwrite("results/neuron_1.png", result2)

with open('results/W.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(W)