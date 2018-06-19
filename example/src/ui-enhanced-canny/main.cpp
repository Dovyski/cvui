/*
This application showcases how the window component of cvui can be
enhanced, i.e. movable anb minimizable, and used to control the
application of the Canny edge algorithm to a loaded image.

This application uses the EnhancedWindow class available in the
"ui-enhanced-window-component" example.

Authors:
	Fernando Bevilacqua <dovyski@gmail.com>

Contributions:
	Amaury Bréhéret - https://github.com/abreheret
	ShengYu - https://github.com/shengyu7697

Code licensed under the MIT license.
*/

#include <opencv2/opencv.hpp>

#define CVUI_IMPLEMENTATION
#include "cvui.h"

// Include the class that provides an enhanced cvui window component
#include "../ui-enhanced-window-component/EnhancedWindow.h"

#define WINDOW_NAME	"CVUI Ehnanced UI Canny Edge"

int main(int argc, const char *argv[])
{
	cv::Mat fruits = cv::imread("fruits.jpg");
	cv::Mat frame = fruits.clone();
	int low_threshold = 50, high_threshold = 150;
	bool use_canny = false;

	// Create a settings window using the EnhancedWindow class.
	EnhancedWindow settings(10, 50, 270, 180, "Settings");

	// Init cvui and tell it to create a OpenCV window, i.e. cv::namedWindow(WINDOW_NAME).
	cvui::init(WINDOW_NAME);
    
	while (true) {
		// Should we apply Canny edge?
		if (use_canny) {
			// Yes, we should apply it.
			cv::cvtColor(fruits, frame, CV_BGR2GRAY);
			cv::Canny(frame, frame, low_threshold, high_threshold, 3);
			cv::cvtColor(frame, frame, CV_GRAY2BGR);
		} else {
			// No, so just copy the original image to the displaying frame.
			fruits.copyTo(frame);
		}

		// Render the settings window and its content, if it is not minimized.
        settings.begin(frame);
			if (!settings.isMinimized()) {
				cvui::checkbox("Use Canny Edge", &use_canny);
				cvui::trackbar(settings.width() - 20, &low_threshold, 5, 150);
				cvui::trackbar(settings.width() - 20, &high_threshold, 80, 300);
				cvui::space(20); // add 20px of empty space
				cvui::text("Drag and minimize this settings window", 0.4, 0xff0000);
			}
        settings.end();
		
		// Update all cvui internal stuff, e.g. handle mouse clicks, and show
		// everything on the screen.
		cvui::imshow(WINDOW_NAME, frame);

		// Check if ESC was pressed
		if (cv::waitKey(30) == 27) {
			break;
		}
	}

	return 0;
}