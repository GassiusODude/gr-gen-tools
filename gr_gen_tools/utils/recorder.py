"""
Recorder
========
This component acts as a user controlled recorder.
Connect a QT/Wx item to the enable toggling the recorder on or off.
"""
import numpy as np
import os
import warnings
from gnuradio import gr
from gr_gen_tools.utils.representation import gen_filename
class Recorder(gr.sync_block):

    def __init__(self, radio_frequency=100e6, sample_rate=0,\
            max_duration_seconds=600, enable=True, output_dir="/tmp",\
            dtype=np.complex64 ):
        """
        Constructor
        """
        gr.sync_block.__init__(self,
            name='Recorder',
            in_sig = [dtype, ],
            out_sig = [],
            )
        # --------------------------- error checking ---------------------------

        # --------------------------- set parameters ---------------------------
        self.radio_frequency = np.float32(radio_frequency)
        self.sample_rate = np.float32(sample_rate)
        self.max_duration_seconds = np.float32(max_duration_seconds)
        self.enable = bool(enable)
        
        self.output_dir = str(output_dir)
        if output_dir:
            if output_dir[-1] != "/":
                self.output_dir += "/"
            

        if not os.path.isdir(self.output_dir):
            os.makedirs(self.output_dir)
        self.dtype = dtype

        # initialize internal properties
        self._filename = None
        self._buffer = []
        self._buffer_ind = 0

        # ----------------------- set internal variables -----------------------
        self._setup_internal_variables()


    def _setup_internal_variables(self, ):
        """
        Overload me to setup internal variables that are dependent on the input
        parameters.
        """
        # ----------------  calculate dependent variables  ------------------
        new_buffer_len = int(self.max_duration_seconds * self.sample_rate)
        new_file = self.output_dir + gen_filename("", self.dtype, 
            fc=self.radio_frequency, fs=self.sample_rate)
        modified = (new_buffer_len != len(self._buffer)) or \
            (new_file != self._filename)
        
        # ---------------------  saved buffered signal  ---------------------
        if modified:
            self._save_buffered_signal()

        # ---------------------  update variables  --------------------------
        # update to new filename
        self._filename = new_file

        # if modified, reallocate buffer size
        if new_buffer_len != len(self._buffer):
            self._buffer = np.zeros(new_buffer_len, dtype=self.dtype)
        self._buffer_ind = 0

    def _save_buffered_signal(self):
        """
        Save the currently buffered signal.
        """
        if self.enable and self._filename and self._buffer_ind > 0:
            # -------------------------  save output  -----------------------
            self._buffer[:self._buffer_ind].astype(self.dtype)\
                .tofile(self._filename)
        
        # --------------------------  reset  --------------------------------
        self._buffer_ind = 0

    def set_radio_frequency(self, radio_frequency=100e6, ):
        """
        Set method for radio_frequency
        """
        # ---------------------------- set property -------------------------
        self.radio_frequency = np.float32(radio_frequency)

        # ---------------------- setup internal variables -------------------
        self._setup_internal_variables()
    

    def set_sample_rate(self, sample_rate=0, ):
        """
        Set method for sample_rate
        """
        # -------------------------- set property ---------------------------
        self.sample_rate = np.float32(sample_rate)

        # ---------------------- setup internal variables ----------------------
        self._setup_internal_variables()
    

    def set_max_duration_seconds(self, max_duration_seconds=600, ):
        """
        Set method for max_duration_seconds
        """
        # ---------------------------- set property ----------------------------
        self.max_duration_seconds = np.float32(max_duration_seconds)

        # ---------------------- setup internal variables ----------------------
        self._setup_internal_variables()
    

    def set_enable(self, enable=True, ):
        """
        Set method for enable
        """
        # --------------------------- error checking ---------------------------
        if self.enable and not enable:
            # previously on and turning off.
            self._save_buffered_signal()

        # ---------------------------- set property ----------------------------
        self.enable = bool(enable)

        # ---------------------- setup internal variables ----------------------
        self._setup_internal_variables()
    

    def set_output_dir(self, output_dir="/tmp", ):
        """
        Set method for output_dir
        """
        # --------------------------- error checking ---------------------------

        # ---------------------------- set property ----------------------------
        self.output_dir = str(output_dir)
        if output_dir:
            if output_dir[-1] != "/":
                self.output_dir += "/"
            
        if not os.path.isdir(self.output_dir):
            os.makedirs(self.output_dir)

        # ---------------------- setup internal variables ----------------------
        self._setup_internal_variables()
    

    def get_radio_frequency(self, radio_frequency=100e6, ):
        """
        Get method for radio_frequency
        """
        return self.radio_frequency
    

    def get_sample_rate(self, sample_rate=0, ):
        """
        Get method for sample_rate
        """
        return self.sample_rate
    

    def get_max_duration_seconds(self, max_duration_seconds=600, ):
        """
        Get method for max_duration_seconds
        """
        return self.max_duration_seconds
    

    def get_enable(self, enable=True, ):
        """
        Get method for enable
        """
        return self.enable
    

    def get_output_dir(self, output_dir="/tmp", ):
        """
        Get method for output_dir
        """
        return self.output_dir
    

    def work(self, input_items, output_items, ):
        """
        main work function
        """
        num_in = len(input_items[0])
        
        if len(self._buffer) > 0:
            diff_1 = len(self._buffer) - self._buffer_ind
            if diff_1 > num_in:
                # -----------------------  buffer  --------------------------
                self._buffer[self._buffer_ind :\
                     self._buffer_ind + num_in]
                self._buffer_ind += num_in
            else:
                # ------------------------  max reached  --------------------
                self._buffer[self._buffer_ind : self._buffer_ind + diff_1]
                self._buffer_ind = len(self._buffer)
                self._save_buffered_signal
                
                # turn off record until user triggers
                self.enable = False


        return num_in
