/*
This is a demo application to showcase how you use buttons
and images.

Copyright (c) 2016 Fernando Bevilacqua <dovyski@gmail.com>
Licensed under the MIT license.
*/

#include <iostream>

#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>

#include "cvui.h"

#define WINDOW_NAME		"Image button"

int main(int argc, const char *argv[])
{
	cv::Mat frame = cv::Mat(300, 600, CV_8UC3);
	cv::Mat lena = cv::imread("./lena-face.jpg", cv::IMREAD_COLOR);
	cv::Mat lenaRed = cv::imread("./lena-face-red.jpg", cv::IMREAD_COLOR);
	cv::Mat lenaGray = cv::imread("./lena-face-gray.jpg", cv::IMREAD_COLOR);

	// Init a OpenCV window and tell cvui to use it.
	// If cv::namedWindow() is not used, mouse events will
	// not be captured by cvui.
	cv::namedWindow(WINDOW_NAME);
	cvui::init(WINDOW_NAME);

	while (true) {
		// Fill the frame with a nice color
		frame = cv::Scalar(49, 52, 49);

		// Check if ESC key was pressed
		if (cvui::lastKeyPressed() == 27) {
			break;
		}

		cvui::image(frame, 10, 10, lena);

		// This function must be called *AFTER* all UI components. It does
		// all the behind the scenes magic to handle mouse clicks, etc.
		cvui::update();

		// Show everything on the screen
		cv::imshow(WINDOW_NAME, frame);
	}

	return 0;
}