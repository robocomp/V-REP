/*
 *    Copyright (C)2020 by YOUR NAME HERE
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
		RoboCompCommonBehavior::Parameter par = params.at("ShowImage");
	SHOW_IMAGE = (par.value == "true");
		par = params.at("Publish");
		PUBLISH = (par.value == "true");
		par = params.at("Depth");
		DEPTH = (par.value == "true");
		cameraName = params.at("CameraName").value;
		if(cameraName == "")
			qFatal("No camera provided, please check config file");
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
	auto handle_camera = b0Client->simxGetObjectHandle(cameraName.c_str(), b0Client->simxServiceCall());
	if( b0RemoteApi::readBool(handle_camera, 0))
		camera = b0RemoteApi::readInt(handle_camera, 1);
	else
		qFatal("Error getting handle");

	this->Period = period;
	timer.start(Period);
}

void SpecificWorker::compute()
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
		// move to DoubleBuffer
		//img_buffer.put(std::move(image));
	}
	else
		qDebug() << __FUNCTION__ << "Error capturing image";

	if( SHOW_IMAGE )
	{
		cv::Mat cvimg = cv::Mat(cv::Size{640,480}, CV_8UC3,  b0RemoteApi::readByteArray(resImg, 2).data() );
		cv::imshow("", cvimg);
		cv::waitKey(1);
	}


	//depth image
	if(DEPTH)
	{
		auto resDepth = b0Client->simxGetVisionSensorDepthBuffer(camera, true, true, b0Client->simxServiceCall());
		if( b0RemoteApi::readBool(resDepth, 0)) 
		{
			b0RemoteApi::readIntArray(resDepth, size, 1);
			int dcols = size[0]; int drows = size[1]; int dlen = dcols*drows*4;  // OJO float size
			depth.cameraID = 0;
			depth.width = dcols; depth.height = drows; depth.focalx = 617; depth.focaly = 617; depth.alivetime = 0; 
			depth.depth.resize(dlen); 
			memcpy(&depth.depth[0], b0RemoteApi::readByteArray(resDepth, 2).data(), dlen);
			//depth_buffer.put(std::move(depth);
		}
		else
			qDebug() << __FUNCTION__ << "Error capturing depth";	
	}

	if(PUBLISH)
	{
		try
		{
			camerargbdsimplepub_pubproxy->pushRGBD(image, depth);
		}catch(const Ice::Exception &e){std::cout << e << std::endl;}
	}

	fps.print();
}

void SpecificWorker::CameraRGBDSimple_getAll(TImage &im, TDepth &dep)
{
	im = image;
	dep = depth;
	//img_buffer.get(im);
	//depth_buffer.get(dep);
}

void SpecificWorker::CameraRGBDSimple_getDepth(TDepth &dep)
{
	dep = depth;
	//depth_buffer.get(dep);
}

void SpecificWorker::CameraRGBDSimple_getImage(TImage &im)
{
	im = image;
	//img_buffer.get(im);
}


