#
# Copyright (C) 2019 by YOUR NAME HERE
#
#    This file is part of RoboComp
#
#    RoboComp is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    RoboComp is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with RoboComp.  If not, see <http://www.gnu.org/licenses/>.
#

import sys, os, traceback, time

from PySide import QtGui, QtCore
from genericworker import *
import vrep
import math
import numpy as np
import cv2

# If RoboComp was compiled with Python bindings you can use InnerModel in Python
# sys.path.append('/opt/robocomp/lib')
# import librobocomp_qmat
# import librobocomp_osgviewer
# import librobocomp_innermodel

class SpecificWorker(GenericWorker):
	def __init__(self, proxy_map):
		super(SpecificWorker, self).__init__(proxy_map)

		clientID = vrep.simxStart('127.0.0.1',19998,True,True,5000,5)
		if clientID != -1:
			print ('Connected to remote API server')
			mode = vrep.simx_opmode_blocking
			
			# getting the handle of the laser object 'fastHokuyo'
			res, laserHandle = vrep.simxGetObjectHandle(clientID,"fastHokuyo", mode)
			res, data = vrep.simxGetStringSignal(clientID,'measuredDataAtThisTime',vrep.simx_opmode_streaming)

		self.timer.timeout.connect(self.compute)
		self.Period = 2000
		self.timer.start(self.Period)

		self.laserHandle = laserHandle
		self.clientID = clientID

	def setParams(self, params):
		#try:
		#	self.innermodel = InnerModel(params["InnerModelPath"])
		#except:
		#	traceback.print_exc()
		#	print "Error reading config params"
		return True

	@QtCore.Slot()
	def compute(self):
		print 'SpecificWorker.compute...'

		return True


	#
	# getLaserData
	#
	def getLaserData(self):

		res, data = vrep.simxGetStringSignal(self.clientID,'measuredDataAtThisTime',vrep.simx_opmode_buffer)
		laserData = []
		if (data):
			# data unpacking
			laserDetectedPoints = vrep.simxUnpackFloats(data)

			# data loading in robocomp laserData format
			for i in range(0, len(laserDetectedPoints)-2, 3):
				x = laserDetectedPoints[i]
				y = laserDetectedPoints[i+1]
				z = laserDetectedPoints[i+2]

				singleLaser = TData()

				# angle and distance are relative to the laser sensor
				# x-axis of the laser points in the direction of movement of robot and z-axis is out of the plane

				# distance is in cm
				singleLaser.dist = (np.sqrt(x**2 + y**2))*100
				
				# angles is in degrees
				singleLaser.angle = math.degrees((y/x))
				laserData.append(singleLaser)

				# print(f'distance: {distance}      angle: {angle}')

		return laserData


	#
	# getLaserConfData
	#
	def getLaserConfData(self):
		ret = LaserConfData()
		#
		#implementCODE
		#
		return ret


	#
	# getLaserAndBStateData
	#
	def getLaserAndBStateData(self):
		ret = TLaserData()
		#
		#implementCODE
		#
		bState = RoboCompGenericBase.TBaseState()
		return [ret, bState]
