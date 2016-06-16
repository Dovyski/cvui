#include <iostream>

#include "opencv2/core/core.hpp"
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc.hpp"

#include "cvui.h"

#define WINDOW_NAME		"CVUI Test"

int main(int argc, const char *argv[])
{
	cv::Mat aFrame = cv::Mat(800, 600, CV_8UC3, cv::Scalar(255, 255, 255));
	bool aCheckbox = false;

	cv::namedWindow(WINDOW_NAME);
	cvui::init(WINDOW_NAME);

	while (true) {
		// Fill the frame with white color
		aFrame = cv::Scalar(255, 255, 255);

		// Check if ESC key was pressed
		if (cv::waitKey(10) == 27) {
			break;
		}

		cvui::text(aFrame, 50, 50, "Hey there!", 0.4);

		if (cvui::button(aFrame, 50, 50, "Button")) {
			std::cout << "Button clicked! \n";
		}

		cvui::checkbox(aFrame, 50, 100, "My checkbox", &aCheckbox);

		cvui::update();

		// Show everything on the screen
		imshow(WINDOW_NAME, aFrame);
	}

	return 0;
}