/*
This is a demo application to showcase how the input component can be used
with different font sizes (font scale) and different width.

Code licensed under the MIT license, check LICENSE file.
*/

#include <iostream>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>

#define CVUI_IMPLEMENTATION
#include "cvui.h"

#define WINDOW_NAME	"Input sizes"

int main(int argc, const char *argv[])
{
	cv::Mat frame = cv::Mat(cv::Size(600, 300), CV_8UC3);

	// Init cvui and tell it to use a value of 20 for cv::waitKey()
	// because we want to enable keyboard shortcut for
	// all components, e.g. button with label "&Quit".
	// If cvui has a value for waitKey, it will call
	// waitKey() automatically for us within cvui::update().
	cvui::init(WINDOW_NAME, 20);
    
    cv::String input1 = "default";
    cv::String input2 = "large width";
    cv::String input3 = "font scale";
    cv::String input4 = "width and font scale";

	while (true) {
		frame = cv::Scalar(49, 52, 49);

		// Display some input elements with different width and font scale.
		cvui::input(frame, 40, 40, 150, "input1", input1);
		cvui::input(frame, 40, 80, 300, "input2", input2);
		cvui::input(frame, 40, 120, 300, "input3", input3, 0.8);
		cvui::input(frame, 40, 200, 400, "input4", input4, 0.9);

		cvui::text(frame, 400, 50, "Click any input to edit.");

		// Exit the application if the quit button was pressed.
		// It can be pressed because of a mouse click or because 
		// the user pressed the "q" key on the keyboard, which is
		// marked as a shortcut in the button label ("&Quit").
		if (cvui::button(frame, 500, 200, "&Quit")) {
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
