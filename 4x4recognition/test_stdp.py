from parameters import A_plus,A_minus,tau_plus,tau_minus,range_stdp
from STDP import rl
import numpy as np
import matplotlib.pyplot as plt


# Определите диапазон значений времени
t = np.linspace(-range_stdp, range_stdp, 1000)

# Вызовите функцию для каждого значения времени
rl_values = [rl(i) for i in t]

# Постройте график функции
plt.plot(t, rl_values)
plt.xlabel('Time')
plt.ylabel('rl(t)')
plt.show()