# This example illustrates how to move an object particularly "A primitive shape in V-REP"
# by changing its position at each iteration of the loop.
#
# Load the demo scene 'moveCuboidShape.ttt' in V-REP, then 
# start the simulation and run this program.


import numpy as np
import sys
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

err_code, cuboid_handle = vrep.simxGetObjectHandle(clientID, "Cuboid", vrep.simx_opmode_blocking) # To get the handle of the object named "Cuboid"
err_code, position = vrep.simxGetObjectPosition(clientID, cuboid_handle, -1, vrep.simx_opmode_streaming) # Get the current position of cuboid_handle

t = time.time() #record the initial time
while (time.time()-t)<10: #run for 10 seconds
    position[0] += 0.02 # changing the x position of the object by 0.02 m
    err_code = vrep.simxSetObjectPosition(clientID, cuboid_handle, -1, position, vrep.simx_opmode_oneshot)        
    #time.sleep(0.2)
    err_code, position = vrep.simxGetObjectPosition(clientID, cuboid_handle, -1, vrep.simx_opmode_buffer)

vrep.simxStopSimulation(clientID,vrep.simx_opmode_oneshot)
print("Done")