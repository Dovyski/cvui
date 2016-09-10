/*
This application demonstrates the use of begin*()/end*() to
create nested rows/columns. Check the "row-column" app to
understand automatic positioning and to check a simpler
use of begin*()/end*().

Code licensed under the MIT license, check LICENSE file.
*/

#include <iostream>

#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>

#include "cvui.h"

#define WINDOW_NAME		"Nested rows and columns"


int main(int argc, const char *argv[])
{
	cv::Mat frame = cv::Mat(600, 800, CV_8UC3);
	std::vector<double> values;
	bool checked = false;
	double value = 1.0;

	// Fill the vector with a few random values
	for (std::vector<double>::size_type i = 0; i < 20; i++) {
		values.push_back(rand() + 0.);
	}

	// Init a OpenCV window and tell cvui to use it.
	// If cv::namedWindow() is not used, mouse events will
	// not be captured by cvui.
	cv::namedWindow(WINDOW_NAME);
	cvui::init(WINDOW_NAME);

	while (true) {
		// Fill the frame with a nice color
		frame = cv::Scalar(49, 52, 49);

		// Define a row at position (10, 50) with width 100 and height 150.
		cvui::beginRow(frame, 10, 50, 100, 150);
			// The components below will be placed one besides the other.
			cvui::text("Row starts");
			cvui::button("here");

			// When a column or row is nested within another, it behaves like
			// an ordinary component with the specified size. In this case,
			// let's create a column with width 100 and height 50. The
			// next component added will behave like it was added after
			// a component with width 100 and heigth 50.
			cvui::beginColumn(100, 150);
				cvui::text("Column 1");
				cvui::button("button1");
				cvui::button("button2");
				cvui::button("button3");
				cvui::text("End of column 1");
			cvui::endColumn();

			// Add two pieces of text
			cvui::text("Hi again,");
			cvui::text("its me!");

			// Start a new column
			cvui::beginColumn(100, 50);
				cvui::text("Column 2");
				cvui::button("button1");
				cvui::button("button2");
				cvui::button("button3");
				cvui::space();
				cvui::text("Another text");
				cvui::space(40);
				cvui::text("End of column 2");
			cvui::endColumn();

			// Add more text
			cvui::text("this is the ");
			cvui::text("end of the row!");
		cvui::endRow();

		// Here is another nested row/column
		cvui::beginRow(frame, 50, 300, 100, 150);
			// If you don't want to calculate the size of any row/column WITHIN
			// a begin*()/end*() block, just use negative width/height when
			// calling beginRow() or beginColumn() (or don't provide width/height at all!)

			// For instance, the following column will have its width/height
			// automatically adjusted according to its content.
			cvui::beginColumn();
				cvui::text("Column 1");
				cvui::button("button with very large label");
				cvui::text("End of column 1");
			cvui::endColumn();

			// Add two pieces of text
			cvui::text("Hi again,");
			cvui::text("its me!");

			// Start a new column
			cvui::beginColumn();
				cvui::text("Column 2");
				cvui::button("btn");
				cvui::space();
				cvui::text("text");
				cvui::button("btn2");
				cvui::text("text2");
				if (cvui::button("&Quit")) {
          			break;
        		}
			cvui::endColumn();

			// Add more text
			cvui::text("this is the ");
			cvui::text("end of the row!");
		cvui::endRow();
		
		// This function must be called *AFTER* all UI components. It does
		// all the behind the scenes magic to handle mouse clicks, etc.
		cvui::update();

		// Show everything on the screen
		cv::imshow(WINDOW_NAME, frame);

		// Check if ESC key was pressed
		if (cvui::lastKeyPressed() == 27) {
			break;
		}
	}

	return 0;
}