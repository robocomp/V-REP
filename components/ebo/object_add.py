# This example illustrates how to create a pure shape(cuboid, sphere etc.) in the scene and get its handle
#
# Load the demo scene 'createPureShape.ttt' in V-REP, then 
# start the simulation and run this program.


import numpy as np
import time
try:
    import vrep
except:
    print ('--------------------------------------------------------------')
    print ('"vrep.py" could not be imported. This means very probably that')
    print ('either "vrep.py" or the remoteApi library could not be found.')
    print ('Make sure both are in the same folder as this file,')
    print ('or appropriately adjust the file "vrep.py"')
    print ('--------------------------------------------------------------')
    print ('')

import sys
import ctypes
print ('Program started')
vrep.simxFinish(-1) # just in case, close all opened connections
clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5) # Connect to V-REP

if clientID!=-1:
    print("Connected to the remote API server")
else:
    print("Not connected to the remote API server")
    sys.exit("Could not connect")

emptyBuff = bytearray()

# Send a code string to execute a function: createPureShape
# See the description: http://www.coppeliarobotics.com/helpFiles/en/regularApi/simCreatePureShape.htm
# See the description of simxCallScriptFunction: http://www.coppeliarobotics.com/helpFiles/en/remoteApiExtension.htm
# and http://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsPython.htm#simxCallScriptFunction
# Lua: use loadstring(str) to compile the code in string str
# Lua: use loadstring(str)() to get the return value, returned in lua code
code="obj_handle = sim.createPureShape(1, 001100, {0.1, 0.1, 0.1}, 0.5, {32, 16})\n" \
"return obj_handle"
res,retInts,retFloats,retStrings,retBuffer=vrep.simxCallScriptFunction(clientID,"remoteApiCommandServer",vrep.sim_scripttype_childscript,'addObject_function',[],[],[code],emptyBuff,vrep.simx_opmode_blocking)
if res==vrep.simx_return_ok:
    print ('Code execution successful')
    if retInts[0] != -1:
        obj_handle = retInts[0]
        # err_code, position = vrep.simxGetObjectPosition(clientID, obj_handle, -1, vrep.simx_opmode_streaming) # Get the current position of obj_handle
        # position[0] += 0.02 # changing the x position of the object by 0.02 m
        # err_code = vrep.simxSetObjectPosition(clientID, obj_handle, -1, position, vrep.simx_opmode_oneshot) # set the absolute position of the obj_handle to position
        print('object created')
else:
    print ('Remote function call failed')

# Now close the connection to V-REP:
vrep.simxFinish(clientID)
