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

/**
       \brief
       @author authorname
*/



#ifndef SPECIFICWORKER_H
#define SPECIFICWORKER_H

#include <genericworker.h>
#include <fps/fps.h>
#include <doublebuffer/DoubleBuffer.h>
#include <opencv2/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/opencv.hpp>
#include <b0RemoteApi.h>


class SpecificWorker : public GenericWorker
{
Q_OBJECT
public:
	SpecificWorker(TuplePrx tprx);
	~SpecificWorker();
	bool setParams(RoboCompCommonBehavior::ParameterList params);

	void CameraRGBDSimple_getAll(TImage &im, TDepth &dep);
	void CameraRGBDSimple_getDepth(TDepth &dep);
	void CameraRGBDSimple_getImage(TImage &im);

public slots:
	void compute();
	void initialize(int period);
private:
	RoboCompCameraRGBDSimple::TDepth depth;
	RoboCompCameraRGBDSimple::TImage image;
	int camera;
	b0RemoteApi *b0Client=nullptr;
	FPSCounter fps;
	std::string cameraName;
	bool SHOW_IMAGE = false;
	bool DEPTH = false;
	bool PUBLISH = false;

	DoubleBuffer<RoboCompCameraRGBDSimple::TImage, RoboCompCameraRGBDSimple::TImage> img_buffer;
	//DoubleBuffer<RoboCompCameraRGBDSimple::TDepth, RoboCompCameraRGBDSimple::TDepth> depth_buffer;
	
};

#endif
