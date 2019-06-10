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
import sys
sys.path.insert(0, './vrep_api')
import vrep
import time

# If RoboComp was compiled with Python bindings you can use InnerModel in Python
# sys.path.append('/opt/robocomp/lib')
# import librobocomp_qmat
# import librobocomp_osgviewer
# import librobocomp_innermodel

class SpecificWorker(GenericWorker):
	clientID = vrep.simxStart('192.168.1.40',19997,True,True,5000,5)
	if clientID != -1:
	    print ('Connected to remote API server')
	    mode = vrep.simx_opmode_blocking
	    res, robot = vrep.simxGetObjectHandle(clientID,"hexapod", mode)
	    res, laser = vrep.simxGetObjectHandle(clientID,"LaserScannerLaser_2D", mode)
	    res, camhandle = vrep.simxGetObjectHandle(clientID, 'Vision_sensor', vrep.simx_opmode_oneshot_wait)
	    res, resolution, image = vrep.simxGetVisionSensorImage(clientID, camhandle, 0, vrep.simx_opmode_streaming)
	    res,data=vrep.simxGetStringSignal(clientID,'MySignal',vrep.simx_opmode_streaming)
	    time.sleep(1)

	def __init__(self, proxy_map):
		super(SpecificWorker, self).__init__(proxy_map)
		self.timer.timeout.connect(self.compute)
		self.Period = 2000
		self.timer.start(self.Period)
		self.laserData = []

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
		res,data=vrep.simxGetStringSignal(self.clientID,'MySignal',vrep.simx_opmode_buffer)
		if (data):
			laserDetectedPoints= vrep.simxUnpackFloats(data)

			for i in range(len(laserDetectedPoints)/2):
				singleLaser = TData()
				singleLaser.dist = laserDetectedPoints[2*i]
				singleLaser.angle = laserDetectedPoints[2*i+1]
				self.laserData.append(singleLaser)
			time.sleep(2)
		#try:
		#	self.differentialrobot_proxy.setSpeedBase(100, 0)
		#except Ice.Exception, e:
		#	traceback.print_exc()
		#	print e

		# The API of python-innermodel is not exactly the same as the C++ version
		# self.innermodel.updateTransformValues("head_rot_tilt_pose", 0, 0, 0, 1.3, 0, 0)
		# z = librobocomp_qmat.QVec(3,0)
		# r = self.innermodel.transform("rgbd", z, "laser")
		# r.printvector("d")
		# print r[0], r[1], r[2]

		return True


	#
	# getLaserData
	#
	def getLaserData(self):

		return self.laserData


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
