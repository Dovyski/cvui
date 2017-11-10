/*
This is a demo application to showcase the UI components of cvui.

Copyright (c) 2016 Fernando Bevilacqua <dovyski@gmail.com>
Licensed under the MIT license.
*/

#include <iostream>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>

#define CVUI_IMPLEMENTATION
#include "cvui.h"

#define WINDOW_NAME	"CVUI Test"

int main(int argc, const char *argv[])
{
	cv::Mat frame = cv::Mat(300, 600, CV_8UC3);
	bool checked = false;
	bool checked2 = true;
	int count = 0;
	double countFloat = 0.0;
	double trackbarValue = 0.0;

	// Init cvui and tell it to create a OpenCV window, i.e. cv::namedWindow(WINDOW_NAME).
	cvui::init(WINDOW_NAME);

	while (true) {
		// Fill the frame with a nice color
		frame = cv::Scalar(49, 52, 49);

		// Show some pieces of text.
		cvui::text(frame, 50, 30, "Hey there!");
		
		// You can also specify the size of the text and its color
		// using hex 0xRRGGBB CSS-like style.
		cvui::text(frame, 200, 30, "Use hex 0xRRGGBB colors easily", 0.4, 0xff0000);
		
		// Sometimes you want to show text that is not that simple, e.g. strings + numbers.
		// You can use cvui::printf for that. It accepts a variable number of parameter, pretty
		// much like printf does.
		cvui::printf(frame, 200, 50, 0.4, 0x00ff00, "Use printf formatting: %d + %.2f = %f", 2, 3.2, 5.2);

		// Buttons will return true if they were clicked, which makes
		// handling clicks a breeze.
		if (cvui::button(frame, 50, 60, "Button")) {
			std::cout << "Button clicked" << std::endl;
		}

		// If you do not specify the button width/height, the size will be
		// automatically adjusted to properly house the label.
		cvui::button(frame, 200, 70, "Button with large label");
		
		// You can tell the width and height you want
		cvui::button(frame, 410, 70, 15, 15, "x");

		// Window components are useful to create HUDs and similars. At the
		// moment, there is no implementation to constraint content within a
		// a window.
		cvui::window(frame, 50, 120, 120, 100, "Window");
		
		// The counter component can be used to alter int variables. Use
		// the 4th parameter of the function to point it to the variable
		// to be changed.
		cvui::counter(frame, 200, 120, &count);

		// Counter can be used with doubles too. You can also specify
		// the counter's step (how much it should change
		// its value after each button press), as well as the format
		// used to print the value.
		cvui::counter(frame, 320, 120, &countFloat, 0.1, "%.1f");

		// The trackbar component can be used to create scales.
		// It works with all numerical types (including chars).
		cvui::trackbar(frame, 420, 110, 150, &trackbarValue, 0., 50.);
		
		// Checkboxes also accept a pointer to a variable that controls
		// the state of the checkbox (checked or not). cvui::checkbox() will
		// automatically update the value of the boolean after all
		// interactions, but you can also change it by yourself. Just
		// do "checked = true" somewhere and the checkbox will change
		// its appearance.
		cvui::checkbox(frame, 200, 160, "Checkbox", &checked);
		cvui::checkbox(frame, 200, 190, "A checked checkbox", &checked2);

		// Display the lib version at the bottom of the screen
		cvui::printf(frame, frame.cols - 80, frame.rows - 20, 0.4, 0xCECECE, "cvui v.%s", cvui::VERSION);

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