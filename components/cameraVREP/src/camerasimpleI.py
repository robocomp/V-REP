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

import sys, os, Ice

ROBOCOMP = ''
try:
	ROBOCOMP = os.environ['ROBOCOMP']
except:
	print('$ROBOCOMP environment variable not set, using the default value /opt/robocomp')
	ROBOCOMP = '/opt/robocomp'
if len(ROBOCOMP)<1:
	print('ROBOCOMP environment variable not set! Exiting.')
	sys.exit()

additionalPathStr = ''
icePaths = []
try:
	icePaths.append('/opt/robocomp/interfaces')
	SLICE_PATH = os.environ['SLICE_PATH'].split(':')
	for p in SLICE_PATH:
		icePaths.append(p)
		additionalPathStr += ' -I' + p + ' '
except:
	print('SLICE_PATH environment variable was not exported. Using only the default paths')
	pass

ice_CameraRGBDSimple = False
for p in icePaths:
	print('Trying', p, 'to load CameraRGBDSimple.ice')
	if os.path.isfile(p+'/CameraRGBDSimple.ice'):
		print('Using', p, 'to load CameraRGBDSimple.ice')
		preStr = "-I/opt/robocomp/interfaces/ -I"+ROBOCOMP+"/interfaces/ " + additionalPathStr + " --all "+p+'/'
		wholeStr = preStr+"CameraRGBDSimple.ice"
		Ice.loadSlice(wholeStr)
		ice_CameraRGBDSimple = True
		break
if not ice_CameraRGBDSimple:
	print('Couldn\'t load CameraRGBDSimple')
	sys.exit(-1)
from RoboCompCameraRGBDSimple import *
ice_CameraRGBDSimplePub = False
for p in icePaths:
	print('Trying', p, 'to load CameraRGBDSimplePub.ice')
	if os.path.isfile(p+'/CameraRGBDSimplePub.ice'):
		print('Using', p, 'to load CameraRGBDSimplePub.ice')
		preStr = "-I/opt/robocomp/interfaces/ -I"+ROBOCOMP+"/interfaces/ " + additionalPathStr + " --all "+p+'/'
		wholeStr = preStr+"CameraRGBDSimplePub.ice"
		Ice.loadSlice(wholeStr)
		ice_CameraRGBDSimplePub = True
		break
if not ice_CameraRGBDSimplePub:
	print('Couldn\'t load CameraRGBDSimplePub')
	sys.exit(-1)
from RoboCompCameraRGBDSimplePub import *
ice_CameraSimple = False
for p in icePaths:
	print('Trying', p, 'to load CameraSimple.ice')
	if os.path.isfile(p+'/CameraSimple.ice'):
		print('Using', p, 'to load CameraSimple.ice')
		preStr = "-I/opt/robocomp/interfaces/ -I"+ROBOCOMP+"/interfaces/ " + additionalPathStr + " --all "+p+'/'
		wholeStr = preStr+"CameraSimple.ice"
		Ice.loadSlice(wholeStr)
		ice_CameraSimple = True
		break
if not ice_CameraSimple:
	print('Couldn\'t load CameraSimple')
	sys.exit(-1)
from RoboCompCameraSimple import *

class CameraSimpleI(CameraSimple):
	def __init__(self, worker):
		self.worker = worker

	def getImage(self, c):
		return self.worker.getImage()
