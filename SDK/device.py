""" DEVICE CONTROL FUNCTIONS: open, check_error, close """

import sys
import ctypes

"""-----------------------------------------------------------------------"""

if sys.platform.startswith("win"):
    dwf = ctypes.cdll.dwf
elif sys.platform.startswith("darwin"):
    dwf = ctypes.cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
else:
    dwf = ctypes.cdll.LoadLibrary("libdwf.so")
    
"""-----------------------------------------------------------------------"""



def open():
    # this is the device handle - it will be used by all functions to "address" the connected device
    device_handle = ctypes.c_int()

    # connect to the first available device
    dwf.FDwfDeviceOpen(ctypes.c_int(-1), ctypes.byref(device_handle))
    print("open device")
    
    if device_handle.value ==0:
        print("failed to open device")
        quit()
    return device_handle
    
"""-----------------------------------------------------------------------"""

def close(hdwf):
    dwf.FDwfDeviceClose(hdwf)
    print("close device")
    return
    
"""-----------------------------------------------------------------------"""
    
def check_error(device_handle):
    """
        check for connection errors
    """
    # if the device handle is empty after a connection attempt
    if device_handle.value == constants.hdwfNone.value:
        # check for errors
        err_nr = ctypes.c_int()            # variable for error number
        dwf.FDwfGetLastError(ctypes.byref(err_nr))  # get error number
    
        # if there is an error
        if err_nr != constants.dwfercNoErc:
            # display it and quit
            err_msg = ctypes.create_string_buffer(512)        # variable for the error message
            dwf.FDwfGetLastErrorMsg(err_msg)                  # get the error message
            err_msg = err_msg.value.decode("ascii")           # format the message
            print("Error: " + err_msg)                        # display error message
            quit()                                            # exit the program
    return
