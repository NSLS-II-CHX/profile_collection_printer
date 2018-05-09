# -*- coding: utf-8 -*-
"""
Created on Tue May 23 16:00:48 2017
Modified 2017-06-06 V2 switched to class structure, added sorting for axis-mask and distance input.
Modified 2017-06-23 V3 Added Freerun

@author: Alexander Cook
"""

import ctypes as ct
import time
from enum import Enum
import collections
from math import sqrt

_AXES = ['X', 'Y', 'ZZ1', 'ZZ2', 'ZZ3', 'ZZ4', 'R', 'I', 'J']
_AXIS_INDEX = {'Y': 0, 'YY': 1, 'X': 2, 'ZZ1': 6, 'ZZ2': 7, 'ZZ3': 8, 'ZZ4': 9} 
_DEFAULT_RAPID_SPEED = {'Y': 50, 'X': 50, 'ZZ1': 20, 'ZZ2': 20, 'ZZ3': 20, 'ZZ4': 20} 

A3200_is_Open = False
A3200Lib = None
handle = None

class Axis_Mask(Enum):
    '''
    Meant to represent the c enums in the A3200 Library
    '''
    # All available axis masks.
    # No axes selected.
    AXISMASK_None = 0,

    Y      =  (1 <<  0), #1
    YY     = (1 <<  1), #2
    X      = (1 <<  2), #4
    ZZ1    = (1 <<  6), #8
    ZZ2    = (1 <<  7), #16
    ZZ3    = (1 <<  8), #32
    ZZ4    = (1 <<  9), #64
    #A      = (1 <<  7), #128


    #Maximum number of axes selected.
    AXISMASK_All = 0xffffffff
        
               
                            
    '''
    Unimplemented axis_masks
    
	AXISMASK_08 = (1 <<  8), #256
	AXISMASK_09 = (1 <<  9), #512

	AXISMASK_10 = (1 << 10), #1024
	AXISMASK_11 = (1 << 11), #2048
	AXISMASK_12 = (1 << 12), 
	AXISMASK_13 = (1 << 13),
	AXISMASK_14 = (1 << 14),
	AXISMASK_15 = (1 << 15),
	AXISMASK_16 = (1 << 16),
	AXISMASK_17 = (1 << 17),
	AXISMASK_18 = (1 << 18),
	AXISMASK_19 = (1 << 19),

	AXISMASK_20 = (1 << 20),
	AXISMASK_21 = (1 << 21),
	AXISMASK_22 = (1 << 22),
	AXISMASK_23 = (1 << 23),
	AXISMASK_24 = (1 << 24),
	AXISMASK_25 = (1 << 25),
	AXISMASK_26 = (1 << 26),
	AXISMASK_27 = (1 << 27),
	AXISMASK_28 = (1 << 28),
	AXISMASK_29 = (1 << 29),

	AXISMASK_30 = (1 << 30),
	AXISMASK_31 = (1 << 31),
        '''
    @classmethod
    def get_mask(cls, axes):
        '''
        Returns the sum of Axes masks for a given list of axes.
        '''
        #check if axes is iterable and not a string
        if isinstance(axes, collections.Iterable) and type(axes) is not str:
            mask = 0
            for ax in axes:
                try:
                    mask += cls[ax].value[0]
                except KeyError:
                    print("Invalid axis: {}".format(ax))
            return ct.c_ulong(mask)
        else:
            try:
                return ct.c_ulong(cls[axes].value[0])
            except KeyError:
                print("Invalid axis: {}".format(axes))
                return 0
                  
def name_to_index(name):
    if type(name) is str:
        #return _AXIS_INDEX[name]        
        #see if someone put an index in a string:
        try: 
            return int(name)
        except ValueError:
            try:
                return _AXIS_INDEX[name]
            except KeyError:
                print("invalid axis")
            
    else:
        #assume it's a proper index
        return name
    
def coords_to_basic(axes, coords, move_type = 'linear', percision = 3, min_move = 0.0005):
    '''
    Take a list of coordinate values and translate to a string of aerobasic.
    
    Coordinated Execution may be limited to four axes due to ITAR restrictions.
    
    Input:
        axes: a list of the axes to make the moves on eg ['x', 'y', 'z']
        coords: list of lists of distances eg [[1, 2, 3], [2, 3, 4]]
        move_type: a list of the aerobasic movement types/commands eg 'linear' or 'cw'
        percision: the percision to which to round the move coordinates
        min_move: moves on axes smaller than this will not be included in the command
    output:
        a string containing the movement command(s)
    '''
    command = ""
    #ensure that we're dealing with a list of coordinates and not a single coord
    if not isinstance(axes, collections.Iterable) or type(axes) is str:
        axes = [axes]
        coords = [coords]
    #check to see if we're using the default linear moves
    if move_type == 'linear':
        g = ['linear' for a in axes]
    else:
        g = move_type
    for j in range(len(coords)):
        line = g
        eol = '\n'
        for i in range(len(axes)):
            #check to make sure it is a valid axis
            if axes[i] in _AXES:
                if abs(coords[j][i]) > min_move: #cut out axes which are nearly zero
                    line += "{a} {v:0.{p}f} ".format(a = axes[i], v = coords[j][i], p = percision)
            else:
                if 'F' or 'f' in axes[i]:
                    eol = "F{v:0.{p}f}".format(coords[j][i], p = percision) + eol
        line += eol
        command += line        
    return command

def dict_coords_to_basic(coords, percision = 3, min_move = 0.0005):
    '''
    Take a list of dictionary coordinate values and translate to a string of aerobasic.
    
    This allows for arbitrary specification of coordinates at each move, nessecary
        if using more than 4 axes.
        
    Input:
        coords: list of dict items eg [{'move_type': 'linear', 'X': 1, 'Y': 2, 'F': 3}]
        percision: the percision to which to round the move coordinates
        min_move: moves on axes smaller than this will not be included in the command
    output:
        a string containing the movement command(s)
    '''
    command = ""
    if isinstance(coords, collections.Iterable) and type(coords) is not dict:
        for coord in coords:
            if 'move_type' in coord.keys():
                line = coord['move_type']
            else:
                line = "Linear "
            eol = '\n'
            for axis, value in coord.items():
                if axis in _AXES:
                    if abs(value) > min_move: #cut out axes which are nearly zero
                        line += "{a} {v:0.{p}f} ".format(a = axis, v = value, p = percision)
                else:
                    if 'F' or 'f' in axis:
                        eol = "F{v:0.{p}f}".format(v = value, p = percision) + eol
            line += eol
            command += line
    else:
        if 'move_type' in coord.keys():
            line = coord['move_type']
        else:
            line = "Linear "
        eol = '\n'
        for axis, value in coord.items():
            line = "Linear "
            eol = '\n'
            for axis, value in coord.items():
                if axis in _AXES:
                    if abs(value) > min_move: #cut out axes which are nearly zero
                          line += "{a} {v:0.{p}f} ".format(a = axis, v = value, p = percision)
                else:
                    if 'F' or 'f' in axis:
                        eol = "F{v:0.{p}f}".format(v = value, p = percision) + eol
            line += eol
            command += line
        line += eol
        command += line
    return command        

def sort_axes(axes, distances):
    '''
    Sorts axes and distances in order of the axis indicies specified in _AXIS_INDEX.
    
    Input:
        axes: list of axes in string or int(index) format
        distances: the distances you wish to travel along axes, ordered respective of
            axes.
    Output: (sorted_axes, sorted_distances)
        sorted_axes: list of the axis strings or indicies sorted as specified
        sorted_distances: list of distances sorted respective of axes
    '''
    sortedaxes = []
    sorteddistances = []
    inserted = False
    if type(axes[0]) is str:
        for a, d in zip(axes, distances):
            if len(sortedaxes) > 0:
                inserted = False
                #scan through the list and figure out where to stick the latest axis
                for i in range(len(sortedaxes)):
                    if _AXIS_INDEX[a] < _AXIS_INDEX[sortedaxes[i]] and not inserted:
                        sortedaxes.insert(i, a)
                        sorteddistances.insert(i, d)
                        inserted = True
                if not inserted:
                    #add element to the end
                    sortedaxes.append(a)
                    sorteddistances.append(d)
            else:
                #for first element
                sortedaxes.append(a)
                sorteddistances.append(d)
    else:
        #assume axes are specified by index number
        for a, d in zip(axes, distances):
            if len(sortedaxes) > 0:
                inserted = False
                #scan through the list and figure out where to stick the latest axis
                for i in range(len(sortedaxes)):
                    if a < sortedaxes[i] and not inserted:
                        sortedaxes.insert(i, a)
                        sorteddistances.insert(i, d)
                        inserted = True
                if not inserted:
                    #add element to the end
                    sortedaxes.append(a)
                    sorteddistances.append(d)
            else:
                #for first element
                sortedaxes.append(a)
                sorteddistances.append(d)
    return sortedaxes, sorteddistances
                

class A3200():
    def __init__(self, connect = True, default_task = 1):
        if connect:
            self.A3200_is_Open = False
            self.handle, self.A3200Lib = self.connect()
            if self.handle is not None:
                self.A3200_is_open = True
            else:
                self.A3200_is_open = False
            #these are required to make the function calls behave
            self.A3200Lib.A3200StatusGetItem.argtypes = [ct.c_void_p, ct.wintypes.WORD, ct.wintypes.DWORD, ct.wintypes.DWORD, ct.POINTER(ct.c_double)]
            self.A3200Lib.A3200StatusGetItem.restypes = ct.c_bool
        else:
            self.A3200_is_open = False
        #set this so that the other functions can use it as a default.
        self.task = default_task
        
            
    def enable(self, axes, task = -1):
        '''
        Enable the axes specified in axes.
        
        task- taskID
        axes- axismask, array or string of axes
        
        returns true (1) if successful.
        '''
        if self.A3200_is_Open:
            #sum the axes
            ax_mask = Axis_Mask.get_mask(axes)
            if task < 0:
                return self.A3200Lib.A3200MotionEnable(self.handle, self.task, ax_mask)
            else:
                return self.A3200Lib.A3200MotionEnable(self.handle, task, ax_mask)

    def disable(self, axes, task = -1):
        '''
        disable the axes specified in axes.
        
        task- taskID
        axes- axismask, array or string of axes
        
        returns true (1) if successful.
        '''
        if self.A3200_is_Open:
            #sum the axes
            ax_mask = Axis_Mask.get_mask(axes)
        if task < 0:    
            return self.A3200Lib.A3200MotionDisable(self.handle, self.task, ax_mask)    
        else:
            return self.A3200Lib.A3200MotionDisable(self.handle, task, ax_mask)    

    def home(self, axes, task = -1):
        '''
        Homes the axes specified in axes.
        
        task- taskID
        axes- axismask, array or string of axes
        
        returns true (1) if successful.
        '''
        if self.A3200_is_Open:
            #sum the axes
            ax_mask = Axis_Mask.get_mask(axes)
            if task < 0:
                return self.A3200Lib.A3200MotionHome(self.handle, self.task, ax_mask)    
            else:
                return self.A3200Lib.A3200MotionHome(self.handle, task, ax_mask)    

    def abort(self, axes):
        '''
        Aborts the motion on the specified axes, returns when abort starts.
        
        axes- axismask, array or string of axes
        
        returns true (1) if successful.
        '''
        if self.A3200_is_Open:
            #sum the axes
            ax_mask = Axis_Mask.get_mask(axes)
            return self.A3200Lib.A3200MotionAbort(self.handle, ax_mask)    

    def rapid(self, axes, distance, speed = None, task = -1):
        '''
        Make a linear coordinated point to point motion on axes a specifed distance.
        
        Note: will fail (not execute) if more than four axes are specified and ITAR controls
                        are enabled.
        
        Input:
            axes: a list of axes or string containing one axis
            distance: the distances to move along the axes, in the same respective order
            speed: the speed each axis should move at in the same order
                    if not specified, defaults to the max speed.
            task: task to execute the move on
        Returns:
            1 if successful
        '''
        if self.A3200_is_Open:
            #need to convert distance into an array structure
            if isinstance(distance, collections.Iterable):
                #need to arrange the distances in order of the axis index
                sort_ax, sort_dist = sort_axes(axes, distance)
                d = (ct.c_double*len(sort_dist))()
                for i in range(len(sort_dist)):
                    d[i] = ct.c_double(sort_dist[i])
            else:
                d = ct.c_double(distance)
            if speed is not None:
                #same things for the speed
                if isinstance(speed, collections.Iterable):
                    #need to arrange the distances in order of the axis index
                    sort_ax, sort_dist = sort_axes(axes, speed)
                    v = (ct.c_double*len(sort_dist))()
                    for i in range(len(sort_dist)):
                        v[i] = ct.c_double(sort_dist[i])
                else:
                    v = ct.c_double(speed)
            else:
                #use default max speeds if it is not specified
                if isinstance(distance, collections.Iterable):
                    s = []
                    for a in sort_ax:
                        s.append(_DEFAULT_RAPID_SPEED[a])
                    v = (ct.c_double*len(sort_dist))()
                    for i in range(len(sort_ax)):
                        v[i] = ct.c_double(s[i])    
                else:
                    v = ct.c_double(_DEFAULT_RAPID_SPEED[axes])
            #sum the axes
            ax_mask = Axis_Mask.get_mask(axes)
            if task < 0:
                return self.A3200Lib.A3200MotionRapid(self.handle, self.task, ax_mask, d, v)    
            else:
                return self.A3200Lib.A3200MotionRapid(self.handle, task, ax_mask, d, v) 

    def linear(self, axes, distance, task = -1):
        '''
        Make a linear coordinated point to point motion on axes a specifed distance.
        
        Note: will fail (not execute) if more than four axes are specified and ITAR controls
                        are enabled.
        
        Input:
            axes: a list of axes or string containing one axis
            distance: the distances to move along the axes, in the same respective order
            task: task to execute the move on
        '''
        if self.A3200_is_Open:
            #need to convert distance into an array structure
            if isinstance(distance, collections.Iterable):
                #need to arrange the distances in order of the axis index
                sort_ax, sort_dist = sort_axes(axes, distance)
                d = (ct.c_double*len(sort_dist))()
                for i in range(len(sort_dist)):
                    d[i] = ct.c_double(sort_dist[i])
            else:
                d = ct.c_double(distance)
            #sum the axes
            ax_mask = Axis_Mask.get_mask(axes)
            if task < 0:
                return self.A3200Lib.A3200MotionLinear(self.handle, self.task, ax_mask, d)    
            else:
                return self.A3200Lib.A3200MotionLinear(self.handle, task, ax_mask, d)    

    def freerun(self, axis, speed, task = -1):
        '''
        Set the axis into freerun mode at speed.
        
        Input:
            axis: an axis on which to operate
            speed: the speed at which to run
            task: the task to operate on, defaults to self.task
        Return:
            1 if successful
        '''
        if self.A3200_is_Open:
            axis_index = name_to_index(axis)
            f = ct.c_double(speed)
            if task < 0:
                return self.A3200Lib.A3200MotionFreeRun(self.handle, self.task, axis_index, f)
            else:
                return self.A3200Lib.A3200MotionFreeRun(self.handle, task, axis_index, f)

    def stop_freerun(self, axis, task = -1):
        '''
        Stops the axis which is freerunning.
        
        Input:
            axis: an axis on which to operate
            speed: the speed at which to run
            task: the task to operate on, defaults to self.task
        Return:
            1 if successful
        '''
        if self.A3200_is_Open:
            axis_index = name_to_index(axis)
            if task < 0:
                return self.A3200Lib.A3200MotionFreeRunStop(self.handle, self.task, axis_index)
            else:
                return self.A3200Lib.A3200MotionFreeRunStop(self.handle, task, axis_index)

    def wait_for_move_done(self, axes, mode = 'move_done', timeout = -1):
        if self.A3200_is_Open:
            if 'in_position' in mode:
                wait_mode = ct.c_ulong(1)
            else:
                wait_mode = ct.c_ulong(0)
            timeout = ct.wintypes.DWORD(timeout)    
            ax_mask = Axis_Mask.get_mask(axes)
            ret_timeout = ct.c_bool(False)
            success = self.A3200Lib.A3200MotionWaitForMotionDone(self.handle, ax_mask, wait_mode, timeout, ct.byref(ret_timeout))
            return success, ret_timeout.value


    def cmd_exe(self, command, task = -1, ret = False):
        '''
        Execute an aerobasic command.
        
        Inputs:
            command: a string containing the command as it would be writen in aerobasic
            task:    the task to run the command on, defaults to self.task
            ret:     specify the return type, defaults to no return
            
        Returns:
            the specified return type for the command (NYI)
        '''
        if self.A3200_is_Open:
            cmd = ct.wintypes.LPCSTR(command.encode('utf-8'))
            if task < 0:
                self.A3200Lib.A3200CommandExecute(self.handle, self.task, cmd , None)
            else:
                self.A3200Lib.A3200CommandExecute(self.handle, task, cmd , None)



    ######IO Functions ######
    
    def AI(self, axis, channel, task = -1):
        '''
        returns the value of analog input channel on axis
        
        Input:
            Channel- DWORD (int)
            axis-    axis mask string or integer index
        Output:
            (success/fail, value)
        '''
        if self.A3200_is_Open:
            a = ct.c_int(name_to_index(axis))
            c = ct.wintypes.DWORD(channel)
            ret = ct.c_double(0)
            if task < 0:
                s = self.A3200Lib.A3200IOAnalogInput(self.handle, self.task, c, a, ct.byref(ret))
            else:
                s = self.A3200Lib.A3200IOAnalogInput(self.handle, task, c, a, ct.byref(ret))
            return s, ret.value

    def AO(self, axis, channel, value, task = -1):
        '''
        Sets the AO channel on axis to value.
        
        Input:
            Channel- DWORD (int)
            axis-   axis mask string or integer index
            value - float specifying the output voltage
        Output:
            returns 1 if successful
        '''
        if self.A3200_is_Open:
            a = ct.c_int(name_to_index(axis))
            c = ct.wintypes.DWORD(channel)
            v = ct.c_double(value)
            if task < 0:
                return self.A3200Lib.A3200IOAnalogOutput(self.handle, self.task, c, a, v)
            else:
                return self.A3200Lib.A3200IOAnalogOutput(self.handle, task, c, a, v)
                
    def DI(self, axis, bit, task = -1):
        '''
        returns the value of the digital bit on axis
        
        Input:
            Channel- DWORD (int)
            axis-    axis mask string or integer index
            task: task to run the query on
        Output:
            (s, v)
            s - 1  if successful
            v - the True/False::1/0 value of the bit
        '''
        if self.A3200_is_Open:
            a = ct.c_int(name_to_index(axis))
            c = ct.wintypes.DWORD(bit)
            ret = ct.wintypes.DWORD()
            if task < 0:
                s = self.A3200Lib.A3200IODigitalInput(self.handle, self.task, c, a, ct.byref(ret))
            else:
                s = self.A3200Lib.A3200IODigitalInput(self.handle, self.task, c, a, ct.byref(ret))
            return s, bool(ret.value)
        
    def DO(self, axis, bit, value, task = -1):
        '''
        Sets the digital out bit on axis to value.
        
        Input
            Channel- DWORD (int)
            axis-    axis mask string or integer index
            value:   Boolean or int value to set the bit
        Output
            1 if successful
        '''
        if self.A3200_is_Open:
            a = ct.c_int(name_to_index(axis))
            c = ct.wintypes.DWORD(bit)
            v = ct.wintypes.DWORD(value)
            if task < 0:
                return self.A3200Lib.A3200IODigitalOutput(self.handle, self.task, c, a, v)
            else:
                return self.A3200Lib.A3200IODigitalOutput(self.handle, task, c, a, v)

    ###### Status Functions ######
    
    def get_position(self, axes, returntype = list):
        '''
        Get the program position feedback of axes.
        
        For some reason only works simultaineously with X, Y or individual ZZ# axes
        Input:
            axes: list of axes to query the position of
            returntype: preferred returntype, list or dict
        Output:
            list or dict of the axis program position feedback, None if unsuccessful
        '''
        if self.A3200_is_Open:
            ax = {}
            if type(axes) is list:
                for a in axes:
                    ax[a] = name_to_index(a)
            else:
                ax[axes] = name_to_index(axes)
                
            n = ct.wintypes.DWORD(1)
            s = 107
            item_code = ct.wintypes.DWORD(s)
            s = 0
            extras = ct.wintypes.DWORD(s)
            ret = ct.c_double()
            
            values = {}
            for k in ax.keys():
                item_index = ct.wintypes.WORD(ax[k])
                s = self.A3200Lib.A3200StatusGetItem(self.handle, item_index, item_code, extras, ret)
                if s == 1:
                    values[k] = ret.value
            print(values)
            if s == 1:
                if type(axes) is str:
                    #ie if we just have one axis
                    return values[axes]
                else:
                    if returntype is list:
                        return [values[i] for i in axes]
                    else:
                        return values
            else:  
                return None
    
    def absolute(self, task = -1):
        '''
        Sets the motion to absolute mode
        '''
        s = 0
        if task < 0:
            s = self.A3200Lib.A3200MotionSetupAbsolute(self.handle, self.task)
        else:
            s = self.A3200Lib.A3200MotionSetupAbsolute(self.handle, task)
        if s == 1:
            self.motion_mode = 'absolute'    
        return s        
    
    def incremental(self, task= - 1):
        '''
        Sets the motion to incremental mode
        '''
        s = 0
        if task < 0:
            s = self.A3200Lib.A3200MotionSetupIncremental(self.handle, self.task)
        else:
            s = self.A3200Lib.A3200MotionSetupIncremental(self.handle, task)
        if s == 1:
            self.motion_mode = 'incremental'    
        return s    
        
    def setup_functions(self):
        '''
        Some functions require arg and return types to be set, this function does so.
        '''    
        self.A3200Lib.A3200MotionLinear.argtypes = [ct.c_void_p, ct.c_uint, ct.c_ulong, ct.POINTER(ct.c_double)]
        self.A3200Lib.A3200MotionLinear.restypes = ct.c_bool
        self.A3200Lib.A3200CommandExecute.argtypes = [ct.c_void_p, ct.c_uint, ct.wintypes.LPCSTR,ct.POINTER(ct.c_double)]
        self.A3200Lib.A3200CommandExecute.restypes = ct.c_bool
    
    def connect(self):
        '''
        Connect to the A3200 and return a handle.
        
        Returns None if not successful.
        '''
        if not self.A3200_is_Open:
            self.A3200Lib = ct.windll.A3200C    
            self.handle = ct.c_void_p()
            if self.A3200Lib.A3200Connect(ct.byref(self.handle)):
                print('success')
                self.A3200_is_Open = True
                return self.handle, self.A3200Lib
            else:
                self.A3200_is_Open = False
                return None
        else:
            #if already open, just return the handly and lib handle
            return self.A3200Lib, self.handle
        
    def disconnect(self):
        '''
        Disconnect from the A3200
        
        Return 1 if successful.
        '''
        if self.A3200_is_Open:
            return self.A3200Lib.A3200Disconnect(self.handle)


#for testing purposes only
if __name__ == '__main__':
    a = A3200()    
    '''
    vertex = [-399.36435095978686, -386.62441417323356]
    corner = [-474.2742791608757, -464.8843769613714]
    d = []
    for r, c in zip(vertex, corner):
        print(r - c)
        d.append(r-c)
    #a.linear(['X', 'Y'], d)
    a.linear(['X', 'Y'], [3*sqrt(3), 3])
    '''
    start = a.get_position(['X', 'Y'])
    print(start)
    '''
    for i in range(1):
        a.DO('ZZ1', 2, 1)
        time.sleep(1)
        a.DO('ZZ1', 2, 0)
        time.sleep(1)
    
    for r, c in zip(start, corner):
        print(r - c)
    '''
    a.disconnect()    
    