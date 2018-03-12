

def get_archived_pv( pv, start_time, end_time, label=None,
                     limit = None, make_wave= True,interpolation = 'raw'  ):

    '''Yugang May 15, 2017
	   Get a archived PV value
       Input:
           start time:  str, e.g., '2017-04-11 09:00', 
           end time: str,   e.g., '2017-04-12 11:00'
           label: str, a meaningful label for the pv
           limit: integer, the limit data point
           make_wave: if True, make a 'square-wave like' data
           interpolation: 'raw', gives the raw archived data
       Return:  a pandas.dataframe with column as
       datetime, float time, and value
data
       An example:
           data = get_archived_pv('XF:11IDA-OP{Mono:DCM-Ax:Bragg}T-I', '2017-04-11 09:00', '2017-04-11 11:00')

       '''
    
    from channelarchiver import Archiver
    archiver = Archiver('http://xf11id-ca.cs.nsls2.local/cgi-bin/ArchiveDataServer.cgi')

    import numpy as np
    import pandas as pd
   
    if label is None:
        label  = pv
    
    #if pv[0][:2] == 'SR':
    #    res = arget( pv,start=start_time,
    #              end=end_time,count=limit, conf = 'middle')
    #else:
    print ('Seraching PV: %s from: %s---to: %s' % (label,start_time, end_time))
    res = archiver.get(pv, start_time, end_time, scan_archives= True, 
                limit=limit, interpolation=interpolation)
 

    #print res
    key = pv         
    v =np.array(res[key][0], dtype = float)
    k1 = res[key][1]
    N= len(k1)
    sec = np.array( [ k1[i][2] for i in range(N)] )
    nsec = np.array( [ k1[i][3] for i in range(N)] )
    tf = sec + nsec*10**(-9)        
    if make_wave:
        v = make_wave_data(v, dtype='y')
        tf = make_wave_data(tf, dtype='x')    
    td = trans_tf_to_td(tf,dtype='array')
    NN= len(td)
    tv = np.array([td, tf.reshape(NN), v.reshape(NN)]).T
    index = np.arange(len(tv))
    data = tv
    df = pd.DataFrame(data, index=index, columns=['td', 'tf', label[0]])
    if make_wave:fnum = len(df.td)/2
    else:fnum=len(df.td)
    return df
    
def trans_tf_to_td(tf, dtype = 'dframe'):
    import pandas as pd
    import numpy as np
    import datetime
    '''translate time.float to time.date,
       td.type dframe: a dataframe
       td.type list,   a list
    ''' 
    if dtype is 'dframe':ind = tf.index
    else:ind = range(len(tf))    
    td = np.array([ datetime.datetime.fromtimestamp(tf[i]) for i in ind ])
    return td


def make_wave_data(x, dtype = 'x'):
    '''x is list or one-d array,'''
    import numpy as np
    x = np.array(x)
    x=x.reshape( len(x) )
    X = np.zeros(len(x) * 2 - 1, dtype=object)
    X[::2] = x
    if dtype == 'x':
        X[1::2] = x[1:]
    else:
        X[1::2] = x[:-1]
    return X






