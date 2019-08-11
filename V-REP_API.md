# A Brief introduction to V-REP

V-REP is a robot simulator, with integrated development environment. It is based on a distributed control architecture: each object/model can be individually controlled via an embedded script, a plugin, ROS nodes, BlueZero nodes, remote API clients, or a custom solution. This makes V-REP very versatile and ideal for multi-robot applications. Controllers can be written in C/C++, Python, Java, Lua, Matlab, Octave or Urbi.

In V-REP there are Pure shapes which have dynamics and physics, and Regular shapes which are just a mesh (the skeleton of a shape). When building a new model, first, we handle only the visual aspect of it (we want it to look right). The dynamic aspect: its underlying model of how it works, joints, sensors, etc. will be handled at a later stage. Go through the following tutorials to understand the basics of robot modeling in V-REP: [Tutorails](http://www.coppeliarobotics.com/helpFiles/en/tutorials.htm).

# Controlling your robot with Python

One of the main requirements of a robotic framework is to control the robot during simulation, the V-REP remote API allows to control a simulation from an external application. The V-REP remote API is composed of many specific functions and one generic function, that can be called from a C/C++ application, a Python script etc. The remote API functions are interacting with V-REP via socket communication. For more information on how remote API is operates, read this [page](http://www.coppeliarobotics.com/helpFiles/en/legacyRemoteApiOverview.htm).
This tutorial gives you an insight on how to use the V-REP remote API functions to control a simulation.

## Files setup
The first thing we need is to set up the environment.
- Decide on what will your working folder (directory). Create it if necessary. This is where your scripts will reside.
- Navigate to your V-REP installation folder
- Navigate into the programming/remoteApiBindings/python/python
- Copy all the .py files into your working folder
- Navigate into the programming/remoteApiBindings/lib/lib/
- On some V-REP installations you may have to navigate to your operating system’s directory (Windows, Linux or Mac OS).
- Copy the .dylib or .dll or .so file to your working directory.

## Setting up a Server
Now, on VREP your scene needs to start a server so that the python scripts can connect to it. To start the server you have to add a threaded script to an object in your scene that will start the server.
- Open the bubbleRob scene.
- Click on any of the cylinders you used as obstacles
- Click on Add→Associated Child ScriptrightarrowThreaded Script
- Open the script by double clicking on the “file” icon next to the cylinder
- Find the function sysCall_threadmain()
- Write the following as the only line in that method: simExtRemoteApiStart(19999).

Now, as soon as the scene is played, a server will be listening on port 19999. Before we start the server we need to disable the existing script

- Open the scripts window (click on the “page” on the left hand side icons)
- Select the script on bubbleRob
- Click on “Disable”
- Close the scripts window. You will see an “x” next to the script for bubbleRob

Now, start the scene. That will start the server.


## Setting up the Client

Switch to Python. Open a new file and immediately save it to your working directory as bubbleRob_control.py. Write the following python code in the file.:

![Setup Clinet](client_setup.png)

And execute the program. You should see “Connected to remote API server” on the screen. You have effectively established communication with the scene.

## Controling the Robot

We will make the robot move by accessing its motors. For this we need a handle to control each individual motor. The function vrep.simxGetObjectHandle will return an error code and a handle to an object. Add the following to the code to obtain a handle to both motors of the robot.

![Get Motor Handle](motor_handle.png)

The parameters to the functions are specified in the Python remote API for VREP at http://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsPython.htm. In this case, the vrep.simxGetObjectHandle, it needs a handle to the server clientID, the name of the object, and a mode (in this case simx_opmode_blocking)
Now that we have handles to the motors, we can make them go with the following code:

![Control Motor](motor_control.png)

Switch to VREP and watch bubbleRob go. You can stop your simulation if bubbleRob goes out of the scene or gets trapped.

## Sensing

Sensors work by detecting objects at a given point. They provide the information to check the distance and coordinates of the detected object with respect to the sensor. Sensors need to be initialized (first detection) and then used over and over again. To initialize a sensor we call the simxReadProximitySensor function. Notice the simx_opmode_streaming at the end. This function returns several variables.

![Proximity Sensor handle and initial sensing](ps_handle.png)

You can print them. The detectedPoint,detectedObjectHandle and detectedSurfaceNormalVector can be used to see if our robot has detected something.
For all subsequent sensing, use

![Proximity Sensor subsequent sensing](ps_sub_sensing.png)

Lastly, an important piece of information with proximity sensors is: How far is the object I detect?
One of the returned values of simxReadProximitySensor is the detected point relative to the sensor’s origin. The norm of that vector tells us the distance from the sensor to the object. To obtain the norm we need to import numpy and then apply the norm function like so:

![Calculate Norm](norm.png)

## An example program to detect obstacles and react to it

![Example Program](example_program.png)

# Conclusion
This tutorial explains how to connect to V-REP with python, move motors and read sensors and images.

# API Reference
To understand the python API reference and the functions used to control simulation, follow [Coppelia Python’s reference API](http://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsPython.htm).