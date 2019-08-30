[RoboComp.VREP Components](http://robocomp.org)
===============================

[![Join the chat at https://gitter.im/robocomp/V-REP](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/robocomp/V-REP?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

by [RoboLab](http://robolab.unex.es), [Aston University](https://www2.aston.ac.uk/eas), [ISIS](http://www.grupoisis.uma.es/index.php?option=com_jresearch&view=staff&Itemid=3&lang=es) and many other collaborators.

RoboComp is an open-source Robotics framework providing the tools to create and modify software components that communicate through public interfaces. RoboComp’s existing simulator, RCIS, is based on OpenSceneGraph technology and custom made actuators and sensor. This repository contains the prototypes of robotics simulation using V-REP that use V-REP's API to connect them to RoboComp ecosystem. Specifically, this repo consists of RoboComp components that uses V-REP as an external simulator.

**If you don't have RoboComp installed on your system, find the installation instructions [here](https://github.com/robocomp/robocomp).**


# V-REP installation

To install V-REP, please follow the following instructions:

1. Download a version of EDUCATIONAL V-REP from [here](http://www.coppeliarobotics.com/downloads.html), according to your system specification. 
2. Unpack the compressed file to somewhere in your system. 
3. Go to the V-REP folder and run the command:
```
sudo ./vrep.sh
```

The above command will start the V-REP simulation software.
If you are not familiar with V-REP, follow our short [tutorial](https://github.com/robocomp/V-REP/blob/master/tutorial/V-REP_API.md) that cover general operational principles of the V-REP simulator or you can go through this awesome [tutorials](https://www.youtube.com/playlist?list=PL38P7Q24q4XA7c0uNj0kO4or-bKhFYdIg) on YouTube that covers the same.


# Testing RoboComp.VREP Components

From here on, we assume you are familiar with RoboComp and the working of components. If not, please follow these [tutorials](https://github.com/robocomp/robocomp/blob/stable/doc/README.md).

Next, we will introduce how one can test the [linefollowingVREP](https://github.com/robocomp/V-REP/tree/master/components/linefollowingVREP) component.

**Note:**  Before moving further, make sure you have RoboComp and V-REP installed on your system.

# linefollowingVREP Component

### Description

This component communicates with cameraVREP component to get images of the floor (floor is in the scene simulated on V-REP). And, using that image it determines the directions to move so as to follow the path on the floor. The below image shows the V-REP scene with the black-colored path drawn on the floor:

