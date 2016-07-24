/*
 A (very) simple UI lib built on top of OpenCV drawing primitives.

 Version: 1.1.0-DEV

 Copyright (c) 2016 Fernando Bevilacqua <dovyski@gmail.com>
 Licensed under the MIT license.
*/

#ifndef _CVUI_H_
#define _CVUI_H_

#include "opencv2/core/core.hpp"
#include <stdarg.h>

namespace cvui
{
// Initializes the library. You must inform the maximum width and
// height of the window where the lib will render the UI components.
void init(const cv::String& theWindowName);

// Display a button. Returns true everytime the user clicks the button.
// The button size will be automatically adjusted to properly house the label content.
bool button(cv::Mat& theWhere, int theX, int theY, const cv::String& theLabel);

// Display a button. Returns true everytime the user clicks the button.
// The button size will be defined by the width and height parameters, no matter the label.
bool button(cv::Mat& theWhere, int theX, int theY, int theWidth, int theHeight, const cv::String& theLabel);

// Display a checkbox. You can use the state parameter to monitor if the
// checkbox is checked or not.
bool checkbox(cv::Mat& theWhere, int theX, int theY, const cv::String& theLabel, bool *theState, unsigned int theColor = 0xCECECE);

// Display a piece of text.
void text(cv::Mat& theWhere, int theX, int theY, const cv::String& theText, double theFontScale = 0.4, unsigned int theColor = 0xCECECE);

// Display a piece of text that can be formated using printf style.
void printf(cv::Mat& theWhere, int theX, int theY, double theFontScale, unsigned int theColor, char *theFmt, ...);

// Display a counter that the user can increase/descrease by clicking
// the up and down arrows.
int counter(cv::Mat& theWhere, int theX, int theY, int *theValue, int theStep = 1, const char *theFormat = "%d");

// Display a counter that the user can increase/descrease by clicking
// the up and down arrows.
double counter(cv::Mat& theWhere, int theX, int theY, double *theValue, double theStep = 0.5, const char *theFormat = "%.2f");

// Display a window (a block with a title and a body).
void window(cv::Mat& theWhere, int theX, int theY, int theWidth, int theHeight, const cv::String& theTitle);

// Display a filled rectangle
void rect(cv::Mat& theWhere, int theX, int theY, int theWidth, int theHeight, unsigned int theColor);

// TODO: add docs
void sparkline(cv::Mat& theWhere, std::vector<double> theValues, int theX, int theY, int theWidth, int theHeight, unsigned int theColor = 0x00FF00);
void sparklineChart(cv::Mat& theWhere, std::vector<double> theValues, int theX, int theY, int theWidth, int theHeight);

// TODO: add docs
void beginRow(cv::Mat &theWhere, int theX, int theY, int theWidth, int theHeight, int thePadding = 0);
void endRow();

// Display a piece of text within beginRow() and endRow();
void text(const cv::String& theText, double theFontScale = 0.4, unsigned int theColor = 0xCECECE);

// Display a button. Returns true everytime the user clicks the button.
// The button size will be defined by the width and height parameters, no matter the label.
bool button(int theWidth, int theHeight, const cv::String& theLabel);

// Display a button. Returns true everytime the user clicks the button.
// The button size will be automatically adjusted to properly house the label content.
bool button(const cv::String& theLabel);

// You need to call this function *AFTER* you are done adding/manipulating
// UI elements in order for them to react to mouse interactions.
void update();

// Internally used to handle mouse events
void handleMouse(int theEvent, int theX, int theY, int theFlags, void* theData);

// Lib version
static const char *VERSION = "1.1.0-DEV";

// TODO: add docs
const int TYPE_ROW = 0;

// TODO: add docs
typedef struct {
	cv::Mat where;
	cv::Rect rect;
	int padding;
	int type;
} cvui_block_t;

// TODO: add docs
namespace render {
	const int IDLE = 0;
	const int OVER = 1;
	const int PRESSED = 2;

	void text(cvui_block_t& theBlock, const cv::String& theText, cv::Point& thePos, double theFontScale, unsigned int theColor);
	void button(cvui_block_t& theBlock, int theState, cv::Rect& theShape, const cv::String& theLabel);
	void buttonLabel(cvui_block_t& theBlock, int theState, cv::Rect theRect, const cv::String& theLabel, cv::Size& theTextSize);
	void counter(cvui_block_t& theBlock, cv::Rect& theShape, const cv::String& theValue);
	void checkbox(cvui_block_t& theBlock, int theState, cv::Rect& theShape);
	void checkboxLabel(cvui_block_t& theBlock, cv::Rect& theRect, const cv::String& theLabel, cv::Size& theTextSize, unsigned int theColor);
	void checkboxCheck(cvui_block_t& theBlock, cv::Rect& theShape);
	void window(cvui_block_t& theBlock, cv::Rect& theTitleBar, cv::Rect& theContent, const cv::String& theTitle);
	void rect(cvui_block_t& theBlock, cv::Rect& thePos, unsigned int theColor);
	void sparkline(cvui_block_t& theBlock, std::vector<double> theValues, cv::Rect &theRect, double theMin, double theMax, unsigned int theColor);
}

} // namespace cvui

#endif // _CVUI_H_