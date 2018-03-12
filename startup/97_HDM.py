

CHA_Vol_PV = 'XF:11IDB-BI{XBPM:02}CtrlDAC:ALevel-SP'
HDM_Encoder_PV  = 'XF:11IDA-OP{Mir:HDM-Ax:P}Pos-I' 


E=np.arange(9.,11.,.05)
SI_STRIPE = -9
RH_STRIPE = 9

def take_Rdata( voltage, E):
    caput(CHA_Vol_PV, voltage)    
    #yield from bp.abs_set(hdm.y, RH_STRIPE)
    hdm.y.user_setpoint.value = RH_STRIPE
    sleep( 3.0 )
    E_scan(list(E))
    hrh=db[-1]
    #yield from bp.abs_set(hdm.y, Si_STRIPE)
    hdm.y.user_setpoint.value = SI_STRIPE
    sleep( 3.0 )
    E_scan(list(E))
    hsi=db[-1]
    return get_R( hsi, hrh )

def get_R(header_si, header_rh):		
    datsi=get_table(header_si)		
    datrh=get_table(header_rh)		
    th_B=-datsi.dcm_b		
    En=xf.get_EBragg('Si111cryo',th_B)		
    Rsi=datsi.elm_sum_all		
    Rrh=datrh.elm_sum_all		
    plt.close(99)		
    plt.figure(99)		
    plt.semilogy(En,Rsi/Rrh,'ro-')		
    plt.xlabel('E [keV]');plt.ylabel('R_si / R_rh')		
    plt.grid()		
    return Rsi/Rrh


voltage_CHA = [ 3.5, 4.0, 4.5, 5.0, 5.5]
voltage_CHA = [ 3.0,3.2,3.4,3.6,3.8,4.0,4.2,4.4,4.6,4.8,5.0,5.2,5.4]

r_eng=np.array(np.loadtxt("/home/xf11id/Downloads/R_Rh_0p180.txt"))[:,0]/1e3
rsi_0p18=np.array(np.loadtxt("/home/xf11id/Downloads/R_Si_0p180.txt"))[:,1]
rrh_0p18=np.array(np.loadtxt("/home/xf11id/Downloads/R_Rh_0p180.txt"))[:,1]

def get_Rdata( voltage_CHA, E ):
    R = np.zeros(len(voltage_CHA), len(E)) 
    fig, ax = plt.subplots()
    ax.plot(r_eng,rsi_0p18/rrh_0p18,label="calc 0.18 deg")
    ax.set_xlabel("E [keV]")
    ax.set_ylabel("R_Si/R_Rh")
    i = 0
    for voltage in voltage_CHA:
        R_SiRh =  take_Rdata( voltage, E)
        R[i]=R_SiRh
        HDM_Encoder = caget ( HDM_Encoder_PV )
        ax.plot(E,R_SiRh/R_SiRh[1:5].mean(),label="%s V, %s urad"%(voltage,HDM_Encoder) )
    ax.legend()
    return R



