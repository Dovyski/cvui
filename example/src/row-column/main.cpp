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

	// Init a OpenCV window and tell cvui to use it.
	// If cv::namedWindow() is not used, mouse events will
	// not be captured by cvui.
	cv::namedWindow(WINDOW_NAME);
	cvui::init(WINDOW_NAME);

	while (true) {
		// Fill the frame with a nice color
		frame = cv::Scalar(49, 52, 49);

		cvui::beginRow(frame, 10, 20, 100, 50);
			cvui::text("Hi again.");
			cvui::text("Its me");
			cvui::text(", a Mario!");
			cvui::button(100, 50, "Test");
			cvui::button(50, 50, "hi");
		cvui::endRow();

		cvui::beginRow(frame, 10, 50, 100, 50);
			cvui::text("2Hi again.");
			cvui::text("2Its me");
			cvui::text("2, a Mario!");
		cvui::endRow();

		cvui::text(frame, 50, 150, "Outside the row!", 0.4, 0x00FF00);
		
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