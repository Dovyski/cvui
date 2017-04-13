/*
This is a demo application to showcase the sparkline components of cvui.
Sparklines are quite useful to display data, e.g. FPS charts.

Code licensed under the MIT license, check LICENSE file.
*/

#include <iostream>
#include <fstream>
#include <stdexcept>

#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>

#include "cvui.h"

#define WINDOW_NAME		"Trackbar"



int main(int argc, const char *argv[])
{
	int intValue1 = 30;
	uchar ucharValue2 = 30;
	char charValue3 = 30;
	float floatValue1 = 12.;
	double doubleValue1 = 15., doubleValue2 = 10.3, doubleValue3 = 2.25;
	cv::Mat frame = cv::Mat(cv::Size(250, 750), CV_8UC3);

	// Create an OpenCV window
	cv::namedWindow(WINDOW_NAME);
	
	// Tell cvui to use a value of 20 for cv::waitKey()
	// because we want to enable keyboard shortcut for
	// all components, e.g. button with label "&Quit".
	// If cvui has a value for waitKey, it will call
	// waitKey() automatically for us within cvui::update().
	cvui::init(WINDOW_NAME, 20);

	while (true) {
		frame = cv::Scalar(50, 50, 50);

		cvui::beginColumn(frame, 20, 20, -1, -1, 6);
			/**
			The API of the tracbkar is shown here for reference (extract from cvui.h)
			trackbar : Display a trackbar
			 \param theValue : pointer to the variable that will hold the value. Will be modified when the user interacts
			 \param theMin : minimum value of the trackbar
			 \param theMax : maximum value of the trackbar
			 \param theNumberOfDecimals : number of decimal digits to be displayed
			 \param theNumberOfLargeSteps : number of large steps (at which a legend will be written, as on a ruler)
			 \param theSmallStep : small steps at which ticks will be drawn (if not given,
			 \                    theSmallStep is a calculated according to theNumberOfDecimals)
			 \param flagForceValuesAsMultiplesOfSmallStep : enforce values to be a multiple of theSmallStep

			 template <typename T> // T can be any float type (float, double, long double)
				bool trackbar(
						T *theValue,
						T theMin, T theMax,
						int theNumberOfDecimals = 1,
						int theNumberOfLargeSteps = 1,
						T theSmallStep = -1.,
						bool flagForceValuesAsMultiplesOfSmallStep = true);

			   Note : remember to cast the minimum and maximum values to your type
			  See examples below :

			   float myValue;
			   cvui::trackbar_float(&myValue, 0.f, 100.f);
			   unsigned char myValue;
			   cvui::trackbar_float(&myValue, (unsigned char)0, (unsigned char)255);

			   Returns true when the value was modified, false otherwise
			*/

			cvui::text("Simple int trackbar, no ticks");
			cvui::trackbar(150, &intValue1, 0, 100, 0);
			cvui::text("");

			cvui::text("Simple uchar trackbar");
			cvui::trackbar(150, &ucharValue2, (uchar)0, (uchar)255, 0);
			cvui::text("");

			cvui::text("Simple signed char trackbar, no large");
			cvui::trackbar(150, &charValue3, (char)-128, (char)127, 0);
			cvui::text("");

			cvui::text("Simple float trackbar");
			cvui::text("1 decimal, no large step");
			cvui::trackbar(150, &floatValue1, 10.f, 15.f, 1);
			cvui::text("");

			cvui::text("Simple float trackbar");
			cvui::text(" 2 decimals, 4 large Steps");
			cvui::trackbar(150, &doubleValue1, 10., 20., 2, 4);
			cvui::text("");

			cvui::text("Simple float trackbar, 1 decimal");
			cvui::text("no larges steps");
			cvui::text("edited value forced to 1 decimal");
			cvui::trackbar(150, &doubleValue2, 10., 10.5, 1, 1, 0.1);

			cvui::text("float trackbar, 2 decimal");
			cvui::text("value multiples of 0.25");
			cvui::text("2 large steps");
			cvui::trackbar(150, &doubleValue3, 0., 4., 2, 2, 0.25, cvui::TRACKBAR_DISCRETE);

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
