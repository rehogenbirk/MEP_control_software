# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 12:08:09 2019

@author: LocalAdmin

Module with functions to control Lakeshore 332 Temperature Controller thorugh a GPIB connection

TODO: 
    - Add function to set PID to autotune (CMODE)
    - Add check for setpoint unit ()
"""

import pyvisa as visa
import time
import numpy as np
import matplotlib.pyplot as plt

### Constants

kelvin = 273.15

### Setup functions

def connect_tc332(address='GPIB0::12::INSTR'):
    """Sets up connection to the instrument at the address"""
    rm = visa.ResourceManager()
    return rm.open_resource(address)

### Queries

def get_device_name(instrument):
    """Queries device name"""
    return instrument.query('*IDN?')


def get_temp(instrument, unit='c'):
    """Queries sensor temperature either in celsius 'c' or kelvin 'k'"""
    if unit == 'k':
        temp = float(instrument.query('KRDG?'))
    elif unit == 'c':
        temp = float(instrument.query('CRDG?'))
    else:
        print('Unit is not given correctly')
    return temp


def get_setpoint(instrument, unit='c'):
    """Queries the setpoint for the heater either in celsius or kelvin.
    NB make sure the setpoint is set to temperature"""
    setpoint = instrument.query('SETP?')
    
    # SETP? returns string, so values have to be parsed
    value = float(setpoint[1:7])
    if setpoint[0] == '-':
        value = -value
        
    #TODO check for units in order to give correct output
    #if unit == 'c':
        #setpoint = setpoint + 273.15
    return value


def get_heater_range(instrument):
    """Query for heater range, 0:off, 1:low, 2:med and 3:high"""
    return int(instrument.query('RANGE?')[0])

### Control functions
def set_heater_range(instrument, range_num):
    """Sets heater range, range_num = 0:off, 1:low, 2:med and 3:high. Tested to be working"""
    instrument.write('RANGE ' + str(range_num))

    # Check if setting is applied
    time.sleep(1)
    range_set = get_heater_range(instrument)
    if range_set != range_num:
        print('Heater range was NOT set correctly as %s' % range_num)
    else:
        ranges = ['OFF', 'low', 'medium', 'high']
        print('Heater range was set to the %s setting' % ranges[range_num])


def set_setpoint(instrument, setpoint, unit='c'):
    """Set the setpoint for the heater, either in celsius or kelvin. """
    ## TODO:  make sure the setpoint is set to temperature and to correct unit
    instrument.write('SETP %s' % setpoint)

    # Check if setting is applied
    time.sleep(0.1)
    setpoint_set = get_setpoint(instrument)
    if setpoint_set != setpoint:
        print('Setpiont was NOT set correctly')
    else:
        print('Setpoint was set to the %s degrees %s' % (setpoint, unit.upper()))