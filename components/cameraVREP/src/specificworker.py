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

from genericworker import *
import vrep
import cv2
import math
import time
import numpy as np

# If RoboComp was compiled with Python bindings you can use InnerModel in Python
# sys.path.append('/opt/robocomp/lib')
# import librobocomp_qmat
# import librobocomp_osgviewer
# import librobocomp_innermodel

class SpecificWorker(GenericWorker):


	def __init__(self, proxy_map):
		super(SpecificWorker, self).__init__(proxy_map)
		clientID = vrep.simxStart('127.0.0.1',19997,True,True,5000,5)
		if clientID != -1:
			print ('Connected to remote API server')
			mode = vrep.simx_opmode_blocking
			# res, robot = vrep.simxGetObjectHandle(clientID,"hexapod", mode)
			res, camhandle = vrep.simxGetObjectHandle(clientID, 'ePuck_lightSensor', vrep.simx_opmode_oneshot_wait)
			res, resolution, image = vrep.simxGetVisionSensorImage(clientID, camhandle, 0, vrep.simx_opmode_streaming)

		self.timer.timeout.connect(self.compute)
		self.Period = 2000
		self.timer.start(self.Period)
		self.im = TImage()
		self.camhandle = camhandle
		self.clientID = clientID

	def __del__(self):
		print 'SpecificWorker destructor'

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
		#computeCODE


		return True


	#
	# getImage
	#
	def getImage(self):
		res, resolution, image = vrep.simxGetVisionSensorImage(self.clientID, self.camhandle, 0, vrep.simx_opmode_buffer)
		img = np.array(image, dtype = np.uint8)
		img.resize([resolution[1], resolution[0], 3])
		img = np.rot90(img,2)
		img = np.fliplr(img)
		img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
		
		# #
		im = TImage()
		im.image = img.data
		im.width, im.height, im.depth = img.shape

		return im
