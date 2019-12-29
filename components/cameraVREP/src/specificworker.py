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

class SpecificWorker(GenericWorker):
	def __init__(self, proxy_map):
		super(SpecificWorker, self).__init__(proxy_map)
		clientID = vrep.simxStart('127.0.0.1',19999,True,True,5000,5)
		if clientID != -1:
			print('Connected to remote API server')
			mode = vrep.simx_opmode_blocking
			#res, camhandle = vrep.simxGetObjectHandle(clientID, 'ePuck_lightSensor', vrep.simx_opmode_oneshot_wait)
			res, self.camhandle = vrep.simxGetObjectHandle(clientID, 'camera_2_rgb', vrep.simx_opmode_oneshot_wait)
			res, camDhandle = vrep.simxGetObjectHandle(clientID, 'camera_2_depth', vrep.simx_opmode_oneshot_wait)
			res, resolution, image = vrep.simxGetVisionSensorImage(clientID, self.camhandle, 0, vrep.simx_opmode_oneshot_wait)
			resD, resolutionD, depth = vrep.simxGetVisionSensorDepthBuffer(clientID, camDhandle, vrep.simx_opmode_oneshot_wait)

		if self.camhandle < 0:
			sys.exit()
		#self.camhandle = camhandle
		self.camDhandle = camDhandle
		self.clientID = clientID

		self.timer.timeout.connect(self.compute)
		self.Period = 50
		self.timer.start(self.Period)
		
		
	def __del__(self):
		print('SpecificWorker destructor')

	def setParams(self, params):
		return True

	@QtCore.Slot()
	def compute(self):
		
		res, resolution, image = vrep.simxGetVisionSensorImage(self.clientID, self.camhandle, 0, vrep.simx_opmode_oneshot_wait)
		if res is not 0:
			sys.exit()
		img = np.array(image, dtype = np.uint8)
		img.resize([resolution[1], resolution[0], 3])
		img = cv2.flip(img, 0)
		self.image = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
		#print(len(img.flatten()))

		#resD, resolutionD, depth = vrep.simxGetVisionSensorDepthBuffer(self.clientID, self.camDhandle, vrep.simx_opmode_buffer)
		
		# imgD = np.array(depth, dtype = np.float32)
		# imgD.resize([resolutionD[1], resolutionD[0], 1])
		# imgD = cv2.resize(imgD, (0, 0), None, .5, .5)
		# #imgD = np.rot90(imgD,2)
		# #imgD = np.fliplr(imgD)
		# imgD = cv2.normalize(imgD, None, alpha = 0, beta = 1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
		# imgDD = cv2.cvtColor(imgD, cv2.COLOR_GRAY2BGR)

		# horizontal_concat = np.concatenate((img, imgDD), axis=1)

		#cv2.imshow("ALab_CameraD_0", horizontal_concat)
		
		cv2.imshow("ALab_CameraD_0", self.image)
		
	
		return True

# =============== STUB ==============================================
# ===================================================================
	#
	# getAll
	#
	def getAll(self):
		#
		# implementCODE
		#
		im = TImage()
		dep = TDepth()
		return [im, dep]

	#
	# getDepth
	#
	def getDepth(self):
		resD, resolutionD, depth = vrep.simxGetVisionSensorDepthBuffer(self.clientID, self.camDhandle, vrep.simx_opmode_buffer)
		imgD = np.array(depth, dtype = np.float32)
		imgD.resize([resolutionD[1], resolutionD[0], 1])
		imgD = cv2.flip(imgD, 0)
		#
		dep = TDepth()
		dep.image = dep.data
		dep.width, dep.height = img.shape[:2]
		return dep

	#
	# getImage
	#
	def getImage(self):
		im = TImage()
		im.image = self.image.flatten()
		im.width, im.height, im.depth = self.image.shape
		print("returning image", self.image.shape)
		return im

# ===================================================================
# ===================================================================



	#
	# getImage
	#
	# def getImage(self):
	# 	res, resolution, image = vrep.simxGetVisionSensorImage(self.clientID, self.camhandle, 0, vrep.simx_opmode_buffer)
	# 	img = np.array(image, dtype = np.uint8)
	# 	img.resize([resolution[1], resolution[0], 3])
	# 	img = np.rot90(img,2)
	# 	img = np.fliplr(img)
	# 	img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
		
	# 	# #
	# 	im = TImage()
	# 	im.image = img.data
	# 	im.width, im.height, im.depth = img.shape

	# 	return im
