#!/usr/bin/python
"""
Throughput measurement block
"""
from gnuradio import gr
import time
import numpy as np
byte = np.byte
short = np.short
from gr_gen_tools.utils.representation import engineering_notation
class Throughput(gr.sync_block):

    def __init__(self, name, period, dtype=float):
        """
        Constructor for the throughput component

        Parameter
        ---------
        name : str
            Name of the stream being measured
        
        period : float
            Period of time to print and gather measurement (in seconds)
        """
        # --------------------------- error checking ------------------------
        if type(name) is not str:
            raise TypeError('name should be of type' + str(str))
        if period <  0:
            raise ValueError('period should be greater than  0')
        """if dtype == complex:
            dtype = np.complex64
        elif dtype == float:
            dtype = np.float32
        elif dtype == np.int16:
            dtype = np.int16
        elif dtype == int:
            dtype = np.int32
        else:
            dtype = np.uint8
        """
        # -----------------------  call the synb block  ---------------------
        gr.sync_block.__init__(self,
            name="Throughput",
            in_sig=[dtype],
            out_sig=None)

        # -----------------------  initialize properties  -------------------
        self.stream_name = name
        self.period = period
        self.last_time = time.time()
        self.num_data = 0

    def set_name(self, name="Default"):
        """
        Set method for name

        Parameter
        ---------
        name : str
            Name of the stream being measured.
        """
        # --------------------------- error checking ---------------------------
        if type(name) is not str:
            raise TypeError('name should be of type' + str(str))

        # ---------------------------- set property ----------------------------
        self.stream_name = name

        # ---------------------- setup internal variables -------------------
        self._setup_internal_variables()
    

    def set_period(self, period=5):
        """
        Set method for period

        Parameter
        ---------
        period : float
            Period of time to print and gather measurement (in seconds)
        """
        # --------------------------- error checking ------------------------
        if type(period) is not float:
            raise TypeError('period should be of type' + str(float))
        if period <  0:
            raise ValueError('period should be greater than  0')

        # ---------------------------- set property -------------------------
        self.period = period

        # ---------------------- setup internal variables -------------------
        self._setup_internal_variables()
    

    def get_name(self):
        """
        Get method for name
        """
        return self.name
    

    def get_period(self):
        """
        Get method for period
        """
        return self.period
    
    
    def work(self, input_items, output_items):
        """
        Work function
        """
        num_in = len(input_items[0])
        self.num_data += num_in
        toc = time.time()
        if toc - self.last_time > self.period:
            # display throughput
            avg_thru = float(self.num_data) / (toc - self.last_time)
            print("Throughput (%s) = %s elements/second"%\
                (self.stream_name, engineering_notation(avg_thru)))

            # update data and last time
            self.num_data = 0
            self.last_time = toc
        return num_in
