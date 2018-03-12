from ophyd import EpicsSignal, Device
from ophyd import Component as Cpt


class FourPVShutter(Device):
    def __init__(self, open=None, open_status=None,
                 close=None, close_status=None):
       super(Shutter, self).__init__()
       signals = [EpicsSignal(open_status, write_pv=open, alias='_open'),
                  EpicsSignal(close_status, write_pv=close, alias='_close'),
                  ]

       for sig in signals:
           self.add_signal(sig)

    def open(self):
        self._open.value = 1

    def close(self):
        self._close.value = 1


class FourPVShutter(Device):
    open_command = Cpt(EpicsSignal, 'Cmd:Opn-Cmd')
    open_status = Cpt(EpicsSignal, 'Cmd:Opn-Sts')
    close_command = Cpt(EpicsSignal, 'Cmd:Cls-Cmd')
    close_status = Cpt(EpicsSignal, 'Cmd:Cls-Sts')

    def open(self):
        self.open_command.put(1)

    def close(self):
        self.close_command.put(1)

    @property
    def is_open(self):
        self._check_sanity()
        return self.open_status.get()

    def _check_sanity(self):
        consistency = self.open_status.get() ^ self.close_status.get()
        assert consistency, "Shutter status is not self-consistent"

fe_sh = FourPVShutter('XF:11ID-PPS{Sh:FE}', name='fe_sh')
foe_sh = FourPVShutter('XF:11IDA-PPS{PSh}', name='foe_sh')

class TwoPVShutter(EpicsSignal):
    "TODO: Make me a Device."
    def open(self):
        self.put(1)
    
    def close(self):
        self.put(0)

fast_sh = TwoPVShutter('XF:11IDB-ES{Zebra}:OUT1_TTL:STA',
                       write_pv='XF:11IDB-ES{Zebra}:SOFT_IN:B0',
                       name='fast_sh')


