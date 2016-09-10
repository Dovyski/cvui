/*
One of the most annoying tasks when building UI is to calculate 
where each component should be placed on the screen. cvui has
a set of methods that abstract the process of positioning
components, so you don't have to think about assigning a
X and Y coordinate. Instead you just add components and cvui
will place them as you go.

In order to use that approach, you must use begin*()/end*().
You use begin*() to start a group of elements, then you add
the components you want (without the X and Y parameters, e.g.
text("Hi") instead of text(50, 35, "Hi")), then you finish
the group by calling end*().

You can create rows (beginRow()/endRow()) and columns
(beginColumn()/endColumn()). This application uses rows and
columns separately, but you can nest them as you want (take
a look at the "nested-rows-columns" app).

Code licensed under the MIT license, check LICENSE file.
*/

#include <iostream>

#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>

#include "cvui.h"

#define WINDOW_NAME		"Rows and Columns"


int main(int argc, const char *argv[])
{
	cv::Mat frame = cv::Mat(600, 800, CV_8UC3);
	
	// Create a variables used by some components
	std::vector<double> values;
	bool checked = false;
	double value = 1.0;
	int padding = 10;

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

		// In a row, all added elements are
		// horizontally placed, one next the other (from left to right)
		//
		// Within the cvui::beginRow() and cvui::endRow(),
		// all elements will be automatically positioned by cvui.
		// 
		// Notice that all component calls within the begin/end block
		// DO NOT have (x,y) coordinates. 
		//
		// Let's create a row at position (10,20) with width 100 and height 50.
		cvui::beginRow(frame, 10, 20, 100, 50);
			cvui::text("This is ");
			cvui::printf("a row");
			cvui::checkbox("checkbox", &checked);
			cvui::window(80, 80, "window");
			cvui::rect(50, 50, 0x00ff00, 0xff0000);
			cvui::sparkline(values, 50, 50);
			cvui::counter(&value);
			cvui::button(100, 30, "Fixed");
		cvui::endRow();

		// Here is another row, this time with a padding of 50px among components.
		padding = 50;
		cvui::beginRow(frame, 10, 150, 100, 50, padding);
			cvui::text("This is ");
			cvui::printf("another row");
			cvui::checkbox("checkbox", &checked);
			cvui::window(80, 80, "window");
			cvui::button(100, 30, "Fixed");
			cvui::printf("with 50px padding.");
		cvui::endRow();

		// In a column, all added elements are vertically placed,
		// one below the other, from top to bottom. Let's create
		// a column at (50, 300) with width 100 and height 200.
		cvui::beginColumn(frame, 50, 300, 100, 200);
			cvui::text("Column 1 (no padding)");
			cvui::button("button1");
			cvui::button("button2");
			cvui::text("End of column 1");
		cvui::endColumn();

		// Here is another column, using a padding value of 10,
		// which will add an space of 10px between each component.
		padding = 10;
		cvui::beginColumn(frame, 300, 300, 100, 200, padding);
			cvui::text("Column 2 (padding = 10)");
			cvui::button("button1");
			cvui::button("button2");

			static double value = 2.25;
			cvui::TrackbarParams params;
			params.MinimumValue = 0.; params.MaximumValue = 5;
			params.LargeStep = 1.; params.SmallStep = 0.25;
			params.Printf_Format = "%3.2lf";
			params.ForceValuesAsMultiplesOfSmallStep = true;
			cvui::trackbar(&value, params);

		cvui::text("End of column 2");
		cvui::endColumn();

		// You can also add an arbitrary amount of space between
		// components by calling cvui::space().
		//
		// cvui::space() is aware of context, so if it is used
		// within a beginColumn()/endColumn() block, the space will
		// be vertical. If it is used within a beginRow()/endRow()
		// block, space will be horizontal.
		cvui::beginColumn(frame, 550, 300, 100, 200);
			cvui::text("Column 3 (use space)");
			// Add 5 pixels of (vertical) space.
			cvui::space(5);
			cvui::button("button1 5px below");
			// Add 50 pixels of (vertical) space. 
			cvui::space(50);
			cvui::text("Text 50px below");
			// Add 20 pixels of (vertical) space.
			cvui::space(20);
			cvui::button("Button 20px below");
			// Add 40 pixels of (vertical) space.
			cvui::space(40);
			cvui::text("End of column 2 (40px below)");
		cvui::endColumn();
		
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