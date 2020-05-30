/*
 *    Copyright (C) 2020 by YOUR NAME HERE
 *
 *    This file is part of RoboComp
 *
 *    RoboComp is free software: you can redistribute it and/or modify
 *    it under the terms of the GNU General Public License as published by
 *    the Free Software Foundation, either version 3 of the License, or
 *    (at your option) any later version.
 *
 *    RoboComp is distributed in the hope that it will be useful,
 *    but WITHOUT ANY WARRANTY; without even the implied warranty of
 *    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *    GNU General Public License for more details.
 *
 *    You should have received a copy of the GNU General Public License
 *    along with RoboComp.  If not, see <http://www.gnu.org/licenses/>.
 */
#include "specificworker.h"

/**
* \brief Default constructor
*/
SpecificWorker::SpecificWorker(TuplePrx tprx) : GenericWorker(tprx)
{

}

/**
* \brief Default destructor
*/
SpecificWorker::~SpecificWorker()
{
	std::cout << "Destroying SpecificWorker" << std::endl;
}

bool SpecificWorker::setParams(RoboCompCommonBehavior::ParameterList params)
{
	try
	{
		RoboCompCommonBehavior::Parameter par = params.at("ShowImage"); SHOW_IMAGE = (par.value == "true");
		par = params.at("Publish"); PUBLISH = (par.value == "true");
		par = params.at("Depth"); DEPTH = (par.value == "true");
		par = params.at("Laser"); LASER = (par.value == "true"); 
		par = params.at("Image"); IMAGE = (par.value == "true"); 
		camera_name = params.at("CameraName").value;
		if(camera_name == "")
			qFatal("No camera provided, please check config file");
		laser_name = params.at("LaserName").value;
		if(laser_name == "")
			qFatal("No laser provided, please check config file");
	}
	catch(const std::exception &e){ 
		qFatal("Error reading config params"); 
	}
	return true;
}

void SpecificWorker::initialize(int period)
{
	std::cout << "Initialize worker" << std::endl;

   	b0Client = new b0RemoteApi("b0RemoteApi_c++Client","b0RemoteApiAddOn");
	qDebug() << __FUNCTION__ << "Connected";
	auto handle_camera = b0Client->simxGetObjectHandle(camera_name.c_str(), b0Client->simxServiceCall());
	if( b0RemoteApi::readBool(handle_camera, 0))
		camera = b0RemoteApi::readInt(handle_camera, 1);
	else
		qFatal("Error getting camera handle");
	auto handle_laser = b0Client->simxGetObjectHandle(laser_name.c_str(), b0Client->simxServiceCall());
	if( b0RemoteApi::readBool(handle_laser, 0))
		laser = b0RemoteApi::readInt(handle_laser, 1);
	else
		qFatal("Error getting laser handle");
		
	OmniRobot_setSpeedBase(0, 0, 0);
	this->Period = period;
	timer.start(50);
}

//constexpr auto fn_ItoO =  [] (const int& i, std::string& o) { o = std::to_string(i);};
//constexpr auto fn_OtoI =  [] (int& i, const std::string& o) { i = std::stoi(o); };

void SpecificWorker::compute()
{
	if(IMAGE)
	{
		std::vector<int> size;
		//color image
		auto resImg = b0Client->simxGetVisionSensorImage(camera, false, b0Client->simxServiceCall());
		if(b0RemoteApi::readBool(resImg, 0))
		{
			b0RemoteApi::readIntArray(resImg, size, 1);
			int cols = size[0]; int rows = size[1]; int depth = 3; int len = cols*rows*depth;
			image.width = cols; image.height = rows; image.depth = 3; image.image.resize(len);
			memcpy(&image.image[0], b0RemoteApi::readByteArray(resImg, 2).data(), len);
			img_buffer.put(image);
		}
		else
			qDebug() << __FUNCTION__ << "Error capturing image";
	}	

	if( IMAGE and SHOW_IMAGE )
	{
		//cv::Mat cvimg = cv::Mat(cv::Size{640,480}, CV_8UC3,  b0RemoteApi::readByteArray(resImg, 2).data() );
		cv::Mat cvimg = cv::Mat(cv::Size{640,480}, CV_8UC3,  &image.image[0] );
		cv::Mat flipped;
		cv::flip(cvimg, flipped, 0);
		cv::imshow("", flipped);
		cv::waitKey(1);
	}

	//depth image
	if(DEPTH)
	{
		std::vector<int> size;
		auto resDepth = b0Client->simxGetVisionSensorDepthBuffer(camera, true, true, b0Client->simxServiceCall());
		if( b0RemoteApi::readBool(resDepth, 0)) 
		{
			b0RemoteApi::readIntArray(resDepth, size, 1);
			int dcols = size[0]; int drows = size[1]; int dlen = dcols*drows*4;  // OJO float size
			depth.cameraID = 0;
			depth.width = dcols; depth.height = drows; depth.focalx = 617; depth.focaly = 617; depth.alivetime = 0; 
			depth.depth.resize(dlen); 
			memcpy(&depth.depth[0], b0RemoteApi::readByteArray(resDepth, 2).data(), dlen);
			//depth_buffer.put(std::move(depth));
		}
		else
			qDebug() << __FUNCTION__ << "Error capturing depth";	
	}

	//laser
	if(LASER)
	{
		std::vector<float> buffer;
		auto res_laser = b0Client->simxGetStringSignal("distances", b0Client->simxServiceCall());
		if(b0RemoteApi::readBool(res_laser, 0)) 
		{
			auto data = b0RemoteApi::readByteArray(res_laser, 1);
			for(auto&& m: iter::chunked(data,12))
			{
				char cx[4] = {m[0],m[1],m[2],m[3]};
				float* x = (float*)cx;
				char cy[4] = {m[4],m[5],m[6],m[7]};
				float* y = (float*)cy;
				//std::cout << "[" << *x << " " << *y << "" << *z << "]" << std::endl;
				// x-axis of the laser points in the direction of movement of robot and z-axis is out of the plane. distance is in meters
				laser_data.emplace_back(RoboCompLaser::TData{(float)sqrt(pow(*x,2) + pow(*y,2))*1000, atan2(*y,*x)});
			}
		}
		else
			qDebug() << __FUNCTION__ << "Error receiving laser data";
	}

	auto j = joy_buffer.get();
	if(j.has_value())
	{
		float rot = 0; float adv = 0; float side = 0;
		for(auto x: j.value().axes)
		{
			if(x.name=="advance")
				adv = x.value/100.;
			if(x.name=="rotate")
				rot = x.value/100.;
			if(x.name=="side")
				side = x.value/100.;
			
			OmniRobot_setSpeedBase(adv, side, rot);
		}
	}

	fps.print();
}

///////////////////////////////////////////////////////////////////
/// STUBS
//////////////////////////////////////////////////////////////////
/// Camera RGBD
//////////////////////////////////////////////////////////////////
void SpecificWorker::CameraRGBDSimple_getAll(TImage &im, TDepth &dep)
{

}

void SpecificWorker::CameraRGBDSimple_getDepth(TDepth &dep)
{

}

void SpecificWorker::CameraRGBDSimple_getImage(TImage &im)
{

}

//////////////////////////////////////////////////////////////////
/// Laser
//////////////////////////////////////////////////////////////////
TLaserData SpecificWorker::Laser_getLaserAndBStateData(RoboCompGenericBase::TBaseState &bState)
{
 	return TLaserData();
}

LaserConfData SpecificWorker::Laser_getLaserConfData()
{
	return LaserConfData();
}

TLaserData SpecificWorker::Laser_getLaserData()
{
	return TLaserData();
}

//////////////////////////////////////////////////////////////////
/// Base
//////////////////////////////////////////////////////////////////
void SpecificWorker::OmniRobot_correctOdometer(int x, int z, float alpha)
{

}

void SpecificWorker::OmniRobot_getBasePose(int &x, int &z, float &alpha)
{

}

void SpecificWorker::OmniRobot_getBaseState(RoboCompGenericBase::TBaseState &state)
{

}

void SpecificWorker::OmniRobot_resetOdometer()
{
//implementCODE

}

void SpecificWorker::OmniRobot_setOdometer(RoboCompGenericBase::TBaseState state)
{
//implementCODE

}

void SpecificWorker::OmniRobot_setOdometerPose(int x, int z, float alpha)
{
//implementCODE

}

void SpecificWorker::OmniRobot_setSpeedBase(float advx, float advz, float rot)
{
	std::tuple<float, float, float> src(advx, advz, rot);
	std::stringstream buffer;
	msgpack::pack(buffer, src);
	auto res = b0Client->simxCallScriptFunction("setSpeed@Viriato#0", 1, buffer.str().c_str(), buffer.str().size(), b0Client->simxServiceCall());
	qDebug() << b0RemoteApi::readBool(res, 0);	
}

void SpecificWorker::OmniRobot_stopBase()
{
//implementCODE

}

//////////////////////////////////////////////////////////////////
/// Joy
//////////////////////////////////////////////////////////////////

void SpecificWorker::JoystickAdapter_sendData(RoboCompJoystickAdapter::TData data)
{
	//qDebug() << QString::fromStdString(data.id);
	for(auto x: data.axes)
	{
		//qDebug() << QString::fromStdString(x.name) << (float)(x.value/500);
		//OmniRobot_setSpeedBase(0, 0, 0);
		joy_buffer.put(data);
	}
}
