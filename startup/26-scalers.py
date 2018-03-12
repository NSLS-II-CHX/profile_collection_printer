from ophyd import EpicsScaler

sclr=EpicsScaler('XF:11IDB-ES{Sclr:1}', name="sclr")
sclr.channels.read_attrs = ['chan2']


