"""
Read analog output from Bartington fluxgate using a Labjack device
Rylan Stutters
June 2025

Adapted from code by Derek Fujimoto:
https://github.com/ucn-triumf/QZFM/blob/main/src/QZFM/LabJack.py

Requires install of the following:
    Labjack
        LJM software for T7 devices: https://labjack.com/pages/support?doc=%2Fsoftware-driver%2Finstaller-downloads%2Fljm-software-installers-t4-t7-digit%2F
        LJM python package: python -m pip install labjack-ljm
"""

import numpy as np
import pandas as pd
from datetime import datetime
import csv

# import labjack-ljm
try:
    from labjack import ljm
except ModuleNotFoundError:
    pass

class fluxgateLJ:
    """Low-level readback from Labjack DAQ module via USB

    Attributes:
        ch: (tuple): channel addresses for analog inputs
        handle (int): handle for sending info to labjack. Output of ljm.openS
        csv_log (bool): controls csv logging of measurements
        filename (str): name of csv file to log to
        increment (float): number of centimeters each measurement is seperated by; set to 0 if not used
        position (float): current position of the measurement
    """

    def __init__(self, fluxgate_name=None, LJ_type='T7', LJ_connection='USB', LJ_id='ANY',
                 fluxgate_nbytes=1000, csv_log=False, increment=1):
        """Initialize object: connect

        Args:
            fluxgate_name (str): name of device to look for (connection)
                             for windows this is likely COM3 or COM5
                             for linux, search Z3T0 or similar
            LJ_type (str): passed to ljm.openS, model type
            LJ_connection (str): passed to ljm.openS, connection type. USB|ANY|ETHERNET
            LJ_identifier (str): passed to ljm.openS, device id
            fluxgate_nbytes (int): serial read chunk size in bytes for status updates
            csv_log (bool): controls whether measurements are logged to csv
            increment (float): number of centimeters each measurement is seperated by; set to 0 if not used
        """

        # get LJ handle
        self.handle = ljm.openS(deviceType=LJ_type,
                                connectionType=LJ_connection,
                                identifier=LJ_id)
        
        self.increment = increment
        
        # start logging csv
        if csv_log == True:
            self.init_csv()
            self.csv_log = True
        else:
            self.csv_log = False
        

    def setup(self, x=0, y=1, z=2):
        """Setup input channels to read from. Use AI#

        Args:
            x (int): AI# channel to read in Bx
            y (int): AI# channel to read in By
            z (int): AI# channel to read in Bz
        """

        # check inputs
        if not (type(x) is int and type(y) is int and type(z) is int):
            raise RuntimeError(f'x, y, and z must be int, not {type(x)}, {type(y)}, and {type(z)}')

        if x == y or y == z or x == z:
            raise RuntimeError('Require that x != y != z')

        # get channel addresses
        self.ch = ljm.namesToAddresses(3, (f'AIN{x}', f'AIN{y}', f'AIN{z}'))[0]

    def read_single(self):
        """Read single set of values from device. Use read_data get a longer sequence
        Logs to csv file as well if csv_log was set true upon init

        Returns:
            np.ndarray: fields in uT
        """
        dataTypes = [ljm.constants.FLOAT32, ljm.constants.FLOAT32,
              ljm.constants.FLOAT32]
        nchannels = len(self.ch)

        # read data
        dat = np.array(ljm.eReadAddresses(self.handle, nchannels, self.ch, dataTypes))

        # write a line to csv file if csv_log enabled
        if self.csv_log == True:
            self.log_csv(dat)

        return dat

    def init_csv(self):
        """Initialize csv file

        """

        self.filename = f'fluxgate_{datetime.now().strftime("20%y-%m-%d_%H.%M.%S")}.csv'

        # write header of csv file
        if self.increment != 0:
            with open(self.filename, 'w', newline='') as csvfile:
                csvfile.write(datetime.now().strftime("20%y-%m-%d, %H:%M:%S\n\n"))
                csvfile.write("Position (cm), B_x (uT), B_y (uT), B_z (uT)\n")

        else:
            with open(self.filename, 'w', newline='') as csvfile:
                csvfile.write(datetime.now().strftime("20%y-%m-%d, %H:%M:%S\n\n"))
                csvfile.write("B_x (uT), B_y (uT), B_z (uT)\n")
                
        
        self.position = 0

    

    def log_csv(self, data):
        """Write np array to newline in the csv file

        Args:
            data (np array): data to be written to the csv file
        """

        # add position to data line if increment enabled
        if self.increment != 0:
            data = np.insert(data, 0, self.position)
            self.position += self.increment

        # write newline into csv file
        try:
            with open(self.filename, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(data.tolist())
        except Exception as e:
            print(f"An error occurred: {e}")
