/*
This is application demonstrates how you can use cvui when your project has
multiple files that use cvui.

Code licensed under the MIT license, check LICENSE file.
*/

#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>

// One (and only one) of your C++ files must define CVUI_IMPLEMENTATION
// before the inclusion of cvui.h to ensure its implementaiton is compiled.
// In this project, main.cpp (this file) is the one to ensure cvui.h gets
// its implementaiton compiled.
#define CVUI_IMPLEMENTATION
#include "cvui.h"

// Include project external classes
#include "Class1.h"
#include "Class2.h"

#define WINDOW_NAME "CVUI Multiple files"

int main(int argc, const char *argv[])
{
	cv::Mat frame = cv::Mat(300, 500, CV_8UC3);

	Class1 c1;
	Class2 c2;

	// Init cvui and tell it to create a OpenCV window, i.e. cv::namedWindow(WINDOW_NAME).
	cvui::init(WINDOW_NAME);

	while (true) {
		// Fill the frame with a nice color
		frame = cv::Scalar(49, 52, 49);

		c1.renderInfo(frame);
		c2.renderMessage(frame);

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