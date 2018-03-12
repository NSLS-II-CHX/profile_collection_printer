import bluesky.plans as bp

def detselect(detector_object, suffix="_stats1_total"):
    """Switch the active detector and set some internal state"""
    print("This does not work anymore. Instead, do:")
    print("dets = [YOUR_DETECTOR_HERE]")


def xpcs_count(detectors, *, md=None):
    """
    Similar to `count`

    Customized to provide access to files before acquisition completes.
    """

    md = md or {}
    _md = {'plan_name': 'xpcs',
           'detectors': [det.name for det in detectors]}
    _md.update(md)

    table = LiveTable([])  # a simple table with seq_num and time

    @bp.subs_decorator([table])
    @bp.stage_decorator(detectors)
    @bp.run_decorator(md=md)
    def inner_xpcs():
        yield from bp.checkpoint()
        yield from bp.create()
        for det in detectors:
            # Start acquisition.
            yield from bp.trigger(det)
            # Read the UID that points to this dataset in progress.
            yield from bp.read(det)
        # Insert an 'Event' document into databroker. Now we can access the (partial) dataset.
        yield from bp.save()
        # *Now* wait for the detector to actual finish acquisition.
        yield from bp.wait()  

    return (yield from inner_xpcs())

def move_E(energy, gap=[], xtal="Si111cryo", gapmode="auto", harm=5):
	"""
	change beamline energy: moving both Bragg axis and gap of IVU
	calling sequence: move_E(energy, gap=[], xtal="Si111cryo", gapmode="auto", harm=5)
	energy: scalar!; X-ray energy in [keV] & xtal define the Bragg angle via xf.get_Bragg()
	gap: manually entered gap value with gapmode="manual" OR calculated from xf.get_gap(energy, harm, default id map) with gapmode="auto"
	note: currently only DCM (not DMM) is implemented
	to-do: need PV that reflects crystal selection -> new default: xtal='current' -> using whatever xtal is currently in the beam
	to-do: with PV above, change xtal if selected xtal is not the currently inserted one
	"""
	th_B=-1*xf.get_Bragg(xtal,energy)[0]
	if gapmode == "manual":
		if len([gap]) == len([energy])==1:
			gap = gap
			print('using manually entered gap value...')
		else: print('error: function accepts only one energy and one gap value at a time')
	elif gapmode =="auto":
		gap=xf.get_gap(energy,harm)
		print('using calculated gap value from xfuncs!')
	print('moving ivu_gap to '+str(gap)[:6]+'mm   and dcm.b to '+str(th_B)[:6]+'deg')
	ivu_gap.move(gap)	
	dcm.b.move(th_B)
	print('Done! New X-ray energy is '+ str(dcm.en.user_readback.value/1000)+'keV')
	

def E_scan(energy, gap=[], xtal="Si111cryo", gapmode="auto",harm=5, det=elm.sum_all): 
	"""
	energy scan: Scanning both Bragg axis and gap of IVU in a linked fashion
	calling sequence: E_scan(energy, gap=[], xtal="Si111cryo", gapmode="auto", harm=5 det=elm.sum_all.value)
	energy: X-ray energy in [keV] & xtal define the Bragg angles used in the scan via xf.get_Bragg()
	gap: manually entered list of gap values with gapmode="manual" OR calculated from xf.get_gap(energy, harm, default id map) with gapmode="auto"
	to-do: allow detector selection from 'detselect()'
	by LW June 2016	
	"""
	from cycler import cycler
	#from bluesky import PlanND
	th_B=list(-1*xf.get_Bragg(xtal,energy)[:,0])
	if gapmode == "manual":
		if len(gap) == len(energy):
			gap = gap
			print('using manually entered gap values...')
		else: print('error: length of manually entered list of gap value does not match number of energy points')
	elif gapmode =="auto":
		gap=list(xf.get_gap(energy,harm))  
		print('using calculated gap values from xfuncs!')
	inner = cycler(dcm.b,th_B)+cycler(ivu_gap,gap)
	#plan = PlanND([det],inner)
	plan = scan_nd([det],inner)
	#RE(plan, [LiveTable([dcm.b,ivu_gap,det]),LivePlot(x='dcm_b',y=det.name,fig = plt.figure())])
	RE(plan, [LiveTable([dcm.b,ivu_gap,det]),LivePlot(x='dcm_b',y=det.name,fig = plt.figure())])


def Energy_scan(energy, gap=[], xtal="Si111cryo", gapmode="auto",harm=5, det=[eiger1m_single]): 
	"""
    Energy_scan(energy, gap=[], xtal="Si111cryo", gapmode="auto",harm=5, det=[eiger1m_single]):
    energy scan: Scanning both Bragg axis and gap of IVU in a linked fashion
	calling sequence: E_scan(energy, gap=[], xtal="Si111cryo", gapmode="auto", harm=5 det=elm.sum_all.value)
	energy: X-ray energy in [keV] & xtal define the Bragg angles used in the scan via xf.get_Bragg()
	gap: manually entered list of gap values with gapmode="manual" OR calculated from xf.get_gap(energy, harm, default id map) with gapmode="auto"
	to-do: allow detector selection from 'detselect()'
	by LW June 2016	
	"""
	from cycler import cycler
	#from bluesky import PlanND
	th_B=list(-1*xf.get_Bragg(xtal,energy)[:,0])
	if gapmode == "manual":
		if len(gap) == len(energy):
			gap = gap
			print('using manually entered gap values...')
		else: print('error: length of manually entered list of gap value does not match number of energy points')
	elif gapmode =="auto":
		gap=list(xf.get_gap(energy,harm))  
		print('using calculated gap values from xfuncs!')
	inner = cycler(dcm.b,th_B)+cycler(ivu_gap,gap)
	#plan = PlanND([det],inner)
	plan = scan_nd(det,inner)
	#RE(plan, [LiveTable([dcm.b,ivu_gap,det]),LivePlot(x='dcm_b',y=det.name,fig = plt.figure())])
	RE(plan)

#### crude test only!!! ####
def refl_scan(incident_angle):
	from cycler import cycler
	from bluesky import PlanND
	det=eiger1m_single
	inner = cycler(diff.phh,-1*incident_angle)+cycler(diff.gam,-2*incident_angle)
	plan = PlanND([det],inner)
	RE(plan, [LiveTable([diff.phh,diff.gam,det]),LivePlot(x='diff_phi',y=det.name+"_stats1_total",fig = plt.figure())])
	### Live plot su$$$s!!! -> plot after the fact...
	dat=get_table(db[-1])
	plt.figure(97)
	plt.semilogy(dat.diff_phh,dat.eiger1m_single_stats1_total)

	
	
	
			
def samy_dscan(start, end, points):
    """
    sampley relative scan using the eiger1m_single detector
    achieves a y motion by combining the incline (diff.xv) and diff.zh
    calling sequence: samy_dscan(start, end, points)
    Note - its a relative scan, start and end are relative from current position
    by YZ, AF Oct 2016	
    """
    from cycler import cycler
    from bluesky import PlanND
    initial_xv = diff.xv.user_readback.value
    initial_zh = diff.xh.user_readback.value
    suffix="_stats1_total"
    det=eiger1m_single
    angle=9.0*np.pi/180.0
    dy_values= np.linspace( start, end, points)
    xv_values = dy_values/np.sin( angle ) + initial_xv 
    zh_values = -1* dy_values/np.tan( angle ) + initial_zh
    inner = cycler(diff.xv, xv_values)+cycler(diff.xh, zh_values)
    plan = PlanND([det],inner)
    RE(plan, [LiveTable([diff.xv,diff.xh,det  ]),LivePlot(x='diff_xv',y=det.name+suffix,fig = plt.figure())])
    diff.xv.set(initial_xv)
    diff.xh.set(initial_zh)



def chx_plot_motor(scan):
    fig = None
    if gs.PLOTMODE == 1:
        fig = plt.gcf()
    elif gs.PLOTMODE == 2:
        fig = plt.gcf()
        fig.clear()
    elif gs.PLOTMODE == 3:
        fig = plt.figure()
    return LivePlot(gs.PLOT_Y, scan.motor._name, fig=fig)


# hacking on the logbook!

from pprint import pformat, pprint
from bluesky.callbacks import CallbackBase

import os
from datetime import datetime

def get_epics_motors():
    return {name: obj for name, obj in globals().items() if isinstance(obj, (EpicsMotor))}


class print_scan_id(CallbackBase):
    def start(self, doc):
        self._scan_id = doc['scan_id']

    def stop(self, doc):
        print("The scan ID is: %s" %self._scan_id)

RE.subscribe(print_scan_id())


#RE.subscribe('stop', Whatever())

#RE.subscribe('all', Whatever())

#wh = Whatever()
#RE.subscribe('start', wh)
#RE.subscribe('stop', wh)


#from bluesky.callbacks.core import LiveSpecFile
#

# for spec_scan in [ascan, dscan, ct]:
    #    Route all documents to the spec callback.
#    spec_scan.subs['all'].append(spec_cb)


def relabel_figure(fig, new_title):
    fig.set_label(new_title)
    fig.canvas.manager.window.setWindowTitle(new_title)
    


from suitcase.spec import DocumentToSpec
import suitcase.spec

# Monkey-patch module globals.
#suitcase.spec._SCANS_WITHOUT_MOTORS.extend(['count'])
#suitcase.spec._SCANS_WITH_MOTORS.extend(['scan', 'relative_scan'])
#suitcase.spec._BLUESKY_PLAN_NAMES.extend(['count', 'scan', 'relative_scan'])
#suitcase.spec._SPEC_SCAN_NAMES.extend(['count', 'scan', 'relative_scan'])

#specpath = os.path.expanduser('/home/xf11id/specfiles/chx_spec_2017_06_22.spec')
specpath = os.path.expanduser('/home/xf11id/specfiles/chx_spec_2017_11_28.spec')

#spec_cb = DocumentToSpec('/home/xf11id/specfiles/testing.spec')
spec_cb = DocumentToSpec(specpath)


RE.subscribe(spec_cb)
 

def reload_macro(filename):
    get_ipython().magic("%run -i ~/.ipython/profile_collection/startup/" + filename)

