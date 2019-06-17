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

# If RoboComp was compiled with Python bindings you can use InnerModel in Python
# sys.path.append('/opt/robocomp/lib')
# import librobocomp_qmat
# import librobocomp_osgviewer
# import librobocomp_innermodel

class SpecificWorker(GenericWorker):
	clientID = vrep.simxStart('192.168.1.40',19999,True,True,5000,5)
	if clientID != -1:
	    print ('Connected to remote API server')
	    mode = vrep.simx_opmode_blocking
	    res, robot = vrep.simxGetObjectHandle(clientID,"Plane", mode)
	    emptyBuff = bytearray()


	def __init__(self, proxy_map):
		super(SpecificWorker, self).__init__(proxy_map)
		self.timer.timeout.connect(self.compute)
		self.Period = 2000
		self.timer.start(self.Period)
		#path to the image EBO
		self.setImageFromFile("/home/carlos/Escritorio/hexapod/sad.png")

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

		return True


	#
	# setImageFromFile
	#
	def setImageFromFile(self, pathImg):
		#
		res,outInts,outFloats,outStrings,outBuffer=\
		vrep.simxCallScriptFunction(self.clientID,'EBO_Screen', vrep.sim_scripttype_childscript,\
		'applyTexture',[],[],[pathImg],self.emptyBuff, vrep.simx_opmode_blocking)
		#
		pass


	#
	# setImage
	#
	def setImage(self, img):
		#
		#implementCODE
		#
		pass
