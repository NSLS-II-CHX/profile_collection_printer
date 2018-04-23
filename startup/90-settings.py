import logging

# metadata set at startup
RE.md['owner'] = 'xf11id'
RE.md['beamline_id'] = 'CHX'
# removing 'custom' as it is raising an exception in 0.3.2
# gs.RE.md['custom'] = {}

def print_md(name, doc):
    if name == 'start':
        print('Metadata:\n', repr(doc))

from pprint import pprint
import builtins

def verify_md(md):
    pprint(RE.md)
    response = builtins.input("Is this metadata correct (y/n)?")
    if response != 'y':
        raise Exception("Killed by user")

RE.md_validator = lambda x: x # the default
# RE.md_validator = verify_md

# RE.subscribe(print_md)

#from eiger_io.fs_handler import LazyEigerHandler
#db.fs.register_handler("AD_EIGER", LazyEigerHandler)

temp_C = EpicsSignal('XF:11IDB-ES{Env:01-Chan:C}T:C-I', name='temp_C')
sd.baseline = [diff, s1, s2, s4, saxs_bst, temp_C, foil_x]
#sd.monitors = []

#bec.disable_baseline()  # Do not show baseline.
