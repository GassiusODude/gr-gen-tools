#!/usr/bin/python
"""
Throughput measurement block
"""
from gnuradio import gr
import time
import numpy as np
from gr_gen_tools.utils.representation import engineering_notation


byte = np.byte
short = np.short


class Throughput(gr.sync_block):

    def __init__(self, name, period, dtype=np.complex64):
        """
        Constructor for the throughput component

        Parameter
        ---------
        name : str
            Name of the stream being measured

        period : float
            Period of time to print and gather measurement (in seconds)

        dtype :  type
            The data format of the input
        """
        # --------------------------- error checking ------------------------
        if type(name) is not str:
            raise TypeError('name should be of type' + str(str))
        if period < 0:
            raise ValueError('period should be greater than  0')

        # -----------------------  call the synb block  ---------------------
        gr.sync_block.__init__(
            self,
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
        # --------------------------- error checking ------------------------
        if type(name) is not str:
            raise TypeError('name should be of type' + str(str))

        # ---------------------------- set property -------------------------
        self.stream_name = name

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
        if period < 0:
            raise ValueError('period should be greater than  0')

        # ---------------------------- set property -------------------------
        self.period = period

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
            print(
                "Throughput (%s) = %s elements/second" %
                (self.stream_name, engineering_notation(avg_thru)))

            # update data and last time
            self.num_data = 0
            self.last_time = toc
        return num_in
