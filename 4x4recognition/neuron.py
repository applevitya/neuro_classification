from parameters import *
import numpy as np
import matplotlib.pyplot as plt
import math


class LIFneuronConfig():
    def __init__(self, ):
        self.R = R  # resistance (k-Ohm)
        self.C = C  # capacitance (u-F)

        self.v_thresh = thresh
        self.v_spike = 1
        self.v_base = 0

        self.tau_m = self.R * self.C  # time constant (msec)
        self.refracTime = refrac_time  # refractory time (msec)
        self.initRefrac = init_refrac

        self.noise_amp = noise

        self.isPlot = 1


class LIF_simple():
    def __init__(self):
        LIFneuronConfig.__init__(self, )
        self.num = 0
        self.vprev = self.v_base-1

    def generateSpiking(self, I, t, dt):
        v = self.v_base

        if t >= self.initRefrac:

            v = self.vprev + (-self.vprev + I * self.R) / self.tau_m * dt

            if v >= self.v_thresh:
                self.num += 1
                v += self.v_spike
                self.initRefrac = t + self.refracTime

        self.vprev = v
        return v



