/*
 A (very) simple UI lib built on top of OpenCV drawing primitives.

 Version: 1.0.0

 Copyright (c) 2016 Fernando Bevilacqua <dovyski@gmail.com>
 Licensed under the MIT license.
*/

#ifndef _CVUI_H_
#define _CVUI_H_

#include "opencv2/core/core.hpp"

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

// You need to call this function *AFTER* you are done adding/manipulating
// UI elements in order for them to react to mouse interactions.
void update();

// Internally used to handle mouse events
void handleMouse(int theEvent, int theX, int theY, int theFlags, void* theData);

} // namespace cvui

#endif // _CVUI_H_