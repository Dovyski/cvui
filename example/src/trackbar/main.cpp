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
#include <opencv2/imgproc/imgproc.hpp>

#include "cvui.h"

#define WINDOW_NAME		"Trackbar"



int main(int argc, const char *argv[])
{
	cv::Mat frame = cv::Mat(cv::Size(250, 550), CV_8UC3);

	cv::namedWindow(WINDOW_NAME);
	cvui::init(WINDOW_NAME);


	while (true) {
		frame = cv::Scalar(50, 50, 50);

		cvui::beginColumn(frame, 20, 20, -1, -1, 6);
			cvui::text("Simple int trackbar, no ticks");
			static int intValue1 = 30;
			cvui::trackbar_int(&intValue1, 0, 100);
			cvui::text("");

			static int intValue2 = 30;
			cvui::text("Simple int trackbar, 5 large steps");
			cvui::trackbar_int(&intValue2, 0, 100, 5);
			cvui::text("");

			static double doubleValue1 = 30.;
			cvui::text("Simple float trackbar");
			cvui::text("1 decimal, no large step");
			cvui::trackbar_float(&doubleValue1, 10., 50., 1);
			cvui::text("");

			static double doubleValue2 = 30.;
			cvui::text("Simple float trackbar");
			cvui::text(" 2 decimals, 4 large Steps");
			cvui::trackbar_float(&doubleValue2, 10., 50., 2,  4, 1.);
			cvui::text("");

			static double doubleValue3 = 10.5;
			cvui::text("Simple float trackbar, 1 decimal");
			cvui::text("no larges steps");
			cvui::text("edited value forced to 1 decimal");
			cvui::trackbar_float(&doubleValue3, 10., 10.5, 1, 1, 0.1, true);

			if (cvui::button("&Quit"))
				break;
		cvui::endColumn();


		cvui::update();
		cv::imshow(WINDOW_NAME, frame);
	}

	return 0;
}
