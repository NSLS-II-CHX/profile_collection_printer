




def custom_GISAXS():
    # Simple script to move srot back-and-forth while measuring

    #sam=SampleGISAXS(filename)

    mov(sth,0)
    cms.modeAlignment()
    beam.setTransmission(0.001)
    beam.on()
    fit_scan(smy,1,20,fit='sigmoid_r')

    fit_scan(sth,4,20,fit='gauss')
    sam.thsetOrigin()
    fit_scan(smy,.4,20,fit='sigmoid_r')
    cms.modeMeasurement()
    sam.measureIncidentAngle(.1,1)

