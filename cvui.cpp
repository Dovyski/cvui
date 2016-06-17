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

// This is an internal namespace with all functions
// that actually render each one of the UI components
namespace render {
	const int IDLE = 0;
	const int OVER = 1;
	const int PRESSED = 2;

	void button(int theState, cv::Mat& theWhere, cv::Rect& theShape, const cv::String& theLabel) {
		// Outline
		cv::rectangle(theWhere, theShape, cv::Scalar(0x29, 0x29, 0x29));

		// Border
		theShape.x++; theShape.y++; theShape.width -= 2; theShape.height -= 2;
		cv::rectangle(theWhere, theShape, cv::Scalar(0x4A, 0x4A, 0x4A));

		// Inside
		theShape.x++; theShape.y++; theShape.width -= 2; theShape.height -= 2;
		cv::rectangle(theWhere, theShape, theState == IDLE ? cv::Scalar(0x42, 0x42, 0x42) : (theState == OVER ? cv::Scalar(0x52, 0x52, 0x52) : cv::Scalar(0x32, 0x32, 0x32)), cv::FILLED);
	}

	void buttonLabel(int theState, cv::Mat& theWhere, cv::Rect theRect, const cv::String& theLabel, cv::Size& theTextSize) {
		cv::Point aPos(theRect.x + theRect.width / 2 - theTextSize.width / 2, theRect.y + theRect.height / 2 + theTextSize.height / 2);
		cv::putText(theWhere, theLabel, aPos, cv::FONT_HERSHEY_SIMPLEX, theState == PRESSED ? 0.39 : 0.4, cv::Scalar(0xCE, 0xCE, 0xCE), 1, cv::LINE_AA);
	}

	void counter(cv::Mat& theWhere, cv::Rect& theShape, const cv::String& theValue) {
		int aBaseline = 0;

		cv::rectangle(theWhere, theShape, cv::Scalar(0x29, 0x29, 0x29), cv::FILLED); // fill
		cv::rectangle(theWhere, theShape, cv::Scalar(0x45, 0x45, 0x45)); // border

		cv::Size aTextSize = getTextSize(theValue, cv::FONT_HERSHEY_SIMPLEX, 0.4, 1, &aBaseline);

		cv::Point aPos(theShape.x + theShape.width / 2 - aTextSize.width / 2, theShape.y + aTextSize.height / 2 + theShape.height / 2);
		cv::putText(theWhere, theValue, aPos, cv::FONT_HERSHEY_SIMPLEX, 0.4, cv::Scalar(0xCE, 0xCE, 0xCE), 1, cv::LINE_AA);
	}

	void checkbox(int theState, cv::Mat& theWhere, cv::Rect& theShape) {
		// Outline
		cv::rectangle(theWhere, theShape, theState == IDLE ? cv::Scalar(0x63, 0x63, 0x63) : cv::Scalar(0x80, 0x80, 0x80));

		// Border
		theShape.x++; theShape.y++; theShape.width -= 2; theShape.height -= 2;
		cv::rectangle(theWhere, theShape, cv::Scalar(0x17, 0x17, 0x17));

		// Inside
		theShape.x++; theShape.y++; theShape.width -= 2; theShape.height -= 2;
		cv::rectangle(theWhere, theShape, cv::Scalar(0x29, 0x29, 0x29), cv::FILLED);
	}

	void checkboxLabel(cv::Mat& theWhere, cv::Rect& theRect, const cv::String& theLabel, cv::Size& theTextSize) {
		cv::Point aPos(theRect.x + theRect.width + 8, theRect.y + theRect.height / 2 + theTextSize.height / 2 + 2);
		cv::putText(theWhere, theLabel, aPos, cv::FONT_HERSHEY_SIMPLEX, 0.4, cv::Scalar(0xCE, 0xCE, 0xCE), 1, cv::LINE_AA);
	}

	void checkboxCheck(cv::Mat& theWhere, cv::Rect& theShape) {
		theShape.x++; theShape.y++; theShape.width -= 2; theShape.height -= 2;
		cv::rectangle(theWhere, theShape, cv::Scalar(0xFF, 0xBF, 0x75), cv::FILLED);
	}

	void window(cv::Mat& theWhere, cv::Rect& theTitleBar, cv::Rect& theContent, const cv::String& theTitle) {
		bool aTransparecy = false;
		double aAlpha = 0.3;
		cv::Mat aOverlay;

		// Render the title bar.
		// First the border
		cv::rectangle(theWhere, theTitleBar, cv::Scalar(0x4A, 0x4A, 0x4A));
		// then the inside
		theTitleBar.x++; theTitleBar.y++; theTitleBar.width -= 2; theTitleBar.height -= 2;
		cv::rectangle(theWhere, theTitleBar, cv::Scalar(0x21, 0x21, 0x21), cv::FILLED);

		// Render title text.
		cv::Point aPos(theTitleBar.x + 5, theTitleBar.y + 12);
		cv::putText(theWhere, theTitle, aPos, cv::FONT_HERSHEY_SIMPLEX, 0.4, cv::Scalar(0xCE, 0xCE, 0xCE), 1, cv::LINE_AA);

		// Render the body.
		// First the border.
		cv::rectangle(theWhere, theContent, cv::Scalar(0x4A, 0x4A, 0x4A));

		// Then the filling.
		theContent.x++; theContent.y++; theContent.width -= 2; theContent.height -= 2;
		cv::rectangle(aOverlay, theContent, cv::Scalar(0x31, 0x31, 0x31), cv::FILLED);

		if (aTransparecy) {
			theWhere.copyTo(aOverlay);
			cv::rectangle(aOverlay, theContent, cv::Scalar(0x31, 0x31, 0x31), cv::FILLED);
			cv::addWeighted(aOverlay, aAlpha, theWhere, 1.0 - aAlpha, 0.0, theWhere);

		} else {
			cv::rectangle(theWhere, theContent, cv::Scalar(0x31, 0x31, 0x31), cv::FILLED);
		}
	}
}

// Variables to keep track of mouse events and stuff
static bool gMouseJustReleased = false;
static bool gMousePressed = false;
static cv::Point gMouse;
static char gBuffer[200];
	
void init(const cv::String& theWindowName) {
	cv::setMouseCallback(theWindowName, handleMouse, NULL);
}

bool button(cv::Mat& theWhere, int theX, int theY, const cv::String& theLabel) {
	// Calculate the space that the label will fill
	int aBaseline = 0;
	cv::Size aTextSize = getTextSize(theLabel, cv::FONT_HERSHEY_SIMPLEX, 0.4, 1, &aBaseline);

	// Create a button based on the size of the text
	return button(theWhere, theX, theY, aTextSize.width + 30, aTextSize.height + 18, theLabel);
}

bool button(cv::Mat& theWhere, int theX, int theY, int theWidth, int theHeight, const cv::String& theLabel) {
	// Calculate the space that the label will fill
	int aBaseline = 0;
	cv::Size aTextSize = getTextSize(theLabel, cv::FONT_HERSHEY_SIMPLEX, 0.4, 1, &aBaseline);

	// Make the button bit enough to house the label
	cv::Rect aRect(theX, theY, theWidth, theHeight);

	// Check the state of the button (idle, pressed, etc.)
	bool aMouseIsOver = aRect.contains(gMouse);

	if (aMouseIsOver) {
		if (gMousePressed) {
			render::button(render::PRESSED, theWhere, aRect, theLabel);
			render::buttonLabel(render::PRESSED, theWhere, aRect, theLabel, aTextSize);
		} else {
			render::button(render::OVER, theWhere, aRect, theLabel);
			render::buttonLabel(render::OVER, theWhere, aRect, theLabel, aTextSize);
		}
	} else {
		render::button(render::IDLE, theWhere, aRect, theLabel);
		render::buttonLabel(render::IDLE, theWhere, aRect, theLabel, aTextSize);
	}

	// Tell if the button was clicked or not
	return aMouseIsOver && gMouseJustReleased;
}

bool checkbox(cv::Mat& theWhere, int theX, int theY, const cv::String& theLabel, bool *theState) {
	int aBaseline = 0;
	cv::Rect aRect(theX, theY, 15, 15);
	cv::Size aTextSize = getTextSize(theLabel, cv::FONT_HERSHEY_SIMPLEX, 0.4, 1, &aBaseline);
	cv::Rect aHitArea(theX, theY, aRect.width + aTextSize.width, aRect.height);
	bool aMouseIsOver = aHitArea.contains(gMouse);

	if (aMouseIsOver) {
		render::checkbox(render::OVER, theWhere, aRect);

		if (gMouseJustReleased) {
			*theState = !(*theState);
		}
	} else {
		render::checkbox(render::IDLE, theWhere, aRect);
	}

	render::checkboxLabel(theWhere, aRect, theLabel, aTextSize);

	if (*theState) {
		render::checkboxCheck(theWhere, aRect);
	}

	return *theState;
}

void text(cv::Mat& theWhere, int theX, int theY, const cv::String& theText, double theFontScale, unsigned int theColor) {
	int aRed, aGreen, aBlue;

	aRed = (theColor >> 16) & 0xff;
	aGreen = (theColor >> 8) & 0xff;
	aBlue = theColor & 0xff;
	
	cv::Point aPos(theX, theY);
	cv::putText(theWhere, theText, aPos, cv::FONT_HERSHEY_SIMPLEX, theFontScale, cv::Scalar(aBlue, aGreen, aRed), 1, cv::LINE_AA);
}

int counter(cv::Mat& theWhere, int theX, int theY, int *theValue) {
	cv::Rect aContentArea(theX + 22, theY + 1, 48, 21);

	if (cvui::button(theWhere, theX, theY, 22, 22, "-")) {
		(*theValue)--;
	}
	
	sprintf_s(gBuffer, "%d", *theValue);
	render::counter(theWhere, aContentArea, gBuffer);

	if (cvui::button(theWhere, aContentArea.x + aContentArea.width, theY, 22, 22, "+")) {
		(*theValue)++;
	}

	return *theValue;
}

void window(cv::Mat& theWhere, int theX, int theY, int theWidth, int theHeight, const cv::String& theTitle) {
	cv::Rect aTitleBar(theX, theY, theWidth, 20);
	cv::Rect aContent(theX, theY + aTitleBar.height, theWidth, theHeight - aTitleBar.height);

	render::window(theWhere, aTitleBar, aContent, theTitle);
}

void update() {
	gMouseJustReleased = false;
}

void handleMouse(int theEvent, int theX, int theY, int theFlags, void* theData) {
	gMouse.x = theX;
	gMouse.y = theY;

	if (theEvent == cv::EVENT_LBUTTONDOWN || theEvent == cv::EVENT_RBUTTONDOWN)	{
		gMousePressed = true;

	} else if (theEvent == cv::EVENT_LBUTTONUP || theEvent == cv::EVENT_RBUTTONUP)	{
		gMouseJustReleased = true;
		gMousePressed = false;
	}
}

} // namespace cvui