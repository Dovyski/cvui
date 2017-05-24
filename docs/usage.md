---
layout: default
title: usage
---

# Usage

There are two mandatory steps you need to perform in order to make cvui work. First you need to call `cvui::init()` to initialize the lib. Second you must call `cv::update()` after you are finished invoking cvui components, so cvui can perform its internal processing to handle mouse interactions.

Below is a very simple program using the basics of cvui:

{% highlight c++ %}

#include <iostream>

#include "opencv2/core/core.hpp"
#include "opencv2/highgui/highgui.hpp"
#include "cvui.h"

#define WINDOW_NAME		"CVUI Test"

int main(int argc, const char *argv[])
{
	cv::Mat frame = cv::Mat(250, 600, CV_8UC3);

	cv::namedWindow(WINDOW_NAME);
	cvui::init(WINDOW_NAME);

	while (true) {
		frame = cv::Scalar(49, 52, 49);

		cvui::text(frame, 50, 30, "Hey there!");
		cvui::update();

		cv::imshow(WINDOW_NAME, frame);
		cv::waitKey(30);
	}

	return 0;
}

{% endhighlight %}

Check out the [examples](https://github.com/Dovyski/cvui/tree/master/example) folder for more code and examples.
