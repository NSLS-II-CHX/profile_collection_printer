#a count with metadata writing func


#count_saxs( 'Silica 1 fr x .1 exp, mbs 0.1x0.6, bds 15x15, prekin .1x.08', 1, .1, .1, new_pos=True)
#RE(count_saxs( 'Silica 1 fr x .1 exp, mbs 0.1x0.6, bds 15x15, prekin .1x.08', 1, .1, .1, new_pos=True))
#RE(go_to_sleep())


#RE(count_saxs( 'AuNP_2DSheet',1,.5,None,new_pos=True))


##def multi_scan( num=10):
##    i=0
##    for i in range(num):
##        RE(count_saxs( 'Au1D_Ladder',1,1,None,new_pos=True, bpm_on=False))
##        print (i)
##        i=i+1

#RE = gs.RE  # convenience alias

def shutter_test():
	for i in range(1,56):
		if caget('XF:11IDB-VA{Att:1-CCG:1}P-I')<=1.1E-7:
			print('taking data series with fast shutter...')
			series(shutter_mode='multi',expt=.00134,acqp=.02,imnum=2000,comment='shutter test')
		else:
			print(time.ctime+':  vacuum > 1.1E-7  -> waiting for 15 min...')
			sleep(900)
			if caget('XF:11IDB-VA{Att:1-CCG:1}P-I')<=1.1E-7:
				print('taking data series with fast shutter...')
				series(shutter_mode='multi',expt=.00134,acqp=.02,imnum=2000,comment='shutter test')
			else: raise vac_Exception('something is wrong: vacuum does not recover...')
		print(str(time.ctime)+':  waiting for 15 min...')		
		sleep(900)
		

class vac_Exception(Exception):
	pass

def capillary_bottom_in():
    ''' This function is wrote for Sandro's three samples, Nov 2, 2016'''
    mov(diff.xh,0.45)
    RE.md['sample']='S2_reference_sample'
    RE.md['sample_description']='Au_30nm_in_0.6mole_glycerol aqueous solution'
    mov(diff.yh,0.37)

def capillary_middle_in():
    mov(diff.xh, 0.45)
    RE.md['sample']='g_0.15'
    RE.md['sample_description']='Au_30nm_in_0.15mole_glycerol aqueous solution'
    mov(diff.yh, 5.5)

def capillary_top_in():
    mov(diff.xh, 0.45)
    RE.md['sample']='g_0.1'
    RE.md['sample_description']='Au_30nm_in_0.1mole_glycerol aqueous solution'
    mov(diff.yh, 10.5)


def xpcs_measure(   Measurement ):
        ''' XPCS routine, Nov 3, 2016'''
        T =     caget( 'XF:11IDB-ES{Env:01-Chan:C}T-I')     
        RE.md['Temperature']= T
        print( RE.md )
        take_xpcs_series(  Measurement  + '--T=%s'%T )

def xpcs_measure_not_used(  pos, Measurement ):
    ''' This function is wrote for Sandro's three samples, Nov 2, 2016'''

    T =     caget( 'XF:11IDB-ES{Env:01-Chan:C}T-I')
    if pos=='bottom':
        capillary_bottom_in()
        print('It will measure the bottom cappilary')
    elif pos=='middle':
        capillary_middle_in()
        print('It will measure the middle cappilary')
    elif pos=='top':
        capillary_bottom_in()
        print('It will measure the top cappilary') 
        
    RE.md['Temperature']= T

    take_xpcs_series( 'S2' + '--'+ Measurement  + '--T=%s'%T )




def measure_bottom( T, Measurement ):
    ''' This function is wrote for Sandro's three samples, Nov 2, 2016'''
    capillary_bottom_in()
    RE.md['sample']='S2_reference_sample'
    RE.md['sample_description']='Au_30nm_in_0.6mole_glycerol aqueous solution'
    RE.md['Temperature']= T
    take_xpcs_series( 'S2' + '--'+ Measurement  + '--T=%s'%T )

def measure_middle( T, Measurement ):
    ''' This function is wrote for Sandro's three samples, Nov 2, 2016'''
    capillary_middle_in()
    RE.md['sample']='g_0.15'
    RE.md['sample_description']='Au_30nm_in_0.15mole_glycerol aqueous solution'
    RE.md['Temperature']= T
    take_xpcs_series( RE.md['sample'] + '--'+ Measurement  + '--T=%s'%T )

def measure_top( T, Measurement ):
    ''' This function is wrote for Sandro's three samples, Nov 2, 2016'''
    capillary_top_in()
    RE.md['sample']='g_0.1'
    RE.md['sample_description']='Au_30nm_in_0.1mole_glycerol aqueous solution'
    RE.md['Temperature']= T
    take_xpcs_series( RE.md['sample'] + '--'+ Measurement  + '--T=%s'%T )


def take_xpcs_series( Measurement   ):
    '''
    Oct 24, 2016, for Pierce measurements
    Open fast shutter, stay one second, 
    Switch X/Y BPM feedback
    Take count
    '''
    RE( bp.abs_set( fast_sh, 1 )  )
    sleep(1)
    xbpm_y_pos = 'XF:11IDB-BI{XBPM:02}Fdbk:BEn-SP'
    xbpm_x_pos = 'XF:11IDB-BI{XBPM:02}Fdbk:AEn-SP'
    caput( xbpm_y_pos, 1 ) 
    caput( xbpm_x_pos, 1 )
    RE(count([eiger4m_single]),Measurement= Measurement  )




def count_saxs(type, fnum=1,  expt= 0.1, acqt = None, att_t = 1,
               save=True, new_pos = False, bpm_on=False):
    #RE( count_('alignment', 1, 0.1, 0.1, att_t =  1, save=True, new_pos = False) )
    #RE( count_( 'XPCS_200C_1000 frames_1s', 1000, 1, 1 , att_t =  1, save=True, new_pos = False) )

    if acqt is None:
        acqt=expt
        
    type=type+ ' %d fr X %s exp'%(fnum,expt)
    if att_t!=1:
        type=type+ ' %d fr X %s exp'%(fnum,expt) + 'att_%s'%att_t
        att.set_T ( att_t )  #put atten
        
    RE.md['Measurement']=type
    ##Did not find how to set save
    eiger4m_save = 'XF:11IDB-ES{Det:Eig4M}cam1:SaveFiles'
    caput ( eiger4m_save,save )

    yield from bp.abs_set(eiger4m.cam.num_images, fnum)
    yield from bp.abs_set(eiger4m.cam.acquire_time, expt)
    yield from bp.abs_set(eiger4m.cam.acquire_period, acqt )

    yield from bp.abs_set(eiger4m.cam.array_counter,0)
    yield from YAG_FastSh( yag='off', fs='on' ) #put fast shutter on, yag at empty position
    
    BPMFeed(  xbpm_y= 'on' )
    sleep(3)
    BPMFeed(  xbpm_y= 'on' )
    
    if new_pos:
        yield from bp.abs_set(diff.yh, diff.yh.user_readback.value + 0.05)    
    yield from count( [eiger4m_single])
    #caput( eiger4m_save, False)

    yield from bp.abs_set(eiger4m.cam.num_images, 1)
    yield from bp.abs_set(eiger4m.cam.acquire_period, .01 )
    yield from bp.abs_set(eiger4m.cam.acquire_time, .01)
    if bpm_on:
        yield from go_to_sleep()
        #YAG_FastSh_BPMFeed( 'off', 'on','on')
        

def go_to_sleep( ):
    yield from YAG_FastSh( yag='on', fs='on' )
    BPMFeed(  xbpm_y= 'on' )
    sleep(3)
    BPMFeed(  xbpm_y= 'on' )
    

    

#a count with metadata writing func
def count_gisaxs(type, fnum=1, acqt = 0.1, expt= 0.1, 
        phh = -0.16, att_t = 1, saxs_bstx = 111.6,
           save=True, new_pos = False):
    #RE( count_('alignment', 1, 0.1, 0.1, att_t =  1, save=True, new_pos = False) )
    #RE( count_( 'XPCS_200C_1000 frames_1s', 1000, 1, 1 , att_t =  1, save=True, new_pos = False) )

    
    RE.md['Measurement']=type
    ##Did not find how to set save
    eiger4m_save = 'XF:11IDB-ES{Det:Eig4M}cam1:SaveFiles'
    caput ( eiger4m_save,save )

    #caput('XF:11IDB-ES{Det:Eig4M}cam1:NumImages',  fnum )
    #caput('XF:11IDB-ES{Det:Eig4M}cam1:AcquireTime',  acqt )
    #caput('XF:11IDB-ES{Det:Eig4M}cam1:AcquirePeriod', expt)
    
    yield from bp.abs_set(eiger4m.cam.num_images, fnum)
    yield from bp.abs_set(eiger4m.cam.acquire_period, acqt )
    yield from bp.abs_set(eiger4m.cam.acquire_time, expt)
    
    yield from bp.abs_set(saxs_bst.x, saxs_bstx ) #move beamstop in
    yield from bp.abs_set(diff.phh, phh)
    yield from bp.abs_set(eiger4m.cam.array_counter,0)
    if new_pos:
        yield from bp.abs_set(diff.xh, diff.xh.user_readback.value + 0.05)
        #yield from bp.abs_set(diff.yh, diff.yh.user_readback.value + 0.05)

#    return None

    yield from YAG_FastSh( yag='off', fs='on' )
    BPMFeed(  xbpm_y= 'on' )    
    att.set_T ( att_t )  #put atten
    
    BPMFeed(  xbpm_y= 'on' )
    yield from count( [eiger4m_single])
    caput( eiger4m_save, False)
    
    
#set Eiger4M image counter as 0

def imn():
    yield from bp.abs_set(eiger4m.cam.array_counter,0)


def gisaxs_yh_align( yh = None, phh = 0, att_t = 1e-4, saxs_bstx = 111.6):
    #RE(gisaxs_yh_align( yh = None, phh = 0, att_t = 1e-4, saxs_bstx = 111.6))

    att.set_T ( att_t )  #put atten
    yield from bp.abs_set(diff.phh, phh)
    yield from bp.abs_set(saxs_bst.x, saxs_bstx + 5) #move beamstop away from beam +5 mm
    if yh is not None:
        yield from bp.abs_set(diff.yh,yh)

    eiger4m_save = 'XF:11IDB-ES{Det:Eig4M}cam1:SaveFiles'
    caput ( eiger4m_save, False )    
    caput('XF:11IDB-ES{Det:Eig4M}cam1:NumImages',1)
    caput('XF:11IDB-ES{Det:Eig4M}cam1:AcquireTime', 0.1)
    caput('XF:11IDB-ES{Det:Eig4M}cam1:AcquirePeriod',0.1)    
    
    yield from dscan(diff.yh,-.05,.05,25)
    
    
    


#Fast YAG in/out, shutter on/off, BPM_Feedback on/off
def YAG_FastSh( yag='on', fs='on' ):
    yag_pos = 'XF:11IDB-OP{Mon:Foil-Ax:X}Mtr.VAL'  # 26 for empty, 
    xbpm_y_pos = 'XF:11IDB-BI{XBPM:02}Fdbk:BEn-SP'
    fs_pos = 'XF:11IDB-ES{Zebra}:SOFT_IN:B0'


    if yag is 'on':
        #caput( yag_pos, 30)
        if abs(foil_x.user_readback.value - (30))>=.3:
            yield from bp.abs_set( foil_x.user_setpoint, 30 )
            sleep(20)
        print ('YAG is in the beam')
    else:
        if abs(foil_x.user_readback.value - (-26))>=.3:
            yield from bp.abs_set( foil_x.user_setpoint, -26.0 )
            sleep(20)
        print ('Empty is in the beam')
        

    if fs is 'on':
        yield from bp.abs_set( fast_sh, 1 )        
    else:
        yield from bp.abs_set( fast_sh, 0 )
        

def BPMFeed(  xbpm_y= 'on' ):
    xbpm_y_pos = 'XF:11IDB-BI{XBPM:02}Fdbk:BEn-SP'
    
    if xbpm_y is 'on':        
        caput( xbpm_y_pos, 1 )   
    else:
        caput( xbpm_y_pos, 0 )


    

#Fast YAG in/out, shutter on/off, BPM_Feedback on/off
def YAG_FastSh_BPMFeed( yag='on', fs='on', xbpm_y= 'on' ):
    yag_pos = 'XF:11IDB-OP{Mon:Foil-Ax:X}Mtr.VAL'  # 26 for empty, 
    xbpm_y_pos = 'XF:11IDB-BI{XBPM:02}Fdbk:BEn-SP'
    fs_pos = 'XF:11IDB-ES{Zebra}:SOFT_IN:B0'

    if fs is 'on':
        caput( fs_pos, 1)
    else:
        caput( fs_pos, 0 )
        xbpm_y = 'off'

    if xbpm_y is 'on':
        sleep(5)
        caput( xbpm_y_pos, 1 )
    
    else:
        caput( xbpm_y_pos, 0 )

    if yag is 'on':
        caput( yag_pos, 30)
    else:
        caput( yag_pos, -26)
    





