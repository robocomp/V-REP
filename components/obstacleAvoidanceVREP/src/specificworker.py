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
import numpy as np

# If RoboComp was compiled with Python bindings you can use InnerModel in Python
# sys.path.append('/opt/robocomp/lib')
# import librobocomp_qmat
# import librobocomp_osgviewer
# import librobocomp_innermodel

class SpecificWorker(GenericWorker):
	def __init__(self, proxy_map):
		super(SpecificWorker, self).__init__(proxy_map)
		self.timer.timeout.connect(self.compute)
		self.Period = 2000
		self.timer.start(self.Period)

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

		while(1):    
			
			laserData = self.laser_proxy.getLaserData();
			obstacleData = [(laserData[i].dist, laserData[i].angle) for i in range(len(laserData))]
			
			# rotational velocity
			rot = 0.7
			
			# distance and angle corresponding to closest obstacle
			distance, angle = min(obstacleData)
			
			if distance < 50 and -30 <= angle <= 30:
				self.differentialrobot_proxy.setSpeedBase(0, rot)
			elif distance < 50 and (-120 >= angle or angle >= 120):
				self.differentialrobot_proxy.setSpeedBase(100, 0)
			elif distance > 50:
				self.differentialrobot_proxy.setSpeedBase(300, 0)


		return True

