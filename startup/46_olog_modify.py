from pyOlog import LogEntry,  Attachment,OlogClient
from pyOlog import SimpleOlogClient
from pyOlog.OlogDataTypes import  Logbook

#from epics import caput, caget

def update_olog_id( logid, text, attachments):   
    '''Update olog book  logid entry with text and attachments files
    logid: integer, the log entry id
    text: the text to update, will add this text to the old text
    attachments: add new attachment files
    An example:
    
    filename1 = '/XF11ID/analysis/2016_2/yuzhang/Results/August/af8f66/Report_uid=af8f66.pdf'
    atch=[  Attachment(open(filename1, 'rb')) ] 
    
    update_olog_id( logid=29327, text='add_test_atch', attachmenents= atch )    
    
    '''
    url='https://logbook.nsls2.bnl.gov/Olog-11-ID/Olog'
    olog_client=SimpleOlogClient(  url= url, 
                                    username= 'xf11id', password= '**REMOVED**'   )
    
    client = OlogClient( url='https://logbook.nsls2.bnl.gov/Olog-11-ID/Olog', 
                                    username= 'xf11id', password= '**REMOVED**' )
    
    old_text =  olog_client.find( id = logid )[0]['text']    
    upd = LogEntry( text= old_text + '\n'+text,   attachments=  attachments,
                      logbooks= [Logbook( name = 'Operations', owner=None, active=True)]
                  )  
    upL = client.updateLog( logid, upd )    
    #print( 'The url=%s was successfully updated with %s and with the attachments'%(url, text))
    
def update_olog_uid( uid, text, attachments):  
    '''Update olog book  logid entry cotaining uid string with text and attachments files
    uid: string, the uid of a scan or a specficial string (only gives one log entry)
    text: the text to update, will add this text to the old text
    attachments: add new attachment files    
    An example:
    
    filename1 = '/XF11ID/analysis/2016_2/yuzhang/Results/August/af8f66/Report_uid=af8f66.pdf'
    atch=[  Attachment(open(filename1, 'rb')) ] 
    update_olog_uid( uid='af8f66', text='Add xpcs pdf report', attachments= atch )    
    
    '''
    
    olog_client=SimpleOlogClient( url='https://logbook.nsls2.bnl.gov/Olog-11-ID/Olog', 
                                    username= 'xf11id', password= '**REMOVED**' )
    
    client = OlogClient( url='https://logbook.nsls2.bnl.gov/Olog-11-ID/Olog', 
                                    username= 'xf11id', password= '**REMOVED**' )
    
    logid = olog_client.find( search= uid )[0]['id']
    update_olog_id( logid, text, attachments) 

def log_manual_count():
    os.environ['HTTPS_PROXY'] = 'https://proxy:8888'
    os.environ['no_proxy'] = 'cs.nsls2.local,localhost,127.0.0.1'
    uid = db[-1]['start']['uid']    
    fp=caget('XF:11IDB-ES{Det:Eig4M}cam1:FWNamePattern_RBV')[:-3] + '%s_master.h5'%( int(caget('XF:11IDB-ES{Det:Eig4M}cam1:SequenceId')) );
    #xh = caget('XF:11IDB-ES{Dif-Ax:XH}Mtr.VAL')
    #yh = caget('XF:11IDB-ES{Dif-Ax:YH2}Mtr.VAL') 
    #phh = caget('XF:11IDB-ES{Dif-Ax:PhH}Mtr.VAL')
 
    text = '\n\n\nMeta data\n--------\n'
    for [k,v] in db[-1]['start'].items():
    	text += '%s: %s\n'%(k,v)
    #text += 'diff_xh: %s\n'%xh
    #text += 'diff_yh: %s\n'%yh
    #text += 'diff_phh: %s\n'%phh
    text += 'filename: %s\n'%fp
    try:
        update_olog_uid( uid= uid, text=text, attachments=None )
        print('Olog was updated!')
    except:
        print("Sorry, it can't log the metadata!")
	  


    
def log_filepath():     
    os.environ['HTTPS_PROXY'] = 'https://proxy:8888'
    os.environ['no_proxy'] = 'cs.nsls2.local,localhost,127.0.0.1'
    uid = db[-1]['start']['uid']
    fp=caget('XF:11IDB-ES{Det:Eig4M}cam1:FWNamePattern_RBV')[:-3] + '%s_master.h5'%( int(caget('XF:11IDB-ES{Det:Eig4M}cam1:SequenceId')) );
    
    print(fp, uid ) 
    
    try:
        update_olog_uid( uid= uid, text='file pattern: %s'%fp, attachments=None )
        print('Done!')
    except:
        print("I can't attach this!")
        
        
