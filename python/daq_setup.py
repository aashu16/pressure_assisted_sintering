#!usr/in/env python3

"""
Work area for testing NI USB-6009 DAQ

Ai1: k-type thermocouple, 0 - 10V
Ai2: 250 kg loadcell, -10V - +10V
Ai3: LVDT +/- 2.5 mm, -10V - +10V

Takes average voltage of 100 samples measured at 1 kHz

Calibration Equations
TC: T(C) = 117.11298671*V  + 0.018616368 
Load Cell:
LVDT:  d(mm) = 0.25*V

File Output:
'#\tClock Time\tElapsed Time [s]\tT [C]\tLoad [N]\tdL [mm]\n'

"""

import time
from PyDAQmx import *
from numpy import zeros, mean, float64

################################    Global Vars    ################################
deviceName = "dev5"
temperatureSlope = 117.11298671
temperatureOffset = 0.0186368
loadSlope = 1
loadOffset = 0
lengthSlope = 0.25
lengthOffset = 0


################################ Initiation Functions ################################

def daq_setup(deviceName):
    #create channel names based on deviceName
    TC_channel = deviceName + "/ai1"
    LC_cahnnel = deviceName + "/ai2"
    LVDT_channel = deviceName + "/ai3"

    #Initial DAQ setup
    analog_input = Task()
    data = np.zeros((100,0), dtype=float64)
    read = int32()

    #Set up analog channels
    analog_input.CreateAIVoltageChan(TC_channel,"",DAQmx_Val_Cfg_Default, 0 , -10.0, DAQmx_Val_Volts, None)
    analog_input.CreateAIVoltageChan(LC_channel,"",DAQmx_Val_Cfg_Default, -10.0 , -10.0, DAQmx_Val_Volts, None)
    analog_input.CreateAIVoltageChan(LVDT_channel,"",DAQmx_Val_Cfg_Default, -10.0 , -10.0, DAQmx_Val_Volts, None)

    #Measurement timing
    analog_input.CfgSampClkTiming("",1000.0, DAQmx_Val_Rising, DAQmx_Val_FiniteSamps, 100)

    #Reading setup
    analog_input.ReadAnalogF64(100, 10.0,  DAQmx_Val_GroupByChannel, data, 100, byref(read), None)

    return analog_input

def file_init():
    #TODO ################################################################
    #Add sample diameter and make load in Pa
    file_name = input("File Name: ")
    initial_length = input('Initial sample thickness (mm): ')

    if file_name[-4:] != '.txt':
        file_name = file_name + '.txt'

    log_file = open(file_name, 'w')
    date = time.strftime('%Y-%m-%d %H:%M:%S')
    log_file.write('Pressure Assisted Sintering\t%s' %  date)
    log_file.write('Inital sample thickness: %s' % initial_length)
    log_file.write('')
    log_file.write('#\tClock Time\tElapsed Time [s]\tT [C]\tLoad [N]\tdL [mm]\n')


    return file, float(initial_length), float(initial_diameter)

def zero_lvdt():
    #TODO ################################################################
    global lengthOffset


def zero_load():
    # TODO ################################################################
    global loadOffset


################################ Measurement Functions ################################

def convert_data(data):
    #takes average of 100 data reading, converts to physical value, and retuns value
    """
    TC: T(C) = 117.11298671*V  + 0.018616368 
    Load Cell:
    LVDT:  d(mm) = 0.25*V
    """
    global temperatureSlope
    global temperatureOffset
    global loadSlope
    global loadOffset
    global lengthSlope
    global lengthOffset

    vTemperature, vLoad, vLength = mean(data)

    temperature = temperatureSlope * vTemperature * temperatureOffset
    load = loadSlope * vLoad * loadOffset
    length = lengthSlope * vLength * lengthOffset

    return temperature, load, length


def read_daq(analog_input):
    try:
        analog_input.ReadAnalogF64(100, 10.0,  DAQmx_Val_GroupByChannel, data, 100, byref(read), None)

        temperature, load, length = convert_data(data)

        return temperature, load, length

    except: #if DAQ reading fails return empty values
        return temperature = None, load = None, length= None



################################    Main    ################################
def main():
    #GUI ????
    #TODO
    # Configure DAQ
    global deviceName
    analog_input = daq_setup(deviceName)

    #Configure file output
    log_file, initial_length, initial_diameter= file_init()

    #zero lvdt
    zero_lvdt()
    
    #start measurement
    
    #shut down
    DAQmxStopTask(analog_input)
    DAQmxClearTask(analog_input)
    log_file.close()


if __name__ = '__main__':
    main()
    
