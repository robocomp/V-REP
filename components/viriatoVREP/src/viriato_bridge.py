# -*- coding: utf-8 -*-

try:
    import vrep
except:
    print ('--------------------------------------------------------------')
    print ('"vrep.py" could not be imported. This means very probably that')
    print ('either "vrep.py" or the remoteApi library could not be found.')
    print ('Make sure both are in the same folder as this file,')
    print ('or appropriately adjust the file "vrep.py"')
    print ('--------------------------------------------------------------')
    print ('')
import sys
from vrep_client import VREPClient
import numpy as np

__package__ = "Viriato"

__version__ = "1.0.1"
__author__ = "Pablo Bustos"
__license__ = "GPL"

class ViriatoBridge(VREPClient):

    __COMPONENTS = {
        'robot': 'Viriato',
        'base': 'viriato_base'
    }

    def __init__(self, host, port, suffix=""):
        VREPClient.__init__(self, host, port)
        self.suffix = suffix
        self.components = {}
        self.handle_objects()
        self.objects = {}
        print(self.components)  #{'robot': {'name': 'Viriato', 'id': None}, 'base': {'name': 'viriato_base#', 'id': None}}

    def handle_objects(self):
        for i, j in ViriatoBridge.__COMPONENTS.items():
            self.components[i] = {'name': j + self.suffix, 'id': None}

        for i in self.components.keys():
            res, comp_id = vrep.simxGetObjectHandle(
                self.client_id, self.components[i]['name'],
                vrep.simx_opmode_oneshot_wait)
            print(res, comp_id)
            if res == 0:
                self.components[i]['id'] = comp_id
            elif res != 0 and self.debug:
                err_print(prefix="HANDLE OBJECTS:" +
                          self.components[i]['name'] + " ",
                          message=parse_error(res))

    def set_new_objects(self, objects):
        for i in objects:
            res, comp_id = vrep.simxGetObjectHandle(
                self.client_id, i, vrep.simx_opmode_oneshot_wait)
            if res == 0:
                self.objects[comp_id] = i
    
    def stop_base(self):
        err_list = []
                
    def set_base_speed(self, adv, rot, side):

        retCode, oitInts, outFloats, outStrings, outBuffer = vrep.simxCallScriptFunction(self.client_id, "Viriato",  self.components['robot']['id'], "move_wheels", [],[adv, rot, side], [], [], vrep.simx_opmode_oneshot_wait)		
        #return res, err_list

    def set_speed_right(self, speed):
        pass
        #return res, err_list

    def get_prox_sensors(self):
        pass

    def get_camera_image(self):
        # data = {
        #     'res': -1,
        #     'err_list': ["camera isn't connected to client"],
        #     'data': {
        #         'image': np.zeros((128, 128, 3)),
        #         'resolution': (128, 128, 3)
        #     }
        # }
        # if self.components['camera']['id'] != None:
        #     res, resolution, image = vrep.simxGetVisionSensorImage(
        #         self.client_id, self.components['camera']['id'], 0,
        #         vrep.simx_opmode_streaming)
        #     data['res'] = res
        #     data['err_list'] = err_list = parse_error(res)
        #     print resolution
        #     if res not in (0, 1) and self.debug:
        #         err_print(prefix='CAMERA', message=err_list)
        #     elif len(resolution) > 1:
        #         resolution = (resolution[0], resolution[1], 3)
        #         data['data']['resolution'] = resolution
        #         mat_image = np.array(image, dtype=np.uint8)
        #         mat_image.resize([resolution[0], resolution[1], 3])

        #         data['data']['image'] = mat_image[::-1]
        # return data
        pass


    def get_base_pose(self):
        res, pos = vrep.simxGetObjectPosition(self.client_id,
                                              self.components['robot']['id'],
                                              -1, vrep.simx_opmode_blocking)
        if res != 0:
            err_print("GET BASE POSE", parse_error(res))
            raise Exception("ERROR IN GET BASE POSE")
        else:
            res, ang = vrep.simxGetObjectOrientation(
                self.client_id, self.components['robot']['id'], -1,
                vrep.simx_opmode_blocking)
            if res != 0:
                err_print("GET BASE POSE", parse_error(res))
                raise Exception("ERROR IN GET BASE POSE")
            else:
                ang = ang[1]
                return pos[0], pos[1], ang
        

    def set_base_orientation(self, omega):
        # res, ang = vrep.simxGetObjectOrientation(
        #         self.client_id, self.components['robot']['id'], -1,
        #         vrep.simx_opmode_blocking)
        # if res != 0:
        #     err_print("GET BASE POSE", parse_error(res))
        #     raise Exception("ERROR IN GET BASE POSE")
        # print "ANG", ang
        # ang[1] = omega
        # res, pos = vrep.simxSetObjectOrientation(self.client_id,
        #                                       self.components['robot']['id'],
        #                                       -1, ang, vrep.simx_opmode_blocking)
        # if res != 0:
        #     err_print("SET BASE ORI", parse_error(res))
        #     raise Exception("ERROR IN SET BASE ORIENTATION")
        pass
