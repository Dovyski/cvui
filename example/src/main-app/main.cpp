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
	bool checked = false;
	bool checked2 = true;
	int count = 0;
	double trackbarValue = 0.0;

	// Init cvui and tell it to create a OpenCV window, i.e. cv::namedWindow(WINDOW_NAME).
	cvui::init(WINDOW_NAME);

    double scaling = 1.0;
    double currentScaling = -1;
    cv::Mat frame;

	while (true) {
        if (scaling != currentScaling) {
            frame = cv::Mat(std::lround(scaling * 300), std::lround(scaling * 600), CV_8UC3);
            currentScaling = scaling;
        }

		// Fill the frame with a nice color
		frame = cv::Scalar(49, 52, 49);

		// Show some pieces of text.
		cvui::text(frame, std::lround(scaling * 50), std::lround(scaling * 30), "Hey there!", scaling*cvui::DEFAULT_FONT_SCALE);
		
		// You can also specify the size of the text and its color
		// using hex 0xRRGGBB CSS-like style.
		cvui::text(frame, std::lround(scaling * 200), std::lround(scaling * 30), "Use hex 0xRRGGBB colors easily", scaling*cvui::DEFAULT_FONT_SCALE, 0xff0000);
		
		// Sometimes you want to show text that is not that simple, e.g. strings + numbers.
		// You can use cvui::printf for that. It accepts a variable number of parameter, pretty
		// much like printf does.
		cvui::printf(frame, std::lround(scaling * 200), std::lround(scaling * 50), scaling*cvui::DEFAULT_FONT_SCALE, 0x00ff00, "Use printf formatting: %d + %.2f = %f", 2, 3.2, 5.2);

		// Buttons will return true if they were clicked, which makes
		// handling clicks a breeze.
		if (cvui::button(frame, std::lround(scaling * 50), std::lround(scaling * 60), "Colored Button", scaling*cvui::DEFAULT_FONT_SCALE, 0xa05050)) {
			std::cout << "Button clicked" << std::endl;
		}

		// If you do not specify the button width/height, the size will be
		// automatically adjusted to properly house the label.
		cvui::button(frame, std::lround(scaling * 200), std::lround(scaling * 70), "Button with large label", scaling*cvui::DEFAULT_FONT_SCALE);
		
		// You can tell the width and height you want
		cvui::button(frame, std::lround(scaling * 410), std::lround(scaling * 70), std::lround(scaling * 15), std::lround(scaling * 15), "x", scaling*cvui::DEFAULT_FONT_SCALE);

		// Window components are useful to create HUDs and similars. At the
		// moment, there is no implementation to constraint content within a
		// a window.
		cvui::window(frame, std::lround(scaling * 50), std::lround(scaling * 120), std::lround(scaling * 120), std::lround(scaling * 100), "Window", scaling*cvui::DEFAULT_FONT_SCALE);
		
		// The counter component can be used to alter int variables. Use
		// the 4th parameter of the function to point it to the variable
		// to be changed.
		cvui::counter(frame, std::lround(scaling * 200), std::lround(scaling * 120), &count, 1, "%d", scaling*cvui::DEFAULT_FONT_SCALE);

		// Counter can be used with doubles too. You can also specify
		// the counter's step (how much it should change
		// its value after each button press), as well as the format
		// used to print the value.
		cvui::counter(frame, std::lround(scaling * 320), std::lround(scaling * 120), &scaling, 0.1, "%.1f", scaling*cvui::DEFAULT_FONT_SCALE, 0x50a050);

        cvui::printf(frame, std::lround(scaling * 340), std::lround(scaling * 150), scaling*cvui::DEFAULT_FONT_SCALE, 0xCECECE, "Scaling");

		// The trackbar component can be used to create scales.
		// It works with all numerical types (including chars).
		cvui::trackbar(frame, std::lround(scaling * 420), std::lround(scaling * 110), std::lround(scaling * 150), &trackbarValue, 0., 50., 1, "%.1Lf", 0, 1.0, scaling*cvui::DEFAULT_FONT_SCALE);
		
		// Checkboxes also accept a pointer to a variable that controls
		// the state of the checkbox (checked or not). cvui::checkbox() will
		// automatically update the value of the boolean after all
		// interactions, but you can also change it by yourself. Just
		// do "checked = true" somewhere and the checkbox will change
		// its appearance.
		cvui::checkbox(frame, std::lround(scaling * 200), std::lround(scaling * 190), "Checkbox", &checked, 0x000000, scaling*cvui::DEFAULT_FONT_SCALE);
		cvui::checkbox(frame, std::lround(scaling * 200), std::lround(scaling * 220), "A checked checkbox", &checked2, 0x000000, scaling*cvui::DEFAULT_FONT_SCALE);

		// Display the lib version at the bottom of the screen
		cvui::printf(frame, frame.cols - std::lround(scaling * 80), frame.rows - std::lround(scaling * 20), scaling*cvui::DEFAULT_FONT_SCALE, 0xCECECE, "cvui v.%s", cvui::VERSION);

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
