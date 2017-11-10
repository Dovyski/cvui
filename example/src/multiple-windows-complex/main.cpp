/*
This demo shows how to use cvui in multiple windows relying on rows and colums.
Code licensed under the MIT license, check LICENSE file.
*/

#include <iostream>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>

#define CVUI_IMPLEMENTATION
#include "cvui.h"

#define WINDOW1_NAME "Windows 1"
#define WINDOW2_NAME "Windows 2"

int main(int argc, const char *argv[])
{
	// We have one mat for each window.
	cv::Mat frame1 = cv::Mat(600, 800, CV_8UC3), frame2 = cv::Mat(600, 800, CV_8UC3);
	
	// Create variables used by some components
	std::vector<double> window1_values;
	std::vector<double> window2_values;
	bool window1_checked = false, window1_checked2 = false;
	bool window2_checked = false, window2_checked2 = false;
	double window1_value = 1.0, window1_value2 = 1.0, window1_value3 = 1.0;
	double window2_value = 1.0, window2_value2 = 1.0, window2_value3 = 1.0;

	cv::Mat img = cv::imread("./lena-face.jpg", cv::IMREAD_COLOR);
	cv::Mat imgRed = cv::imread("./lena-face-red.jpg", cv::IMREAD_COLOR);
	cv::Mat imgGray = cv::imread("./lena-face-gray.jpg", cv::IMREAD_COLOR);

	int padding = 10;

	// Fill the vector with a few random values
	for (std::vector<double>::size_type i = 0; i < 20; i++) {
		window1_values.push_back(rand() + 0.);
		window2_values.push_back(rand() + 0.);
	}

	// Start two OpenCV windows
	cv::namedWindow(WINDOW1_NAME);
	cv::namedWindow(WINDOW2_NAME);
	
	// Init cvui and inform it to use the first window as the default one.
	// cvui::init() will automatically watch the informed window.
	cvui::init(WINDOW1_NAME);

	// Tell cvui to keep track of mouse events in window2 as well.
	cvui::watch(WINDOW2_NAME);

	while (true) {
		// Inform cvui that all subsequent component calls and events are related to window 1.
		cvui::context(WINDOW1_NAME);

		// Fill the frame with a nice color
		frame1 = cv::Scalar(49, 52, 49);

		cvui::beginRow(frame1, 10, 20, 100, 50);
			cvui::text("This is ");
			cvui::printf("a row");
			cvui::checkbox("checkbox", &window1_checked);
			cvui::window(80, 80, "window");
			cvui::rect(50, 50, 0x00ff00, 0xff0000);
			cvui::sparkline(window1_values, 50, 50);
			cvui::counter(&window1_value);
			cvui::button(100, 30, "Fixed");
			cvui::image(img);
			cvui::button(img, imgGray, imgRed);
		cvui::endRow();

		padding = 50;
		cvui::beginRow(frame1, 10, 150, 100, 50, padding);
			cvui::text("This is ");
			cvui::printf("another row");
			cvui::checkbox("checkbox", &window1_checked2);
			cvui::window(80, 80, "window");
			cvui::button(100, 30, "Fixed");
			cvui::printf("with 50px paddin7hg.");
		cvui::endRow();

		cvui::beginRow(frame1, 10, 250, 100, 50);
			cvui::text("This is ");
			cvui::printf("another row with a trackbar ");
			cvui::trackbar(150, &window1_value2, 0., 5.);
			cvui::printf(" and a button ");
			cvui::button(100, 30, "button");
		cvui::endRow();

		cvui::beginColumn(frame1, 50, 330, 100, 200);
			cvui::text("Column 1 (no padding)");
			cvui::button("button1");
			cvui::button("button2");
			cvui::text("End of column 1");
		cvui::endColumn();

		padding = 10;
		cvui::beginColumn(frame1, 300, 330, 100, 200, padding);
			cvui::text("Column 2 (padding = 10)");
			cvui::button("button1");
			cvui::button("button2");
			cvui::trackbar(150, &window1_value3, 0., 5., 1, "%3.2Lf", cvui::TRACKBAR_DISCRETE, 0.25);
			cvui::text("End of column 2");
		cvui::endColumn();

		cvui::beginColumn(frame1, 550, 330, 100, 200);
			cvui::text("Column 3 (use space)");
			cvui::space(5);
			cvui::button("button1 5px below");
			cvui::space(50);
			cvui::text("Text 50px below");
			cvui::space(20);
			cvui::button("Button 20px below");
			cvui::space(40);
			cvui::text("End of column 2 (40px below)");
		cvui::endColumn();
		
		// Update all components of window1, e.g. mouse clicks, and show it.
		cvui::update(WINDOW1_NAME);
		cv::imshow(WINDOW1_NAME, frame1);

		// From this point on, we are going to render the second window. We need to inform cvui
		// that all updates and components from now on are connected to window 2.
		// We do that by calling cvui::context().
		cvui::context(WINDOW2_NAME);
		frame2 = cv::Scalar(49, 52, 49);
		
		cvui::beginRow(frame2, 10, 20, 100, 50);
			cvui::text("This is ");
			cvui::printf("a row");
			cvui::checkbox("checkbox", &window2_checked);
			cvui::window(80, 80, "window");
			cvui::rect(50, 50, 0x00ff00, 0xff0000);
			cvui::sparkline(window2_values, 50, 50);
			cvui::counter(&window2_value);
			cvui::button(100, 30, "Fixed");
			cvui::image(img);
			cvui::button(img, imgGray, imgRed);
		cvui::endRow();

		padding = 50;
		cvui::beginRow(frame2, 10, 150, 100, 50, padding);
			cvui::text("This is ");
			cvui::printf("another row");
			cvui::checkbox("checkbox", &window2_checked2);
			cvui::window(80, 80, "window");
			cvui::button(100, 30, "Fixed");
			cvui::printf("with 50px paddin7hg.");
		cvui::endRow();

		// Another row mixing several components 
		cvui::beginRow(frame2, 10, 250, 100, 50);
		cvui::text("This is ");
		cvui::printf("another row with a trackbar ");
		cvui::trackbar(150, &window2_value2, 0., 5.);
		cvui::printf(" and a button ");
		cvui::button(100, 30, "button");
		cvui::endRow();

		cvui::beginColumn(frame2, 50, 330, 100, 200);
			cvui::text("Column 1 (no padding)");
			cvui::button("button1");
			cvui::button("button2");
			cvui::text("End of column 1");
		cvui::endColumn();

		padding = 10;
		cvui::beginColumn(frame2, 300, 330, 100, 200, padding);
			cvui::text("Column 2 (padding = 10)");
			cvui::button("button1");
			cvui::button("button2");
			cvui::trackbar(150, &window2_value3, 0., 5., 1, "%3.2Lf", cvui::TRACKBAR_DISCRETE, 0.25);
			cvui::text("End of column 2");
		cvui::endColumn();

		cvui::beginColumn(frame2, 550, 330, 100, 200);
			cvui::text("Column 3 (use space)");
			cvui::space(5);
			cvui::button("button1 5px below");
			cvui::space(50);
			cvui::text("Text 50px below");
			cvui::space(20);
			cvui::button("Button 20px below");
			cvui::space(40);
			cvui::text("End of column 2 (40px below)");
		cvui::endColumn();

		// Update all components of window2, e.g. mouse clicks, and show it.
		cvui::update(WINDOW2_NAME);
		cv::imshow(WINDOW2_NAME, frame2);

		// Check if ESC key was pressed
		if (cv::waitKey(20) == 27) {
			break;
		}
	}

	return 0;
}