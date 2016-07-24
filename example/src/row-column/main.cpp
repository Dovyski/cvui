/*
This is a demo application to showcase rows and columns in cvui.

Copyright (c) 2016 Fernando Bevilacqua <dovyski@gmail.com>
Licensed under the MIT license.
*/

#include <iostream>

#include "opencv2/core/core.hpp"
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc.hpp"

#include "cvui.h"

#define WINDOW_NAME		"Rows and Columns"


int main(int argc, const char *argv[])
{
	cv::Mat frame = cv::Mat(600, 800, CV_8UC3);
	std::vector<double> values(10, 90);
	bool checked = false;
	double value = 1.0;

	// Init a OpenCV window and tell cvui to use it.
	// If cv::namedWindow() is not used, mouse events will
	// not be captured by cvui.
	cv::namedWindow(WINDOW_NAME);
	cvui::init(WINDOW_NAME);

	while (true) {
		// Fill the frame with a nice color
		frame = cv::Scalar(49, 52, 49);

		//cvui::rect(frame, 10, 20, 800, 400, 0x909090);

		cvui::beginRow(frame, 10, 20, 100, 50);
			cvui::text("Hi again.");
			cvui::printf("Its me");
			cvui::printf(0.4, 0x00ff00, "again");
			cvui::checkbox("checkbox", &checked);
			cvui::window(80, 80, "window");
			cvui::window(80, 100, "window");
			cvui::rect(50, 50, 0x00ff00);
			cvui::sparkline(values, 50, 50);
			cvui::counter(&value);
			cvui::counter(&value);
			cvui::button(100, 30, "Fixed");
		cvui::endRow();

		cvui::beginRow(frame, 10, 100, 100, 50);
			cvui::text("2Hi again.");
			cvui::text("2Its me,");
			cvui::text("2a Mario!");
		cvui::endRow();

		cvui::text(frame, 50, 150, "Outside the row!", 0.4, 0x00FF00);
		cvui::printf(frame, 50, 180, "Outside the row! %d", 23);
		
		// This function must be called *AFTER* all UI components. It does
		// all the behind the scenes magic to handle mouse clicks, etc.
		cvui::update();

		// Show everything on the screen
		cv::imshow(WINDOW_NAME, frame);

		// Check if ESC key was pressed
		if (cv::waitKey(10) == 27) {
			break;
		}
	}

	return 0;
}