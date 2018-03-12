#######
"""Test Fast shutter with beam intensity monitered by XBPM
   
  Codes:
  /home/xf11id/.ipython/profile_collection/startup/34_fash_shutter_bpm_test.py
  Usage:
  
1) define exposetime list:  expt_list = [0.001, 0.002, 0.003, 0.004,]
2) take data d = do_fh_series(expt_list=expt_list, filename='test_5--90ms' )
2.1) or load data,  bpm_data = pkl.load( open(data_path + 'test_5--90ms' + '.pkl','rb') )
3) plot data 
   plot some data with keys
   plot_dict(d, xlim=None, ylim=[-9, 1], keys=['5.0_ms', '6.0_ms', '7.0_ms','8.0_ms','9.0_ms',],xlabel='data p
     ...: oints', ylabel='intensity', title='XBPM Read ~Fast Shutter Test')
   Or plot all the data    
   plot_dict(d, xlim=None, ylim=[-9, 1], keys=None,xlabel='data p
     ...: oints', ylabel='intensity', title='XBPM Read ~Fast Shutter Test')

   plot_dict(d, xlim= [24700, 25727], ylim=[-9, 1], keys=['9.0_ms','10.0_ms','20.0_ms','30.0_ms','40.0_ms', '5
     ...: 0.0_ms','60.0_ms','70.0_ms','80.0_ms','90.0_ms'],xlabel='data points', ylabel='intensity', title='XBPM Read
     ...:  ~Fast Shutter Test')
4) Get width of xbpm data
   dicts = get_bpm_dict_width( d, [24700, 25727], -6)

5)  t = np.array( [  0.01, 0.02, 0.03, 0.04,  0.05, 0.06, 0.07, 0.08, 0.09] )
    y =  np.array( list(dicts.values() ) )
    plot_data_with_linfit( t,y)

One example:
expt_list =   [0.01, 0.02, 0.03, 0.04,  0.05, 0.06, 0.07, 0.08, 0.09]
d = do_fh_series(expt_list=expt_list, filename='new_shutter_pos_10--90ms_repeat' )
plot_dict(d, xlim=[24740, 25927], ylim=[-9, 1], keys=['10.0_ms','20.0_ms','30.0_ms','40.0_ms', '50.0_ms','60.0_ms','70.0_ms','80.0_ms','90.0_ms'],xlabel='data points', ylabel='intensity', title='XBPM Read~Fast Shutter Test')
dicts = get_bpm_dict_width( d, [24740, 25927], -2);print(dicts)
t = np.array( expt_list);y =  np.array( list(dicts.values() ) )
plot_data_with_linfit( t,y ) 

    
"""
from scipy.optimize import leastsq

#plot_dict(d, xlim=None, ylim=[-9, 1], keys=['9.0_ms','10.0_ms','20.0_ms','30.0_ms','40.0_ms', '50.0_ms','60.0_ms','70.0_ms','80.0_ms','90.0_ms'],xlabel='data points', ylabel='intensity', title='XBPM Read ~Fast Shutter Test')
 

delay_time_list = np.array( [ 2,3,4,5,6,7,8,9,10,11,12,13,14,15,16, 17, 18, 19, 20, 21,22 ] )  #ms
expt_time = 10 #ms
delay_list=0
input_time_width = delay_list + expt_time #ms

measured_width_by_bpm = np.array( [26, 42, 49, 57, 65, 76, 87, 96,
                   109, 116, 124, 134, 145, 156, 166, 176, 185, 195,207, 217, 228 ] )/10.  #ms

def plot_exp_meas():
   fig,ax=plt.subplots()
   plot1D( x=input_time_width, y=measured_width_by_bpm, ax=ax,
           xlabel='input_time (ms)', ylabel='time_from_XBPM (ms)',
           c='b',m='o', )#ls='', legend='data')
   ax.grid('on')





data_path = '/XF11ID/analysis/Commissioning/BPM_Stability/Data/'
import pickle as pkl
from datetime import datetime

expt_list = [0.001, 0.002, 0.003, 0.004, 0.005, 0.006, 0.007, 0.008, 0.009,
0.01, 0.02, 0.03, 0.04,  0.05, 0.06, 0.07, 0.08, 0.09]
#expt_list = [0.01 ]
expt_list = [0.001, 0.002, 0.003, 0.004,]
#expt_list = #[0.005, 0.006, 0.007, 0.008, 0.009,
expt_list =   [0.01, 0.02, 0.03, 0.04,  0.05, 0.06, 0.07, 0.08, 0.09]


def get_triger_delay_xbpm( delay_list, filename=None):
   bpm_data = {}
   for delay in delay_list:
       print('Do data acquisition for triger dealy time=%s ms'%(1000*expt))
       #caput( 'XF:11IDB-BI{XBPM:02}FaSoftTrig-SP',1 )
       caput('XF:11IDB-ES{Det:Eig4M}ExposureDelay-SP',delay);
       series(det='eiger4m',shutter_mode='multi',expt=0.01,acqp=0.1,
             imnum=10,comment='Test: fast shutter-eiger4M',use_xbpm=True);
       x = caget('XF:11IDB-BI{XBPM:02}FA-S');
       bpm_data[str(delay*1000)+'_ms']= len(np.where(x<=-5)[0])/100 #in ms
       print(len(np.where(x<=-5)[0])/10)
       print('Sleep 5 sec here')		
       time.sleep(5)        
   
   dt =datetime.now()
   times = '%s%02d%02d-%02d%02d' % (dt.year, dt.month, dt.day,dt.hour,dt.minute)
   if filename is None:
       filename = times
   else:
       filename = filename #+ '_' + times
   pkl.dump(bpm_data, open(data_path + filename + '.pkl','wb') ) 
   #for load data
   #bpm_data = pkl.load( open(data_path + filename + '.pkl','rb') )
   return bpm_data   



def do_fh_series( expt_list, filename=None ):
   bpm_data = {}
   for expt in expt_list:
       print('Do data acquisition for exposure time=%s ms'%(1000*expt))
       #caput( 'XF:11IDB-BI{XBPM:02}FaSoftTrig-SP',1 )
       series(det='eiger4m',shutter_mode='multi',expt=expt,acqp=0.1,imnum= 100,comment='Test: fast shutter-eiger4M_expt=%s ms'%(1000*expt), use_xbpm=True)
       print('Sleep 5 sec here')		
       time.sleep(5)
       bpm_data[str(expt*1000)+'_ms']=caget('XF:11IDB-BI{XBPM:02}FA-S')
   
   dt =datetime.now()
   times = '%s%02d%02d-%02d%02d' % (dt.year, dt.month, dt.day,dt.hour,dt.minute)
   if filename is None:
       filename = times
   else:
       filename = filename #+ '_' + times
   pkl.dump(bpm_data, open(data_path + filename + '.pkl','wb') ) 
   #for load data
   #bpm_data = pkl.load( open(data_path + filename + '.pkl','rb') )
   return bpm_data


def plot_dict(dicts,keys=None,*argv,**kwargs):
    fig, ax = plt.subplots()
    if keys is None:
        keys= list(dicts.keys())
    i=0
    for k in keys:
        plot1D( dicts[k], ax=ax, legend=k, c= colors[i], m=markers[i], *argv,**kwargs )
        i += 1

def get_bpm_width( data, thres=-8 ):
    w = np.where( data <=thres )
    return len( w[0] )

def get_bpm_dict_width( bpm_data, xranges=[33400, 34500], thres=-8, keys=None ):
   if keys is None:
      keys= list(bpm_data.keys())
   w = {}
   for k in keys:
      data = bpm_data[k][xranges[0]:xranges[1]]
      w[k] = get_bpm_width( data, thres=thres )    
   return w 

def linear_fit_func( paras, ydata, xdata, k=None ):
   if k is None:
      k = paras[1]   
   a = paras[0]
   err = np.abs( ydata - k*xdata - a )
   return np.sqrt( err )   

def get_linear_fit( xdata, ydata,  paras,  k=None   ):
    res = leastsq(linear_fit_func, [ paras ], args=( ydata, xdata,k ),
                                  ftol=1.49012e-10, xtol=1.49012e-10, factor=100,
                                  full_output= 0)
    return res 


def plot_data_with_linfit( x,y,*argv,**kwargs):
   fig = plt.figure( )            
   ax = fig.add_subplot(2,1,1 )
   #fig, ax = plt.subplots()
   #z = np.polyfit(t, y, 1)
   #p = np.poly1d(z)
   #plot1D(x=t, y= p(t),  ls='-',m='',c='r',ax=ax, legend = 'fit-k=%s_b=%s'%(round(z[1],1),round(z[0],1)) )
   b= get_linear_fit( x, y,  [0], k=10000 ) [0][0]

   plot1D(x=t, y=y,ax=ax,xlabel='exp_time (ms)', ylabel='time_from_XBPM (points)',c='b',m='o', ls='', legend='data')
   plot1D(x=t, y= t*10000 + b,  ls='-',m='',c='r',ax=ax, legend = 'fit-(fix k=10K)_b=%s'%( round(b,1)) )
   
   ax = fig.add_subplot(2,1,2 )   
   #plot1D(x=t, y= (y - z[1])/z[0],ax=ax,xlabel='exp_time (ms)', ylabel='time_from_XBPM',c='b',m='o', ls='', legend='')
   plot1D(x=t, y= (y - b )/10000,ax=ax,xlabel='exp_time (ms)', ylabel='time_from_XBPM',c='b',m='o', ls='', legend='')

   ax.grid('on')







        

