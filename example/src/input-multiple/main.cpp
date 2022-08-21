/*
This is a demo application to showcase how to use multiple inputs
at the same time

Code licensed under the MIT license, check LICENSE file.
*/

#include <iostream>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>

#define CVUI_IMPLEMENTATION
#include "cvui.h"

#define WINDOW_NAME	"Input multiple"

int main(int argc, const char *argv[])
{
	cv::Mat frame = cv::Mat(cv::Size(650, 150), CV_8UC3);

	// Init cvui and tell it to use a value of 20 for cv::waitKey()
	// because we want to enable keyboard shortcut for
	// all components, e.g. button with label "&Quit".
	// If cvui has a value for waitKey, it will call
	// waitKey() automatically for us within cvui::update().
	cvui::init(WINDOW_NAME, 20);
    
    cv::String input1 = "text1";
    cv::String input2 = "text2";

	while (true) {
		frame = cv::Scalar(49, 52, 49);

		// Each input must have a unique name to ensure its focus behavior works.
		// In the inputs below, the first one is uniquely named `myInput1` and the
		// second one is uniquely named `myInput2`.
		cvui::input(frame, 40, 40, 100, "myInput1", input1);
		cvui::input(frame, 40, 80, 100, "myInput2", input2);

		cvui::text(frame, 160, 50, "Click any input to edit.");

		// Exit the application if the quit button was pressed.
		// It can be pressed because of a mouse click or because 
		// the user pressed the "q" key on the keyboard, which is
		// marked as a shortcut in the button label ("&Quit").
		if (cvui::button(frame, 300, 100, "&Quit")) {
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
