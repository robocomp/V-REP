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
		self.cameraid = int(params["cameraid"])  # range must be controlled 1..MAX_CAMERAS
		self.display = "true" in params["display"]
		self.callapriltags = "true" in params["callapriltags"]
		self.initialize()
		return True

	def initialize(self):
		self.client = b0RemoteApi.RemoteApiClient('b0RemoteApi_pythonClient','b0RemoteApiAddOn')
		self.wall_camera = self.client.simxGetObjectHandle('camera_' + str(self.cameraid) + '_rgb',self.client.simxServiceCall())
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

#		self.camerargbdsimplepub_proxy.pushRGBD(self.t_image, TDepth())

		if self.callapriltags:
			self.getAprilTags(image, resolution)
		
		if self.display:
			self.displayImage(image, resolution)

		return True

	def displayImage(self, image, resolution):
		img = np.fromstring(image, np.uint8).reshape( resolution[1],resolution[0], 3)
		img = cv2.flip(img, 0)
		img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
		cv2.drawMarker(img, (int(resolution[0]/2), int(resolution[1]/2)),  (0, 0, 255), cv2.MARKER_CROSS, 100, 1);
		cv2.imshow("ALab_Camera_" + str(self.cameraid), img)
		cv2.waitKey(1)
		if time.time() - self.start() > 1:
			print("FPS:", cont)
			self.start = time.time()
			self.contFPS = 0
		self.contFPS += 1
	
	def getAprilTags(self, image, resolution):
		try:
			frame = Image()
			#frame.data = img.flatten()
			frame.data = image
			frame.frmt = Format(Mode.RGB888Packet, resolution[0], resolution[1], 3)
			frame.timeStamp = time.time()
			# 280 porque es la parte de negro que ocupa todo el png
			tags_list = self.apriltagsserver_proxy.getAprilTags(frame=frame, tagsize=280, mfx=462, mfy=462);
			if len(tags_list) > 0:
				dist = np.sqrt(tags_list[0].tx*tags_list[0].tx+tags_list[0].ty*tags_list[0].ty+tags_list[0].tz*tags_list[0].tz)
			else:
				dist = 0
			print(frame.timeStamp, tags_list,dist)
		except Ice.Exception as ex:
			print(ex)

# =============== STUB ==============================================
# ===================================================================
	#
	# getImage
	#
	def CameraRGBDSimple_getImage(self):
		#ml = QMutexLocker(self.mutex)
		#print("returning image", self.t_image.width, self.t_image.height, self.t_image.depth)
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



# res, resolution, image = vrep.simxGetVisionSensorImage(self.clientID, self.camhandle, 0, vrep.simx_opmode_oneshot_wait)
		# if res is not 0:
		# 	sys.exit()

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
