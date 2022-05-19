#!/usr/bin/python
"""
Common Representations
"""
from datetime import datetime
import numpy as np
def engineering_notation(value, n_dec=6):
    """
    Represent a numeric value in engineering notation.

    2400,000,000 Hz = 2.4 GHz
    31,300,000 Hz = 31,3 MHz

    """
    form = "%" + ("1.%df "%n_dec)
    if value >= 1e12:
        # Terra (1e12)
        return (form + "T")%(float(value) / 1e12)
    elif  value >= 1e9:
        # Giga (1e9)
        return (form + "G")%(float(value) / 1e9)
    elif value >= 1e6:
        # Mega (1e6)
        return (form + "M")%(float(value) / 1e6)
    elif value >= 1e3:
        # kilo (1e3)
        return (form + "k")%(float(value) / 1e3)
    else:
        return (form)%(float(value))

def gen_filename(name, dtype=np.float32, fc=None, fs=None, n_dec=4,
        is_complex=False,):
    """
    Generate a filename.

    YYYYMMDD_hour-min-sec_<NAME>_fc_<FC>_Hz_fs_<FS>_sps.ext
    """
    # ---------------  initialize filename with timestamp  ------------------
    curr_time = datetime.now()
    filename = curr_time.strftime("%Y%m%d_%H-%M-%S_")

    # add name
    filename += name

    # -------------------------  add information  ---------------------------
    # add center frequency
    if fc:
        fc_str = engineering_notation(fc, n_dec)
        fc_str = fc_str.replace(" ", "_")
        filename += "_fc_%sHz"%fc_str

    # add sampling rate
    if fs:
        fs_str = engineering_notation(fs, n_dec)
        fs_str = fs_str.replace(" ", "_")
        filename += "_fs_%ssps"%fs_str

    # -----------------------  add file extension  --------------------------
    ext = ""
    mode = "c" if is_complex else ""
    if dtype in [np.float32]:
        # float
        ext = ".32%sf"%mode
    elif dtype in [np.complex64]:
        # complex float (force complex)
        ext = ".32cf"
    elif dtype in [np.int32]:
        # integer
        ext = ".32%si"%mode
    elif dtype in [np.int16]:
        # short
        ext = ".16%ss"%mode
    elif dtype in [np.uint8, np.int8]:
        # 8 bit octet
        ext = ".8o"
    elif dtype in [str]:
        ext = ".txt"
    
    # add file extension
    filename += ext

    return filename
    