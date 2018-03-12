"""
Developed at Jan 31, 2017 for Point Detector Commissioning
"""

count_PV =  'XF:11IDB-BI{IM:1}:C1'
integer_time = 10 #10 seconds
acquisition_period = 0.1 #seconds

HV_enable_PV = 'XF:11IDB-BI{IM:1}:ENBHIV1' 
HV_set_PV = 'XF:11IDB-BI{IM:1}:NEW_HIV1'
HV_set_action_PV = 'XF:11IDB-BI{IM:1}:SETHIVS'
Init_PV =  'XF:11IDB-BI{IM:1}:INIT_DAQ'

low_v_PV = 'XF:11IDB-BI{IM:1}:NEW_LO1'  #-1 e.g.
low_v_set_PV = 'XF:11IDB-BI{IM:1}:SETLOS'

high_v_PV = 'XF:11IDB-BI{IM:1}:NEW_HI1' #-2 e.g.
high_v_set_PV = 'XF:11IDB-BI{IM:1}:SETHIS'

acq_time_pv = 'XF:11IDB-BI{IM:1}:SET_PERIOD'

def set_HV( hv ):
        '''
        Set the applied high voltage
        '''
        caput( HV_enable_PV, 1)
        caput( HV_set_PV , hv )
        caput( HV_set_action_PV, 1)
        if hv ==0:
                caput( HV_enable_PV, 0)



def get_pdet_count( integer_time, acquisition_period  ):
        '''
        get the averaged count during integer_time
        '''
        Nt = int( integer_time/acquisition_period )
        data = 0 
        for i in range( Nt ):
                time.sleep( acquisition_period ) 
                data += caget( count_PV)
        return data/Nt


#def get_current_count( ):
#        '''get the count for the current setup'''
        


def get_count_hv( hv, low_v, high_v, atts=None ):
        '''get count for different attenuation at one applied high voltage
         Example:
                #for LaBr
                data = get_count_hv( -2000, -1.05, -1.45 )
                
        '''
        set_HV(hv)
        if atts is None:
                atts = att_real        
        data = np.zeros( len(atts) )
        caput( low_v_PV, low_v)
        caput( low_v_set_PV, 1)
        caput( high_v_PV, high_v)
        caput( high_v_set_PV, 1)        
        for i, transm in enumerate(atts):                
                att.set_T(transm)
                caput( Init_PV, 1)
                time.sleep( 30 )
                data[i] = get_pdet_count(10, 1) #do 10 seconds average
                print( "The count for %s HV wit attenuation as %s is: %s" %(hv, transm, data[i] ) )
        att.set_T(1)
        return data

def get_count_acqt( hv, low_v, high_v, acq_time):
        '''get count at one hv for different acq_time
                get_count_acqt( -1100, -0.0, -0.15, acq_time)
        '''
        data = np.zeros( len(acq_time))
        for i, t in enumerate(acq_time):
                caput( acq_time_pv, t )
                print('*'*40)
                print( 'The current acquistion time is: %s'%t)
                print('*'*40)
                d= get_count_hv( hv, low_v, high_v, atts= [1] )
                data[i] = d[0]
        return data
        

def get_count_hv_series( hvs, vol_peak, atts=None ):
        '''
        get count for different attenuation at different applied high voltage
        Example:
        #for LaBr
        data = get_count_hv_series( HV_LB  )
        '''
        data = {}
        for i, hv in enumerate( hvs ):
                print( '*'*40)
                print( 'The current applied voltage is: %s'%hv )
                print( '*'*40)
                low_v = max( vol_peak[i] - v_window, 0 )
                high_v = min(vol_peak[i] + v_window, 5 )
                data[hv] = get_count_hv( hv, -low_v, -high_v, atts=atts )
        return data



att_n = np.array(       [1,     .9,     0.7,   0.5,    0.4,    0.3,       0.2,    0.1,  0.05, 0.025, 0.01, 0.005,  0.001    ]                                           )
att_real =  np.array(  [ 1,   0.812,   0.66,  0.54,   0.44,   0.288,      0.19,   0.1,  0.0546, 0.024, 0.01, 0.0045, 0.001       ])

#for LaBr3 detector
HV_LB = -np.linspace( 1100, 2000, 10)
#         array([  1100.,1200.,1300.,1400.,1500.,  1600.,  1700.,  1800.,  1900.,  2000.])
vol_LB = np.array(  [0.04, 0.26, 0.58, 1.12, 1.17, 1.2, 1.21, 1.22, 1.24, 1.25 ]  )
v_window = .2


#for NaI detector, same box with LaBr3, 
#dead time 250 ns
#HV_NI = -np.linspace( 1000,  2000, 11)
HV_NI = -np.linspace( 1100,  2000, 10)
#         array([   1100.,  1200.,  1300.,  1400., 1500.,  1600.,  1700.,  1800.,  1900.,  2000.])
vol_NI = np.array(  [ 0.28,    0.28,  0.27,    0.27,   0.28,   0.28,   0.28 ]  )

v_window = .27
background = 0.6 #for HV = -1600, without beam but with light
#background = np.array( [ 0, 0, 0, 0, 0.1,  0.2, 0.3, 1.8, 2.5, 5.8, 9.8  ] )
background = np.array( [ 0, 0, 0, 0.1,  0.2, 0.3, 1.8, 2.5, 5.8, 9.8  ] )


hv = -2000 
hvs = HV_LB

acq_time = np.array( [ 0.0001, 0.001, 0.01, 0.1, 1 ] )


data_dir ='/XF11ID/analysis/2017_1/commissioning/Results/Point_Detector/'
#np.savetxt( data_dir + 'count_2000V.txt', np.vstack( [att_real, data] ) )
#pickle.dump(data, open(data_dir + 'LaBr_1100_2000.pkl', 'wb') )
#pickle.dump(data, open(data_dir + 'NaI-I_1100_2000.pkl', 'wb') )


#For LaBr, other metadata: Triger Mode: INTermal; Intergration time: 0.1 second;Dwell time 1ms; Deadtime: 20 ns
#plot1D( x = att_real, y = data, c='r', m = 'o', ls='--', legend='LaBr@2000', title='LaBr detector@2000V', xlabel='attenuation', ylabel='count' )        
#plot1D( x = acq_time, y = d, c='r', m = 'o', ls='--', logx=True, logy=True, legend='LaBr@1100', title='LaBr detector~acqtime@1100V',xlabel='acquisition time', ylabel='count', save=True, path= data_dir )        

#plot1D( x = att_real, y = data, c='r', m = 'o', ls='--', legend='%s@1600'%det, title='%s detector@1600V'%det, xlabel='attenuation', ylabel='count' )        



det='LaBr'
det = 'NaI_1'

def save_data( data ):
        keys = sorted(list( data.keys() ))
        for k in keys:
                dk = data[k]
                np.savetxt( data_dir + 'count_'+det+'_%sV.txt'%(-int(k)), np.vstack( [att_real, dk] ) )
        

def plot_data( data,  background= None, all_in_one = False ):
        keys = sorted( list( data.keys() ) )
        if all_in_one:
                fig, ax = plt.subplots()
        for i, k in enumerate(keys):
                dk = data[k]
                if background is not None:
                        print( i, background[i]  )
                        dk = data[k].copy() -  background[i]                        
                if not all_in_one:
                        plot1D( x = att_real, y = dk,c='r', m = 'o', ls='--',  logx=True, logy=True,
                        legend=det+'@%s V'%(int(k)), title=det+' detector@%s V'%(int(k)), xlabel='attenuation', ylabel='count' )
                        
                        plt.savefig(  data_dir + 'count_'+det+'_%sV.png'%(-int(k)) )
                else:
                        plot1D( x = att_real, y = dk, ls='--',  logx=True, logy=True, ax=ax, 
                        legend=det+'@%s V'%(int(k)), title=det+' detector', xlabel='attenuation', ylabel='count' )
                        plt.savefig(  data_dir + 'count_'+ det +'.png' )
                        
                






















        
