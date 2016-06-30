/*
This is a demo application to showcase the UI components of cvui.

Copyright (c) 2016 Fernando Bevilacqua <dovyski@gmail.com>
Licensed under the MIT license.
*/

#include <iostream>

#include "opencv2/core/core.hpp"
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc.hpp"

#include "cvui.h"

#define WINDOW_NAME		"Complex layout"

void group(cv::Mat& frame, int x, int y, int width, int height) {
	int padding = 5, w = (width - padding) / 4, h = (height - 15 - padding) / 2;
	cv::Point pos(x + padding, y + 15);

	cvui::text(frame, pos.x, pos.y, "Group title");
	pos.y += 10;

	cvui::window(frame, pos.x, pos.y, width - padding * 2, h - padding, "FFT");
	cvui::rect(frame, pos.x + 2, pos.y + 20, width - padding * 2 - 5, h - padding - 20, 0xff0000);
	pos.y += h;

	cvui::window(frame, pos.x, pos.y, w / 3 - padding, h, "HR");
	cvui::text(frame, pos.x + 25, pos.y + 60, "65", 1.1);
	pos.x += w / 3;

	cvui::window(frame, pos.x, pos.y, w / 3 - padding, h, "HF");
	cvui::text(frame, pos.x + 25, pos.y + 60, "30", 1.1);
	pos.x += w / 3;

	cvui::window(frame, pos.x, pos.y, w / 3 - padding, h, "LF");
	cvui::text(frame, pos.x + 25, pos.y + 60, "70", 1.1);
	pos.x += w / 3;

	cvui::window(frame, pos.x, pos.y, w - padding, h, "Bpms");
	cvui::rect(frame, pos.x + 2, pos.y + 22, w - padding - 5, h - padding - 20, 0xff0000);
	pos.x += w;

	cvui::window(frame, pos.x, pos.y, w - padding, h, "Means");
	cvui::rect(frame, pos.x + 2, pos.y + 22, w - padding - 5, h - padding - 20, 0xff0000);
	pos.x += w;

	cvui::window(frame, pos.x, pos.y, w - padding, h, "Normalized power");
	cvui::rect(frame, pos.x + 2, pos.y + 22, w - padding - 5, h - padding - 20, 0xff0000);
	pos.x += w;
	
	//cvui::text(frame, 50, 30, "Hey there!");
	//cvui::text(frame, 200, 30, "Use hex 0xRRGGBB colors easily", 0.4, 0xff0000);
}


int main(int argc, const char *argv[])
{
	int height = 220;
	cv::Mat frame = cv::Mat(height * 3, 1300, CV_8UC3);

	// Init a OpenCV window and tell cvui to use it.
	// If cv::namedWindow() is not used, mouse events will
	// not be captured by cvui.
	cv::namedWindow(WINDOW_NAME);
	cvui::init(WINDOW_NAME);

	while (true) {
		// Fill the frame with a nice color
		frame = cv::Scalar(49, 52, 49);

		// Check if ESC key was pressed
		if (cv::waitKey(10) == 27) {
			break;
		}

		group(frame, 0, 0, frame.cols, height - 10);
		
		// This function must be called *AFTER* all UI components. It does
		// all the behind the scenes magic to handle mouse clicks, etc.
		cvui::update();

		// Show everything on the screen
		cv::imshow(WINDOW_NAME, frame);
	}

	return 0;
}