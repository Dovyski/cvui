/*
This is a demo application to showcase the image button component.

Copyright (c) 2016 Fernando Bevilacqua <dovyski@gmail.com>
Licensed under the MIT license.
*/

#include <iostream>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>

#define CVUI_IMPLEMENTATION
#include "cvui.h"

#define WINDOW_NAME	"Image button"

int main(int argc, const char *argv[])
{
	cv::Mat frame = cv::Mat(300, 600, CV_8UC3);
	cv::Mat out = cv::imread("./lena-face.jpg", cv::IMREAD_COLOR);
	cv::Mat down = cv::imread("./lena-face-red.jpg", cv::IMREAD_COLOR);
	cv::Mat over = cv::imread("./lena-face-gray.jpg", cv::IMREAD_COLOR);

	// Init cvui and tell it to create a OpenCV window, i.e. cv::namedWindow(WINDOW_NAME).
	cvui::init(WINDOW_NAME);

	while (true) {
		// Fill the frame with a nice color
		frame = cv::Scalar(49, 52, 49);

		// Render an image-based button. You can provide images
		// to be used to render the button when the mouse cursor is
		// outside, over or down the button area.
		if (cvui::button(frame, 200, 80, out, over, down)) {
			std::cout << "Image button clicked!" << std::endl;
		}
		cvui::text(frame, 150, 200, "This image behaves as a button");

		// Render a regular button.
		if (cvui::button(frame, 360, 80, "Button")) {
			std::cout << "Regular button clicked!" << std::endl;
		}

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