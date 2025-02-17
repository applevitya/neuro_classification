import numpy as np
from parameters import firing_delimeter
import cv2
import matplotlib.pyplot as plt

def Poisson_generator(time,dt,rate, n, myseed=False):
  """
  Generates poisson trains

  Args:
    rate            : noise amplitute [Hz]
    n               : number of Poisson trains
    myseed          : random seed. int or boolean

  Returns:
    pre_spike_train : spike train matrix, ith row represents whether
                      there is a spike in ith spike train over time
                      (1 if spike, 0 otherwise)
  """

  # Retrieve simulation parameters
  range_t = np.arange(0, time+dt, dt)  # Vector of discretized time points [ms]
  Lt = range_t.size

  # set random seed
  if myseed:
      np.random.seed(seed=myseed)
  else:
      np.random.seed()

  # generate uniformly distributed random variables
  u_rand = np.random.rand(n, Lt)

  # generate Poisson train
  poisson_train = 1. * (u_rand < rate * (dt /firing_delimeter))

  return poisson_train


def read_img(name_file):

	img = cv2.imread(name_file, 0)
	img2 = cv2.imread(name_file,0)

	img = np.ndarray.flatten(img)
	return img




def threshold(train):
    tu = np.shape(train[0])[0]
    thresh = 0
    for i in range(tu):
        simul_active = sum(train[:, i])
        if simul_active > thresh:
            thresh = simul_active

    return (thresh / 3)


def reconst_weights(weights):
	weights = np.array(weights)
	weights = np.reshape(weights, (2,2))
	img = np.zeros((2,2))
	for i in range(2):
		for j in range(2):
			img[i][j] = weights[i][j]*255

	#cv2.imwrite('neuron' + str(num) + '.png' ,img)
	return img





def spikes_graph(in_array,k):
    # Пример входного двумерного массива
    input_arr = in_array

    # Создание графика с полосками для каждой строки входного массива
    fig, ax = plt.subplots(figsize=(12, 6))

    # Перебираем каждую строку входного массива
    for i, row in enumerate(input_arr):
        # Получаем индексы, где значение равно 1
        indices = np.where(row == 1)[0]
        # Для каждого индекса рисуем полоску на графике
        for index in indices:
            ax.fill_between([index, index+1], i*0.1, (i+1)*0.1, color='red', alpha=0.8)

    # Установка свойств графика
    ax.set_xlim(-1, input_arr.shape[1])
    ax.set_ylim(-0.1, input_arr.shape[0]*0.1)
    ax.set_xticks(np.arange(0, input_arr.shape[1], 100))
    ax.set_xticklabels(np.arange(1, input_arr.shape[1]+1, 100))
    ax.set_yticks(np.arange(0, input_arr.shape[0], 2)*0.1+0.05) # установка меток на каждой второй строке
    ax.set_yticklabels(np.arange(1, input_arr.shape[0]+1, 2))
    ax.set_xlabel('Время, (ms)')
    ax.set_ylabel('Входные нейроны')
    ax.set_title('Входные спайки обучения')
    fig.savefig('results/in_spikes'+str(k)+'.png', dpi=300)