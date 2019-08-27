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
			data = self.camerasimple_proxy.getImage()
			arr = np.fromstring(data.image, np.uint8)
			img = np.reshape(arr, (data.width, data.height, data.depth))

			lightSens = [img[0, 1, 1], img[0, 7, 1], img[0, 14, 1]]
			v = 44
			omega = 0
			if lightSens and ((lightSens[0]<50)or(lightSens[1]<50)or(lightSens[2]<50)):
				if (lightSens[0]<50):
					omega = 0.7
				if (lightSens[2]<50):
					omega = -0.7
			else:
				v=44
				omega=0

			self.differentialrobot_proxy.setSpeedBase(v, omega)

		return True

