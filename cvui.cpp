/*
 A (very) simple UI lib built on top of OpenCV drawing primitives.

 Version: 1.0.0

 Copyright (c) 2016 Fernando Bevilacqua <dovyski@gmail.com>
 Licensed under the MIT license.
*/

#include <iostream>

#include "opencv2/imgproc.hpp"
#include "opencv2/highgui/highgui.hpp"
#include "cvui.h"

namespace cvui
{

// Variables to keep track of mouse events and stuff
static bool gMouseJustReleased = false;
static bool gMousePressed = false;
static cv::Point gMouse;
static char gBuffer[1024];

static cvui_block_t gStack[100]; // TODO: make it dynamic?
static int gStackCount = -1;
static cvui_block_t gScreen;


// This is an internal namespace with all code
// that is shared among components/functions
namespace internal {
	// Find the min and max values of a vector
	void findMinMax(std::vector<double>& theValues, double *theMin, double *theMax) {
		std::vector<double>::size_type aSize = theValues.size(), i;
		double aMin = theValues[0], aMax = theValues[0];

		for (i = 0; i < aSize; i++) {
			if (theValues[i] < aMin) {
				aMin = theValues[i];
			}

			if (theValues[i] > aMax) {
				aMax = theValues[i];
			}
		}

		*theMin = aMin;
		*theMax = aMax;
	}

	void separateChannels(int *theRed, int *theGreen, int *theBlue, unsigned int theColor) {
		*theRed = (theColor >> 16) & 0xff;
		*theGreen = (theColor >> 8) & 0xff;
		*theBlue = theColor & 0xff;
	}

	bool button(cvui_block_t& theBlock, int theX, int theY, int theWidth, int theHeight, const cv::String& theLabel) {
		// Calculate the space that the label will fill
		int aBaseline = 0;
		cv::Size aTextSize = getTextSize(theLabel, cv::FONT_HERSHEY_SIMPLEX, 0.4, 1, &aBaseline);

		// Make the button bit enough to house the label
		cv::Rect aRect(theX, theY, theWidth, theHeight);

		// Check the state of the button (idle, pressed, etc.)
		bool aMouseIsOver = aRect.contains(gMouse);

		if (aMouseIsOver) {
			if (gMousePressed) {
				render::button(theBlock, render::PRESSED, aRect, theLabel);
				render::buttonLabel(theBlock, render::PRESSED, aRect, theLabel, aTextSize);
			}
			else {
				render::button(theBlock, render::OVER, aRect, theLabel);
				render::buttonLabel(theBlock, render::OVER, aRect, theLabel, aTextSize);
			}
		}
		else {
			render::button(theBlock, render::IDLE, aRect, theLabel);
			render::buttonLabel(theBlock, render::IDLE, aRect, theLabel, aTextSize);
		}

		// Tell if the button was clicked or not
		return aMouseIsOver && gMouseJustReleased;
	}

	bool button(cvui_block_t& theBlock, int theX, int theY, const cv::String& theLabel) {
		// Calculate the space that the label will fill
		int aBaseline = 0;
		cv::Size aTextSize = getTextSize(theLabel, cv::FONT_HERSHEY_SIMPLEX, 0.4, 1, &aBaseline);

		// Create a button based on the size of the text
		return internal::button(theBlock, theX, theY, aTextSize.width + 30, aTextSize.height + 18, theLabel);
	}

	bool checkbox(cvui_block_t& theBlock, int theX, int theY, const cv::String& theLabel, bool *theState, unsigned int theColor) {
		int aBaseline = 0;
		cv::Rect aRect(theX, theY, 15, 15);
		cv::Size aTextSize = getTextSize(theLabel, cv::FONT_HERSHEY_SIMPLEX, 0.4, 1, &aBaseline);
		cv::Rect aHitArea(theX, theY, aRect.width + aTextSize.width, aRect.height);
		bool aMouseIsOver = aHitArea.contains(gMouse);

		if (aMouseIsOver) {
			render::checkbox(theBlock, render::OVER, aRect);

			if (gMouseJustReleased) {
				*theState = !(*theState);
			}
		}
		else {
			render::checkbox(theBlock, render::IDLE, aRect);
		}

		render::checkboxLabel(theBlock, aRect, theLabel, aTextSize, theColor);

		if (*theState) {
			render::checkboxCheck(theBlock, aRect);
		}

		return *theState;
	}

	void text(cvui_block_t& theBlock, int theX, int theY, const cv::String& theText, double theFontScale, unsigned int theColor) {
		cv::Point aPos(theX, theY);
		render::text(theBlock, theText, aPos, theFontScale, theColor);
	}

	void printf(cvui_block_t& theBlock, int theX, int theY, double theFontScale, unsigned int theColor, char *theFmt, ...) {
		cv::Point aPos(theX, theY);
		va_list aArgs;

		va_start(aArgs, theFmt);
		vsprintf_s(gBuffer, theFmt, aArgs);
		va_end(aArgs);

		render::text(theBlock, gBuffer, aPos, theFontScale, theColor);
	}

	int counter(cvui_block_t& theBlock, int theX, int theY, int *theValue, int theStep, const char *theFormat) {
		cv::Rect aContentArea(theX + 22, theY + 1, 48, 21);

		if (internal::button(theBlock, theX, theY, 22, 22, "-")) {
			*theValue -= theStep;
		}

		sprintf_s(gBuffer, theFormat, *theValue);
		render::counter(theBlock, aContentArea, gBuffer);

		if (internal::button(theBlock, aContentArea.x + aContentArea.width, theY, 22, 22, "+")) {
			*theValue += theStep;
		}

		return *theValue;
	}

	double counter(cvui_block_t& theBlock, int theX, int theY, double *theValue, double theStep, const char *theFormat) {
		cv::Rect aContentArea(theX + 22, theY + 1, 48, 21);

		if (internal::button(theBlock, theX, theY, 22, 22, "-")) {
			*theValue -= theStep;
		}

		sprintf_s(gBuffer, theFormat, *theValue);
		render::counter(theBlock, aContentArea, gBuffer);

		if (internal::button(theBlock, aContentArea.x + aContentArea.width, theY, 22, 22, "+")) {
			*theValue += theStep;
		}

		return *theValue;
	}

	void window(cvui_block_t& theBlock, int theX, int theY, int theWidth, int theHeight, const cv::String& theTitle) {
		cv::Rect aTitleBar(theX, theY, theWidth, 20);
		cv::Rect aContent(theX, theY + aTitleBar.height, theWidth, theHeight - aTitleBar.height);

		render::window(theBlock, aTitleBar, aContent, theTitle);
	}

	void rect(cvui_block_t& theBlock, int theX, int theY, int theWidth, int theHeight, unsigned int theColor) {
		cv::Rect aRect(theX, theY, theWidth, theHeight);
		render::rect(theBlock, aRect, theColor);
	}

	void sparkline(cvui_block_t& theBlock, std::vector<double> theValues, int theX, int theY, int theWidth, int theHeight, unsigned int theColor) {
		double aMin, aMax;
		cv::Rect aRect(theX, theY, theWidth, theHeight);

		internal::findMinMax(theValues, &aMin, &aMax);
		render::sparkline(theBlock, theValues, aRect, aMin, aMax, theColor);
	}

	void sparklineChart(cvui_block_t& theBlock, std::vector<double> theValues, int theX, int theY, int theWidth, int theHeight) {
		double aMin, aMax, aScale = 0;

		internal::findMinMax(theValues, &aMin, &aMax);
		aScale = aMax - aMin;

		sparkline(theBlock, theValues, theX, theY, theWidth, theHeight, 0x00FF00);

		internal::printf(theBlock, theX + 2, theY + 8, 0.25, 0x717171, "%.1f", aMax);
		internal::printf(theBlock, theX + 2, theY + theHeight / 2, 0.25, 0x717171, "%.1f", aScale / 2 + aMin);
		internal::printf(theBlock, theX + 2, theY + theHeight - 5, 0.25, 0x717171, "%.1f", aMin);
	}
}

// This is an internal namespace with all functions
// that actually render each one of the UI components
namespace render {
	void text(cvui_block_t& theBlock, const cv::String& theText, cv::Point& thePos, double theFontScale, unsigned int theColor) {
		int aRed, aGreen, aBlue;

		internal::separateChannels(&aRed, &aGreen, &aBlue, theColor);
		cv::putText(theBlock.where, theText, thePos, cv::FONT_HERSHEY_SIMPLEX, theFontScale, cv::Scalar(aBlue, aGreen, aRed), 1, cv::LINE_AA);

		// TODO: calculate the real width of the text
		theBlock.rect.x += 50;
	}

	void button(cvui_block_t& theBlock, int theState, cv::Rect& theShape, const cv::String& theLabel) {
		// Outline
		cv::rectangle(theBlock.where, theShape, cv::Scalar(0x29, 0x29, 0x29));

		// Border
		theShape.x++; theShape.y++; theShape.width -= 2; theShape.height -= 2;
		cv::rectangle(theBlock.where, theShape, cv::Scalar(0x4A, 0x4A, 0x4A));

		// Inside
		theShape.x++; theShape.y++; theShape.width -= 2; theShape.height -= 2;
		cv::rectangle(theBlock.where, theShape, theState == IDLE ? cv::Scalar(0x42, 0x42, 0x42) : (theState == OVER ? cv::Scalar(0x52, 0x52, 0x52) : cv::Scalar(0x32, 0x32, 0x32)), cv::FILLED);

		// TODO: calculate the real width of the text
		theBlock.rect.x += 50;
	}

	void buttonLabel(cvui_block_t& theBlock, int theState, cv::Rect theRect, const cv::String& theLabel, cv::Size& theTextSize) {
		cv::Point aPos(theRect.x + theRect.width / 2 - theTextSize.width / 2, theRect.y + theRect.height / 2 + theTextSize.height / 2);
		cv::putText(theBlock.where, theLabel, aPos, cv::FONT_HERSHEY_SIMPLEX, theState == PRESSED ? 0.39 : 0.4, cv::Scalar(0xCE, 0xCE, 0xCE), 1, cv::LINE_AA);
	}

	void counter(cvui_block_t& theBlock, cv::Rect& theShape, const cv::String& theValue) {
		int aBaseline = 0;

		cv::rectangle(theBlock.where, theShape, cv::Scalar(0x29, 0x29, 0x29), cv::FILLED); // fill
		cv::rectangle(theBlock.where, theShape, cv::Scalar(0x45, 0x45, 0x45)); // border

		cv::Size aTextSize = getTextSize(theValue, cv::FONT_HERSHEY_SIMPLEX, 0.4, 1, &aBaseline);

		cv::Point aPos(theShape.x + theShape.width / 2 - aTextSize.width / 2, theShape.y + aTextSize.height / 2 + theShape.height / 2);
		cv::putText(theBlock.where, theValue, aPos, cv::FONT_HERSHEY_SIMPLEX, 0.4, cv::Scalar(0xCE, 0xCE, 0xCE), 1, cv::LINE_AA);
	}

	void checkbox(cvui_block_t& theBlock, int theState, cv::Rect& theShape) {
		// Outline
		cv::rectangle(theBlock.where, theShape, theState == IDLE ? cv::Scalar(0x63, 0x63, 0x63) : cv::Scalar(0x80, 0x80, 0x80));

		// Border
		theShape.x++; theShape.y++; theShape.width -= 2; theShape.height -= 2;
		cv::rectangle(theBlock.where, theShape, cv::Scalar(0x17, 0x17, 0x17));

		// Inside
		theShape.x++; theShape.y++; theShape.width -= 2; theShape.height -= 2;
		cv::rectangle(theBlock.where, theShape, cv::Scalar(0x29, 0x29, 0x29), cv::FILLED);
	}

	void checkboxLabel(cvui_block_t& theBlock, cv::Rect& theRect, const cv::String& theLabel, cv::Size& theTextSize, unsigned int theColor) {
		cv::Point aPos(theRect.x + theRect.width + 8, theRect.y + theRect.height / 2 + theTextSize.height / 2 + 2);
		text(theBlock, theLabel, aPos, 0.4, theColor);
	}

	void checkboxCheck(cvui_block_t& theBlock, cv::Rect& theShape) {
		theShape.x++; theShape.y++; theShape.width -= 2; theShape.height -= 2;
		cv::rectangle(theBlock.where, theShape, cv::Scalar(0xFF, 0xBF, 0x75), cv::FILLED);
	}

	void window(cvui_block_t& theBlock, cv::Rect& theTitleBar, cv::Rect& theContent, const cv::String& theTitle) {
		bool aTransparecy = false;
		double aAlpha = 0.3;
		cv::Mat aOverlay;

		// Render the title bar.
		// First the border
		cv::rectangle(theBlock.where, theTitleBar, cv::Scalar(0x4A, 0x4A, 0x4A));
		// then the inside
		theTitleBar.x++; theTitleBar.y++; theTitleBar.width -= 2; theTitleBar.height -= 2;
		cv::rectangle(theBlock.where, theTitleBar, cv::Scalar(0x21, 0x21, 0x21), cv::FILLED);

		// Render title text.
		cv::Point aPos(theTitleBar.x + 5, theTitleBar.y + 12);
		cv::putText(theBlock.where, theTitle, aPos, cv::FONT_HERSHEY_SIMPLEX, 0.4, cv::Scalar(0xCE, 0xCE, 0xCE), 1, cv::LINE_AA);

		// Render the body.
		// First the border.
		cv::rectangle(theBlock.where, theContent, cv::Scalar(0x4A, 0x4A, 0x4A));

		// Then the filling.
		theContent.x++; theContent.y++; theContent.width -= 2; theContent.height -= 2;
		cv::rectangle(aOverlay, theContent, cv::Scalar(0x31, 0x31, 0x31), cv::FILLED);

		if (aTransparecy) {
			theBlock.where.copyTo(aOverlay);
			cv::rectangle(aOverlay, theContent, cv::Scalar(0x31, 0x31, 0x31), cv::FILLED);
			cv::addWeighted(aOverlay, aAlpha, theBlock.where, 1.0 - aAlpha, 0.0, theBlock.where);

		} else {
			cv::rectangle(theBlock.where, theContent, cv::Scalar(0x31, 0x31, 0x31), cv::FILLED);
		}
	}

	void rect(cvui_block_t& theBlock, cv::Rect& thePos, unsigned int theColor) {
		int aRed, aGreen, aBlue;

		aRed = (theColor >> 16) & 0xff;
		aGreen = (theColor >> 8) & 0xff;
		aBlue = theColor & 0xff;

		cv::rectangle(theBlock.where, thePos, cv::Scalar(aBlue, aGreen, aRed), cv::FILLED, cv::LINE_AA);
	}

	void sparkline(cvui_block_t& theBlock, std::vector<double> theValues, cv::Rect &theRect, double theMin, double theMax, unsigned int theColor) {
		std::vector<double>::size_type aSize = theValues.size(), i;
		double aGap, aPosX, aScale = 0, x, y;
		int aRed, aGreen, aBlue ;

		internal::separateChannels(&aRed, &aGreen, &aBlue, theColor);

		aScale = theMax - theMin;
		aGap = (double)theRect.width / aSize;
		aPosX = theRect.x;

		for (i = 0; i <= aSize - 2; i++) {
			x = aPosX;
			y = (theValues[i] - theMin) / aScale * -(theRect.height - 5) + theRect.y + theRect.height - 5;
			cv::Point aPoint1((int)x, (int)y);

			x = aPosX + aGap;
			y = (theValues[i + 1] - theMin) / aScale * -(theRect.height - 5) + theRect.y + theRect.height - 5;
			cv::Point aPoint2((int)x, (int)y);

			cv::line(theBlock.where, aPoint1, aPoint2, cv::Scalar(aBlue, aGreen, aRed));
			aPosX += aGap;
		}
	}
}
	
void init(const cv::String& theWindowName) {
	cv::setMouseCallback(theWindowName, handleMouse, NULL);

	//TODO: init gScreen here?
}

bool button(cv::Mat& theWhere, int theX, int theY, const cv::String& theLabel) {
	gScreen.where = theWhere;
	return internal::button(gScreen, theX, theY, theLabel);
}

bool button(cv::Mat& theWhere, int theX, int theY, int theWidth, int theHeight, const cv::String& theLabel) {
	gScreen.where = theWhere;
	return internal::button(gScreen, theX, theY, theWidth, theHeight, theLabel);
}

bool checkbox(cv::Mat& theWhere, int theX, int theY, const cv::String& theLabel, bool *theState, unsigned int theColor) {
	gScreen.where = theWhere;
	return internal::checkbox(gScreen, theX, theY, theLabel, theState, theColor);
}

void text(cv::Mat& theWhere, int theX, int theY, const cv::String& theText, double theFontScale, unsigned int theColor) {
	gScreen.where = theWhere;
	internal::text(gScreen, theX, theY, theText, theFontScale, theColor);
}

void printf(cv::Mat& theWhere, int theX, int theY, double theFontScale, unsigned int theColor, char *theFmt, ...) {
	va_list aArgs;

	va_start(aArgs, theFmt);
	vsprintf_s(gBuffer, theFmt, aArgs);
	va_end(aArgs);

	gScreen.where = theWhere;
	internal::text(gScreen, theX, theY, gBuffer, theFontScale, theColor);
}

int counter(cv::Mat& theWhere, int theX, int theY, int *theValue, int theStep, const char *theFormat) {
	gScreen.where = theWhere;
	return internal::counter(gScreen, theX, theY, theValue, theStep, theFormat);
}

double counter(cv::Mat& theWhere, int theX, int theY, double *theValue, double theStep, const char *theFormat) {
	gScreen.where = theWhere;
	return internal::counter(gScreen, theX, theY, theValue, theStep, theFormat);
}

void window(cv::Mat& theWhere, int theX, int theY, int theWidth, int theHeight, const cv::String& theTitle) {
	gScreen.where = theWhere;
	internal::window(gScreen, theX, theY, theWidth, theHeight, theTitle);
}

void rect(cv::Mat& theWhere, int theX, int theY, int theWidth, int theHeight, unsigned int theColor) {
	gScreen.where = theWhere;
	internal::rect(gScreen, theX, theY, theWidth, theHeight, theColor);
}

void sparkline(cv::Mat& theWhere, std::vector<double> theValues, int theX, int theY, int theWidth, int theHeight, unsigned int theColor) {
	gScreen.where = theWhere;
	internal::sparkline(gScreen, theValues, theX, theY, theWidth, theHeight, theColor);
}

void sparklineChart(cv::Mat& theWhere, std::vector<double> theValues, int theX, int theY, int theWidth, int theHeight) {
	gScreen.where = theWhere;
	internal::sparkline(gScreen, theValues, theX, theY, theWidth, theHeight, 0x00FF00);
}

void beginRow(cv::Mat &theWhere, int theX, int theY, int theWidth, int theHeight) {
	// TODO: move this to internal namespace?
	cvui_block_t& aBlock = gStack[++gStackCount];
	
	aBlock.where = theWhere;
	aBlock.rect.x = theX;
	aBlock.rect.y = theY;
	aBlock.rect.width = theWidth;
	aBlock.rect.height = theHeight;
	aBlock.type = TYPE_ROW;
}

void endRow() {
	// TODO: check for empty stack before getting things out of it.
	gStackCount--;
}

bool button(const cv::String& theLabel) {
	cvui_block_t& aBlock = gStack[gStackCount];
	return internal::button(aBlock, aBlock.rect.x, aBlock.rect.y, theLabel);
}

bool button(int theWidth, int theHeight, const cv::String& theLabel) {
	cvui_block_t& aBlock = gStack[gStackCount];
	return internal::button(aBlock, aBlock.rect.x, aBlock.rect.y, theWidth, theHeight, theLabel);
}

bool checkbox(const cv::String& theLabel, bool *theState, unsigned int theColor) {
	cvui_block_t& aBlock = gStack[gStackCount];
	return internal::checkbox(aBlock, aBlock.rect.x, aBlock.rect.y, theLabel, theState, theColor);
}

void text(const cv::String& theText, double theFontScale, unsigned int theColor) {
	cvui_block_t& aBlock = gStack[gStackCount];
	internal::text(aBlock, aBlock.rect.x, aBlock.rect.y, theText, theFontScale, theColor);
}

void printf(double theFontScale, unsigned int theColor, char *theFmt, ...) {
}

int counter(int *theValue, int theStep, const char *theFormat) {
	cvui_block_t& aBlock = gStack[gStackCount];
	return internal::counter(aBlock, aBlock.rect.x, aBlock.rect.y, theValue, theStep, theFormat);
}

double counter(double *theValue, double theStep, const char *theFormat) {
	cvui_block_t& aBlock = gStack[gStackCount];
	return internal::counter(aBlock, aBlock.rect.x, aBlock.rect.y, theValue, theStep, theFormat);
}

void window(int theWidth, int theHeight, const cv::String& theTitle) {
	cvui_block_t& aBlock = gStack[gStackCount];
	internal::window(aBlock, aBlock.rect.x, aBlock.rect.y, theWidth, theHeight, theTitle);
}

void rect(int theWidth, int theHeight, unsigned int theColor) {
	cvui_block_t& aBlock = gStack[gStackCount];
	internal::rect(aBlock, aBlock.rect.x, aBlock.rect.y, theWidth, theHeight, theColor);
}

void sparkline(std::vector<double> theValues, int theX, int theY, int theWidth, int theHeight, unsigned int theColor) {
	cvui_block_t& aBlock = gStack[gStackCount];
	internal::sparkline(aBlock, theValues, aBlock.rect.x, aBlock.rect.y, theWidth, theHeight, theColor);
}

void sparklineChart(std::vector<double> theValues, int theX, int theY, int theWidth, int theHeight) {
	cvui_block_t& aBlock = gStack[gStackCount];
	internal::sparkline(aBlock, theValues, aBlock.rect.x, aBlock.rect.y, theWidth, theHeight, 0x00FF00);
}

void update() {
	gMouseJustReleased = false;

	gScreen.rect.x = 0;
	gScreen.rect.y = 0;
	gScreen.rect.width = 0;
	gScreen.rect.height = 0;
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