class Printer3D(Device):
    Z = Cpt(EpicsMotor,"Mtr")
    X_platform = Cpt(EpicsMotor,"-ax2Mtr")
    Y = Cpt(EpicsMotor,"-ax3Mtr")
    X_printhead1 = Cpt(EpicsMotor,"-ax4Mtr")
    B = Cpt(EpicsMotor,"-ax5Mtr")

printer3d = Printer3D("alexHost:smaract2", name="printer3d")

xray_eye_printer = StandardProsilicaWithTIFF("XF:MOBILE-BI{Mir:1}cam1:NumImages",
                         name="xray_eye_printer")
