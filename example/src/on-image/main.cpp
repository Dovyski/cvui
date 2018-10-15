/*
This is a demo application to showcase the UI components of cvui.
Author: Pascal Thomet
*/

#include <iostream>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>

#define CVUI_IMPLEMENTATION
#include "cvui.h"

#define WINDOW_NAME	"CVUI Test"

int main(int argc, const char *argv[])
{
	cv::Mat lena = cv::imread("lena.jpg");
	cv::Mat frame = lena.clone();
	cv::Mat doubleBuffer = frame.clone();
	int trackbarWidth = 130;

	// Init cvui and tell it to use a value of 20 for cv::waitKey()
	// because we want to enable keyboard shortcut for
	// all components, e.g. button with label "&Quit".
	// If cvui has a value for waitKey, it will call
	// waitKey() automatically for us within cvui::update().
	cvui::init(WINDOW_NAME, 20);

	while (true) {
		doubleBuffer.copyTo(frame);

		// Exit the application if the quit button was pressed.
		// It can be pressed because of a mouse click or because 
		// the user pressed the "q" key on the keyboard, which is
		// marked as a shortcut in the button label ("&Quit").
		if (cvui::button(frame, frame.cols - 100, frame.rows - 30, "&Quit")) {
			break;
		}

		// RGB HUD
		cvui::window(frame, 20, 50, 180, 240, "RGB adjust");

		// Within the cvui::beginColumns() and cvui::endColumn(),
		// all elements will be automatically positioned by cvui.
		// In a columns, all added elements are vertically placed,
		// one under the other (from top to bottom).
		//
		// Notice that all component calls within the begin/end block
		// below DO NOT have (x,y) coordinates.
		//
		// Let's create a row at position (35,80) with automatic
		// width and height, and a padding of 10
		cvui::beginColumn(frame, 35, 80, -1, -1, 10);
			static double rgb[3] {1., 1., 1};
			bool rgbModified = false;

			// Trackbar accept a pointer to a variable that controls their value
			// They return true upon edition
			if (cvui::trackbar(trackbarWidth, &rgb[0], (double)0., (double)2., 2, "%3.02Lf")) {
				rgbModified = true;
			}
			if (cvui::trackbar(trackbarWidth, &rgb[1], (double)0., (double)2., 2, "%3.02Lf")) {
				rgbModified = true;
			}
			if (cvui::trackbar(trackbarWidth, &rgb[2], (double)0., (double)2., 2, "%3.02Lf")) {
				rgbModified = true;
			}
			
			cvui::space(2);
			cvui::printf(0.35, 0xcccccc, "   RGB: %3.02lf,%3.02lf,%3.02lf", rgb[0], rgb[1], rgb[2]);

			if (rgbModified) {
				std::vector<cv::Mat> channels(3);
				cv::split(lena, channels);
				for (int c = 0; c < 3; c++) {
					channels[c] = channels[c] * rgb[c];
				}
				cv::merge(channels, doubleBuffer);
			}
		cvui::endColumn();

		// HSV
		cvui::window(frame, lena.cols - 200, 50, 180, 240, "HSV adjust");
		cvui::beginColumn(frame, lena.cols - 180, 80, -1, -1, 10);
			static double hsv[3] {1., 1., 1};
			bool hsvModified = false;
			
			if (cvui::trackbar(trackbarWidth, &hsv[0], (double)0., (double)2., 2, "%3.02Lf")) {
				hsvModified = true;
			}
			if (cvui::trackbar(trackbarWidth, &hsv[1], (double)0., (double)2., 2, "%3.02Lf")) {
				hsvModified = true;
			}
			if (cvui::trackbar(trackbarWidth, &hsv[2], (double)0., (double)2., 2, "%3.02Lf")) {
				hsvModified = true;
			}

			cvui::space(2);
			cvui::printf(0.35, 0xcccccc, "   HSV: %3.02lf,%3.02lf,%3.02lf", hsv[0], hsv[1], hsv[2]);

			if (hsvModified) {
				cv::Mat hsvMat;
				cv::cvtColor(lena, hsvMat, cv::COLOR_BGR2HSV);
				std::vector<cv::Mat> channels(3);
				cv::split(hsvMat, channels);

				for (int c = 0; c < 3; c++) {
					channels[c] = channels[c] * hsv[c];
				}

				cv::merge(channels, hsvMat);
				cv::cvtColor(hsvMat, doubleBuffer, cv::COLOR_HSV2BGR);
			}
		cvui::endColumn();

		// Display the lib version at the bottom of the screen
		cvui::printf(frame, frame.cols - 300, frame.rows - 20, 0.4, 0xCECECE, "cvui v.%s", cvui::VERSION);

		// This function must be called *AFTER* all UI components. It does
		// all the behind the scenes magic to handle mouse clicks, etc.
		//
		// Since cvui::init() received a param regarding waitKey,
		// there is no need to call cv::waitKey() anymore. cvui::update()
		// will do it automatically.
		cvui::update();

		// Show everything on the screen
		cv::imshow(WINDOW_NAME, frame);
	}

	return 0;
}