/*
This is application uses the mouse API to dynamically create a ROI
for image visualization.

Copyright (c) 2017 Fernando Bevilacqua <dovyski@gmail.com>
Licensed under the MIT license.
*/

#include <iostream>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>

#define CVUI_IMPLEMENTATION
#include "cvui.h"

#define WINDOW_NAME	"Mouse - ROI interaction"
#define ROI_WINDOW	"ROI"

int main(int argc, const char *argv[])
{
	cv::Mat lena = cv::imread("lena.jpg");
	cv::Mat frame = lena.clone();
	cv::Point anchor;
	cv::Rect roi(0, 0, 0, 0);
	bool working = false;

	// Init cvui and tell it to create a OpenCV window, i.e. cv::namedWindow(WINDOW_NAME).
	cvui::init(WINDOW_NAME);

	while (true) {
		// Fill the frame with Lena's image
		lena.copyTo(frame);

		// Show the coordinates of the mouse pointer on the screen
		cvui::text(frame, 10, 10, "Click (any) mouse button and drag the pointer around to select a ROI.");

		// The function "bool cvui::mouse(int query)" allows you to query the mouse for events.
		// E.g. cvui::mouse(cvui::DOWN)
		//
		// Available queries:
		//	- cvui::DOWN: any mouse button was pressed. cvui::mouse() returns true for single frame only.
		//	- cvui::UP: any mouse button was released. cvui::mouse() returns true for single frame only.
		//	- cvui::CLICK: any mouse button was clicked (went down then up, no matter the amount of frames in between). cvui::mouse() returns true for single frame only.
		//	- cvui::IS_DOWN: any mouse button is currently pressed. cvui::mouse() returns true for as long as the button is down/pressed.

		// Did any mouse button go down?
		if (cvui::mouse(cvui::DOWN)) {
			// Position the anchor at the mouse pointer.
			anchor.x = cvui::mouse().x;
			anchor.y = cvui::mouse().y;

			// Inform we are working, so the ROI window is not updated every frame
			working = true;
		}

		// Is any mouse button down (pressed)?
		if (cvui::mouse(cvui::IS_DOWN)) {
			// Adjust roi dimensions according to mouse pointer
			int width = cvui::mouse().x - anchor.x;
			int height = cvui::mouse().y - anchor.y;
			
			roi.x = width < 0 ? anchor.x + width : anchor.x;
			roi.y = height < 0 ? anchor.y + height : anchor.y;
			roi.width = std::abs(width);
			roi.height = std::abs(height);

			// Show the roi coordinates and size
			cvui::printf(frame, roi.x + 5, roi.y + 5, 0.3, 0xff0000, "(%d,%d)", roi.x, roi.y);
			cvui::printf(frame, cvui::mouse().x + 5, cvui::mouse().y + 5, 0.3, 0xff0000, "w:%d, h:%d", roi.width, roi.height);
		}

		// Was the mouse clicked (any button went down then up)?
		if (cvui::mouse(cvui::UP)) {
			// We are done working with the ROI.
			working = false;
		}

		// Ensure ROI is within bounds
		roi.x = roi.x < 0 ? 0 : roi.x;
		roi.y = roi.y < 0 ? 0 : roi.y;
		roi.width = roi.x + roi.width > lena.cols ? roi.width + lena.cols - (roi.x + roi.width) : roi.width;
		roi.height = roi.y + roi.height > lena.rows ? roi.height + lena.rows - (roi.y + roi.height) : roi.height;

		// Render the roi
		cvui::rect(frame, roi.x, roi.y, roi.width, roi.height, 0xff0000);

		// This function must be called *AFTER* all UI components. It does
		// all the behind the scenes magic to handle mouse clicks, etc.
		cvui::update();

		// Show everything on the screen
		cv::imshow(WINDOW_NAME, frame);

		// If the ROI is valid, show it.
		if (roi.area() > 0 && !working) {
			cv::imshow(ROI_WINDOW, lena(roi));
		}

		// Check if ESC key was pressed
		if (cv::waitKey(20) == 27) {
			break;
		}
	}

	return 0;
}