/*
This is a demo application to showcase the sparkline components of cvui.

Copyright (c) 2016 Fernando Bevilacqua <dovyski@gmail.com>
Licensed under the MIT license.
*/

#include <iostream>
#include <fstream>

#include "opencv2/core/core.hpp"
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc.hpp"

#include "cvui.h"

#define WINDOW_NAME		"Sparkline"


std::vector<double> load(std::string thePath) {
	std::vector<double> data;
	double time, value;
	std::ifstream file(thePath);

	if (!file)	{
		throw std::exception("Unable to open file");
	}

	while (file >> time >> value) {
		data.push_back(value);
	}

	return data;
}

int main(int argc, const char *argv[])
{
	std::vector<double> points = load("sparkline.csv");

	cv::Mat frame = cv::Mat(600, 800, CV_8UC3);

	// Init a OpenCV window and tell cvui to use it.
	// If cv::namedWindow() is not used, mouse events will
	// not be captured by cvui.
	cv::namedWindow(WINDOW_NAME);
	cvui::init(WINDOW_NAME);

	while (true) {
		// Fill the frame with a nice color
		frame = cv::Scalar(49, 52, 49);

		// Check if ESC key was pressed
		if (cv::waitKey(1) == 27) {
			break;
		}

		cvui::sparkline(frame, points, 0, 0, 800, 200);
		cvui::sparkline(frame, points, 0, 200, 800, 100, 0xFF0000);
		cvui::sparkline(frame, points, 0, 300, 400, 100, 0x0000FF);
		
		// This function must be called *AFTER* all UI components. It does
		// all the behind the scenes magic to handle mouse clicks, etc.
		cvui::update();

		// Show everything on the screen
		cv::imshow(WINDOW_NAME, frame);
	}

	return 0;
}