def launch_4m():
    det=eiger_4M_cam_img
    caput ('XF:11IDB-BI{Det:Eig4M}cam1:SaveFiles', 'Yes')
    gs.RE(Count([det],1,0))

def dlup(m,start,stop,nstep):
    plan = DeltaScanPlan([det],m,start,stop,nstep)
    plan.subs=[ LiveTable( [m, str(det.stats1.name)+'_'+str(det.stats1.read_attrs[0])]), LivePlot(x=str(m.name), y=str(det.stats1.name)+'_'+str(det.stats1.read_attrs[0]), markersize=10,  marker='o',color='r' ),spec_cb]
    RE(plan)


def alup(m,start,stop,nstep):
    plan = AbsScanPlan([det],m,start,stop,nstep)
    plan.subs=[ LiveTable( [m, str(det.stats1.name)+'_'+str(det.stats1.read_attrs[0])]), LivePlot(x=str(m.name), y=str(det.stats1.name)+'_'+str(det.stats1.read_attrs[0]), markersize=10,  marker='o',color='r' ),spec_cb]
    RE(plan)

def dscan_bpm_vlt( start, stop, num,  ):
    pv = 'XF:11IDB-BI{XBPM:02}CtrlDAC:BLevel-SP'
    cur_vlt = caget( pv )
    vlt = np.linspace( start, stop, num ) +  cur_vlt
    inten = []
    #fig, ax = plt.subplots()
    for i in vlt:
        caput(  pv, i )
        sleep( 1 )
        inten.append(  xray_eye1.stats1.total.value  )
        # ax.plot(   vlt, np.array( inten),  '-go')
        #ax.plot( i, xray_eye1.stats1.total.value, '-go')
    caput( pv, cur_vlt )
    fig, ax = plt.subplots()
    ax.plot(   vlt, np.array( inten),  '-go')

def dscan_smaract( start, stop, num,ax,statnum=1, globalcoord=True):
    ''' statnum is the statistic to plot
        if globalcoord is true, plot w.r.t. the global (sample + amp) coordinates
    '''
    if ax == 'x':
        axislab= 'x'
        pv = 'XF:11IDB-OP{BS:Samp-Ax:X}Mtr.VAL'
    if ax == 'y':
        axislab= 'y'
        pv = 'XF:11IDB-OP{BS:Samp-Ax:Y}Mtr.VAL'
    if ax == 'z':
        axislab= 'z'
        pv = 'XF:11IDB-OP{Stg:Samp-Ax:Phi}Mtr.VAL'
    if globalcoord:
        axislab = axislab + " (GLOBAL)"
    cur_vlt = caget( pv )
    vlt = np.linspace( start, stop, num ) +  cur_vlt
    if globalcoord:
        if ax == 'x':
            cur_sample= diff.xh.user_readback.value
        elif ax == 'y':
            cur_sample= diff.yh.user_readback.value
        else:
            # for z do nothing
            cur_sample = 0
        vlt += cur_sample
    inten = []
    fig, ax = plt.subplots()
    ax.set_xlabel(axislab)
    for n,i in enumerate(vlt):
        caput(  pv, i )
        #print(str(i))
        sleep( 2 )
        statstr = '_stats{}_total'.format(statnum)
        detselect(eiger4m_single,suffix=statstr)
        RE(ct())
        if statnum == 1:
            inten.append(  eiger4m_single.stats1.total.value  )
        elif statnum == 2:
            inten.append(  eiger4m_single.stats2.total.value  )
        elif statnum == 3:
            inten.append(  eiger4m_single.stats3.total.value  )
        elif statnum == 4:
            inten.append(  eiger4m_single.stats4.total.value  )

        ax.cla()
        ax.set_xlabel(axislab)
        ax.plot(   vlt[:n+1], np.array( inten),  '-go')
        #ax.plot( i, xray_eye1.stats1.total.value, '-go')
    caput( pv, cur_vlt )
    #fig, ax = plt.subplots()
    ax.plot(   vlt, np.array( inten),  '-go')
    return vlt, inten


def dscan_hdm_p( start, stop, num,  ):
    pv = 'XF:11IDA-OP{Mir:HDM-Ax:P}PID-SP'
    cur_vlt = caget( pv )
    vlt = np.linspace( start, stop, num ) +  cur_vlt
    inten = []
    #fig, ax = plt.subplots()
    for i in vlt:
        caput(  pv, i )
        sleep( 1 )
        inten.append(  xray_eye1.stats1.total.value  )
        # ax.plot(   vlt, np.array( inten),  '-go')
        #ax.plot( i, xray_eye1.stats1.total.value, '-go')
    caput( pv, cur_vlt )
    fig, ax = plt.subplots()
    ax.plot(   vlt, np.array( inten),  '-go')


#diff.xh.user_readback.name = 'diff_xh'

def get_filenames(header):
    keys = [k for k, v in header.descriptors[0]['data_keys'].items() if 'external' in v]
    events = get_events(db[-1], keys, handler_overrides={key: RawHandler for key in keys})
    key, = keys
    unique_filenames = set([ev['data'][key][0] for ev in events])
    return unique_filenames


def show_filenames(name, doc):
    time.sleep(5)
    print('Files generated:', get_filenames(db[doc['run_start']]))


# RE.subscribe('stop', show_filenames)

def yg_snap(**subs ):
    movr(diff.xh,.7)
    caput('XF:11IDB-ES{Det:Eig4M}cam1:NumImages',subs['frames'])
    caput('XF:11IDB-ES{Det:Eig4M}cam1:AcquireTime',subs['acq'])
    caput('XF:11IDB-ES{Det:Eig4M}cam1:AcquirePeriod',subs['acq'])
    count(**RE.md)
    movr(diff.xh,-.7)
    caput('XF:11IDB-ES{Det:Eig4M}cam1:NumImages',1)
    caput('XF:11IDB-ES{Det:Eig4M}cam1:AcquireTime',.1)
    caput('XF:11IDB-ES{Det:Eig4M}cam1:AcquirePeriod',.1)

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




# 2016 Mar
# CFN specific code

class Sample(object):

    def __init__(self, name, **md):

        self.md = md
        self.md['name'] = name

        self.sample_tilt = 0 # degrees
        self.references = None # referenc points for gridMoveAbs

        # sample_tilt positive means sample (and scattering) is misrotated counter-clockwise

    def xr(self, move_amount):
        target = diff.xh.user_readback.value + move_amount
        diff.xh.move( target, timeout=180 )
        diff.xh.move( target, timeout=180 )

    def yr(self, move_amount):
        target = diff.yh.user_readback.value + move_amount
        diff.yh.move( target, timeout=180 )
        diff.yh.move( target, timeout=180 )


    def get_md(self, **md):

        md_current = {}
        md_current['user'] = 'CFN'
        md_current.update(md)
        md_current['energy_keV'] = caget('XF:11IDA-OP{Mono:DCM-Ax:Energy}Mtr.RBV')/1000.0
        md_current['exposure_time'] = caget('XF:11IDB-ES{Det:Eig4M}cam1:AcquireTime')
        md_current['sequence_ID'] = caget('XF:11IDB-ES{Det:Eig4M}cam1:SequenceId') + 1
        md_current['sample'] = self.md
        md_current['sample']['x'] = diff.xh.user_readback.value
        md_current['sample']['y'] = diff.yh.user_readback.value
        #md_current['sample']['holder'] = 'air capillary holder'
        #md_current['sample']['holder'] = 'vacuum bar holder (kinematic)'
        md_current['sample']['holder'] = 'air bar holder (kinematic)'

        md_current.update(self.md)
        md_current['x_position'] = md_current['sample']['x']
        md_current['y_position'] = md_current['sample']['y']
        md_current['holder'] = md_current['sample']['holder']

        return md_current


    def snap(self, exposure_time=1, measure_type='snap', **md):

        if exposure_time is not None:
            caput('XF:11IDB-ES{Det:Eig4M}cam1:AcquireTime', exposure_time)

        md_current = self.get_md(**md)
        md_current['measure_type'] = measure_type


        #count(**md_current)
        RE(count([eiger4m_single]),**md_current)



    def measure(self, exposure_time=1, measure_type='measure', **md):

        self.snap(exposure_time=exposure_time, measure_type=measure_type, **md)




    def measureSpots(self, num_spots=4, translation_amount=0.03, axis='y', exposure_time=None, measure_type='measureSpots', **md):
        '''Measure multiple spots on the sample.'''

        if 'spot_number' not in self.md:
            self.md['spot_number'] = 1


        for spot_num in range(num_spots):

            self.measure(exposure_time=exposure_time, measure_type=measure_type, **md)

            if axis=='y':
                self.yr(translation_amount)
            elif axis=='x':
                self.xr(translation_amount)
            else:
                print('Axis not recognized.')

            self.md['spot_number'] += 1


    def measureXPCS(self, exposure_time=0.00134, num_frame=2000, measure_type='XPCS', **md):


        caput('XF:11IDB-ES{Det:Eig4M}cam1:AcquireTime', exposure_time)
        caput('XF:11IDB-ES{Det:Eig4M}cam1:AcquirePeriod', exposure_time)
        caput('XF:11IDB-ES{Det:Eig4M}cam1:NumImages', num_frame)

        md_current = self.get_md(**md)
        md_current['measure_type'] = measure_type


        count(**md_current)

        caput('XF:11IDB-ES{Det:Eig4M}cam1:AcquireTime', 1)
        caput('XF:11IDB-ES{Det:Eig4M}cam1:AcquirePeriod', 1)
        caput('XF:11IDB-ES{Det:Eig4M}cam1:NumImages', 1)


    def measureTimeSeries(self, exposure_time=0.002, num_frame=5000, measure_type='measureTimeSeries', **md):


        caput('XF:11IDB-ES{Det:Eig4M}cam1:AcquireTime', exposure_time)
        caput('XF:11IDB-ES{Det:Eig4M}cam1:AcquirePeriod', exposure_time)
        caput('XF:11IDB-ES{Det:Eig4M}cam1:NumImages', num_frame)

        md_current = self.get_md(**md)
        md_current['measure_type'] = measure_type


        count(**md_current)

        caput('XF:11IDB-ES{Det:Eig4M}cam1:AcquireTime', 1)
        caput('XF:11IDB-ES{Det:Eig4M}cam1:AcquirePeriod', 1)
        caput('XF:11IDB-ES{Det:Eig4M}cam1:NumImages', 1)

    def gotoOrigin(self):
        diff.xh.move( 0, timeout=180 )
        diff.yh.move( -2.39178, timeout=180 )


    def spiralSearch(self, step_size=0.05, max_stride=10):

        # 1 * +y
        # 1 * +x
        # 2 * -y
        # 2 * -x
        # 3 * +y
        # 3 * +x
        # 4 * -y
        # 4 * -x
        # etc.

        #self.snap()

        stride_length = 1
        polarity = +1
        while(stride_length<max_stride):

            for istride in range(stride_length):
                print('Move y {:.3f}'.format(polarity*step_size))
                self.yr(polarity*step_size)
                self.snap(exposure_time=None)

            for istride in range(stride_length):
                print('Move x {:.3f}'.format(polarity*step_size))
                self.xr(polarity*step_size)
                self.snap(exposure_time=None)

            stride_length += 1
            polarity *= -1


    def gridMeasure(self, nx=10, ny = 10, step_size=.005,exposure_time=None, skip=0, wait_time=None, **md):
        '''  Measure in an nx * ny grid. Move in a snake manner
            Assumes you start in lower left corner.
            SKip the first skip points (useful when a run prematurely ends)
            Note: This starts from wherever you were last positioned. If a 
            run is cancelled, make sure to reposition accordingly before running to
            resume.
        '''
        scl = -1
        xtmp,ytmp = 0,0
        
        for i in range(nx*ny):
            if i > skip:
                self.measure(exposure_time=exposure_time, **md)
                if wait_time is not None:
                    time.sleep(wait_time)
                
            if i%nx == 0:
                # Move up one and now switch move direction
                scl *= -1
                self.yr(step_size)
                #ytmp += step_size
                #print("Now at {}, {}".format(xtmp,ytmp))
            else:
                # move left or right (depends on scl)
                self.xr(step_size*scl)
                #xtmp += step_size*scl
                #print("Now at {}, {}".format(xtmp, ytmp))

                
    def gridMove(self, amt=[0,0], grid_spacing=0.075):
        '''Move in the sample coordinate grid. The amt is [x,y].'''

        tilt = np.radians(self.sample_tilt)

        rot_matrix = np.array( [ 
            [+np.cos(tilt), +np.sin(tilt)],
            [-np.sin(tilt), +np.cos(tilt)]
            ] )

        dv = np.array(np.asarray(amt)*grid_spacing) # vector in sample coordinate system
        dvp = np.dot(dv, rot_matrix) # dx in instrument coordinate system

        print('Move by ({:.4f}, {:.4f})'.format(dvp[0], -dvp[1]))
        self.xr(dvp[0])
        self.yr(-dvp[1])



    def gridMoveAbs(self, amt=[0,0], grid_spacing=0.075):
        '''Move in the sample coordinate grid. The amt is [x,y].
            Moves with respect to a reference point
        '''
        if self.references is None:
            print("Error, no reference point set, please set\
                by selecting addreferencepoint.")
        
        tilt = np.radians(self.sample_tilt)

        rot_matrix = np.array( [ 
            [+np.cos(tilt), +np.sin(tilt)],
            [-np.sin(tilt), +np.cos(tilt)]
            ] )

        dv = np.array(np.asarray(amt)*grid_spacing) # vector in sample coordinate system
        dvp = np.dot(dv, rot_matrix) # dx in instrument coordinate system

        print('Move by ({:.4f}, {:.4f})'.format(dvp[0], -dvp[1]))
        self.xr(dvp[0])
        self.yr(-dvp[1])


def measurecustom1():
    x0 = 0.715003
    y0 = -0.46736
    dx = 0.075
    dy = 0.075
    mov(diff.yh,y0)
    mov(diff.xh,x0)
    # neg move
    # up on sample
    jlst = -(np.arange(8)-3)
    ilst = [0]
    for j in jlst:
        for i in ilst:
            mov(diff.yh,y0-j*dy)
            mov(diff.xh, x0+i*dx)
            mov(diff.yh,y0-j*dy)
            mov(diff.xh, x0+i*dx)
            sam.measure(600,comment="box ({},{})".format(12+j,16+i))

def measurecustom2():
    print("tile structures")
    # ref coordinates:
    #print("WARNING : need optimized box (5,3) poxition")
    #x0 = 0.715003
    #y0 = -0.46736
    #reference coordinates box label:
    #box is y,x pair where y increasing goes down and x increasing right
    box0 = 3,5
    #x0, y0 = -.486268, -1.05503 # from box (4,0) tile 2
    #x0, y0 = -.485841, -.90597 # from box (6,1) tile 4
    x0, y0 = -.106606, -1.13920# box 2,3, (x,y
    dx = 0.075
    dy = 0.075
    mov(diff.yh,y0)
    mov(diff.xh,x0)
    #mov(sam_x, -.33532-0.075*3);mov(sam_y, -1.13244 -0.075*3);

    #tile 1,2,3,4 elements 0 to 3:
    #positive y is down and pos x is right
    jlst = [4]
    ilst = [0, 1, 2, 3,4,5,6]
          
    for i in ilst:
        for j in jlst:
            mov(diff.yh,y0+j*dy)
            mov(diff.xh, x0+i*dx)
            mov(diff.yh,y0+j*dy)
            mov(diff.xh, x0+i*dx)
            sam.measure(600,comment="box ({},{})".format(box0[0]+j,box0[1]+i))

    #tile 1,2,4 elements 4 to 8 (same ref box, (5,3)):
    #positive y is up and pos x is right
    #jlst = [-2,-1,1]
    #ilst = np.arange(8)-3
          
    #for j in jlst:
        #for i in ilst:
            #mov(diff.yh,y0-j*dy)
            #mov(diff.xh, x0+i*dx)
            #mov(diff.yh,y0-j*dy)
            #mov(diff.xh, x0+i*dx)
            #sam.measure(600,comment="box ({},{})".format(box0[0]-j,box0[1]+i))

def measurecustom3():
    print("hex structures vary number, 60 sec exposures")
    #reference coordinates box label:
    #box is y,x pair where y increasing goes down and x increasing right
    #box0 = 0, 15 # (y,x)
    #x0, y0 = .632094, -1.37608# box 0, 15 (y,x)
    #box0 = 4, 15 # (y,x)
    #x0, y0 = 0.6400, -1.07768 # box (4, 15) 
    
    box0 = 9, 15
    x0, y0=.644901, -.68919

    dx = 0.075
    dy = 0.075

    mov(diff.yh,y0)
    mov(diff.xh,x0)

    #positive y is down and pos x is right
    jlst = [0, 1, 2, 3, 4, 5, 6, 7]
    ilst = [-6, -5, -4, -3, -2, -1, 0, 1]
          
    for i in ilst:
        for j in jlst:
            mov(diff.yh,y0+j*dy)
            mov(diff.xh, x0+i*dx)
            mov(diff.yh,y0+j*dy)
            mov(diff.xh, x0+i*dx)
            sam.measure(60,comment="box ({},{}) (5x5 hex arrays vary N)".format(box0[0]+j,box0[1]+i))

    #tile 1,2,4 elements 4 to 8 (same ref box, (5,3)):
    #positive y is up and pos x is right
    #jlst = [-2,-1,1]
    #ilst = np.arange(8)-3
          
    #for j in jlst:
        #for i in ilst:
            #mov(diff.yh,y0-j*dy)
            #mov(diff.xh, x0+i*dx)
            #mov(diff.yh,y0-j*dy)
            #mov(diff.xh, x0+i*dx)
            #sam.measure(600,comment="box ({},{})".format(box0[0]-j,box0[1]+i))


#template
    
def measurecustomscratch():
    x0 = .03765
    y0 = -.99294
    dx = 0.075
    dy = 0.075
    mov(diff.yh,y0)
    mov(diff.xh,x0)

    jlst = [0]
    ilst = [-4, -5, -6, -7]
    for j in jlst:
        for i in ilst:
            mov(diff.yh,y0-j*dy)
            mov(diff.xh, x0+i*dx)
            mov(diff.yh,y0-j*dy)
            mov(diff.xh, x0+i*dx)
            sam.measure(600,comment="box ({},{})".format(5-j,i+7))


    jlst = [2, 1, -1, -2]
    ilst = [-7, -6, -5, -4, -3,-2, -1,0,1]
    for j in jlst:
        for i in ilst:
            mov(diff.yh,y0-j*dy)
            mov(diff.xh, x0+i*dx)
            mov(diff.yh,y0-j*dy)
            mov(diff.xh, x0+i*dx)
            sam.measure(600,comment="box ({},{})".format(6-j,i+7))

    #this ref is box (9,16) upper right box of lower right quad
    x0 = .71645
    y0 = -.68810
    jlst = [0, -1, -2, -3, -4, -5, -6, -7]
    ilst = [0,-1, -2, -3, -4, -5, -6, -7]
    for j in jlst:
        for i in ilst:
            mov(diff.yh,y0-j*dy)
            mov(diff.xh, x0+i*dx)
            mov(diff.yh,y0-j*dy)
            mov(diff.xh, x0+i*dx)
            sam.measure(600,comment="box ({},{})".format(6-j,i+7))


