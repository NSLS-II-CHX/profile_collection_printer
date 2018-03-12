from pyOlog.ophyd_tools import *

# Uncomment the following lines to turn on verbose messages for
# debugging.
# import logging
# ophyd.logger.setLevel(logging.DEBUG)
# logging.basicConfig(level=logging.DEBUG)

# Add a callback that prints scan IDs at the start of each scan.
def print_scan_ids(name, start_doc):
    print("Transient Scan ID: {0} @ {1}".format(start_doc['scan_id'],time.strftime("%Y/%m/%d %H:%M:%S")))
    print("Persistent Unique Scan ID: '{0}'".format(start_doc['uid']))

RE.subscribe(print_scan_ids, 'start')


from chxtools import attfuncs as att
from chxtools import attfuncs2 as att2
from chxtools import xfuncs as xf
from chxtools.bpm_stability import bpm_read
from chxtools import transfuncs as trans  
from chxtools import bpm_stability as bpmst

