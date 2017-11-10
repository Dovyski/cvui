/*
This application showcase how UI components can be placed in order
to create a more complex layout. The position of all components is
determined by a (x,y) pair prodived by the developer.

Take a look at the "row-column" application to see how to use
automatic positioning by leveraging the begin*()/end*() API.

Code licensed under the MIT license, check LICENSE file.
*/

#include <iostream>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>

#define CVUI_IMPLEMENTATION
#include "cvui.h"

#define WINDOW_NAME	"Complex layout"

void group(cv::Mat& frame, int x, int y, int width, int height) {
	int padding = 5, w = (width - padding) / 4, h = (height - 15 - padding) / 2;
	cv::Point pos(x + padding, y + 5);

	cvui::text(frame, pos.x, pos.y, "Group title");
	pos.y += 15;

	cvui::window(frame, pos.x, pos.y, width - padding * 2, h - padding, "Something");
	cvui::rect(frame, pos.x + 2, pos.y + 20, width - padding * 2 - 5, h - padding - 20, 0xff0000);
	pos.y += h;

	cvui::window(frame, pos.x, pos.y, w / 3 - padding, h, "Some");
	cvui::text(frame, pos.x + 25, pos.y + 60, "65", 1.1);
	pos.x += w / 3;

	cvui::window(frame, pos.x, pos.y, w / 3 - padding, h, "Info");
	cvui::text(frame, pos.x + 25, pos.y + 60, "30", 1.1);
	pos.x += w / 3;

	cvui::window(frame, pos.x, pos.y, w / 3 - padding, h, "Here");
	cvui::text(frame, pos.x + 25, pos.y + 60, "70", 1.1);
	pos.x += w / 3;

	cvui::window(frame, pos.x, pos.y, w - padding, h, "And");
	cvui::rect(frame, pos.x + 2, pos.y + 22, w - padding - 5, h - padding - 20, 0xff0000);
	pos.x += w;

	cvui::window(frame, pos.x, pos.y, w - padding, h, "Here");
	cvui::rect(frame, pos.x + 2, pos.y + 22, w - padding - 5, h - padding - 20, 0xff0000);
	pos.x += w;

	cvui::window(frame, pos.x, pos.y, w - padding, h, "More info");
	cvui::rect(frame, pos.x + 2, pos.y + 22, w - padding - 5, h - padding - 20, 0xff0000);
	pos.x += w;
}


int main(int argc, const char *argv[])
{
	int height = 220, spacing = 10;
	cv::Mat frame = cv::Mat(height * 3, 1300, CV_8UC3);

	// Init cvui and tell it to create a OpenCV window, i.e. cv::namedWindow(WINDOW_NAME).
	cvui::init(WINDOW_NAME);

	while (true) {
		// Fill the frame with a nice color
		frame = cv::Scalar(49, 52, 49);

		// Render three groups of components.
		group(frame, 0, 0, frame.cols, height - spacing);
		group(frame, 0, height, frame.cols, height - spacing);
		group(frame, 0, height * 2, frame.cols, height - spacing);
		
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