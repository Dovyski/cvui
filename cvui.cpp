/*
 A (very) simple UI lib built on top of OpenCV drawing primitives.

 Version: 1.1.0

 Copyright (c) 2016 Fernando Bevilacqua <dovyski@gmail.com>
 Licensed under the MIT license.
*/

#include <iostream>

#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>
#include "cvui.h"

// Compatibility macros : this enables to compile the code with either Opencv 2 or Opencv 3
#define CVUI_Filled -1
#if (CV_MAJOR_VERSION < 3)
#define CVUI_Antialiased CV_AA
#else
#define CVUI_Antialiased cv::LINE_AA
#endif


#if !defined(_MSC_VER)
// sprintf_s and vsprintf_s only work with Visual Studio !
#define vsprintf_s vsprintf
#define sprintf_s sprintf
#endif

namespace cvui
{

// Variables to keep track of mouse events and stuff
static bool gMouseJustReleased = false;
static bool gMousePressed = false;
static cv::Point gMouse;
static char gBuffer[1024];
static int gLastKeyPressed;
static int gDelayWaitKey;
static cvui_block_t gScreen;

// This is an internal namespace with all code
// that is shared among components/functions
namespace internal {
	static cvui_block_t gStack[100]; // TODO: make it dynamic?
	static int gStackCount = -1;

	void error(int theId, std::string theMessage) {
		std::cout << "[CVUI] Fatal error (code " << theId << "): " << theMessage << "\n";
		cv::waitKey(100000);
		exit(-1);
	}

	void updateLayoutFlow(cvui_block_t& theBlock, cv::Size theSize) {
		int aValue;

		if (theBlock.type == ROW) {
			aValue = theSize.width + theBlock.padding;

			theBlock.anchor.x += aValue;
			theBlock.fill.width += aValue;
			theBlock.fill.height = std::max(theSize.height, theBlock.fill.height);

		}
		else if (theBlock.type == COLUMN) {
			aValue = theSize.height + theBlock.padding;

			theBlock.anchor.y += aValue;
			theBlock.fill.height += aValue;
			theBlock.fill.width = std::max(theSize.width, theBlock.fill.width);
		}
	}

	bool blockStackEmpty() {
		return gStackCount == -1;
	}

	cvui_block_t& topBlock() {
		if (gStackCount < 0) {
			error(3, "You are using a function that should be enclosed by begin*() and end*(), but you probably forgot to call begin*().");
		}

		return gStack[gStackCount];
	}

	cvui_block_t& pushBlock() {
		return gStack[++gStackCount];
	}

	cvui_block_t& popBlock() {
		// Check if there is anything to be popped out from the stack.
		if (gStackCount < 0) {
			error(1, "Mismatch in the number of begin*()/end*() calls. You are calling one more than the other.");
		}
		
		return gStack[gStackCount--];
	}

	void begin(int theType, cv::Mat &theWhere, int theX, int theY, int theWidth, int theHeight, int thePadding) {
		cvui_block_t& aBlock = internal::pushBlock();

		aBlock.where = theWhere;
		
		aBlock.rect.x = theX;
		aBlock.rect.y = theY;
		aBlock.rect.width = theWidth;
		aBlock.rect.height = theHeight;
		
		aBlock.fill = aBlock.rect;
		aBlock.fill.width = 0;
		aBlock.fill.height = 0;

		aBlock.anchor.x = theX;
		aBlock.anchor.y = theY;
		
		aBlock.padding = thePadding;
		aBlock.type = theType;
	}

	void end(int theType) {
		cvui_block_t& aBlock = popBlock();

		if (aBlock.type != theType) {
			error(4, "Calling wrong type of end*(). E.g. endColumn() instead of endRow(). Check if your begin*() calls are matched with their appropriate end*() calls.");
		}

		// If we still have blocks in the stack, we must update
		// the current top with the dimensions that were filled by
		// the newly popped block.

		if (!blockStackEmpty()) {
			cvui_block_t& aTop = topBlock();
			cv::Size aSize;
			
			// If the block has rect.width < 0 or rect.heigth < 0, it means the
			// user don't want to calculate the block's width/height. It's up to
			// us do to the math. In that case, we use the block's fill rect to find
			// out the occupied space. If the block's width/height is greater than
			// zero, then the user is very specific about the desired size. In that
			// case, we use the provided width/height, no matter what the fill rect
			// actually is.
			aSize.width = aBlock.rect.width < 0 ? aBlock.fill.width : aBlock.rect.width;
			aSize.height = aBlock.rect.height < 0 ? aBlock.fill.height : aBlock.rect.height;

			updateLayoutFlow(aTop, aSize);
		}
	}

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

	// Contains info about a shortcut
	// If a label contains "Re&start", then :
	// - hasShortcut will be true
	// - shortcut will be 's'
	// - labelBeforeShortcut will be "Re"
	// - labelAfterShortcut will be "tart"
	struct cvui_labelshortcutinfo {
		bool hasShortcut;
		char shortcut;
		std::string labelBeforeShortcut;
		std::string labelAfterShortcut;
	};

	cvui_labelshortcutinfo labelShortcutInfo(const std::string &theLabel) {
		cvui_labelshortcutinfo info;
		info.hasShortcut = false;
		info.shortcut = 0;
		info.labelBeforeShortcut = std::string("");
		info.labelAfterShortcut = std::string("");

		std::stringstream before, after;
		for (size_t i = 0; i < theLabel.size(); i++) {
			char c = theLabel[i];
			if ((c == '&') && (i < theLabel.size() - 1)) {
				info.hasShortcut = true;
				info.shortcut = theLabel[i + 1];
				++i;
			} else if (!info.hasShortcut) {
				before << c;
			} else {
				after << c;
			}
		}
		info.labelBeforeShortcut = before.str();
		info.labelAfterShortcut = after.str();
		return info;
	}


	cv::Scalar hexToScalar(unsigned int theColor) {
		int aAlpha = (theColor >> 24) & 0xff;
		int aRed = (theColor >> 16) & 0xff;
		int aGreen = (theColor >> 8) & 0xff;
		int aBlue = theColor & 0xff;

		return cv::Scalar(aBlue, aGreen, aRed, aAlpha);
	}


	inline double clamp01(double value)
	{
		value = value > 1. ? 1. : value;
		value = value < 0. ? 0. : value;
		return value;
	}

	static const int trackbar_XMargin = 14;

	inline void trackbar_ForceValuesAsMultiplesOfSmallStep(const TrackbarParams & theParams, double *theValue)
	{
		if (theParams.ForceValuesAsMultiplesOfSmallStep)
		{
			double k = (*theValue - theParams.MinimumValue) / theParams.SmallStep;
			k = cvRound(k);
			*theValue = theParams.MinimumValue + theParams.SmallStep * k;
		}
	}

	inline double trackbar_XPixelToValue(const TrackbarParams & theParams, cv::Rect & theBounding, int xPixel)
	{
		double ratio = (xPixel - (double)(theBounding.x + trackbar_XMargin) ) / (double)( theBounding.width - 2 * trackbar_XMargin);
		ratio = clamp01(ratio);
		double value = theParams.MinimumValue + ratio * (theParams.MaximumValue - theParams.MinimumValue);
		return value;
	}

	inline int trackbar_ValueToXPixel(const TrackbarParams & theParams, cv::Rect & theBounding, double value)
	{
		double ratio = (value - theParams.MinimumValue) / (theParams.MaximumValue - theParams.MinimumValue);
		ratio = clamp01(ratio);
		double xPixels = (double)theBounding.x + trackbar_XMargin + ratio * (double)(theBounding.width - 2 * trackbar_XMargin);
		return (int)xPixels;
	}


	bool button(cvui_block_t& theBlock, int theX, int theY, int theWidth, int theHeight, const cv::String& theLabel, bool theUpdateLayout) {
		// Calculate the space that the label will fill
		cv::Size aTextSize = getTextSize(theLabel, cv::FONT_HERSHEY_SIMPLEX, 0.4, 1, nullptr);

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

		// Update the layout flow according to button size
		// if we were told to update.
		if (theUpdateLayout) {
			cv::Size aSize(theWidth, theHeight);
			updateLayoutFlow(theBlock, aSize);
		}

		//Handle keyboard shortcuts
		bool wasShortcutPressed = false;
		if (gLastKeyPressed != -1) {
			auto info = internal::labelShortcutInfo(theLabel);
			if (info.hasShortcut && ( tolower(info.shortcut) == tolower((char)gLastKeyPressed)) )
				wasShortcutPressed = true;
		}

		// Tell if the button was clicked or not
		return ( aMouseIsOver && gMouseJustReleased ) || wasShortcutPressed;
	}

	bool button(cvui_block_t& theBlock, int theX, int theY, const cv::String& theLabel) {
		// Calculate the space that the label will fill
		cv::Size aTextSize = getTextSize(theLabel, cv::FONT_HERSHEY_SIMPLEX, 0.4, 1, nullptr);

		// Create a button based on the size of the text
		return internal::button(theBlock, theX, theY, aTextSize.width + 30, aTextSize.height + 18, theLabel, true);
	}

	bool checkbox(cvui_block_t& theBlock, int theX, int theY, const cv::String& theLabel, bool *theState, unsigned int theColor) {
		cv::Rect aRect(theX, theY, 15, 15);
		cv::Size aTextSize = getTextSize(theLabel, cv::FONT_HERSHEY_SIMPLEX, 0.4, 1, nullptr);
		cv::Rect aHitArea(theX, theY, aRect.width + aTextSize.width + 6, aRect.height);
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

		// Update the layout flow
		cv::Size aSize(aHitArea.width, aHitArea.height);
		updateLayoutFlow(theBlock, aSize);

		return *theState;
	}

	void text(cvui_block_t& theBlock, int theX, int theY, const cv::String& theText, double theFontScale, unsigned int theColor, bool theUpdateLayout) {
		cv::Size aTextSize = cv::getTextSize(theText, cv::FONT_HERSHEY_SIMPLEX, theFontScale, 1, nullptr);
		cv::Point aPos(theX, theY + aTextSize.height);

		render::text(theBlock, theText, aPos, theFontScale, theColor);

		if (theUpdateLayout) {
			// Add an extra pixel to the height to overcome OpenCV font size problems.
			aTextSize.height += 1;
			
			updateLayoutFlow(theBlock, aTextSize);
		}
	}

	int counter(cvui_block_t& theBlock, int theX, int theY, int *theValue, int theStep, const char *theFormat) {
		cv::Rect aContentArea(theX + 22, theY, 48, 22);

		if (internal::button(theBlock, theX, theY, 22, 22, "-", false)) {
			*theValue -= theStep;
		}

		sprintf_s(gBuffer, theFormat, *theValue);
		render::counter(theBlock, aContentArea, gBuffer);

		if (internal::button(theBlock, aContentArea.x + aContentArea.width, theY, 22, 22, "+", false)) {
			*theValue += theStep;
		}

		// Update the layout flow
		cv::Size aSize(22 * 2 + aContentArea.width, 22 * 2 + aContentArea.height);
		updateLayoutFlow(theBlock, aSize);

		return *theValue;
	}

	double counter(cvui_block_t& theBlock, int theX, int theY, double *theValue, double theStep, const char *theFormat) {
		cv::Rect aContentArea(theX + 22, theY, 48, 22);

		if (internal::button(theBlock, theX, theY, 22, 22, "-", false)) {
			*theValue -= theStep;
		}

		sprintf_s(gBuffer, theFormat, *theValue);
		render::counter(theBlock, aContentArea, gBuffer);

		if (internal::button(theBlock, aContentArea.x + aContentArea.width, theY, 22, 22, "+", false)) {
			*theValue += theStep;
		}

		// Update the layout flow
		cv::Size aSize(22 * 2 + aContentArea.width, 22 * 2 + aContentArea.height);
		updateLayoutFlow(theBlock, aSize);

		return *theValue;
	}

	bool trackbar(cvui_block_t& theBlock, int theX, int theY, double *theValue, const TrackbarParams & theParams) {
		cv::Rect aContentArea(theX, theY, 150, 45);
		double valueOrig = *theValue;
		bool aMouseIsOver = aContentArea.contains(gMouse);
		render::trackbar(theBlock, aContentArea, *theValue, theParams, aMouseIsOver);
		if (gMousePressed && aMouseIsOver) {
			*theValue = internal::trackbar_XPixelToValue(theParams, aContentArea, gMouse.x);
			if (theParams.ForceValuesAsMultiplesOfSmallStep) {
				internal::trackbar_ForceValuesAsMultiplesOfSmallStep(theParams, theValue);
			}
		}

		// Update the layout flow
		cv::Size aSize = aContentArea.size();
		updateLayoutFlow(theBlock, aSize);

		return (*theValue != valueOrig);
	}


	void window(cvui_block_t& theBlock, int theX, int theY, int theWidth, int theHeight, const cv::String& theTitle) {
		cv::Rect aTitleBar(theX, theY, theWidth, 20);
		cv::Rect aContent(theX, theY + aTitleBar.height, theWidth, theHeight - aTitleBar.height);

		render::window(theBlock, aTitleBar, aContent, theTitle);

		// Update the layout flow
		cv::Size aSize(theWidth, theHeight);
		updateLayoutFlow(theBlock, aSize);
	}

	void rect(cvui_block_t& theBlock, int theX, int theY, int theWidth, int theHeight, unsigned int theBorderColor, unsigned int theFillingColor) {
		cv::Rect aRect(theX, theY, theWidth, theHeight);
		render::rect(theBlock, aRect, theBorderColor, theFillingColor);

		// Update the layout flow
		cv::Size aSize(aRect.width, aRect.height);
		updateLayoutFlow(theBlock, aSize);
	}

	void sparkline(cvui_block_t& theBlock, std::vector<double>& theValues, int theX, int theY, int theWidth, int theHeight, unsigned int theColor) {
		double aMin, aMax;
		cv::Rect aRect(theX, theY, theWidth, theHeight);

		internal::findMinMax(theValues, &aMin, &aMax);
		render::sparkline(theBlock, theValues, aRect, aMin, aMax, theColor);

		// Update the layout flow
		cv::Size aSize(theWidth, theHeight);
		updateLayoutFlow(theBlock, aSize);
	}

}

// This is an internal namespace with all functions
// that actually render each one of the UI components
namespace render {
	void text(cvui_block_t& theBlock, const cv::String& theText, cv::Point& thePos, double theFontScale, unsigned int theColor) {
		cv::putText(theBlock.where, theText, thePos, cv::FONT_HERSHEY_SIMPLEX, theFontScale, internal::hexToScalar(theColor), 1, CVUI_Antialiased);
	}

	void button(cvui_block_t& theBlock, int theState, cv::Rect& theShape, const cv::String& theLabel) {
		// Outline
		cv::rectangle(theBlock.where, theShape, cv::Scalar(0x29, 0x29, 0x29));

		// Border
		theShape.x++; theShape.y++; theShape.width -= 2; theShape.height -= 2;
		cv::rectangle(theBlock.where, theShape, cv::Scalar(0x4A, 0x4A, 0x4A));

		// Inside
		theShape.x++; theShape.y++; theShape.width -= 2; theShape.height -= 2;
		cv::rectangle(theBlock.where, theShape, theState == IDLE ? cv::Scalar(0x42, 0x42, 0x42) : (theState == OVER ? cv::Scalar(0x52, 0x52, 0x52) : cv::Scalar(0x32, 0x32, 0x32)), CVUI_Filled);
	}

	void buttonLabel(cvui_block_t& theBlock, int theState, cv::Rect theRect, const cv::String& theLabel, cv::Size& theTextSize) {
		cv::Point aPos(theRect.x + theRect.width / 2 - theTextSize.width / 2, theRect.y + theRect.height / 2 + theTextSize.height / 2);
		cv::Scalar color = cv::Scalar(0xCE, 0xCE, 0xCE);

		auto putTextAndReturnWidth = [&] (const std::string & str, const cv::Point & position) -> int {
			double fontSize = theState == PRESSED ? 0.39 : 0.4;
			cv::putText(theBlock.where, str, position, cv::FONT_HERSHEY_SIMPLEX, fontSize, color, 1, CVUI_Antialiased);
			int baseline;
			cv::Size size = cv::getTextSize(str, cv::FONT_HERSHEY_SIMPLEX, fontSize, 1, &baseline);
			return size.width;
		};
		auto shortcutInfo = internal::labelShortcutInfo(theLabel);
		if ( ! shortcutInfo.hasShortcut ) {
			putTextAndReturnWidth(theLabel, aPos);
		}
		else {
			int widthBeforeShortcut = putTextAndReturnWidth(shortcutInfo.labelBeforeShortcut, aPos);
			int xStart = aPos.x + widthBeforeShortcut;
			aPos.x += widthBeforeShortcut;
			std::string shortcut; shortcut.push_back(shortcutInfo.shortcut);
			int widthOfShortcut = putTextAndReturnWidth(shortcut, aPos);
			int xEnd = xStart + widthOfShortcut;
			aPos.x += widthOfShortcut;
			putTextAndReturnWidth(shortcutInfo.labelAfterShortcut, aPos);
			cv::line(theBlock.where, cv::Point(xStart, aPos.y + 3), cv::Point(xEnd, aPos.y + 3), color, 1, CVUI_Antialiased);
		}
	}

	void counter(cvui_block_t& theBlock, cv::Rect& theShape, const cv::String& theValue) {
		cv::rectangle(theBlock.where, theShape, cv::Scalar(0x29, 0x29, 0x29), CVUI_Filled); // fill
		cv::rectangle(theBlock.where, theShape, cv::Scalar(0x45, 0x45, 0x45)); // border

		cv::Size aTextSize = getTextSize(theValue, cv::FONT_HERSHEY_SIMPLEX, 0.4, 1, nullptr);

		cv::Point aPos(theShape.x + theShape.width / 2 - aTextSize.width / 2, theShape.y + aTextSize.height / 2 + theShape.height / 2);
		cv::putText(theBlock.where, theValue, aPos, cv::FONT_HERSHEY_SIMPLEX, 0.4, cv::Scalar(0xCE, 0xCE, 0xCE), 1, CVUI_Antialiased);
	}

	void trackbar(cvui_block_t& theBlock, cv::Rect& theShape, double theValue, const TrackbarParams &theParams, bool theMouseIsOver) {
		auto drawTextCentered = [&](const cv::Point & position, const std::string &text) {
			auto fontFace = cv::FONT_HERSHEY_SIMPLEX;
			auto fontScale = 0.3;
			int baseline;
			auto size = cv::getTextSize(text, fontFace, fontScale, 1, &baseline);
			cv::Point positionDecentered(position.x - size.width / 2, position.y);
			cv::putText(theBlock.where, text, positionDecentered, fontFace, fontScale, cv::Scalar(0xCE, 0xCE, 0xCE), 1, CVUI_Antialiased);
		};
		cv::Rect internalShape(theShape.x + internal::trackbar_XMargin, theShape.y,
							   theShape.width - 2 * internal::trackbar_XMargin, theShape.height);
		auto color = cv::Scalar(150, 150, 150);
		if (theMouseIsOver)
			color = cv::Scalar(200, 200, 200);

		cv::Point barTopLeft(internalShape.x, internalShape.y + 20);
		int barHeight = 7;
		{
			// Draw bar
			cv::Rect bar(barTopLeft, cv::Size(internalShape.width, barHeight));
			cv::rectangle(theBlock.where, bar, color, -1);
		}

		//Draw small steps
		if (theParams.DrawSmallSteps)
		{
			for (double value = theParams.MinimumValue; value <= theParams.MaximumValue; value += theParams.SmallStep)
			{
				int xPixel = internal::trackbar_ValueToXPixel(theParams, theShape, value);
				cv::Point pt1(xPixel, barTopLeft.y);
				cv::Point pt2(xPixel, barTopLeft.y - 3);
				cv::line(theBlock.where, pt1, pt2, color);
			}
		}

		//Draw large steps and legends
		for (double value = theParams.MinimumValue; value <= theParams.MaximumValue; value += theParams.LargeStep)
		{
			int xPixel = internal::trackbar_ValueToXPixel(theParams, theShape, value);
			cv::Point pt1(xPixel, barTopLeft.y);
			cv::Point pt2(xPixel, barTopLeft.y - 8);
			cv::line(theBlock.where, pt1, pt2, color);

			if (theParams.DrawValuesAtLargeSteps)
			{
				char legend[100];
				std::string printFormat = theParams.Printf_Format_Steps.empty() ? theParams.Printf_Format : theParams.Printf_Format_Steps;
				sprintf(legend, printFormat.c_str(), value);
				cv::Point textPos(xPixel, barTopLeft.y - 11);
				drawTextCentered(textPos, legend);
			}
		}

		// Draw current value indicator
		{
			cv::Scalar contrastedColor(100, 100, 100);

			int xPixel = internal::trackbar_ValueToXPixel(theParams, theShape, theValue);
			int indicatorWidth = 3;
			int indicatorHeightAdd = 4;
			cv::Point pt1(xPixel - indicatorWidth, barTopLeft.y - indicatorHeightAdd);
			cv::Point pt2(xPixel + indicatorWidth, barTopLeft.y + barHeight + indicatorHeightAdd);
			cv::rectangle(theBlock.where, cv::Rect(pt1, pt2), contrastedColor, -1);

			// Draw current value as text
			cv::Point textPos(xPixel, pt2.y + 11);
			char legend[100];
			sprintf(legend, theParams.Printf_Format.c_str(), theValue);
			drawTextCentered(textPos, legend);
		}
	}

	void checkbox(cvui_block_t& theBlock, int theState, cv::Rect& theShape) {
		// Outline
		cv::rectangle(theBlock.where, theShape, theState == IDLE ? cv::Scalar(0x63, 0x63, 0x63) : cv::Scalar(0x80, 0x80, 0x80));

		// Border
		theShape.x++; theShape.y++; theShape.width -= 2; theShape.height -= 2;
		cv::rectangle(theBlock.where, theShape, cv::Scalar(0x17, 0x17, 0x17));

		// Inside
		theShape.x++; theShape.y++; theShape.width -= 2; theShape.height -= 2;
		cv::rectangle(theBlock.where, theShape, cv::Scalar(0x29, 0x29, 0x29), CVUI_Filled);
	}

	void checkboxLabel(cvui_block_t& theBlock, cv::Rect& theRect, const cv::String& theLabel, cv::Size& theTextSize, unsigned int theColor) {
		cv::Point aPos(theRect.x + theRect.width + 6, theRect.y + theTextSize.height + theRect.height / 2 - theTextSize.height / 2 - 1);
		text(theBlock, theLabel, aPos, 0.4, theColor);
	}

	void checkboxCheck(cvui_block_t& theBlock, cv::Rect& theShape) {
		theShape.x++; theShape.y++; theShape.width -= 2; theShape.height -= 2;
		cv::rectangle(theBlock.where, theShape, cv::Scalar(0xFF, 0xBF, 0x75), CVUI_Filled);
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
		cv::rectangle(theBlock.where, theTitleBar, cv::Scalar(0x21, 0x21, 0x21), CVUI_Filled);

		// Render title text.
		cv::Point aPos(theTitleBar.x + 5, theTitleBar.y + 12);
		cv::putText(theBlock.where, theTitle, aPos, cv::FONT_HERSHEY_SIMPLEX, 0.4, cv::Scalar(0xCE, 0xCE, 0xCE), 1, CVUI_Antialiased);

		// Render the body.
		// First the border.
		cv::rectangle(theBlock.where, theContent, cv::Scalar(0x4A, 0x4A, 0x4A));

		// Then the filling.
		theContent.x++; theContent.y++; theContent.width -= 2; theContent.height -= 2;
		cv::rectangle(aOverlay, theContent, cv::Scalar(0x31, 0x31, 0x31), CVUI_Filled);

		if (aTransparecy) {
			theBlock.where.copyTo(aOverlay);
			cv::rectangle(aOverlay, theContent, cv::Scalar(0x31, 0x31, 0x31), CVUI_Filled);
			cv::addWeighted(aOverlay, aAlpha, theBlock.where, 1.0 - aAlpha, 0.0, theBlock.where);

		} else {
			cv::rectangle(theBlock.where, theContent, cv::Scalar(0x31, 0x31, 0x31), CVUI_Filled);
		}
	}

	void rect(cvui_block_t& theBlock, cv::Rect& thePos, unsigned int theBorderColor, unsigned int theFillingColor) {
		cv::Scalar aBorder = internal::hexToScalar(theBorderColor);
		cv::Scalar aFilling = internal::hexToScalar(theFillingColor);
		
		bool aHasFilling = aFilling[3] != 0xff;

		if (aHasFilling) {
			cv::rectangle(theBlock.where, thePos, aFilling, CVUI_Filled, CVUI_Antialiased);
		}

		// Render the border
		cv::rectangle(theBlock.where, thePos, aBorder, 1, CVUI_Antialiased);
	}

	void sparkline(cvui_block_t& theBlock, std::vector<double>& theValues, cv::Rect &theRect, double theMin, double theMax, unsigned int theColor) {
		std::vector<double>::size_type aSize = theValues.size(), i;
		double aGap, aPosX, aScale = 0, x, y;

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

			cv::line(theBlock.where, aPoint1, aPoint2, internal::hexToScalar(theColor));
			aPosX += aGap;
		}
	}

}
	
void init(const cv::String& theWindowName, int theDelayWaitKey) {
	cv::setMouseCallback(theWindowName, handleMouse, NULL);
	gDelayWaitKey = theDelayWaitKey;
	gLastKeyPressed = 0;
	//TODO: init gScreen here?
}

int lastKeyPressed() {
	return gLastKeyPressed;
}

bool button(cv::Mat& theWhere, int theX, int theY, const cv::String& theLabel) {
	gScreen.where = theWhere;
	return internal::button(gScreen, theX, theY, theLabel);
}

bool button(cv::Mat& theWhere, int theX, int theY, int theWidth, int theHeight, const cv::String& theLabel) {
	gScreen.where = theWhere;
	return internal::button(gScreen, theX, theY, theWidth, theHeight, theLabel, true);
}

bool checkbox(cv::Mat& theWhere, int theX, int theY, const cv::String& theLabel, bool *theState, unsigned int theColor) {
	gScreen.where = theWhere;
	return internal::checkbox(gScreen, theX, theY, theLabel, theState, theColor);
}

void text(cv::Mat& theWhere, int theX, int theY, const cv::String& theText, double theFontScale, unsigned int theColor) {
	gScreen.where = theWhere;
	internal::text(gScreen, theX, theY, theText, theFontScale, theColor, true);
}

void printf(cv::Mat& theWhere, int theX, int theY, double theFontScale, unsigned int theColor, const char *theFmt, ...) {
	va_list aArgs;

	va_start(aArgs, theFmt);
	vsprintf(gBuffer, theFmt, aArgs);
	va_end(aArgs);	

	gScreen.where = theWhere;
	internal::text(gScreen, theX, theY, gBuffer, theFontScale, theColor, true);
}

void printf(cv::Mat& theWhere, int theX, int theY, const char *theFmt, ...) {
	va_list aArgs;

	va_start(aArgs, theFmt);
	vsprintf_s(gBuffer, theFmt, aArgs);
	va_end(aArgs);

	gScreen.where = theWhere;
	internal::text(gScreen, theX, theY, gBuffer, 0.4, 0xCECECE, true);
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

void rect(cv::Mat& theWhere, int theX, int theY, int theWidth, int theHeight, unsigned int theBorderColor, unsigned int theFillingColor) {
	gScreen.where = theWhere;
	internal::rect(gScreen, theX, theY, theWidth, theHeight, theBorderColor, theFillingColor);
}

void sparkline(cv::Mat& theWhere, std::vector<double>& theValues, int theX, int theY, int theWidth, int theHeight, unsigned int theColor) {
	gScreen.where = theWhere;
	internal::sparkline(gScreen, theValues, theX, theY, theWidth, theHeight, theColor);
}

void beginRow(cv::Mat &theWhere, int theX, int theY, int theWidth, int theHeight, int thePadding) {
	internal::begin(ROW, theWhere, theX, theY, theWidth, theHeight, thePadding);
}

void endRow() {
	internal::end(ROW);
}

void beginColumn(cv::Mat &theWhere, int theX, int theY, int theWidth, int theHeight, int thePadding) {
	internal::begin(COLUMN, theWhere, theX, theY, theWidth, theHeight, thePadding);
}

void endColumn() {
	internal::end(COLUMN);
}

void beginRow(int theWidth, int theHeight, int thePadding) {
	cvui_block_t& aBlock = internal::topBlock();
	internal::begin(ROW, aBlock.where, aBlock.anchor.x, aBlock.anchor.y, theWidth, theHeight, thePadding);
}

void beginColumn(int theWidth, int theHeight, int thePadding) {
	cvui_block_t& aBlock = internal::topBlock();
	internal::begin(COLUMN, aBlock.where, aBlock.anchor.x, aBlock.anchor.y, theWidth, theHeight, thePadding);
}

void space(int theValue) {
	cvui_block_t& aBlock = internal::topBlock();
	cv::Size aSize(theValue, theValue);

	internal::updateLayoutFlow(aBlock, aSize);
}

bool button(const cv::String& theLabel) {
	cvui_block_t& aBlock = internal::topBlock();
	return internal::button(aBlock, aBlock.anchor.x, aBlock.anchor.y, theLabel);
}

bool button(int theWidth, int theHeight, const cv::String& theLabel) {
	cvui_block_t& aBlock = internal::topBlock();
	return internal::button(aBlock, aBlock.anchor.x, aBlock.anchor.y, theWidth, theHeight, theLabel, true);
}

bool checkbox(const cv::String& theLabel, bool *theState, unsigned int theColor) {
	cvui_block_t& aBlock = internal::topBlock();
	return internal::checkbox(aBlock, aBlock.anchor.x, aBlock.anchor.y, theLabel, theState, theColor);
}

void text(const cv::String& theText, double theFontScale, unsigned int theColor) {
	cvui_block_t& aBlock = internal::topBlock();
	internal::text(aBlock, aBlock.anchor.x, aBlock.anchor.y, theText, theFontScale, theColor, true);
}

void printf(double theFontScale, unsigned int theColor, const char *theFmt, ...) {
	cvui_block_t& aBlock = internal::topBlock();
	va_list aArgs;

	va_start(aArgs, theFmt);
	vsprintf_s(gBuffer, theFmt, aArgs);
	va_end(aArgs);

	internal::text(aBlock, aBlock.anchor.x, aBlock.anchor.y, gBuffer, theFontScale, theColor, true);
}

void printf(const char *theFmt, ...) {
	cvui_block_t& aBlock = internal::topBlock();
	va_list aArgs;

	va_start(aArgs, theFmt);
	vsprintf_s(gBuffer, theFmt, aArgs);
	va_end(aArgs);

	internal::text(aBlock, aBlock.anchor.x, aBlock.anchor.y, gBuffer, 0.4, 0xCECECE, true);
}

int counter(int *theValue, int theStep, const char *theFormat) {
	cvui_block_t& aBlock = internal::topBlock();
	return internal::counter(aBlock, aBlock.anchor.x, aBlock.anchor.y, theValue, theStep, theFormat);
}

double counter(double *theValue, double theStep, const char *theFormat) {
	cvui_block_t& aBlock = internal::topBlock();
	return internal::counter(aBlock, aBlock.anchor.x, aBlock.anchor.y, theValue, theStep, theFormat);
}

//
// Note : these macros could be avoided using type_traits and enable_if
// I do not master these enough to make it like this for now
//
#define instantiate_for_integral_types(what_to_instantiate) \
	what_to_instantiate(int);                               \
	what_to_instantiate(unsigned int);                      \
	what_to_instantiate(long);                              \
	what_to_instantiate(unsigned long);                     \
	what_to_instantiate(long long);                         \
	what_to_instantiate(unsigned long long);                \
	what_to_instantiate(char);                              \
	what_to_instantiate(unsigned char);

#define instantiate_for_float_types(what_to_instantiate) \
	what_to_instantiate(float);                          \
	what_to_instantiate(double);                         \
	what_to_instantiate(long double);



#define template_trackbarParams_Floats(num_type)                                       \
template<>                                                                             \
TrackbarParams trackbarParams_Floats(                                                  \
		num_type min, num_type max,                                                    \
		int nbDecimals,                                                                \
		int nbLargeSteps,                                                              \
		num_type smallStep,                                                            \
		bool forceValuesAsMultiplesOfSmallStep)                                        \
{                                                                                      \
	TrackbarParams params;                                                             \
	params.MinimumValue = (long double) min;                                           \
	params.MaximumValue = (long double) max;                                           \
	params.DrawValuesAtLargeSteps = true;                                              \
	params.LargeStep = (max - min) / (double) nbLargeSteps;                            \
	params.SmallStep = (long double) smallStep;                                        \
	if (smallStep > 0)                                                                 \
		params.DrawSmallSteps = true;                                                  \
	else                                                                               \
		params.DrawSmallSteps = false;                                                 \
	params.ForceValuesAsMultiplesOfSmallStep                                           \
			= forceValuesAsMultiplesOfSmallStep;                                       \
                                                                                       \
	{                                                                                  \
		int nbSignsBeforeDecimals = (int) ( log((double) max) / log(10.)) + 1;         \
		int totalSigns = nbSignsBeforeDecimals + 1 + nbDecimals;                       \
		std::stringstream format;                                                      \
		format << "%" << totalSigns << "." << nbDecimals << "lf";                      \
		params.Printf_Format = format.str();                                           \
	}                                                                                  \
	return params;                                                                     \
}
instantiate_for_float_types(template_trackbarParams_Floats)

#define template_trackbarParams_Ints(num_type)                                         \
template<>                                                                             \
TrackbarParams trackbarParams_Ints(                                                    \
		num_type min, num_type max,                                                    \
		int nbLargeSteps)                                                              \
{                                                                                      \
	TrackbarParams params;                                                             \
	params.MinimumValue = (long double)min;                                            \
	params.MaximumValue = (long double)max;                                            \
	params.DrawValuesAtLargeSteps = true;                                              \
	params.DrawSmallSteps = false;                                                     \
	params.LargeStep = (double)(max - min) / (double) nbLargeSteps;                    \
	params.SmallStep = 1.;                                                             \
	params.ForceValuesAsMultiplesOfSmallStep = true;                                   \
	params.Printf_Format = "%.0lf";                                                    \
	return params;                                                                     \
}
instantiate_for_float_types(template_trackbarParams_Ints)
instantiate_for_integral_types(template_trackbarParams_Ints)



#define trackbar_template_simple_api(numeric_type)                                                                   \
	template <>                                                                                                      \
	bool trackbar(numeric_type *theValue, const TrackbarParams & theParams) {                                        \
		cvui_block_t& aBlock = internal::topBlock();                                                                 \
		double theValue_asdouble = static_cast<double>(*theValue);                                                   \
		bool result  = internal::trackbar(aBlock, aBlock.anchor.x, aBlock.anchor.y, & theValue_asdouble, theParams); \
		*theValue = static_cast<numeric_type>(theValue_asdouble);                                                    \
		return result;                                                                                               \
	}
instantiate_for_integral_types(trackbar_template_simple_api);
instantiate_for_float_types(trackbar_template_simple_api);

#define trackbar_template_complete_api(numeric_type)                                                                 \
	template <>                                                                                                      \
	bool trackbar(cv::Mat& theWhere, int theX, int theY, numeric_type *theValue, const TrackbarParams & theParams) { \
		gScreen.where = theWhere;                                                                                    \
		double theValue_asdouble = static_cast<double>(*theValue);                                                   \
		bool result = internal::trackbar(gScreen, theX, theY, & theValue_asdouble, theParams);                       \
		*theValue = static_cast<numeric_type>(theValue_asdouble);                                                    \
		return result;                                                                                               \
	}
instantiate_for_integral_types(trackbar_template_complete_api);
instantiate_for_float_types(trackbar_template_complete_api);


#define trackbar_int_template_complete_api(numeric_type)                                  \
	template <>                                                                           \
	bool trackbar_int(cv::Mat& theWhere, int theX, int theY,                              \
					  numeric_type *theValue, numeric_type theMin, numeric_type theMax,   \
					  int theNumberOfLargeSteps)                                          \
	{                                                                                     \
		TrackbarParams params = trackbarParams_Ints(theMin, theMax,theNumberOfLargeSteps);\
		return trackbar<numeric_type>(theWhere, theX, theY, theValue, params);            \
	}
instantiate_for_integral_types(trackbar_int_template_complete_api);
instantiate_for_float_types(trackbar_int_template_complete_api);

#define trackbar_int_template_simple_api(numeric_type)                                    \
	template <>                                                                           \
	bool trackbar_int(                                                                    \
					  numeric_type *theValue, numeric_type theMin, numeric_type theMax,   \
					  int theNumberOfLargeSteps)                                          \
	{                                                                                     \
		TrackbarParams params = trackbarParams_Ints(theMin, theMax,theNumberOfLargeSteps);\
		return trackbar<numeric_type>(theValue, params);                                  \
	}
instantiate_for_integral_types(trackbar_int_template_simple_api);
instantiate_for_float_types(trackbar_int_template_simple_api);

#define trackbar_float_template_complete_api(numeric_type)          \
	template <>                                                     \
	bool trackbar_float(cv::Mat& theWhere, int theX, int theY,      \
						numeric_type *theValue,                     \
						numeric_type theMin, numeric_type theMax,   \
						int theNumberOfDecimals,                    \
						int theNumberOfLargeSteps,                  \
						numeric_type theSmallStep,                  \
						bool flagForceValuesAsMultiplesOfSmallStep) \
	{                                                               \
		TrackbarParams params =                                     \
			trackbarParams_Floats(                                  \
					theMin, theMax,                                 \
					theNumberOfDecimals, theNumberOfLargeSteps,     \
					theSmallStep,                                   \
					flagForceValuesAsMultiplesOfSmallStep);         \
		return trackbar<numeric_type>(                              \
					theWhere, theX, theY,                           \
					theValue, params);                              \
	}
instantiate_for_float_types(trackbar_float_template_complete_api);

#define trackbar_float_template_simple_api(numeric_type)            \
	template <>                                                     \
	bool trackbar_float(                                            \
						numeric_type *theValue,                     \
						numeric_type theMin, numeric_type theMax,   \
						int theNumberOfDecimals,                    \
						int theNumberOfLargeSteps,                  \
						numeric_type theSmallStep,                  \
						bool flagForceValuesAsMultiplesOfSmallStep) \
	{                                                               \
		TrackbarParams params =                                     \
			trackbarParams_Floats(                                  \
					theMin, theMax,                                 \
					theNumberOfDecimals, theNumberOfLargeSteps,     \
					theSmallStep,                                   \
					flagForceValuesAsMultiplesOfSmallStep);         \
		return trackbar<numeric_type>(theValue, params);            \
	}
instantiate_for_float_types(trackbar_float_template_simple_api);



void window(int theWidth, int theHeight, const cv::String& theTitle) {
	cvui_block_t& aBlock = internal::topBlock();
	internal::window(aBlock, aBlock.anchor.x, aBlock.anchor.y, theWidth, theHeight, theTitle);
}

void rect(int theWidth, int theHeight, unsigned int theBorderColor, unsigned int theFillingColor) {
	cvui_block_t& aBlock = internal::topBlock();
	internal::rect(aBlock, aBlock.anchor.x, aBlock.anchor.y, theWidth, theHeight, theBorderColor, theFillingColor);
}

void sparkline(std::vector<double>& theValues, int theWidth, int theHeight, unsigned int theColor) {
	cvui_block_t& aBlock = internal::topBlock();
	internal::sparkline(aBlock, theValues, aBlock.anchor.x, aBlock.anchor.y, theWidth, theHeight, theColor);
}

void update() {
	gMouseJustReleased = false;

	gScreen.rect.x = 0;
	gScreen.rect.y = 0;
	gScreen.rect.width = 0;
	gScreen.rect.height = 0;
	
	gScreen.fill = gScreen.rect;
	gScreen.fill.width = 0;
	gScreen.fill.height = 0;

	gScreen.anchor.x = 0;
	gScreen.anchor.y = 0;
	
	gScreen.padding = 0;

	gLastKeyPressed = cv::waitKey(gDelayWaitKey);

	if (!internal::blockStackEmpty()) {
		internal::error(2, "Calling update() before finishing all begin*()/end*() calls. Did you forget to call a begin*() or an end*()? Check if every begin*() has an appropriate end*() call before you call update().");
	}
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