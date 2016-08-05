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
	std::vector<double> values;
	bool checked = false;
	double value = 1.0;

	// Fill the vector with a few random values
	for (std::vector<double>::size_type i = 0; i < 20; i++) {
		values.push_back(rand() + 0.);
	}

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

		cvui::beginRow(frame, 10, 150, 100, 50);
			cvui::button("Expanding as needed");
			cvui::button("Hey!");
			cvui::text("2Hi again.");
			cvui::text("2Its me,");
			cvui::text("2a Mario!");
		cvui::endRow();

		cvui::beginRow(frame, 10, 250, 100, 50);
			cvui::button("Expanding as needed");
			cvui::button("Hey!");

			cvui::beginRow(600, 50);
				cvui::button("inner0");
				cvui::button("inner1");
				cvui::button("inner2");
				cvui::text("inner3");
				cvui::text("inner4");
			cvui::endRow();

			cvui::text("2Hi again.");
			cvui::text("2Its me,");
			cvui::text("2a Mario!");
		cvui::endRow();
		
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