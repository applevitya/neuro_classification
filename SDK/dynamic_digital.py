""" DEVICE CONTROL FUNCTIONS: open, check_error, close """

import sys
from ctypes import *
from dwfconstants import DwfDigitalOutTypeCustom
import time

"""-----------------------------------------------------------------------"""

if sys.platform.startswith("win"):
    dwf = cdll.dwf
elif sys.platform.startswith("darwin"):
    dwf = cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
else:
    dwf = cdll.LoadLibrary("libdwf.so")

hzSys = c_double()
"""-----------------------------------------------------------------------"""

def pulse(device_handle,channel,duration): #duration in s
    dwf.FDwfDigitalOutRunSet(device_handle, c_double(duration)) # second run
    dwf.FDwfDigitalOutRepeatSet(device_handle, c_int(1)) # once
    dwf.FDwfDigitalOutIdleSet(device_handle, c_int(channel), c_int(1)) # 1=DwfDigitalOutIdleLow, low when not running
    dwf.FDwfDigitalOutCounterInitSet(device_handle, c_int(channel), c_int(1), c_int(0)) # initialize high on start
    dwf.FDwfDigitalOutCounterSet(device_handle, c_int(channel), c_int(0), c_int(0)) # low/high count zero, no toggle during run
    dwf.FDwfDigitalOutEnableSet(device_handle, c_int(channel), c_int(1))
    dwf.FDwfDigitalOutConfigure(device_handle, c_int(1))
    time.sleep(duration)

    return

"""-----------------------------------------------------------------------"""


def led_matrix(device_handle,shift,clock,data,matrix):
    d_shift = [0 for x in range(194)]
    d_clock =[0]

    d_shift[0] = 0
    d_shift[193] = 1
    matrix = matrix[::-1]

    data_new = [0] + [1 if matrix[i] == 1 else 0 for i in range(len(matrix)) for j in range(3)]
    d_clock = [0]+[0, 1, 0] * len(matrix)

    hzSys = c_double()
    dwf.FDwfDigitalOutInternalClockInfo(device_handle, byref(hzSys))

    rgbdata_shift=(c_ubyte*((len(d_shift)+7)>>3))(0)
    rgbdata_data=(c_ubyte*((len(data_new)+7)>>3))(0)
    rgbdata_clock=(c_ubyte*((len(d_clock)+7)>>3))(0)

    for i in range(len(d_shift)):
        if d_shift[i] != 0:
            rgbdata_shift[i>>3] |= 1<<(i&7)

    for i in range(len(data_new)):
        if data_new[i] != 0:
            rgbdata_data[i>>3] |= 1<<(i&7)

    for i in range(len(d_clock)):
        if d_clock[i] != 0:
            rgbdata_clock[i>>3] |= 1<<(i&7)

    pin_shift = shift
    pin_data = data
    pin_clock = clock
    
    duration_1 = 0.000252



    dwf.FDwfDigitalOutRunSet(device_handle, c_double(duration_1)) # 1ms run
    dwf.FDwfDigitalOutEnableSet(device_handle, c_int(pin_shift), c_int(1))

    dwf.FDwfDigitalOutTypeSet(device_handle, c_int(pin_shift), DwfDigitalOutTypeCustom)
    dwf.FDwfDigitalOutIdleSet(device_handle, c_int(0), c_int(1))
    dwf.FDwfDigitalOutDividerSet(device_handle, c_int(pin_shift), c_int(int(hzSys.value/(6*128e3)))) # set sample rate
    dwf.FDwfDigitalOutDataSet(device_handle, c_int(pin_shift), byref(rgbdata_shift), c_int(len(d_shift)))
    dwf.FDwfDigitalOutCounterInitSet(device_handle, c_int(0), c_int(1), c_int(0)) # initialize high on start
    ######
    dwf.FDwfDigitalOutRunSet(device_handle, c_double(duration_1)) # 1ms run
    dwf.FDwfDigitalOutEnableSet(device_handle, c_int(pin_data), c_int(1))

    dwf.FDwfDigitalOutTypeSet(device_handle, c_int(pin_data), DwfDigitalOutTypeCustom)
    dwf.FDwfDigitalOutIdleSet(device_handle, c_int(0), c_int(1))
    dwf.FDwfDigitalOutDividerSet(device_handle, c_int(pin_data), c_int(int(hzSys.value/(6*128e3)))) # set sample rate
    dwf.FDwfDigitalOutDataSet(device_handle, c_int(pin_data), byref(rgbdata_data), c_int(len(data_new)))
    dwf.FDwfDigitalOutCounterInitSet(device_handle, c_int(0), c_int(1), c_int(0)) # initialize high on start

    ######
    dwf.FDwfDigitalOutRunSet(device_handle, c_double(duration_1)) # 1ms run
    dwf.FDwfDigitalOutEnableSet(device_handle, c_int(pin_clock), c_int(1))

    dwf.FDwfDigitalOutTypeSet(device_handle, c_int(pin_clock), DwfDigitalOutTypeCustom)
    dwf.FDwfDigitalOutIdleSet(device_handle, c_int(0), c_int(1))
    dwf.FDwfDigitalOutDividerSet(device_handle, c_int(pin_clock), c_int(int(hzSys.value/(6*128e3)))) # set sample rate
    dwf.FDwfDigitalOutDataSet(device_handle, c_int(pin_clock), byref(rgbdata_clock), c_int(len(d_clock)))
    dwf.FDwfDigitalOutCounterInitSet(device_handle, c_int(0), c_int(1), c_int(0)) # initialize high on start


    dwf.FDwfDigitalOutConfigure(device_handle, c_int(1))
    time.sleep(0.0003)
    
    return










    
