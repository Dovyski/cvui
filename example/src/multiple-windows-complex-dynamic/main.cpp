/*
This demo shows how to use cvui in multiple windows, using rows and colums.
Additionally a custom error window (an OpenCV window) is dynamically opened/closed
based on UI buttons.

Code licensed under the MIT license, check LICENSE file.
*/

#include <iostream>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>

#define CVUI_IMPLEMENTATION
#include "cvui.h"

#define GUI_WINDOW1_NAME "Window 1"
#define GUI_WINDOW2_NAME "Window 2"
#define ERROR_WINDOW_NAME "Error window"

// Check if an OpenCV window is open.
// From: https://stackoverflow.com/a/48055987/29827
int isWindowOpen(const cv::String &name) {
	return cv::getWindowProperty(name, cv::WND_PROP_AUTOSIZE) != -1;
}

// Open a new OpenCV window and watch it using cvui
void openWindow(const cv::String &name) {
	cv::namedWindow(name);
	cvui::watch(name);
}

// Open an OpenCV window
void closeWindow(const cv::String &name) {
	cv::destroyWindow(name);

	// Ensure OpenCV window event queue is processed, otherwise the window
	// will not be closed.
	cv::waitKey(1);
}

int main(int argc, const char *argv[])
{
	// We have one mat for each window.
	cv::Mat frame1 = cv::Mat(150, 600, CV_8UC3), frame2 = cv::Mat(150, 600, CV_8UC3), error_frame = cv::Mat(100, 300, CV_8UC3);
	
	// Flag to control if we should show an error window.
	bool error = false;

	// Create two OpenCV windows
	cv::namedWindow(GUI_WINDOW1_NAME);
	cv::namedWindow(GUI_WINDOW2_NAME);
	
	// Init cvui and inform it to use the first window as the default one.
	// cvui::init() will automatically watch the informed window.
	cvui::init(GUI_WINDOW1_NAME);

	// Tell cvui to keep track of mouse events in window2 as well.
	cvui::watch(GUI_WINDOW2_NAME);

	while (true) {
		// Inform cvui that all subsequent component calls and events are related to window 1.
		cvui::context(GUI_WINDOW1_NAME);

		// Fill the frame with a nice color
		frame1 = cv::Scalar(49, 52, 49);

		cvui::beginColumn(frame1, 50, 20, -1, -1, 10);
			cvui::text("[Win1] Use the buttons below to control the error window");
			
			if (cvui::button("Close")) {
				closeWindow(ERROR_WINDOW_NAME);
			}

			// If the button is clicked, we open the error window.
			// The content and rendering of such error window will be performed
			// after we handled all other windows.
			if (cvui::button("Open")) {
				error = true;
				openWindow(ERROR_WINDOW_NAME);
			}
		cvui::endColumn();

		// Update all components of window1, e.g. mouse clicks, and show it.
		cvui::update(GUI_WINDOW1_NAME);
		cv::imshow(GUI_WINDOW1_NAME, frame1);

		// From this point on, we are going to render the second window. We need to inform cvui
		// that all updates and components from now on are connected to window 2.
		// We do that by calling cvui::context().
		cvui::context(GUI_WINDOW2_NAME);
		frame2 = cv::Scalar(49, 52, 49);
		
		cvui::beginColumn(frame2, 50, 20, -1, -1, 10);
			cvui::text("[Win2] Use the buttons below to control the error window");

			if (cvui::button("Close")) {
				closeWindow(ERROR_WINDOW_NAME);
			}

			// If the button is clicked, we open the error window.
			// The content and rendering of such error window will be performed
			// after we handled all other windows.
			if (cvui::button("Open")) {
				openWindow(ERROR_WINDOW_NAME);
				error = true;
			}
		cvui::endColumn();

		// Update all components of window2, e.g. mouse clicks, and show it.
		cvui::update(GUI_WINDOW2_NAME);
		cv::imshow(GUI_WINDOW2_NAME, frame2);

		// Handle the content and rendering of the error window,
		// if we have un active error and the window is actually open.
		if (error && isWindowOpen(ERROR_WINDOW_NAME)) {
			// Inform cvui that all subsequent component calls and events are
			// related to the error window from now on
			cvui::context(ERROR_WINDOW_NAME);

			// Fill the error window if a vibrant color
			error_frame = cv::Scalar(10, 10, 49);

			cvui::text(error_frame, 70, 20, "This is an error message", 0.4, 0xff0000);

			if (cvui::button(error_frame, 110, 40, "Close")) {
				error = false;
			}

			if (error) {
				// We still have an active error.
				// Update all components of the error window, e.g. mouse clicks, and show it.
				cvui::update(ERROR_WINDOW_NAME);
				cv::imshow(ERROR_WINDOW_NAME, error_frame);
			} else {
				// No more active error. Let's close the error window.
				closeWindow(ERROR_WINDOW_NAME);
			}
		}

		// Check if ESC key was pressed
		if (cv::waitKey(20) == 27) {
			break;
		}
	}

	return 0;
}