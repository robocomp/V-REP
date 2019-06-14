# This example illustrates how to move the motors in vrep and sense the obstacles in VREP
#
# Load the demo scene 'bubbleRob.ttt' in V-REP, then 
# start the simulation and run this program.


import vrep
import numpy as np
import time

vrep.simxFinish(-1) # just in case, close all opened connections
clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5)
print(clientID) # if 1, then we are connected.

if clientID!=-1:
    print ("Connected to remote API server")
else:
    print("Not connected to remote API server")
    sys.exit("Could not connect")

err_code,l_motor_handle = vrep.simxGetObjectHandle(clientID,"bubbleRob_leftMotor", vrep.simx_opmode_blocking)
err_code,r_motor_handle = vrep.simxGetObjectHandle(clientID,"bubbleRob_rightMotor", vrep.simx_opmode_blocking)

err_code,ps_handle = vrep.simxGetObjectHandle(clientID,"bubbleRob_sensingNose", vrep.simx_opmode_blocking)
err_code,detectionState,detectedPoint,detectedObjectHandle,detectedSurfaceNormalVector=vrep.simxReadProximitySensor(clientID,ps_handle,vrep.simx_opmode_streaming)

t = time.time() #record the initial time

while (time.time()-t)<10: #run for 20 seconds
    sensor_val = np.linalg.norm(detectedPoint)
    if sensor_val < 0.2 and sensor_val>0.01:
        l_steer = -1/sensor_val
    else:
        l_steer = 1.0
    err_code = vrep.simxSetJointTargetVelocity(clientID,l_motor_handle,l_steer,vrep.simx_opmode_streaming)
    err_code = vrep.simxSetJointTargetVelocity(clientID,r_motor_handle,1.0,vrep.simx_opmode_streaming)
    time.sleep(0.2)
    err_code,detectionState,detectedPoint,detectedObjectHandle,detectedSurfaceNormalVector=vrep.simxReadProximitySensor(clientID,ps_handle,vrep.simx_opmode_buffer)
    print (sensor_val,detectedPoint)
vrep.simxStopSimulation(clientID,vrep.simx_opmode_oneshot)
print("Done")