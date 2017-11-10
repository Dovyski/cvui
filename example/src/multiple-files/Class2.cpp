/*
Copyright (c) 2017 Fernando Bevilacqua <dovyski@gmail.com>
Licensed under the MIT license.
*/

#include "cvui.h"
#include "Class2.h"

Class2::Class2() {
}

void Class2::renderMessage(cv::Mat & frame) {
	cvui::text(frame, 10, 10, "Message");
}
