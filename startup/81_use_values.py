def set_abs_value( pv_prefix, abs_value ):       
    """
    Use an absolute value for a PV
    Input
    ---
    pv_prefix:string, the prefix of a pv, e.g., 'XF:11IDB-ES{Dif-Ax:YV}' for diff.yv
    abs_value, float, the absolute value to be set 
    
    Example:
    set_abs_value( 'XF:11IDB-ES{Dif-Ax:YV}', 0 ) #set diff.yv abolute value to 0
    """    
    pv_set = pv_prefix  + 'Mtr.VAL'
    pv_use_button = pv_prefix + 'Mtr.SET'
    caput( pv_use_button, 'Set')
    old_val = caget( pv_set )
    #import bluesky.plans as bp
    #yield from bp.abs_set( pv_set, abs_value)  not working
    caput( pv_set, abs_value )
    caput( pv_use_button, 'Use')
    print('The absolute value of %s was changed from %s to %s.'%(pv_set, old_val, abs_value))


