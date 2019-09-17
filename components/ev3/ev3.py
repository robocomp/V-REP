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

class EV3(VREPClient):

    __COMPONENTS = {
        'robot': 'LEGO_EV3',
        'base':  'V_LEGO_EV3'
    }

    def __init__(self, host="127.0.0.1", port=20000, suffix=""):
        VREPClient.__init__(self, host, port)
        self.suffix = suffix
        self.components = {}
        self.handle_objects()
        self.objects = {}
        #print(self.components)  #{'robot': {'name': 'Viriato', 'id': None}, 'base': {'name': 'viriato_base#', 'id': None}}

    def handle_objects(self):
        for i, j in EV3.__COMPONENTS.items():
            self.components[i] = {'name': j + self.suffix, 'id': None}

        for i in self.components.keys():
            res, comp_id = vrep.simxGetObjectHandle(
                self.client_id, self.components[i]['name'],
                vrep.simx_opmode_oneshot_wait)
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
                
    def set_base_speed(self, adv, rot):
        emptyBuff = bytearray()
        retCode, outInts, outFloats, outStrings, outBuffer = vrep.simxCallScriptFunction(self.client_id, "Funciones",  vrep.sim_scripttype_childscript, "On", [adv, rot], [], [], emptyBuff, vrep.simx_opmode_blocking)		
        
    def get_sonar(self):
        emptyBuff = bytearray()
        retCode, outInts, outFloats, outStrings, outBuffer = vrep.simxCallScriptFunction(self.client_id, "Funciones",  vrep.sim_scripttype_childscript, "SensorSonar", [], [], [], emptyBuff, vrep.simx_opmode_blocking)		
        return outFloats[0]

    def get_light_sensor(self):
        emptyBuff = bytearray()
        retCode, outInts, outFloats, outStrings, outBuffer = vrep.simxCallScriptFunction(self.client_id, "Funciones",  vrep.sim_scripttype_childscript, "SensorLight", [], [], [], emptyBuff, vrep.simx_opmode_blocking)		
        return outInts[0]

    def get_color_sensor(self):
        emptyBuff = bytearray()
        retCode, outInts, outFloats, outStrings, outBuffer = vrep.simxCallScriptFunction(self.client_id, "Funciones",  vrep.sim_scripttype_childscript, "SensorColor", [], [], [], emptyBuff, vrep.simx_opmode_blocking)
        return outFloats
    
    def get_angular_speed(self):
        emptyBuff = bytearray()
        retCode, outInts, outFloats, outStrings, outBuffer = vrep.simxCallScriptFunction(self.client_id, "Funciones",  vrep.sim_scripttype_childscript, "SensorGyroVA", [], [], [], emptyBuff, vrep.simx_opmode_blocking)		
        return outInts[0]

    def get_angle(self):
        emptyBuff = bytearray()
        retCode, outInts, outFloats, outStrings, outBuffer = vrep.simxCallScriptFunction(self.client_id, "Funciones",  vrep.sim_scripttype_childscript, "SensorGyroA", [], [], [], emptyBuff, vrep.simx_opmode_blocking)		
        return outInts[0]

    def get_base_pose(self):
        res, pos = vrep.simxGetObjectPosition(self.client_id,self.components['robot']['id'],-1, vrep.simx_opmode_blocking)
        if res != 0:
            err_print("GET BASE POSE", parse_error(res))
            raise Exception("ERROR IN GET BASE POSE")
        else:
            res, ang = vrep.simxGetObjectOrientation(self.client_id, self.components['robot']['id'], -1,vrep.simx_opmode_blocking)
            if res != 0:
                err_print("GET BASE POSE", parse_error(res))
                raise Exception("ERROR IN GET BASE POSE")
            else:
                ang = ang[1]
                return pos[0], pos[1], ang
        


if __name__ == "__main__":
    ev3 = EV3()
    #ev3.set_base_speed(0,0)
    print(ev3.get_base_pose())
    print("sonar:",ev3.get_sonar())
    print("image:",ev3.get_light_sensor())
    print("color:",ev3.get_color_sensor())
    print("angular speed:",ev3.get_angular_speed())
    print("angle:",ev3.get_angle())
