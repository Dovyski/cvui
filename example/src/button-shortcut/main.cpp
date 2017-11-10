/*
This is a demo application to showcase keyboard shortcuts. 
Author: Pascal Thomet
*/

#include <iostream>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>

#define CVUI_IMPLEMENTATION
#include "cvui.h"

#define WINDOW_NAME	"Button shortcut"

int main(int argc, const char *argv[])
{
	cv::Mat frame = cv::Mat(cv::Size(650, 150), CV_8UC3);

	// Init cvui and tell it to use a value of 20 for cv::waitKey()
	// because we want to enable keyboard shortcut for
	// all components, e.g. button with label "&Quit".
	// If cvui has a value for waitKey, it will call
	// waitKey() automatically for us within cvui::update().
	cvui::init(WINDOW_NAME, 20);

	while (true) {
		frame = cv::Scalar(49, 52, 49);

		cvui::text(frame, 40, 40, "To exit this app click the button below or press Q (shortcut for the button below).");

		// Exit the application if the quit button was pressed.
		// It can be pressed because of a mouse click or because 
		// the user pressed the "q" key on the keyboard, which is
		// marked as a shortcut in the button label ("&Quit").
		if (cvui::button(frame, 300, 80, "&Quit")) {
			break;
		}

		// Since cvui::init() received a param regarding waitKey,
		// there is no need to call cv::waitKey() anymore. cvui::update()
		// will do it automatically.
		cvui::update();
		
		cv::imshow(WINDOW_NAME, frame);
	}

	return 0;
}
