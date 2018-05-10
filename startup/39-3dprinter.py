class Printer3D(Device):
    Z = Cpt(EpicsMotor,"Mtr")
    X_platform = Cpt(EpicsMotor,"-ax2Mtr")
    Y = Cpt(EpicsMotor,"-ax3Mtr")
    X_printhead1 = Cpt(EpicsMotor,"-ax4Mtr")
    B = Cpt(EpicsMotor,"-ax5Mtr")

printer3d = Printer3D("alexHost:smaract2", name="printer3d")

class StandardProsilicaWithTIFFtmp(StandardProsilica):
    tiff = Cpt(TIFFPluginWithFileStore,
               suffix='TIFF1:',
               write_path_template='/tmp/%Y/%m/%d/',
               root='/tmp',
               reg=db.reg)
xray_eye_printer = StandardProsilicaWithTIFFtmp("XF:MOBILE-BI{Mir:1}",
                         name="xray_eye_printer")
