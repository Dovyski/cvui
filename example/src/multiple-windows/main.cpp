/*
This demo shows how you can use cvui in an application that uses
more than one OpenCV window.

Code licensed under the MIT license, check LICENSE file.
*/

#include <opencv2/opencv.hpp>
#include "cvui.h"

#define WINDOW1_NAME "Window 1"
#define WINDOW2_NAME "Windows 2"
#define WINDOW3_NAME "Windows 3"

// Render and update a window
void window(const cv::String& name) {
	// Create a frame for this window and fill it with a nice color
	cv::Mat frame = cv::Mat(200, 500, CV_8UC3);
	frame = cv::Scalar(49, 52, 49);

	// Show info regarding the window
	cvui::printf(frame, 110, 50, "%s - click the button", name.c_str());

	// Buttons return true if they are clicked
	if (cvui::button(frame, 110, 90, "Button")) {
		cvui::printf(frame, 200, 95, "Button clicked!");
		std::cout << "Button clicked on: " << name << std::endl;
	}

	// This function must be called *AFTER* all UI components. It does
	// all the behind the scenes magic to handle mouse clicks, etc.
	cvui::update();

	// Show the content of this window on the screen
	cv::imshow(name, frame);
}

int main(int argc, const char *argv[])
{
	// Init a OpenCV window and tell cvui to use it.
	// If cv::namedWindow() is not used, mouse events will
	// not be captured by cvui.
	cv::namedWindow(WINDOW1_NAME);
	cv::namedWindow(WINDOW2_NAME);
	cv::namedWindow(WINDOW3_NAME);
	
	cvui::init(WINDOW1_NAME);
	cvui::watch(WINDOW2_NAME);
	cvui::watch(WINDOW3_NAME);

	while (true) {
		window(WINDOW1_NAME);
		window(WINDOW2_NAME);
		window(WINDOW3_NAME);

		// Check if ESC key was pressed
		if (cv::waitKey(20) == 27) {
			break;
		}
	}

	return 0;
}