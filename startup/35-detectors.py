from ophyd import (Device, Component as Cpt, EpicsSignalRO)


class XBpm(Device):
    x = Cpt(EpicsSignalRO, 'Pos:X-I')
    y = Cpt(EpicsSignalRO, 'Pos:Y-I')
    a = Cpt(EpicsSignalRO, 'Ampl:ACurrAvg-I')
    b = Cpt(EpicsSignalRO, 'Ampl:BCurrAvg-I')
    c = Cpt(EpicsSignalRO, 'Ampl:CCurrAvg-I')
    d = Cpt(EpicsSignalRO, 'Ampl:DCurrAvg-I')
    


class Elm(Device):
	sum_x = Cpt(EpicsSignalRO, 'SumX:MeanValue_RBV')
	sum_y = Cpt(EpicsSignalRO, 'SumY:MeanValue_RBV')
	sum_all = Cpt(EpicsSignalRO, 'SumAll:MeanValue_RBV')
	@property
	def hints(self):
            return {'fields': [self.sum_all.name,
                           ]}



xbpm = XBpm('XF:11IDB-BI{XBPM:02}', name='xbpm')
xbpm.read_attrs = ['x', 'y', 'ca', 'cb', 'cc', 'cd']


elm = Elm('XF:11IDA-BI{AH401B}AH401B:', name='elm')
#elm.read_attrs = ['sum_x', 'sum_y', 'sum_all']






