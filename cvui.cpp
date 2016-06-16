/*
 A (very) simple UI lib built on top of OpenCV drawing primitives.

 Copyright (c) 2016 Fernando Bevilacqua <dovyski@gmail.com>
 Licensed under the MIT license.
*/

#include <iostream>
#include "opencv2/imgproc.hpp"
#include "opencv2/highgui/highgui.hpp"
#include "cvui.h"

namespace cvui
{
	
void init(const cv::String& theWindowName) {
	cv::setMouseCallback(theWindowName, handleMouse, NULL);
}

bool button(cv::Mat& theWhere, int theX, int theY, const cv::String& theLabel) {

}

void checkbox(cv::Mat& theWhere, int theX, int theY, const cv::String& theLabel, bool *theState) {

}

void text(cv::Mat& theWhere, int theX, int theY, const cv::String& theText, double theFontScale) {
	cv::Point aPos(theX, theY);
	cv::putText(theWhere, theText, aPos, cv::FONT_HERSHEY_SIMPLEX, theFontScale, cv::Scalar(0, 0, 0), 1, cv::LINE_AA);
}

int counter(cv::Mat& theWhere, int theX, int theY, int &theValue) {

}

int window(cv::Mat& theWhere, int theX, int theY, int theWidth, int theHeigh, const cv::String& theTitle) {

}

void handleMouse(int theEvent, int theX, int theY, int theFlags, void* theData) {
	if (theEvent == cv::EVENT_LBUTTONDOWN)	{
		std::cout << "Left button of the mouse is clicked - position (" << theX << ", " << theY << ")" << std::endl;

	}
	else if (theEvent == cv::EVENT_RBUTTONDOWN) {
		std::cout << "Right button of the mouse is clicked - position (" << theX << ", " << theY << ")" << std::endl;

	}
	else if (theEvent == cv::EVENT_MBUTTONDOWN) {
		std::cout << "Middle button of the mouse is clicked - position (" << theX << ", " << theY << ")" << std::endl;

	}
	else if (theEvent == cv::EVENT_MOUSEMOVE) {
		std::cout << "Mouse move over the window - position (" << theX << ", " << theY << ")" << std::endl;
	}
}

} // namespace cvui