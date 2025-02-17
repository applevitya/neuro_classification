""" STATIC I/O CONTROL FUNCTIONS: set_mode, get_state, set_state, set_current, set_pull, close """

import ctypes
import sys
import time

if sys.platform.startswith("win"):
    dwf = ctypes.cdll.dwf
elif sys.platform.startswith("darwin"):
    dwf = ctypes.cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
else:
    dwf = ctypes.cdll.LoadLibrary("libdwf.so")

"""-----------------------------------------------------------------------"""

#set DIO to input/output
def set_mode(device_handle, channel, output):
    """
        set a DIO line as input, or as output

        parameters: - device handle
                    - selected DIO channel number
                    - True means output, False means input
    """
    # load current state of the output enable buffer
    mask = ctypes.c_uint16()
    dwf.FDwfDigitalIOOutputEnableGet(device_handle, ctypes.byref(mask))
    
    # convert mask to list
    mask = list(bin(mask.value)[2:].zfill(16))
    
    # set bit in mask
    if output:
        mask[15 - channel] = "1"
    else:
        mask[15 - channel] = "0"
    
    # convert mask to number
    mask = "".join(element for element in mask)
    mask = int(mask, 2)
    
    # set the pin to output
    dwf.FDwfDigitalIOOutputEnableSet(device_handle, ctypes.c_int(mask))
    return
 
"""-----------------------------------------------------------------------"""
#get state from DIO
def get_state(device_handle, channel):
    """
        get the state of a DIO line

        parameters: - device handle
                    - selected DIO channel number

        returns:    - True if the channel is HIGH, or False, if the channel is LOW
    """
    # load internal buffer with current state of the pins
    dwf.FDwfDigitalIOStatus(device_handle)
    
    # get the current state of the pins
    data = ctypes.c_uint32()  # variable for this current state
    dwf.FDwfDigitalIOInputStatus(device_handle, ctypes.byref(data))
    
    # convert the state to a 16 character binary string
    data = list(bin(data.value)[2:].zfill(16))
    
    # check the required bit
    if data[15 - channel] != "0":
        state = True
    else:
        state = False
    return state

"""-----------------------------------------------------------------------"""

#set state to DIO
def set_state(device_handle, channel, state):
    """
        set a DIO line as input, or as output

        parameters: - device handle
                    - selected DIO channel number
                    - True means HIGH, False means LOW
    """
    # load current state of the output state buffer
    mask = ctypes.c_uint16()
    dwf.FDwfDigitalIOOutputGet(device_handle, ctypes.byref(mask))
    
    # convert mask to list
    mask = list(bin(mask.value)[2:].zfill(16))
    
    # set bit in mask
    if state:
        mask[15 - channel] = "1"
    else:
        mask[15 - channel] = "0"
    
    # convert mask to number
    mask = "".join(element for element in mask)
    mask = int(mask, 2)
    
    # set the pin state
    dwf.FDwfDigitalIOOutputSet(device_handle, ctypes.c_int(mask))
    return
    
"""-----------------------------------------------------------------------"""

def reset_IO(device_handle):
    dwf.FDwfDigitalIOReset(device_handle)
    return


def turn_on_channel(device_handle,channel):
    set_mode(device_handle,channel,True)
    set_state(device_handle,channel,True)
    return
    
def turn_off_channel(device_handle,channel):
    set_state(device_handle,channel,False)

"""-----------------------------------------------------------------------"""







