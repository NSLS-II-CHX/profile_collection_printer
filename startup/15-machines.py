from ophyd import PVPositionerPC, EpicsSignal, EpicsSignalRO
from ophyd import Component as Cpt

# Undulator

class Undulator(PVPositionerPC):
    readback = Cpt(EpicsSignalRO, '-LEnc}Gap')
    setpoint = Cpt(EpicsSignal, '-Mtr:2}Inp:Pos')
    actuate = Cpt(EpicsSignal, '-Mtr:2}Sw:Go')
    actuate_value = 1
    stop_signal = Cpt(EpicsSignal, '-Mtr:2}Pos.STOP')
    stop_value = 1

ivu_gap = Undulator('SR:C11-ID:G1{IVU20:1', name='ivu_gap')
# ivu_gap.readback = 'ivu_gap'   ####what the ^*(*()**)(* !!!!
#To solve the "KeyError Problem" when doing dscan and trying to save to a spec file, Y.G., 20170110
ivu_gap.readback.name = 'ivu_gap' 

# This class is defined in 10-optics.py
fe = VirtualMotorCenterAndGap('FE:C11A-OP{Slt:12', name='fe') # Front End Slits (Primary Slits)
