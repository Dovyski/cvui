/*
This is a demo application to showcase the sparkline components of cvui.
Sparklines are quite useful to display data, e.g. FPS charts.

Code licensed under the MIT license, check LICENSE file.
*/

#include <iostream>
#include <fstream>
#include <stdexcept>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>

#define CVUI_IMPLEMENTATION
#include "cvui.h"

#define WINDOW_NAME	"Sparkline"

std::vector<double> load(std::string thePath) {
	std::vector<double> data;
	double time, value;
	std::ifstream file(thePath.c_str());

	if (!file)	{
		throw std::runtime_error("Unable to open file");
	}

	while (file >> time >> value) {
		data.push_back(value);
	}

	return data;
}

int main(int argc, const char *argv[])
{
	cv::Mat frame = cv::Mat(600, 800, CV_8UC3);

	// Init cvui and tell it to create a OpenCV window, i.e. cv::namedWindow(WINDOW_NAME).
	cvui::init(WINDOW_NAME);

	// Load some data points from a file
	std::vector<double> points = load("sparkline.csv");

	while (true) {
		// Fill the frame with a nice color
		frame = cv::Scalar(49, 52, 49);

		// Add 3 sparklines that are displaying the same data, but with
		// different width/height/colors.
		cvui::sparkline(frame, points, 0, 0, 800, 200);
		cvui::sparkline(frame, points, 0, 200, 800, 100, 0xff0000);
		cvui::sparkline(frame, points, 0, 300, 400, 100, 0x0000ff);
		
		// This function must be called *AFTER* all UI components. It does
		// all the behind the scenes magic to handle mouse clicks, etc.
		cvui::update();

		// Show everything on the screen
		cv::imshow(WINDOW_NAME, frame);

		// Check if ESC key was pressed
		if (cv::waitKey(20) == 27) {
			break;
		}
	}

	return 0;
}
