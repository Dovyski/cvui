---
layout: default
permalink: /usage
id: usage
---

# Usage

Check the [examples](https://github.com/Dovyski/cvui/tree/master/example) folder for some code, but the general idea is the following:

```c++
#include <iostream>

#include "opencv2/core/core.hpp"
#include "opencv2/highgui/highgui.hpp"

#define WINDOW_NAME		"CVUI Test"

int main(int argc, const char *argv[])
{
	cv::Mat frame = cv::Mat(250, 600, CV_8UC3);
	bool checked = false;
	int count = 0;

	cv::namedWindow(WINDOW_NAME);
	cvui::init(WINDOW_NAME);

	while (true) {
		frame = cv::Scalar(49, 52, 49);

		cvui::text(frame, 50, 30, "Hey there!");
		cvui::text(frame, 200, 30, "Use hex 0xRRGGBB colors easily", 0.4, 0xff0000);

		if (cvui::button(frame, 50, 50, "Button")) {
			std::cout << "Button clicked!" << std::endl;
		}

		cvui::window(frame, 50, 100, 120, 100, "Window");
		cvui::counter(frame, 200, 100, &count);
		cvui::checkbox(frame, 200, 150, "Checkbox", &checked);

		cvui::update();

		cv::imshow(WINDOW_NAME, frame);

        // Check if ESC key was pressed
        if (cvui::lastKeyPressed() == 27) {
            break;
        }

	}

	return 0;
}
```
