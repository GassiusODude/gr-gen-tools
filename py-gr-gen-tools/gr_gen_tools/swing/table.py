"""
Generic table block.  This takes two strings to describe the
column names and data type in comma separated variable format.

Example:
=======
column_names = ["Name", "Age", "Salary", "Employed"]
column_types = ["str", "int", "float", "bool"]
"""
import pmt
import numpy as np
import warnings
from gnuradio import gr
import jnius
TableUI = jnius.autoclass("net.kcundercover.jdsp.swing.TableFrame")
class Table(gr.sync_block):

    def __init__(self, table_name="Table", column_names="", column_types="", ):
        """
        Constructor

        Parameters
        ----------
        table_name : str
            The name of the table displayed

        column_names : str
            The name of the columns in comma separated format

        column_types : str
            The types for the columns from ({str, int, bool, double, float})
        """
        gr.sync_block.__init__(self, name='Table', in_sig=[], out_sig = [])

        # --------------------------- error checking ---------------------------

        # --------------------------- set parameters ---------------------------
        self.table_name = table_name
        self.column_names = str(column_names)
        self.column_types = str(column_types)

        self.table = TableUI(self.table_name)

        # ----------------------- set internal variables -----------------------
        self._setup_internal_variables()
        self.message_port_register_in(pmt.intern("in"))
        self.set_msg_handler(pmt.intern("in"), self.msg_handler)

    def msg_handler(self, msg):
        """
        Message handler
        """
        try:
            # NOTE: some error in passing strings through jnius to Java
            #       swapping to pass list of string instead
            #self.table.addRow(str(msg) ,",")
            self.table.addRows([str(msg)], [","])

        except Exception as e:
            print("Exception caught %s"%str(e))

    def _setup_internal_variables(self, ):
        """
        Overload me to setup internal variables that are dependent on the input
        parameters.
        """
        # get list of column names and types
        my_list = self.column_names.split(",")
        my_type = self.column_types.split(",")

        if len(my_list) == len(my_type):
            # matches, provide types
            self.table.setDataFormat(my_list, my_type)
        else:
            # does not match, assume string type
            self.table.setDataFormat(my_list)

    def set_column_names(self, column_names="", ):
        """
        Set method for column_names
        """
        # --------------------------- error checking ---------------------------

        # ---------------------------- set property ----------------------------
        self.column_names = str(column_names)

        # ---------------------- setup internal variables ----------------------
        self._setup_internal_variables()

    def set_column_types(self, column_types="", ):
        """
        Set method for column_types
        """
        # --------------------------- error checking ---------------------------

        # ---------------------------- set property ----------------------------
        self.column_types = str(column_types)

        # ---------------------- setup internal variables ----------------------
        self._setup_internal_variables()


    def set_table_name(self, name):
        """
        Set method for table_name
        """
        self.table_name = name
        self.table.setTitle(self.table_name)

    def get_table_name(self):
        """
        Get table name
        """
        return self.table_name

    def get_column_names(self,):
        """
        Get method for column_names
        """
        return self.column_names


    def get_column_types(self):
        """
        Get method for column_types
        """
        return self.column_types


    def work(self, input_items, output_items, ):
        """
        main work function
        """
        # consume everything
        return 0
