from parameters import A_plus,A_minus, tau_plus, tau_minus
import numpy as np

tau_1 = 0.14
tau_2 = 1.35

def af(t):
    if t >= 0:
        return -A_plus * np.exp(-float(t) / tau_plus)
    if t < 0:
        return A_minus * np.exp(float(t) / tau_minus)

def rl(t):
    if t >= 0:
        return -A_plus * np.exp(-float(t) / tau_1)-A_plus * np.exp(-float(t) / tau_2)
    if t < 0:
        return A_minus * np.exp(float(t) / tau_1)+A_minus * np.exp(float(t) / tau_2)


# STDP weight update rule
def update(w, t):
    del_w = rl(t)
    if del_w < 0:
        if w+del_w>0:
            if w+del_w>1:
                return 1
            else: return w + del_w
        else:
            return 0.15

    elif del_w > 0:
        if w + del_w > 0:
            if w + del_w > 1:
                return 1
            else:
                return w + del_w
        else:
            return 0.15




