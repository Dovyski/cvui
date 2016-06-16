#include <iostream>

#include "opencv2/core/core.hpp"
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc.hpp"

#include "cvui.h"

#define WINDOW_NAME		"CVUI Test"

int main(int argc, const char *argv[])
{
	cv::Mat aFrame = cv::Mat(800, 600, CV_8UC3);
	bool aCheckbox = false;
	int aCount = 0;

	cv::namedWindow(WINDOW_NAME);
	cvui::init(WINDOW_NAME);

	while (true) {
		// Fill the frame with white
		aFrame = cv::Scalar(49, 52, 49);

		// Check if ESC key was pressed
		if (cv::waitKey(10) == 27) {
			break;
		}

		cvui::text(aFrame, 50, 50, "Hey there!", 0.4);

		if (cvui::button(aFrame, 50, 50, "Button very large")) {
			std::cout << "Button clicked!" << std::endl;
		}

		cvui::checkbox(aFrame, 50, 100, "My checkbox", &aCheckbox);
		cvui::overlay(aFrame, 50, 150, 100, 90, "Overlay");
		cvui::counter(aFrame, 50, 300, &aCount);

		cvui::update();

		// Show everything on the screen
		imshow(WINDOW_NAME, aFrame);
	}

	return 0;
}