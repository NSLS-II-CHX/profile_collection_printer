from ophyd import (EpicsMotor, PVPositioner, Device, EpicsSignal,
                   EpicsSignalRO,PVPositionerPC)
from ophyd import (Component as Cpt, FormattedComponent,
                   DynamicDeviceComponent as DDC)

#gap
#und_gap = 'SR:C11-ID:G1{IVU20:1-Mtr:2}'  #SR:C11-ID:G1{IVU20:1-Mtr:2}Inp:Pos ??




class MotorCenterAndGap(Device):
    "Center and gap using Epics Motor records"
    xc = Cpt(EpicsMotor, '-Ax:XCtr}Mtr')
    yc = Cpt(EpicsMotor, '-Ax:YCtr}Mtr')
    xg = Cpt(EpicsMotor, '-Ax:XGap}Mtr')
    yg = Cpt(EpicsMotor, '-Ax:YGap}Mtr')

    @property
    def hints(self):
        fields = []
        for name in self.component_names:
            motor = getattr(self, name)
            fields.extend(motor.hints['fields'])
        return {'fields': fields}


class VirtualGap(PVPositioner):
    readback = Cpt(EpicsSignalRO, 't2.C')
    setpoint = Cpt(EpicsSignal, 'size')
    done = Cpt(EpicsSignalRO, 'DMOV')
    done_value = 1


class VirtualCenter(PVPositioner):
    readback = Cpt(EpicsSignalRO, 't2.D')
    setpoint = Cpt(EpicsSignal, 'center')
    done = Cpt(EpicsSignalRO, 'DMOV')
    done_value = 1


class VirtualMotorCenterAndGap(Device):
    "Center and gap with virtual motors"
    xc = Cpt(VirtualCenter, '-Ax:X}')
    yc = Cpt(VirtualCenter, '-Ax:Y}')
    xg = Cpt(VirtualGap, '-Ax:X}')
    yg = Cpt(VirtualGap, '-Ax:Y}')


class Blades(Device):
    top = Cpt(EpicsMotor, '-Ax:T}Mtr')
    bottom = Cpt(EpicsMotor, '-Ax:B}Mtr')
    outboard = Cpt(EpicsMotor, '-Ax:O}Mtr')
    inboard = Cpt(EpicsMotor, '-Ax:I}Mtr')


class MotorSlits(Blades, MotorCenterAndGap):
    "combine t b i o and xc yc xg yg"
    pass

class VirtualMotorSlits(Blades, VirtualMotorCenterAndGap):
    "combine t b i o and xc yc xg yg"
#    def __init__(self, *args, **kwargs):
#      super().__init__(*args, **kwargs)
#        self.xc.readback.name = self.name
#        self.yc.readback.name = self.name
 #       self.xg.readback.name = self.name
    pass


class XYMotor(Device):
    x = Cpt(EpicsMotor, '-Ax:X}Mtr')
    y = Cpt(EpicsMotor, '-Ax:Y}Mtr')


class XYThetaMotor(XYMotor):
    "used for GI mirror"
    th = Cpt(EpicsMotor, '-Ax:Th}Mtr')


class HorizontalDiffractionMirror(XYMotor):
    "x and y with pitch, which has different read and write PVs"
    #p = FormattedComponent(EpicsSignal, read_pv='{self.prefix}-Ax:P}}E-I', write_pv='{self.prefix}-Ax:P}}E-SP', add_prefix=('read_pv', 'write_pv', 'suffix'))
    p = FormattedComponent(EpicsSignal, read_pv='{self.prefix}-Ax:P}}Pos-I', write_pv='{self.prefix}-Ax:P}}PID-SP', add_prefix=('read_pv', 'write_pv', 'suffix'))
    # for some reason we cannot scan on E-SP. This is the actual piezo voltage (max 100) while our 'usual values' are converted to urad by some other laye rof logic in the ioc
    # the currrent SP is the input of the PID feedback loop. This requitred the feedback loop to be turned ON

class DCM(Device):
    en = Cpt(EpicsMotor, '-Ax:Energy}Mtr')
    b = Cpt(EpicsMotor, '-Ax:B}Mtr')
    r = Cpt(EpicsMotor, '-Ax:R}Mtr')
    x = Cpt(EpicsMotor, '-Ax:X}Mtr')
    fp = Cpt(EpicsMotor, '-Ax:FP}Mtr')
    p = Cpt(EpicsMotor, '-Ax:P}Mtr')

 

class SAXSBeamStop( Device):
    x = Cpt(     EpicsMotor, '-Ax:X}Mtr' )
    y1 = Cpt(     EpicsMotor, '-Ax:YFT}Mtr')
    x2 = Cpt(     EpicsMotor, '-Ax:XFB}Mtr')
    y2 = Cpt(     EpicsMotor, '-Ax:YFB}Mtr')
  
    @property
    def hints(self):
        fields = []
        for name in self.component_names:
            motor = getattr(self, name)
            fields.extend(motor.hints['fields'])
        return {'fields': fields}
 

class DMM(Device):
    # en = Cpt(EpicsMotor, '-Ax:Energy}Mtr')
    b = Cpt(EpicsMotor, '-Ax:B}Mtr')
    r = Cpt(EpicsMotor, '-Ax:R}Mtr')
    x = Cpt(EpicsMotor, '-Ax:X}Mtr')
    y = Cpt(EpicsMotor, '-Ax:Y}Mtr')
    fp = Cpt(EpicsMotor, '-Ax:FP}Mtr')


class Transfocator(Device):
    crl = DDC({'num%d' % i: (EpicsMotor, '%d-Ax:X}Mtr' % i, {})
               for i in range(1, 9)})
    x = Cpt(EpicsMotor, 'Ves-Ax:X}Mtr')
    y = Cpt(EpicsMotor, 'Ves-Ax:Y}Mtr')
    z = Cpt(EpicsMotor, 'Ves-Ax:Z}Mtr')
    ph = Cpt(EpicsMotor, 'Ves-Ax:Ph}Mtr')
    th = Cpt(EpicsMotor, 'Ves-Ax:Th}Mtr')


class Kinoform(Device):
    z = Cpt(EpicsMotor, '-Ax:ZB}Mtr')
    x = Cpt(EpicsMotor, '-Ax:XB}Mtr')
    y = Cpt(EpicsMotor, '-Ax:YB}Mtr')
    chi = Cpt(EpicsMotor, '-Ax:Ch}Mtr')
    theta = Cpt(EpicsMotor, '-Ax:Th}Mtr')
    phi = Cpt(EpicsMotor, '-Ax:Ph}Mtr')
    lx = Cpt(EpicsMotor, '-Ax:XT}Mtr')
    ly = Cpt(EpicsMotor, '-Ax:YT}Mtr')

class SmarPod_x(PVPositionerPC):
    readback = Cpt(EpicsSignalRO, '-Ax:1}Pos-I')
    setpoint = Cpt(EpicsSignal, '-Ax:1}Pos-SP')
    actuate = Cpt(EpicsSignal, '}Move-Cmd')
    actuate_value = 1
smp_x = SmarPod_x('XF:11IDB-ES{SPod:1',name='smp_x')
smp_x.readback.name = 'smp_x'

class SmarPod_y(PVPositionerPC):
    readback = Cpt(EpicsSignalRO, '-Ax:3}Pos-I')
    setpoint = Cpt(EpicsSignal, '-Ax:3}Pos-SP')
    actuate = Cpt(EpicsSignal, '}Move-Cmd')
    actuate_value = 1
smp_y = SmarPod_y('XF:11IDB-ES{SPod:1',name='smp_y')
smp_y.readback.name = 'smp_y'    

class SmarPod_z(PVPositionerPC):
    readback = Cpt(EpicsSignalRO, '-Ax:2}Pos-I')
    setpoint = Cpt(EpicsSignal, '-Ax:2}Pos-SP')
    actuate = Cpt(EpicsSignal, '}Move-Cmd')
    actuate_value = 1
smp_z = SmarPod_z('XF:11IDB-ES{SPod:1',name='smp_z')
smp_z.readback.name = 'smp_z'    

class SmarPod_rx(PVPositionerPC):
    readback = Cpt(EpicsSignalRO, '-Ax:1}Rot-I')
    setpoint = Cpt(EpicsSignal, '-Ax:1}Rot-SP')
    actuate = Cpt(EpicsSignal, '}Move-Cmd')
    actuate_value = 1
smp_rx = SmarPod_rx('XF:11IDB-ES{SPod:1',name='smp_rx')
smp_rx.readback.name = 'smp_rx'

class SmarPod_ry(PVPositionerPC):
    readback = Cpt(EpicsSignalRO, '-Ax:3}Rot-I')
    setpoint = Cpt(EpicsSignal, '-Ax:3}Rot-SP')
    actuate = Cpt(EpicsSignal, '}Move-Cmd')
    actuate_value = 1
smp_ry = SmarPod_ry('XF:11IDB-ES{SPod:1',name='smp_ry')
smp_ry.readback.name = 'smp_ry'

class SmarPod_rz(PVPositionerPC):
    readback = Cpt(EpicsSignalRO, '-Ax:2}Rot-I')
    setpoint = Cpt(EpicsSignal, '-Ax:2}Rot-SP')
    actuate = Cpt(EpicsSignal, '}Move-Cmd')
    actuate_value = 1
smp_rz = SmarPod_rz('XF:11IDB-ES{SPod:1',name='smp_rz')
smp_rz.readback.name = 'smp_rz'

class Diffractometer(Device):
    
    Del= Cpt( EpicsMotor, '-Ax:Del}Mtr')
    gam = Cpt(EpicsMotor, '-Ax:Gam}Mtr')
    om = Cpt(EpicsMotor, '-Ax:Om}Mtr')
    phi = Cpt(EpicsMotor, '-Ax:Ph}Mtr')
    xb = Cpt(EpicsMotor, '-Ax:XB}Mtr')
    yb = Cpt(EpicsMotor, '-Ax:YB}Mtr')
    chh = Cpt(EpicsMotor, '-Ax:ChH}Mtr')
    thh = Cpt(EpicsMotor, '-Ax:ThH}Mtr')
    phh = Cpt(EpicsMotor, '-Ax:PhH}Mtr')
    xh = Cpt(EpicsMotor, '-Ax:XH}Mtr')
    yh = Cpt(EpicsMotor, '-Ax:YH2}Mtr')
    zh = Cpt(EpicsMotor, '-Ax:ZH}Mtr')
    chv = Cpt(EpicsMotor, '-Ax:ChV}Mtr')
    thv = Cpt(EpicsMotor, '-Ax:ThV}Mtr')
    xv = Cpt(EpicsMotor, '-Ax:XV}Mtr')
    yv = Cpt(EpicsMotor, '-Ax:YV}Mtr')
    zv = Cpt(EpicsMotor, '-Ax:ZV}Mtr')
    xv2 = Cpt(EpicsMotor, '-Ax:XV2}Mtr')

    @property
    def hints(self):
        fields = []
        for name in self.component_names:
            motor = getattr(self, name)
            fields.extend(motor.hints['fields'])
        return {'fields': fields}



class XBPM( Device):
   vt = Cpt( EpicsSignal, 'CtrlDAC:BLevel-SP' )
xBPM =XBPM( 'XF:11IDB-BI{XBPM:02}', name = 'xBPM' )

diff = Diffractometer('XF:11IDB-ES{Dif', name='diff')

# sample beamstop
#sambst = XYMotor('XF:11IDB-OP{BS:Samp', name='sambst')

s1 = MotorCenterAndGap('XF:11IDB-OP{Slt:1', name='s1')
k1 = Kinoform('XF:11IDB-OP{Lens:1', name='k1')  # upstream
k2 = Kinoform('XF:11IDB-OP{Lens:2', name='k2')  # downstream
gi = XYThetaMotor('XF:11IDB-OP{Mir:GI', name='gi')  # GI-mirror
s2 = MotorCenterAndGap('XF:11IDB-OP{Slt:2', name='s2') #Beam-defining (large JJ) slits
pbs = MotorSlits('XF:11IDA-OP{Slt:PB', name='pbs')  # pink beam slits
flt_y = EpicsMotor('XF:11IDA-OP{Flt:1-Ax:Y}Mtr', name='flt_y')  # filters
dcm = DCM('XF:11IDA-OP{Mono:DCM', name='dcm') #, check position, e.g., by dcm.b.user_readback.value
dmm = DMM('XF:11IDA-OP{Mono:DMM', name='dmm')
mbs = VirtualMotorSlits('XF:11IDA-OP{Slt:MB', name='mbs')  # Mono-beam Slits, check position, e.g., by mbs.xc.readback.value
tran= Transfocator('XF:11IDA-OP{Lens:', name='tran')    # Transfocator
s4 = MotorCenterAndGap('XF:11IDB-ES{Slt:4', name='s4')  # temp guard slits
fsh_x=EpicsMotor('XF:11IDB-OP{FS:1-Ax:X}Mtr', name='fsh_x')  # fast shutter positioner: X
fsh_y=EpicsMotor('XF:11IDB-OP{FS:1-Ax:Y}Mtr', name='fsh_y')  # fast shutter positioner: Y
#smp =SmarPod('XF:11IDB-ES{SPod:1-',name='smp')    # SmarPod
saxs_detector = XYMotor('XF:11IDB-ES{Det:SAXS', name='saxs_detector')  # SAXS detector motion

# Diagnostic Manipulators
foil_y = EpicsMotor('XF:11IDA-BI{Foil:Bpm-Ax:Y}Mtr', name='foil_y')

# foil_x for DBPM (note foil_y is for a different device, perhaps we should rename ...)
foil_x = EpicsMotor('XF:11IDB-OP{Mon:Foil-Ax:X}Mtr', name='foil_x')

#Sample chamber smaract linear stages
# Note crazy names only for Julien!!!
#amp = XYMotor('XF:11IDB-OP{BS:Sam', name='amp')

class amp_motor(Device):
    #x = EpicsMotor('XF:11IDB-OP{BS:Sam-Ax:X}Mtr')
    ampx = EpicsSignal('XF:11IDB-OP{BS:Samp-Ax:X}Mtr.VAL', name='ampx')
    ampy = EpicsSignal('XF:11IDB-OP{Stg:Samp-Ax:Phi}Mtr.VAL', name='ampy')
    ampz = EpicsSignal('XF:11IDB-OP{BS:Samp-Ax:Y}Mtr.VAL', name='ampz')
    #caput('XF:11IDB-ES{Det:Eig4M}cam1:NumImages',  fnum )

# SAXS table: WAXS section rotation
SAXS_x1 = EpicsMotor('XF:11IDB-ES{Tbl:SAXS-Ax:X1}Mtr',name='SAXS_x1')
SAXS_x2 = EpicsMotor('XF:11IDB-ES{Tbl:SAXS-Ax:X2}Mtr',name='SAXS_x2')


# Note inconsistency in capitalization of Bpm/BPM below.
bpm1 = XYMotor('XF:11IDA-BI{Bpm:1', name='bpm1')
bpm2 = XYMotor('XF:11IDB-BI{BPM:2', name='bpm2')

w1 = XYMotor('XF:11IDB-OP{Win:1', name='w1')  # window positioners
hdm = HorizontalDiffractionMirror('XF:11IDA-OP{Mir:HDM', name='hdm')
gsl = VirtualMotorCenterAndGap('XF:11IDB-OP{Slt:Guard', name='gsl')  #Guard rSlits (SmarAct)
#gsl = VirtualMotorSlits('XF:11IDB-OP{Slt:Guard', name='gsl')  #Guard rSlits (SmarAct)



#SAXS beam stop
saxs_bst = SAXSBeamStop( 'XF:11IDB-ES{BS:SAXS', name = 'saxs_bst' )
 
#To solve the "KeyError Problem" when doing dscan and trying to save to a spec file, Y.G., 20170110
gsl.xc.readback.name = 'gsl_xc'
gsl.yc.readback.name = 'gsl_yc'
gsl.xg.readback.name = 'gsl_xg'
gsl.yg.readback.name = 'gsl_yg'

mbs.xc.readback.name = 'mbs_xc'
mbs.yc.readback.name = 'mbs_yc'
mbs.xg.readback.name = 'mbs_xg'
mbs.yg.readback.name = 'mbs_yg'

fe = VirtualMotorCenterAndGap('FE:C11A-OP{Slt:12', name='fe') # Front End Slits (Primary Slits)

fe.xc.readback.name = 'fe_xc'
fe.yc.readback.name = 'fe_yc'
fe.xg.readback.name = 'fe_xg'
fe.yg.readback.name = 'fe_yg'





