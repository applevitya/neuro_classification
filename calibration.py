from ctypes import *
from  SDK import staticIO, device, dynamic_digital, dynamic_analog
import sys
import numpy as np

import time


from matplotlib.figure import Figure


##### инициализирование####################################################################################################################################
hdwf = c_int()
hdwf = device.open()


led_off = [0 for i in range(64)]
led_on = [1 for i in range(64)]
dynamic_digital.led_matrix(hdwf, 6, 7, 5, led_off) # выключаем светодиоды

iteration = 100

def measure(index):
    struct_index = [0 for i in range(64)]
    struct_index[index-1] = 1
    dynamic_analog.struct_measure(hdwf, 10, 9, 8, struct_index) # struct_measure(device_handle,shift,clock,data,matrix)
    values = []
    for i in range(iteration):
        values.append(dynamic_analog.measure(hdwf, 1))
    return sum(values) / len(values)

def measure_2(index):
    struct_index = [0 for i in range(64)]
    struct_index[index-1] = 1
    dynamic_analog.struct_measure(hdwf, 10, 9, 8, struct_index) # struct_measure(device_handle,shift,clock,data,matrix)
    values = []
    for i in range(iteration):
        values.append(dynamic_analog.measure(hdwf, 2))
    return sum(values) / len(values)



############################################################################################################################################################
#calibration procedure



# known_indices = [22, 23, 24, 30]  # Заранее известные индексы
# initial_weights = []
# final_weights = []

# for index in known_indices:
#     value = measure(index)  # Получаем значение из функции measure
#     initial_weights.append(value)  # Добавляем значение в массив initial_weights

# print(initial_weights)

#led-stimulation
# dynamic_digital.led_matrix(hdwf, 6, 7, 5, led_on)
# time.sleep(1000)
# dynamic_digital.led_matrix(hdwf, 6, 7, 5, led_off)


# for index in known_indices:
#     value = measure(index)  # Получаем значение из функции measure
#     final_weights.append(value)  # Добавляем значение в массив initial_weights

# print(final_weights)

# data=np.vstack((initial_weights,final_weights))
# # Запись массивов в файл
# with open("calibration.txt", "w") as file:
#     np.savetxt(file, data)



############################################################################################################################################################
#one impulse detection

known_indices = list(range(19, 25)) + list(range(27, 33)) + [34] + list(range(36, 41)) + list(range(43, 49)) + list(range(49, 50))
weights_array=np.empty(shape=(50000,len(known_indices)))

time_impulses = 500 

for i in range(time_impulses):
    dynamic_digital.led_matrix(hdwf, 6, 7, 5, led_on)
    time.sleep(1)
    dynamic_digital.led_matrix(hdwf, 6, 7, 5, led_off)
    for j,val in enumerate(known_indices):
        if val<33:
            weights_array[i][j] = measure(val)
        else:
            weights_array[i][j] = measure_2(val)

for i in range(time_impulses,time_impulses+400):
    time.sleep(1)
    for j,val in enumerate(known_indices):
        if val<33:
            weights_array[i][j] = measure(val)
        else:
            weights_array[i][j] = measure_2(val)


data = np.array(weights_array)
with open("results/calibration.txt", "w") as file:
    np.savetxt(file, data)


device.close(hdwf)