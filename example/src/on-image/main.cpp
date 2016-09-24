/*
This is a demo application to showcase the UI components of cvui.

Copyright (c) 2016 Fernando Bevilacqua <dovyski@gmail.com>
Licensed under the MIT license.
*/

#include <iostream>

#include <opencv2/core/core.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>

#include "cvui.h"

#define WINDOW_NAME		"CVUI Test"

int main(int argc, const char *argv[])
{
	cv::Mat frame_orig = cv::imread("lena.jpg");
	cv::Mat frame = frame_orig.clone();
	cv::Mat doubleBuffer = frame.clone();

	// Init a OpenCV window and tell cvui to use it.
	// If cv::namedWindow() is not used, mouse events will
	// not be captured by cvui.
	cv::namedWindow(WINDOW_NAME);
	cvui::init(WINDOW_NAME);

	while (true) {
		doubleBuffer.copyTo(frame);

		if (cvui::button(frame, frame.cols - 100, frame.rows - 30, "&Quit")) {
			break;
		}

		//Quick info about the Tracbar params
		//double MinimumValue, MaximumValue : self-explanatory
		//double SmallStep, LargeStep : steps at which smaller and larger ticks are drawn
		//bool ForceValuesAsMultiplesOfSmallStep : we can enforce the value to be a multiple of the small step
		//bool DrawValuesAtLargeSteps : draw value at large steps
		//string Printf_Format : printf format string of the value
		//string Printf_Format_Steps : printf format string of the steps (will be replaced by Printf_Format if empty)
		cvui::TrackbarParams colorTrackbarParams;
		colorTrackbarParams.MinimumValue = 0.;
		colorTrackbarParams.MaximumValue = 2.;
		colorTrackbarParams.LargeStep = 0.5;
		colorTrackbarParams.SmallStep = 0.1;
		colorTrackbarParams.Printf_Format = "%3.02lf";
		colorTrackbarParams.Printf_Format_Steps = "%3.02lf";
		colorTrackbarParams.ForceValuesAsMultiplesOfSmallStep = false;

		//
		// RGB HUD
		//

		// Window components are useful to create HUDs and similars. At the
		// moment, there is no implementation to constraint content within a
		// a window.
		cvui::window(frame, 20, 50, 180, 220, "RGB adjust");

		// In a columns, all added elements are
		// vertically placed, one under the other (from top to bottom)
		//
		// Within the cvui::beginColumns() and cvui::endColumn(),
		// all elements will be automatically positioned by cvui.
		//
		// Notice that all component calls within the begin/end block
		// DO NOT have (x,y) coordinates.
		//
		// Let's create a row at position (35,80) with automatic width and height, and a padding of 10
		cvui::beginColumn(frame, 35, 80, -1, -1, 10);
			static double rgb[3] {1., 1., 1};
			bool rgbModified = false;
			// Trackbar accept a pointer to a variable that controls their value
			// They return true upon edition
			if (cvui::trackbar(&rgb[0], colorTrackbarParams))
				rgbModified = true;
			if (cvui::trackbar(&rgb[1], colorTrackbarParams))
				rgbModified = true;
			if (cvui::trackbar(&rgb[2], colorTrackbarParams))
				rgbModified = true;
			cvui::printf(0.35, 0xcccccc, "   RGB: %3.02lf,%3.02lf,%3.02lf", rgb[0], rgb[1], rgb[2]);

			if (rgbModified) {
				std::vector<cv::Mat> channels;
				cv::split(frame_orig, channels);
				for (int c = 0; c < 3; c++)
					channels[c] = channels[c] * rgb[c];
				cv::merge(channels, doubleBuffer);
			}
		cvui::endColumn();

		// HSV
		cvui::window(frame, frame_orig.cols - 180, 50, 180, 220, "HSV adjust");
		cvui::beginColumn(frame, frame_orig.cols - 180, 80, -1, -1, 10);
			static double hsv[3] {1., 1., 1};
			bool hsvModified = false;
			if (cvui::trackbar(&hsv[0], colorTrackbarParams))
				hsvModified = true;
			if (cvui::trackbar(&hsv[1], colorTrackbarParams))
				hsvModified = true;
			if (cvui::trackbar(&hsv[2], colorTrackbarParams))
				hsvModified = true;
			cvui::printf(0.35, 0xcccccc, "   HSV: %3.02lf,%3.02lf,%3.02lf", hsv[0], hsv[1], hsv[2]);

			if (hsvModified) {
				cv::Mat hsvMat;
				cv::cvtColor(frame_orig, hsvMat, cv::COLOR_BGR2HSV);
				std::vector<cv::Mat> channels;
				cv::split(hsvMat, channels);
				for (int c = 0; c < 3; c++)
					channels[c] = channels[c] * hsv[c];
				cv::merge(channels, hsvMat);
				cv::cvtColor(hsvMat, doubleBuffer, cv::COLOR_HSV2BGR);
			}
		cvui::endColumn();

		// Display the lib version at the bottom of the screen
		cvui::printf(frame, frame.cols - 300, frame.rows - 20, 0.4, 0xCECECE, "cvui v.%s", cvui::VERSION);

		// This function must be called *AFTER* all UI components. It does
		// all the behind the scenes magic to handle mouse clicks, etc.
		cvui::update();

		// Show everything on the screen
		cv::imshow(WINDOW_NAME, frame);
	}

	return 0;
}