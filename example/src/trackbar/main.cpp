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
	cv::Mat frame = cv::Mat(cv::Size(250, 750), CV_8UC3);

	cv::namedWindow(WINDOW_NAME);
	cvui::init(WINDOW_NAME);


	while (true) {
		frame = cv::Scalar(50, 50, 50);


		cvui::beginColumn(frame, 20, 20, -1, -1, 6);
			cvui::text("Simple int trackbar, no ticks");
			static int intValue1 = 30;
			cvui::trackbar(&intValue1, 0, 100, 0);
			cvui::text("");

			static uchar ucharValue2 = 30;
			cvui::text("Simple uchar trackbar");
			cvui::trackbar(&ucharValue2, (uchar)0, (uchar)255, 0);
			cvui::text("");

			static char charValue3 = 30;
			cvui::text("Simple signed char trackbar, no large");
			cvui::trackbar(&charValue3, (char)-128, (char)127, 0);
			cvui::text("");

			static float floatValue1 = 12.;
			cvui::text("Simple float trackbar");
			cvui::text("1 decimal, no large step");
			cvui::trackbar(&floatValue1, 10.f, 15.f, 1);
			cvui::text("");

			static double doubleValue2 = 15.;
			cvui::text("Simple float trackbar");
			cvui::text(" 2 decimals, 4 large Steps");
			cvui::trackbar(&doubleValue2, 10., 20., 2,  4);
			cvui::text("");

			static double doubleValue3 = 10.3;
			cvui::text("Simple float trackbar, 1 decimal");
			cvui::text("no larges steps");
			cvui::text("edited value forced to 1 decimal");
			cvui::trackbar(&doubleValue3, 10., 10.5, 1, 1, 0.1);

			static double doubleValue4 = 2.25;
			cvui::text("float trackbar, 2 decimal");
			cvui::text("value multiples of 0.25");
			cvui::text("2 large steps");
			cvui::trackbar(&doubleValue4, 0., 4., 2, 2, 0.25);

			if (cvui::button("&Quit"))
				break;
		cvui::endColumn();


		cvui::update();
		cv::imshow(WINDOW_NAME, frame);
	}

	return 0;
}
