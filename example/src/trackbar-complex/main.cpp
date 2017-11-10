/*
This is a demo application to showcase the use of trackbars and columns.
Authors: Pascal Thomet, Fernando Bevilacqua
*/

#include <iostream>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>

#define CVUI_IMPLEMENTATION
#include "cvui.h"

#define WINDOW_NAME	"Trackbar and columns"

int main(int argc, const char *argv[])
{
	int intValue1 = 30;
	uchar ucharValue2 = 30;
	char charValue3 = 30;
	float floatValue1 = 12.;
	double doubleValue1 = 15., doubleValue2 = 10.3, doubleValue3 = 2.25;
	cv::Mat frame = cv::Mat(cv::Size(450, 650), CV_8UC3);

	// Size of trackbars
	int width = 400;

	// Init cvui and tell it to use a value of 20 for cv::waitKey()
	// because we want to enable keyboard shortcut for
	// all components, e.g. button with label "&Quit".
	// If cvui has a value for waitKey, it will call
	// waitKey() automatically for us within cvui::update().
	cvui::init(WINDOW_NAME, 20);

	while (true) {
		frame = cv::Scalar(49, 52, 49);

		cvui::beginColumn(frame, 20, 20, -1, -1, 6);
			cvui::text("int trackbar, no customization");
			cvui::trackbar(width, &intValue1, 0, 100);
			cvui::space(5);

			cvui::text("uchar trackbar, no customization");
			cvui::trackbar(width, &ucharValue2, (uchar)0, (uchar)255);
			cvui::space(5);

			cvui::text("signed char trackbar, no customization");
			cvui::trackbar(width, &charValue3, (char)-128, (char)127);
			cvui::space(5);

			cvui::text("float trackbar, no customization");
			cvui::trackbar(width, &floatValue1, 10.f, 15.f);
			cvui::space(5);

			cvui::text("float trackbar, 4 segments");
			cvui::trackbar(width, &doubleValue1, 10., 20., 4);
			cvui::space(5);

			cvui::text("double trackbar, label %.1Lf, TRACKBAR_DISCRETE");
			cvui::trackbar(width, &doubleValue2, 10., 10.5, 1, "%.1Lf", cvui::TRACKBAR_DISCRETE, 0.1);
			cvui::space(5);

			cvui::text("double trackbar, label %.2Lf, 2 segments, TRACKBAR_DISCRETE");
			cvui::trackbar(width, &doubleValue3, 0., 4., 2, "%.2Lf", cvui::TRACKBAR_DISCRETE, 0.25);
			cvui::space(10);

			// Exit the application if the quit button was pressed.
			// It can be pressed because of a mouse click or because 
			// the user pressed the "q" key on the keyboard, which is
			// marked as a shortcut in the button label ("&Quit").
			if (cvui::button("&Quit")) {
				break;
			}
		cvui::endColumn();

		// Since cvui::init() received a param regarding waitKey,
		// there is no need to call cv::waitKey() anymore. cvui::update()
		// will do it automatically.
		cvui::update();
		
		cv::imshow(WINDOW_NAME, frame);
	}

	return 0;
}
