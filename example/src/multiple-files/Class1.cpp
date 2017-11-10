/*
Copyright (c) 2017 Fernando Bevilacqua <dovyski@gmail.com>
Licensed under the MIT license.
*/

#include "cvui.h"
#include "Class1.h"

Class1::Class1() {
	checked = false;
}

void Class1::renderInfo(cv::Mat & frame) {
	cvui::window(frame, 10, 50, 100, 120, "Info");
	cvui::checkbox(frame, 15, 80, "Checked", &checked);
}
