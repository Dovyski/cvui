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

static bool mouseJustReleased = false;
static bool mousePressed = true;
static cv::Point mouse;
	
void init(const cv::String& theWindowName) {
	cv::setMouseCallback(theWindowName, handleMouse, NULL);
}

bool button(cv::Mat& theWhere, int theX, int theY, const cv::String& theLabel) {
	cv::Rect aRect(theX, theY, theLabel.length() * 10, 20);
	bool aContainsMouse = aRect.contains(mouse),
		 aWasClicked = mouseJustReleased && aContainsMouse;

	cv::rectangle(theWhere, aRect, aContainsMouse && mousePressed ? cv::Scalar(0, 0, 255) : cv::Scalar(255, 0, 0), cv::FILLED);
	text(theWhere, theX, theY, theLabel, 0.4);

	return aWasClicked;
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

void update() {
	mouseJustReleased = false;
}

void handleMouse(int theEvent, int theX, int theY, int theFlags, void* theData) {
	mouse.x = theX;
	mouse.y = theY;

	if (theEvent == cv::EVENT_LBUTTONDOWN || theEvent == cv::EVENT_RBUTTONDOWN)	{
		mousePressed = true;

	} else if (theEvent == cv::EVENT_LBUTTONUP || theEvent == cv::EVENT_RBUTTONUP)	{
		mouseJustReleased = true;
		mousePressed = false;
	}
}

} // namespace cvui