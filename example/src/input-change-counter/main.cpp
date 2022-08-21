/*
This is a demo application to showcase how the input component can be used
to interact with other components.

Code licensed under the MIT license, check LICENSE file.
*/

#include <iostream>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>

#define CVUI_IMPLEMENTATION
#include "cvui.h"

#define WINDOW_NAME	"Input change counter"

int main(int argc, const char *argv[])
{
	cv::Mat frame = cv::Mat(cv::Size(650, 150), CV_8UC3);

	// Init cvui and tell it to use a value of 20 for cv::waitKey()
	// because we want to enable keyboard shortcut for
	// all components, e.g. button with label "&Quit".
	// If cvui has a value for waitKey, it will call
	// waitKey() automatically for us within cvui::update().
	cvui::init(WINDOW_NAME, 20);
    
    cv::String input = "123";
    int count = 0;

	while (true) {
		frame = cv::Scalar(49, 52, 49);

		// Input component will return an integer value representing
		// they key that was pressed.
		int key = cvui::input(frame, 40, 40, 100, "myInput", input);

		cvui::printf(frame, 160, 50, "Click the input, type a number then press enter");

        // The contants defined as cvui::KEY_* can be used to identify pressed keys.
        // You can use them to detect special keys as cvui::KEY_HOME and cvui::KEY_END.
        if (key == cvui::KEY_ENTER) {
            count = atoi(input.c_str());
        }

		cvui::counter(frame, 500, 45, &count);

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
