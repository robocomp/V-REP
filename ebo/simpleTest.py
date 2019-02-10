# Make sure to have the server side running in V-REP: 
# in a child script of a V-REP scene, add following command
# to be executed just once, at simulation start:
#
# simRemoteApi.start(19999)
#
# then start simulation, and run this program.
#
# IMPORTANT: for each successful call to simxStart, there
# should be a corresponding call to simxFinish at the end!

import vrep
import time
import random
import math

vrep.simxFinish(-1) # just in case, close all opened connections
clientID = vrep.simxStart('127.0.0.1',19999,True,True,5000,5) # Connect to V-REP

if clientID != -1:
    print ('Connected to remote API server')
    mode = vrep.simx_opmode_blocking
    res, robot = vrep.simxGetObjectHandle(clientID,"remoteApiControlledBubbleRob", mode) 
    res, leftMotor = vrep.simxGetObjectHandle(clientID,"remoteApiControlledBubbleRobLeftMotor", mode) 
    res, rightMotor = vrep.simxGetObjectHandle(clientID,"remoteApiControlledBubbleRobRightMotor", mode) 
    res, laser = vrep.simxGetObjectHandle(clientID,"remoteApiControlledBubbleRobSensingNose", mode) 

    while True:
        res, pos = vrep.simxGetObjectPosition(clientID, robot, -1, mode)
        res, detected, closest_point, object_handle, normal = vrep.simxReadProximitySensor(clientID, laser, mode)
        dist = math.sqrt(closest_point[0]*closest_point[0]+closest_point[1]*closest_point[1])
        #print(detected, closest_point, dist)
        if detected and dist < 0.3: 
            res = vrep.simxSetJointTargetVelocity(clientID, leftMotor, -3, mode)
            res = vrep.simxSetJointTargetVelocity(clientID, rightMotor,-1 , mode)
            time.sleep(1)
        res = vrep.simxSetJointTargetVelocity(clientID, leftMotor, 3, mode)
        res = vrep.simxSetJointTargetVelocity(clientID, rightMotor, 3 , mode)
   
    # Before closing the connection to V-REP, make sure that the last command sent out had time to arrive. You can guarantee this with (for example):
    vrep.simxGetPingTime(clientID)

    # Now close the connection to V-REP:
    vrep.simxFinish(clientID)
else:
    print ('Failed connecting to remote API server')
print ('Program ended')
