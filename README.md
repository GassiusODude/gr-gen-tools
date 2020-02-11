# gr-gen-tools
General GNU Radio Tools

This project will provide a range of tools to help evaluate GNU Radio components.

# Installation

### Setup the Environmental Variables

~~~bash
export PYTHONPATH=$PYTHONPATH:/path/to/gr-gen-tools
export GRC_BLOCKS_PATH=$GRC_BLOCKS_PATH:/path/to/gr-gen-tools/grc_xml
~~~

### Install GRC files
~~~bash
python -B install_grc.py --recursive
~~~

# Measurement
These components provide measurments to help evaluate the performance of various algorithms or statistics of data.

| Measurement | Description |
| :-: | :-: |
| Throughput | Averages the throughput over a given evaluation period |

## Throughput
Evaluate supported maximum throughtput of various components.  This is useful for comparing multiple implementations of similar algorithms.

# Swing
These are Java Swing components used to provide better awareness of the output of various components.

| Swing Tool | Description |
| :-: | :-: |
| Table | Display messages received in the form of a table. |

### Table
This table takes in messages as strings and assumes comma separated values.  The component allows the user/developer to configure the columns of the table and the data types of the columns to configure the display of information.  As messages are received, the table will update (given successful evaluation)