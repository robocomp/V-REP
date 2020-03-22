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
from PySide2.QtCore import QMutexLocker
import vrep
import cv2
import math
import time
import numpy as np
import b0RemoteApi

class SpecificWorker(GenericWorker):
	def __init__(self, proxy_map):
		super(SpecificWorker, self).__init__(proxy_map)

		self.t_image = TImage()
		self.t_depth = TDepth()
		self.timer.timeout.connect(self.compute)
		self.Period = 50
		self.timer.start(self.Period)
		self.contFPS = 0


	def __del__(self):
		print('SpecificWorker destructor')

	def setParams(self, params):
		print("Reading params")
		self.cameraid = int(params["cameraid"])  # range must be controlled 1..MAX_CAMERAS
		self.display = "true" in params["display"]
		self.publish = "true" in params["publish"]
		self.cameraName = params["cameraName"]
		self.initialize()
		return True

	def initialize(self):
		print("Initialize")
		self.client = b0RemoteApi.RemoteApiClient('b0RemoteApi_pythonClient','b0RemoteApiAddOn')
		self.wall_camera = self.client.simxGetObjectHandle(self.cameraName,self.client.simxServiceCall())
		self.start = time.time()

	@QtCore.Slot()
	def compute(self):
		res, resolution, image = self.client.simxGetVisionSensorImage(self.wall_camera[1],False, self.client.simxServiceCall())
		depth_res, depth_resolution, depth = self.client.simxGetVisionSensorDepthBuffer(self.wall_camera[1],True, True, self.client.simxServiceCall())
	
		if not res:
			return

		self.t_image.image = image
		self.t_image.width = resolution[0]
		self.t_image.height = resolution[1]
		self.t_image.depth = 3
		
		self.t_depth.depth = depth
		self.t_depth.width = resolution[0]
		self.t_depth.height = resolution[1]

		if self.publish:
			self.camerargbdsimplepub_proxy.pushRGBD(self.t_image, self.t_depth)

		if self.display:
			self.displayImage(image, resolution)

		return True

	def displayImage(self, image, resolution):
		img = np.fromstring(image, np.uint8).reshape( resolution[1],resolution[0], 3)
		img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
		cv2.drawMarker(img, (int(resolution[0]/2), int(resolution[1]/2)),  (0, 0, 255), cv2.MARKER_CROSS, 100, 1);
		cv2.imshow(self.cameraName, img)
		cv2.waitKey(1)
		if time.time() - self.start > 1:
			print("FPS:", self.contFPS)
			self.start = time.time()
			self.contFPS = 0
		self.contFPS += 1
	

# =============== STUB ==============================================
# ===================================================================
	#
	# getImage
	#
	def CameraRGBDSimple_getImage(self):
		return self.t_image
	#
	# getAll
	#
	def CameraRGBDSimple_getAll(self):
		return (self.t_image, self.t_depth)

	#
	# getDepth
	#
	def CameraRGBDSimple_getDepth(self):
		return self.t_depth

# ===================================================================
# ===================================================================
