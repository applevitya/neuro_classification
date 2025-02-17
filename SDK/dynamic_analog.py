""" DEVICE CONTROL FUNCTIONS: open, check_error, close """

import sys
from ctypes import *
from dwfconstants import DwfDigitalOutTypeCustom
import time
import numpy as np

"""-----------------------------------------------------------------------"""

if sys.platform.startswith("win"):
    dwf = cdll.dwf
elif sys.platform.startswith("darwin"):
    dwf = cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
else:
    dwf = cdll.LoadLibrary("libdwf.so")

hzSys = c_double()
"""-----------------------------------------------------------------------"""

#Analog to digital

def measure(device_handle,channel):
    """
        measure a voltage
        parameters: - device data
                    - the selected oscilloscope channel (1-2, or 1-4)
 
        returns:    - the measured voltage in Volts
    
    """
    
    # set up the instrument
    dwf.FDwfAnalogInConfigure(device_handle, c_bool(False), c_bool(False))
 
    # read data to an internal buffer
    dwf.FDwfAnalogInStatus(device_handle, c_bool(False), c_int(0))
 
    # extract data from that buffer
    voltage = c_double()   # variable to store the measured voltage
    dwf.FDwfAnalogInStatusSample(device_handle, c_int(channel - 1), byref(voltage))
 
    # store the result as float
    voltage = voltage.value
    return voltage
    

def osc(device_data,param, channel):
    '''
    param=[sampling_frequency,buffer_size,offset,amplitude_range]
    '''
    #initialize osc
    dwf.FDwfAnalogInChannelEnableSet(device_data.handle, c_int(0), c_bool(True))
    dwf.FDwfAnalogInChannelOffsetSet(device_data.handle, c_int(0), c_double(param[2]))
    dwf.FDwfAnalogInChannelRangeSet(device_data.handle, c_int(0), c_double(param[3]))
    dwf.FDwfAnalogInBufferSizeSet(device_data.handle, c_int(param[1]))
    dwf.FDwfAnalogInFrequencySet(device_data.handle, c_double(param[0]))
    dwf.FDwfAnalogInChannelFilterSet(device_data.handle, c_int(-1), constants.filterDecimate)
    
    #record
    
    dwf.FDwfAnalogInConfigure(device_data.handle, c_bool(False), c_bool(True))
    
    while True:
        status = ctypes.c_byte()    # variable to store buffer status
        dwf.FDwfAnalogInStatus(device_data.handle, ctypes.c_bool(True), ctypes.byref(status))
 
        
        if status.value == constants.DwfStateDone.value:
                # exit loop when ready
                break
 
    buffer = (ctypes.c_double * data.buffer_size)()   # create an empty buffer
    dwf.FDwfAnalogInStatusData(device_data.handle, ctypes.c_int(channel - 1), buffer, ctypes.c_int(data.buffer_size))
 

    time = range(0, data.buffer_size)
    time = [moment / data.sampling_frequency for moment in time]
 

    buffer = [float(element) for element in buffer]
    
    return buffer,time
 
 
 
def close(device_data):
    """
        reset the scope
    """
    dwf.FDwfAnalogInReset(device_data)
    return




def struct_measure(device_handle,shift,clock,data,matrix): #shift - это защелка, clock - вход тактовых импульсв, data- входные данные

    for i in range(8):
	    block =matrix[i*8 : (i+1)*8]
	    if np.sum(block) > 1:
	        # Количество единиц в блоке не равно 1 - завершаем программу с ошибкой
	        raise ValueError("Ошибка: каждый блок по 8 элементов должен содержать только одну единицу. Потому что мы считываем за один такт только 1 структуру для каждого мультиплексора. То есть одновременно можно только 8")


    truth_tables = {}
    values = [[0,0,0], [1,0,0], [0,1,0], [1,1,0], [0,0,1], [1,0,1], [0,1,1], [1,1,1]]

    for i in range(1, 9):
	    truth_tables[i] = np.array(values[i-1])


    shift_register = []

    blocks = [matrix[i:i+8] for i in range(0, len(matrix), 8)]

    for i, block in enumerate(blocks):
        index = block.index(1) if 1 in block else 0
        shift_register = np.append(shift_register,truth_tables[index+1])



    blocks = [np.flip(shift_register[i:i+3]) for i in range(0, len(shift_register), 3)]

    shift_register = np.flip(blocks, axis=0)

    matrix = list(np.concatenate(shift_register))

    d_shift = [0 for x in range(74)]
    d_shift[0] = 0
    d_shift[73] = 1

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

    duration_1 = 0.000097



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
    time.sleep(0.001)
    
    return














	
			    
